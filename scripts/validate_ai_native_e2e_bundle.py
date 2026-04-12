#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - exercised via CLI tests
    Draft202012Validator = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"

SCHEMA_FILES = {
    "case": "ai-native-e2e.case.schema.json",
    "replay_artifact": "ai-native-e2e.replay-artifact.schema.json",
    "assertion_report": "ai-native-e2e.assertion-report.schema.json",
    "run_metadata": "ai-native-e2e.run-metadata.schema.json",
    "adapter_contract": "ai-native-e2e.adapter-contract.schema.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an AI-Native E2E replay bundle and emit a machine-readable summary."
    )
    parser.add_argument("--case", required=True, help="Path to ai-native-e2e case contract")
    parser.add_argument("--replay-artifact", required=True, help="Path to replay artifact")
    parser.add_argument("--assertion-report", required=True, help="Path to assertion report")
    parser.add_argument("--run-metadata", required=True, help="Path to run metadata")
    parser.add_argument("--adapter-contract", required=True, help="Path to adapter contract")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_validator(schema_name: str) -> Draft202012Validator:
    if Draft202012Validator is None:
        raise RuntimeError("jsonschema package is required to validate AI-Native E2E bundles")
    schema = load_json(SCHEMA_ROOT / SCHEMA_FILES[schema_name])
    return Draft202012Validator(schema)


def validation_errors(validator: Draft202012Validator, payload: dict, label: str) -> list[str]:
    errors: list[str] = []
    for issue in sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path)):
        pointer = "$"
        for item in issue.absolute_path:
            pointer += f"[{item}]" if isinstance(item, int) else f".{item}"
        errors.append(f"{label}: schema violation at {pointer}: {issue.message}")
    return errors


def main() -> int:
    args = parse_args()
    paths = {
        "case": Path(args.case),
        "replay_artifact": Path(args.replay_artifact),
        "assertion_report": Path(args.assertion_report),
        "run_metadata": Path(args.run_metadata),
        "adapter_contract": Path(args.adapter_contract),
    }

    errors: list[str] = []
    payloads: dict[str, dict] = {}
    validators = {name: build_validator(name) for name in paths}

    for name, path in paths.items():
        if not path.exists():
            errors.append(f"{name}: file not found `{path}`")
            continue
        payload = load_json(path)
        payloads[name] = payload
        errors.extend(validation_errors(validators[name], payload, name))

    if errors:
        print(json.dumps({"status": "invalid", "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    case = payloads["case"]
    replay_artifact = payloads["replay_artifact"]
    assertion_report = payloads["assertion_report"]
    run_metadata = payloads["run_metadata"]
    adapter = payloads["adapter_contract"]

    expected_buckets = {
        "route": "route_assertions",
        "read": "read_assertions",
        "write": "write_assertions",
        "boundary": "boundary_assertions",
        "projection": "projection_assertions",
        "recovery": "recovery_assertions",
        "trajectory": "trajectory_assertions",
    }

    if replay_artifact["case_ref"] != case["case_id"]:
        errors.append("replay_artifact.case_ref must match case.case_id")
    if replay_artifact["adapter_ref"] != adapter["adapter_id"]:
        errors.append("replay_artifact.adapter_ref must match adapter_contract.adapter_id")
    if replay_artifact["run_ref"] != run_metadata["run_id"]:
        errors.append("replay_artifact.run_ref must match run_metadata.run_id")
    if assertion_report["case_ref"] != case["case_id"]:
        errors.append("assertion_report.case_ref must match case.case_id")
    if assertion_report["replay_artifact_ref"] != replay_artifact["replay_artifact_id"]:
        errors.append("assertion_report.replay_artifact_ref must match replay_artifact.replay_artifact_id")
    if assertion_report["run_ref"] != run_metadata["run_id"]:
        errors.append("assertion_report.run_ref must match run_metadata.run_id")
    if run_metadata["case_ref"] != case["case_id"]:
        errors.append("run_metadata.case_ref must match case.case_id")
    if run_metadata["adapter_ref"] != adapter["adapter_id"]:
        errors.append("run_metadata.adapter_ref must match adapter_contract.adapter_id")

    for scope_key in ("capability_scope", "project_scope", "runtime_scope"):
        reference_value = case["scope_context"][scope_key]
        if replay_artifact["scope_context"][scope_key] != reference_value:
            errors.append(f"replay_artifact.scope_context.{scope_key} must match case.scope_context.{scope_key}")
        if run_metadata["scope_context"][scope_key] != reference_value:
            errors.append(f"run_metadata.scope_context.{scope_key} must match case.scope_context.{scope_key}")

    categories = {item["category"] for item in assertion_report["assertions"]}
    for category, bucket in expected_buckets.items():
        if bucket not in case["expected_assertions"]:
            errors.append(f"case.expected_assertions must declare `{bucket}`")
        if category not in categories:
            errors.append(f"assertion_report.assertions must contain category `{category}`")

    if assertion_report["overall_status"] != run_metadata["result"]:
        errors.append("assertion_report.overall_status must match run_metadata.result")
    if not any(turn["role"] == "tool" for turn in replay_artifact["transcript"]):
        errors.append("replay_artifact.transcript must include at least one tool turn")
    if not replay_artifact["workspace_diff"]:
        errors.append("replay_artifact.workspace_diff must include at least one observed diff")

    if errors:
        print(json.dumps({"status": "invalid", "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    summary = {
        "status": "valid",
        "case_id": case["case_id"],
        "run_id": run_metadata["run_id"],
        "replay_artifact_id": replay_artifact["replay_artifact_id"],
        "adapter_id": adapter["adapter_id"],
        "checked_categories": list(expected_buckets.keys()),
        "scenario_kind": case["scenario_kind"],
        "execution_mode": run_metadata["execution_mode"],
        "workspace_label": run_metadata["workspace_label"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
