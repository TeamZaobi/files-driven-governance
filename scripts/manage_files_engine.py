#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import validate_files_engine_scaffold as scaffold


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Operate files-driven meta-skill actions: register, repair, and audit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    register = subparsers.add_parser("register", help="Register a tracked file into governance/files.registry.json.")
    register.add_argument("project_root", help="Root directory of a files engine project.")
    register.add_argument("--file-id", required=True, help="Stable file id for the registry entry.")
    register.add_argument("--path", required=True, help="Project-relative file path to register.")
    register.add_argument("--family", required=True, help="Structure family for the file.")
    register.add_argument("--layer", required=True, help="Layer for the file.")
    register.add_argument("--work-post", required=True, help="Work post for the file.")
    register.add_argument("--evidence-type", help="Optional annotation: evidence type.")
    register.add_argument("--truth-status", help="Optional annotation: truth status.")
    register.add_argument("--write-role", action="append", default=[], help="Optional annotation: write role.")
    register.add_argument("--consumed-as", action="append", default=[], help="Optional annotation: consumed_as.")
    register.add_argument("--upstream-ref", action="append", default=[], help="Optional annotation: upstream ref.")
    register.add_argument("--stale-policy", help="Optional annotation: stale policy.")
    register.add_argument("--replace", action="store_true", help="Replace an existing entry with the same file_id/path.")
    register.add_argument("--format", choices=["text", "json"], default="text")

    audit = subparsers.add_parser("audit", help="Produce a finding-style audit report for a files engine project.")
    audit.add_argument("project_root", help="Root directory of a files engine project.")
    audit.add_argument("--format", choices=["text", "json"], default="text")

    repair = subparsers.add_parser("repair", help="Produce an ordered repair plan for scaffold drift.")
    repair.add_argument("project_root", help="Root directory of a files engine project.")
    repair.add_argument("--format", choices=["text", "json"], default="text")

    return parser.parse_args()


def dump_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_entry(args: argparse.Namespace) -> dict:
    entry = {
        "file_id": args.file_id,
        "path": args.path,
        "family": args.family,
        "layer": args.layer,
        "work_post": args.work_post,
    }

    annotations: dict[str, object] = {}
    if args.evidence_type:
        annotations["evidence_type"] = args.evidence_type
    if args.truth_status:
        annotations["truth_status"] = args.truth_status
    if args.write_role:
        annotations["write_roles"] = args.write_role
    if args.consumed_as:
        annotations["consumed_as"] = args.consumed_as
    if args.upstream_ref:
        annotations["upstream_refs"] = args.upstream_ref
    if args.stale_policy:
        annotations["stale_policy"] = args.stale_policy

    if annotations:
        entry["annotations"] = annotations
    return entry


def print_payload(payload: dict, fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    status = payload.get("status")
    print(f"status: {status}")
    if "message" in payload:
        print(payload["message"])
    if "findings" in payload:
        for finding in payload["findings"]:
            print(f"- [{finding['category']}] {finding['message']}")
    if "steps" in payload:
        for step in payload["steps"]:
            print(f"{step['order']}. {step['summary']}")
            for finding in step["findings"]:
                print(f"   - {finding['message']}")


def run_register(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        print(f"error: project root does not exist: `{project_root}`", file=sys.stderr)
        return 1

    errors: list[str] = []
    manifest, _, registry, _ = scaffold.ensure_required_paths(project_root, errors)
    if manifest is None or registry is None:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    target_path = project_root / args.path
    if not target_path.exists():
        print(f"error: target file does not exist: `{args.path}`", file=sys.stderr)
        return 1

    entry = build_entry(args)
    schema_errors: list[str] = []
    scaffold.validate_against_schema(entry, "file.registration.schema.json", "registry entry", schema_errors)
    if schema_errors:
        for error in schema_errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    registry_path = project_root / manifest["registry_path"]
    original_registry = json.loads(json.dumps(registry))
    matches = [
        index
        for index, existing in enumerate(registry["entries"])
        if existing["file_id"] == args.file_id or existing["path"] == args.path
    ]

    if matches and not args.replace:
        print(
            "error: matching file_id/path already exists in governance/files.registry.json; use --replace to overwrite",
            file=sys.stderr,
        )
        return 1

    if matches:
        for index in reversed(matches):
            registry["entries"].pop(index)

    registry["entries"].append(entry)
    registry["entries"].sort(key=lambda item: item["path"])

    try:
        dump_json(registry_path, registry)
    except Exception:
        dump_json(registry_path, original_registry)
        raise

    payload = {
        "status": "registered",
        "project_root": str(project_root),
        "entry": entry,
        "message": f"registered `{args.path}` into governance/files.registry.json",
    }
    print_payload(payload, args.format)
    return 0


def run_audit(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        print(f"error: project root does not exist: `{project_root}`", file=sys.stderr)
        return 1

    _, _, _, _, errors = scaffold.load_scaffold_assets(project_root)
    findings = scaffold.build_findings(errors)
    payload = {
        "status": "valid" if not findings else "invalid",
        "project_root": str(project_root),
        "finding_count": len(findings),
        "findings": findings,
    }
    print_payload(payload, args.format)
    return 0 if not findings else 1


def build_repair_steps(findings: list[dict]) -> list[dict]:
    priorities = ["manifest", "starter_profile", "registry", "routes", "scaffold"]
    summaries = {
        "manifest": "Fix starter topology and tracked-path declarations first",
        "starter_profile": "Align starter-specific shape expectations with registry second",
        "registry": "Fix file registrations, identity drift, and annotations next",
        "routes": "Repair route references after registry is stable",
        "scaffold": "Review remaining scaffold-level findings",
    }
    steps: list[dict] = []
    for category in priorities:
        category_findings = [finding for finding in findings if finding["category"] == category]
        if not category_findings:
            continue
        steps.append(
            {
                "order": len(steps) + 1,
                "category": category,
                "summary": summaries[category],
                "findings": category_findings,
            }
        )
    return steps


def run_repair(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        print(f"error: project root does not exist: `{project_root}`", file=sys.stderr)
        return 1

    _, _, _, _, errors = scaffold.load_scaffold_assets(project_root)
    findings = scaffold.build_findings(errors)
    steps = build_repair_steps(findings)
    payload = {
        "status": "clean" if not steps else "repair_needed",
        "project_root": str(project_root),
        "step_count": len(steps),
        "steps": steps,
    }
    print_payload(payload, args.format)
    return 0 if not steps else 1


def main() -> int:
    args = parse_args()
    if args.command == "register":
        return run_register(args)
    if args.command == "audit":
        return run_audit(args)
    if args.command == "repair":
        return run_repair(args)
    print(f"error: unknown command `{args.command}`", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
