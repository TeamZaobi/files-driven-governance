#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATEGORY_TO_BUCKET = {
    "route": "route_assertions",
    "read": "read_assertions",
    "write": "write_assertions",
    "boundary": "boundary_assertions",
    "projection": "projection_assertions",
    "recovery": "recovery_assertions",
    "trajectory": "trajectory_assertions",
}
ORDERED_CATEGORIES = list(CATEGORY_TO_BUCKET)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an AI-Native E2E bundle judge using a project-selected CLI/runtime."
    )
    parser.add_argument("--case", required=True, help="Path to ai-native-e2e case contract")
    parser.add_argument(
        "--observed-replay-artifact",
        required=True,
        help="Path to the observed replay artifact that should be judged",
    )
    parser.add_argument(
        "--observed-run-metadata",
        required=True,
        help="Path to the observed run metadata that should be judged",
    )
    parser.add_argument("--adapter-contract", required=True, help="Path to adapter contract")
    parser.add_argument("--output-dir", required=True, help="Directory for emitted judged bundle artifacts")
    parser.add_argument(
        "--cli-command-json",
        required=True,
        help='JSON array command to execute, e.g. ["kimicc","--profile","glm","--print","--output-format","json","--tools",""]',
    )
    parser.add_argument("--runtime-name", required=True, help="Logical runtime label for the judged run")
    parser.add_argument("--runtime-version", required=True, help="Runtime or model version label")
    parser.add_argument(
        "--output-envelope",
        choices=("claude_json_envelope", "raw_json"),
        default="claude_json_envelope",
        help="How to parse CLI stdout",
    )
    parser.add_argument("--system-prompt", help="Optional system prompt string if the CLI supports it")
    parser.add_argument("--timeout-seconds", type=int, default=90, help="Subprocess timeout")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_prompt(case: dict, observed_replay: dict, observed_run: dict) -> str:
    expected = {
        category: " ".join(case["expected_assertions"][bucket])
        for category, bucket in CATEGORY_TO_BUCKET.items()
    }
    prompt_payload = {
        "case": {
            "case_id": case["case_id"],
            "title": case["title"],
            "scenario_kind": case["scenario_kind"],
            "scope_context": case["scope_context"],
            "expected_assertions": expected,
        },
        "observed_replay_artifact": {
            "replay_artifact_id": observed_replay["replay_artifact_id"],
            "scope_context": observed_replay["scope_context"],
            "transcript": observed_replay["transcript"],
            "workspace_diff": observed_replay["workspace_diff"],
        },
        "observed_run_metadata": {
            "run_id": observed_run["run_id"],
            "execution_mode": observed_run["execution_mode"],
            "runtime_name": observed_run["runtime_name"],
            "runtime_version": observed_run["runtime_version"],
            "scope_context": observed_run["scope_context"],
            "result": observed_run["result"],
        },
    }
    return (
        "You are judging an observed AI-Native E2E replay bundle.\n"
        "Return only a JSON object with this exact shape:\n"
        "{"
        '"overall_status":"pass|fail|blocked",'
        '"summary":"short summary",'
        '"assertions":[{"category":"route","status":"pass|fail|blocked","actual":"...","evidence_turn_ids":["turn-id"]}]'
        "}\n"
        "Rules:\n"
        "- categories must be exactly route, read, write, boundary, projection, recovery, trajectory in that order.\n"
        "- use only turn ids that exist in observed_replay_artifact.transcript.\n"
        "- judge from the supplied observed replay artifact and observed run metadata.\n"
        "- if evidence is insufficient for a category, mark that category blocked.\n"
        "- overall_status may be pass, fail, or blocked.\n"
        "- do not invent missing reads, writes, or tool traces.\n"
        "- output only JSON and do not use markdown fences.\n\n"
        f"Bundle payload:\n{json.dumps(prompt_payload, ensure_ascii=False, indent=2)}\n"
    )


def parse_stdout(stdout: str, envelope_mode: str) -> tuple[dict | None, str]:
    if envelope_mode == "raw_json":
        return None, stdout.strip()

    start = stdout.find("{")
    if start == -1:
        raise ValueError("CLI output did not contain a JSON payload")
    envelope = json.loads(stdout[start:])
    if envelope.get("type") != "result":
        raise ValueError("CLI output did not contain a result envelope")
    return envelope, envelope["result"]


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        first_newline = stripped.find("\n")
        if first_newline != -1:
            stripped = stripped[first_newline + 1 :]
        if stripped.endswith("```"):
            stripped = stripped[:-3]
    stripped = stripped.strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("model output did not contain a JSON object")
    return stripped[start : end + 1]


def validate_model_payload(payload: dict, observed_replay: dict) -> None:
    if payload.get("overall_status") not in {"pass", "fail", "blocked"}:
        raise ValueError("overall_status must be pass, fail, or blocked")

    assertions = payload.get("assertions")
    if not isinstance(assertions, list) or len(assertions) != len(ORDERED_CATEGORIES):
        raise ValueError("assertions must contain exactly seven category entries")

    categories = [item.get("category") for item in assertions]
    if categories != ORDERED_CATEGORIES:
        raise ValueError("assertion categories must follow the canonical order")

    known_turn_ids = {turn["turn_id"] for turn in observed_replay["transcript"]}
    for item in assertions:
        if item.get("status") not in {"pass", "fail", "blocked"}:
            raise ValueError(f"invalid assertion status for {item.get('category')}")
        if not isinstance(item.get("actual"), str) or not item["actual"].strip():
            raise ValueError(f"missing actual text for {item.get('category')}")
        evidence_turn_ids = item.get("evidence_turn_ids")
        if not isinstance(evidence_turn_ids, list):
            raise ValueError(f"evidence_turn_ids must be a list for {item.get('category')}")
        unknown = sorted(set(evidence_turn_ids) - known_turn_ids)
        if unknown:
            raise ValueError(
                f"unknown evidence turn ids for {item.get('category')}: {', '.join(unknown)}"
            )


def execute_cli(command: list[str], prompt: str, timeout_seconds: int) -> tuple[dict | None, dict]:
    completed = subprocess.run(
        command,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        cwd=ROOT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or "CLI execution failed")

    envelope, raw_result = parse_stdout(completed.stdout, args.output_envelope)  # type: ignore[name-defined]
    model_payload = json.loads(strip_code_fences(raw_result))
    return envelope, model_payload


def main() -> int:
    global args
    args = parse_args()

    case = load_json(Path(args.case).resolve())
    observed_replay = load_json(Path(args.observed_replay_artifact).resolve())
    observed_run = load_json(Path(args.observed_run_metadata).resolve())
    adapter = load_json(Path(args.adapter_contract).resolve())
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    command = json.loads(args.cli_command_json)
    if not isinstance(command, list) or not command or not all(isinstance(item, str) for item in command):
        raise ValueError("--cli-command-json must decode to a non-empty JSON array of strings")

    prompt = build_prompt(case, observed_replay, observed_run)
    started_at = utc_now()
    envelope, model_payload = execute_cli(command, prompt, args.timeout_seconds)
    finished_at = utc_now()
    validate_model_payload(model_payload, observed_replay)

    run_id = f"run.{case['case_id']}.{args.runtime_name}"
    replay_artifact_id = f"replay.{case['case_id']}.{args.runtime_name}"
    report_id = f"report.{case['case_id']}.{args.runtime_name}"

    run_metadata = {
        "schema_version": "1.0",
        "run_id": run_id,
        "family": "ai_native_e2e_run_metadata",
        "version_anchor": case["version_anchor"],
        "case_ref": case["case_id"],
        "adapter_ref": adapter["adapter_id"],
        "execution_mode": case["scenario_kind"],
        "runtime_name": args.runtime_name,
        "runtime_version": args.runtime_version,
        "scope_context": case["scope_context"],
        "started_at": started_at,
        "finished_at": finished_at,
        "workspace_label": str(output_dir),
        "result": model_payload["overall_status"],
    }

    replay_artifact = {
        "schema_version": "1.0",
        "replay_artifact_id": replay_artifact_id,
        "family": "ai_native_e2e_replay_artifact",
        "version_anchor": case["version_anchor"],
        "case_ref": case["case_id"],
        "adapter_ref": adapter["adapter_id"],
        "run_ref": run_id,
        "scope_context": case["scope_context"],
        "captured_at": finished_at,
        "transcript": [
            *observed_replay["transcript"],
            {
                "turn_id": "turn-live-judge",
                "role": "tool",
                "content": json.dumps(model_payload, ensure_ascii=False),
                "tool_name": args.runtime_name,
                "tool_call_id": envelope.get("session_id", "no-session-envelope") if envelope else "raw-json",
            },
        ],
        "workspace_diff": [
            *observed_replay["workspace_diff"],
            {
                "path": "assertion_report.json",
                "change_kind": "observed",
                "summary": f"live CLI judge emitted overall_status={model_payload['overall_status']}",
            },
        ],
    }

    assertions = []
    for item in model_payload["assertions"]:
        category = item["category"]
        expected_bucket = CATEGORY_TO_BUCKET[category]
        assertions.append(
            {
                "assertion_id": f"{category}.{case['case_id']}.{args.runtime_name}",
                "category": category,
                "status": item["status"],
                "expected": " ".join(case["expected_assertions"][expected_bucket]),
                "actual": item["actual"],
                "evidence_refs": [
                    f"{replay_artifact_id}#{turn_id}" for turn_id in item.get("evidence_turn_ids", [])
                ],
                "notes": model_payload.get("summary", ""),
            }
        )

    assertion_report = {
        "schema_version": "1.0",
        "report_id": report_id,
        "family": "ai_native_e2e_assertion_report",
        "version_anchor": case["version_anchor"],
        "case_ref": case["case_id"],
        "replay_artifact_ref": replay_artifact_id,
        "run_ref": run_id,
        "overall_status": model_payload["overall_status"],
        "assertions": assertions,
        "generated_at": finished_at,
    }

    run_path = output_dir / "run_metadata.json"
    replay_path = output_dir / "replay_artifact.json"
    report_path = output_dir / "assertion_report.json"
    raw_path = output_dir / "cli_raw_output.json"

    dump_json(run_path, run_metadata)
    dump_json(replay_path, replay_artifact)
    dump_json(report_path, assertion_report)
    dump_json(raw_path, envelope if envelope is not None else {"raw_result": model_payload})

    print(
        json.dumps(
            {
                "status": "ok",
                "runtime_name": args.runtime_name,
                "adapter_id": adapter["adapter_id"],
                "case_id": case["case_id"],
                "overall_status": model_payload["overall_status"],
                "run_metadata_path": str(run_path),
                "replay_artifact_path": str(replay_path),
                "assertion_report_path": str(report_path),
                "raw_output_path": str(raw_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # pragma: no cover - integration failure path
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
