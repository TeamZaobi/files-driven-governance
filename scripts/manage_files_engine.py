#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import validate_files_engine_scaffold as scaffold
import validate_governance_assets as pack_validator

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_RUNNER = ROOT / "scripts" / "run_project_director_capability_improvement.py"
HOOK_POLICY_PATH = Path("governance/hooks.policy.md")
AUDIT_LAYERS = ("scaffold", "pack", "runtime", "governance", "adoption")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Operate files-driven meta-skill actions such as register, repair, audit, and capability improvement runs.",
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
    audit.add_argument(
        "--layer",
        choices=AUDIT_LAYERS,
        default="scaffold",
        help="Audit layer to run. Defaults to `scaffold`.",
    )
    audit.add_argument("--format", choices=["text", "json"], default="text")

    repair = subparsers.add_parser("repair", help="Produce an ordered repair plan for scaffold drift.")
    repair.add_argument("project_root", help="Root directory of a files engine project.")
    repair.add_argument("--format", choices=["text", "json"], default="text")

    capability = subparsers.add_parser(
        "capability-improve",
        help="Run the self-hosting project-director capability-improvement workflow through a script-controlled Codex CLI runner.",
    )
    capability.add_argument("output_root", help="Directory where the governed run pack should be written.")
    capability.add_argument(
        "--workspace-root",
        default=str(ROOT),
        help="Workspace root whose canonical docs should be snapshotted into the run pack.",
    )
    capability.add_argument(
        "--benchmark",
        action="append",
        default=[],
        help="Benchmark anchor or conversation id. Repeat for multiple anchors.",
    )
    capability.add_argument("--codex-bin", default="codex", help="Codex CLI binary to call. Defaults to `codex`.")
    capability.add_argument("--model", help="Optional Codex model override.")
    capability.add_argument("--profile", help="Optional Codex profile override.")
    capability.add_argument(
        "--reasoning-effort",
        default="high",
        choices=("minimal", "low", "medium", "high"),
        help="Safe Codex reasoning effort override. Defaults to `high`.",
    )
    capability.add_argument("--force", action="store_true", help="Allow overwriting an existing output directory.")
    capability.add_argument("--format", choices=["text", "json"], default="text")

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
    if "layer" in payload:
        print(f"layer: {payload['layer']}")
    if "message" in payload:
        print(payload["message"])
    if "findings" in payload:
        for finding in payload["findings"]:
            print(f"- [{finding['category']}] {finding['message']}")
    if "warnings" in payload:
        for warning in payload["warnings"]:
            print(f"- [warning/{warning['category']}] {warning['message']}")
    if "steps" in payload:
        for step in payload["steps"]:
            print(f"{step['order']}. {step['summary']}")
            for finding in step["findings"]:
                print(f"   - {finding['message']}")
    if "next_refs" in payload:
        print("next refs:")
        for ref in payload["next_refs"]:
            print(f"- {ref}")


def registry_entry_by_path(registry: dict | None, relative_path: str) -> dict | None:
    if registry is None:
        return None
    for entry in registry.get("entries", []):
        if entry.get("path") == relative_path:
            return entry
    return None


def route_references_file_id(routes: dict | None, file_id: str) -> bool:
    if routes is None:
        return False

    for route in routes.get("routes", []):
        refs = [
            route.get("entrypoint_file_id"),
            *route.get("required_file_ids", []),
            *route.get("write_targets", []),
        ]
        if file_id in refs:
            return True
    return False


def read_text_if_exists(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def read_events_if_exists(path: Path) -> list[dict] | None:
    if not path.exists() or not path.is_file():
        return None

    events: list[dict] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            events.append(json.loads(raw))
        except json.JSONDecodeError:
            return [
                {
                    "event_id": f"invalid-json-{line_no}",
                    "subject_ref": "workflow.events.jsonl",
                    "state_after": {},
                }
            ]
    return events


def text_contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def missing_markers(text: str, markers: tuple[str, ...]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def discover_hook_adapter_paths(project_root: Path) -> list[str]:
    matches: set[str] = set()

    for relative in [
        Path("tooling/hooks/README.md"),
        Path(".codex/hooks.json"),
    ]:
        path = project_root / relative
        if path.exists() and path.is_file():
            matches.add(relative.as_posix())

    for relative_dir in [
        Path("tooling/hooks/templates"),
        Path("tooling/hooks/scripts"),
        Path(".github/hooks"),
    ]:
        root = project_root / relative_dir
        if not root.exists() or not root.is_dir():
            continue
        for child in root.rglob("*"):
            if child.is_file():
                matches.add(child.relative_to(project_root).as_posix())

    return sorted(matches)


def build_hook_findings(
    project_root: Path,
    registry: dict | None,
    routes: dict | None,
) -> list[dict]:
    findings: list[dict] = []
    adapter_paths = discover_hook_adapter_paths(project_root)
    policy_path = project_root / HOOK_POLICY_PATH
    policy_entry = registry_entry_by_path(registry, HOOK_POLICY_PATH.as_posix())

    if adapter_paths and not policy_path.exists():
        findings.append(
            {
                "category": "hooks",
                "message": (
                    "hook adapters are present but `governance/hooks.policy.md` is missing: "
                    + ", ".join(adapter_paths[:4])
                ),
            }
        )

    if policy_path.exists() and policy_entry is None:
        findings.append(
            {
                "category": "hooks",
                "message": (
                    "`governance/hooks.policy.md` exists but is not registered in "
                    "`governance/files.registry.json`"
                ),
            }
        )

    if (
        adapter_paths
        and policy_entry is not None
        and routes is not None
        and not route_references_file_id(routes, policy_entry["file_id"])
    ):
        findings.append(
            {
                "category": "hooks",
                "message": (
                    "hook adapters are present but no route consumes "
                    f"`{policy_entry['file_id']}` from `governance/intent.routes.json`"
                ),
            }
        )

    return findings


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

    if args.layer == "scaffold":
        return run_scaffold_audit(project_root, args.format)
    if args.layer == "pack":
        return run_pack_audit(project_root, args.format)
    if args.layer == "runtime":
        return run_runtime_audit(project_root, args.format)
    if args.layer == "governance":
        return run_governance_audit(project_root, args.format)
    if args.layer == "adoption":
        return run_adoption_audit(project_root, args.format)
    return run_routed_audit(project_root, args.layer, args.format)


def run_scaffold_audit(project_root: Path, fmt: str) -> int:
    _, _, registry, routes, errors = scaffold.load_scaffold_assets(project_root)
    findings = scaffold.build_findings(errors)
    findings.extend(build_hook_findings(project_root, registry, routes))
    payload = {
        "status": "valid" if not findings else "invalid",
        "layer": "scaffold",
        "project_root": str(project_root),
        "finding_count": len(findings),
        "findings": findings,
    }
    print_payload(payload, fmt)
    return 0 if not findings else 1


def pack_finding_category(message: str) -> str:
    prefix = message.split(":", 1)[0]
    mapping = {
        "BOUNDARY.md": "boundary",
        "workflow.contract.json": "workflow_contract",
        "agent.contract.json": "agent_contract",
        "rules.contract.json": "rules_contract",
        "workflow.state.json": "workflow_state",
        "status.projection.json": "status_projection",
        "objects/": "objects",
        "schemas/": "schemas",
        "transition.from_node": "workflow_contract",
        "transition.to_node": "workflow_contract",
    }
    if prefix.startswith("workflow.events.jsonl"):
        return "workflow_events"
    return mapping.get(prefix, "pack")


def build_pack_findings(messages: list[str]) -> list[dict]:
    return [{"category": pack_finding_category(message), "message": message} for message in messages]


def run_pack_audit(project_root: Path, fmt: str) -> int:
    if pack_validator.Draft202012Validator is None:
        print(
            "error: jsonschema package is required; install it with `python3 -m pip install -r requirements-dev.txt`",
            file=sys.stderr,
        )
        return 2

    workflow = pack_validator.maybe_load(project_root / "workflow.contract.json")
    if not workflow:
        payload = {
            "status": "invalid",
            "layer": "pack",
            "project_root": str(project_root),
            "finding_count": 1,
            "findings": [
                {
                    "category": "workflow_contract",
                    "message": "workflow.contract.json not found",
                }
            ],
        }
        print_payload(payload, fmt)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    policy = pack_validator.maybe_load(project_root / "rules.contract.json")
    agent = pack_validator.maybe_load(project_root / "agent.contract.json")
    state = pack_validator.maybe_load(project_root / "workflow.state.json")
    status_projection = pack_validator.maybe_load(project_root / "status.projection.json")
    object_contracts = pack_validator.collect_object_contracts(project_root, warnings, errors)

    pack_validator.validate_boundary_anchor(project_root, errors)
    pack_validator.validate_against_schema(
        workflow,
        "workflow.contract.schema.json",
        "workflow.contract.json",
        errors,
    )
    if agent:
        pack_validator.validate_against_schema(
            agent,
            "agent.contract.schema.json",
            "agent.contract.json",
            errors,
        )

    policy_ids = {policy["policy_id"]} if policy and policy.get("policy_id") else set()
    object_ref_ids = pack_validator.object_ids(object_contracts)
    object_kind_registry = pack_validator.object_kinds(object_contracts)
    agent_contract_ids = pack_validator.contract_agent_ids(agent)
    agent_role_ids = pack_validator.role_ids(agent)
    valid_actor_ids = pack_validator.actor_ids(agent)
    role_approval_registry = pack_validator.role_approval_refs(agent)

    pack_validator.validate_policy_contract(policy, errors)
    node_ids, transition_ids = pack_validator.validate_workflow_contract(
        workflow,
        policy_ids,
        object_ref_ids,
        object_kind_registry,
        agent_contract_ids,
        agent_role_ids,
        role_approval_registry,
        errors,
    )
    pack_validator.validate_state(state, workflow, node_ids, errors)
    event_ids = pack_validator.validate_events(
        project_root / "workflow.events.jsonl",
        workflow,
        node_ids,
        transition_ids,
        valid_actor_ids,
        warnings,
        errors,
    )
    if state and state.get("last_event_id") and event_ids and state["last_event_id"] not in event_ids:
        errors.append(
            f"workflow.state.json: last_event_id `{state['last_event_id']}` not found in workflow.events.jsonl"
        )
    pack_validator.validate_status_projection(status_projection, state, workflow, node_ids, errors)
    pack_validator.validate_markdown_tokens(project_root, warnings)

    findings = build_pack_findings(errors)
    warning_payload = build_pack_findings(warnings)
    payload = {
        "status": "valid" if not findings else "invalid",
        "layer": "pack",
        "project_root": str(project_root),
        "finding_count": len(findings),
        "findings": findings,
        "warning_count": len(warning_payload),
        "warnings": warning_payload,
    }
    print_payload(payload, fmt)
    return 0 if not findings else 1


def runtime_chain_applicable(project_root: Path, workflow: dict | None) -> bool:
    node_ids = {node.get("node_id") for node in workflow.get("nodes", [])} if workflow else set()
    return any(
        [
            (project_root / "active-observations.md").exists(),
            (project_root / "candidate_trial.md").exists(),
            (project_root / "activation_decision.md").exists(),
            "node.candidate_trial" in node_ids,
            "node.activation_or_rollback" in node_ids,
        ]
    )


def runtime_finding(category: str, message: str) -> dict:
    return {"category": category, "message": message}


def governance_finding(category: str, message: str) -> dict:
    return {"category": category, "message": message}


def adoption_finding(category: str, message: str) -> dict:
    return {"category": category, "message": message}


def projection_denies_authority(summary: str) -> bool:
    lower = summary.lower()
    derived_markers = ("derived", "read-only")
    deny_markers = (
        "does not authorize",
        "not authorize",
        "no authority",
        "deny activation authority",
    )
    return (
        any(marker in lower for marker in derived_markers) or text_contains_any(summary, ("派生", "只读"))
    ) and (
        any(marker in lower for marker in deny_markers)
        or text_contains_any(summary, ("不授权", "不能授权", "不负责授权", "不构成放行"))
    )


def self_hosting_governance_applicable(project_root: Path) -> bool:
    return all(
        [
            (project_root / "README.md").exists(),
            (project_root / "SKILL.md").exists(),
            (project_root / "docs" / "项目治理能力模型.md").exists(),
            (project_root / "agents" / "openai.yaml").exists(),
        ]
    )


def self_hosting_adoption_applicable(project_root: Path) -> bool:
    return all(
        [
            (project_root / "README.md").exists(),
            (project_root / "SKILL.md").exists(),
            (project_root / "agents" / "openai.yaml").exists(),
        ]
    )


def downstream_governance_applicable(project_root: Path) -> bool:
    return all(
        [
            (project_root / "BOUNDARY.md").exists(),
            (project_root / "workflow.contract.json").exists(),
            (project_root / "governance" / "files.registry.json").exists(),
            (project_root / "governance" / "intent.routes.json").exists(),
        ]
    )


def downstream_skill_paths(project_root: Path) -> list[Path]:
    skills_root = project_root / "skills"
    if not skills_root.exists() or not skills_root.is_dir():
        return []
    return sorted(path for path in skills_root.rglob("SKILL.md") if path.is_file())


def run_governance_audit(project_root: Path, fmt: str) -> int:
    findings: list[dict] = []
    profile: str | None = None

    if self_hosting_governance_applicable(project_root):
        profile = "self_hosting_capability_repo"

        readme = read_text_if_exists(project_root / "README.md")
        if readme is None:
            findings.append(governance_finding("entrypoint", "README.md missing for self-hosting governance audit"))
        elif "docs/项目治理能力模型.md" not in readme:
            findings.append(
                governance_finding(
                    "truth_source",
                    "README.md must point back to `docs/项目治理能力模型.md` instead of defining parallel truth",
                )
            )

        skill = read_text_if_exists(project_root / "SKILL.md")
        if skill is None:
            findings.append(governance_finding("entrypoint", "SKILL.md missing for self-hosting governance audit"))
        else:
            if "docs/项目治理能力模型.md" not in skill:
                findings.append(
                    governance_finding(
                        "truth_source",
                        "SKILL.md must point back to `docs/项目治理能力模型.md` as canonical source",
                    )
                )
            if not text_contains_any(skill, ("只负责执行导览", "不与真源平行定义本体")):
                findings.append(
                    governance_finding(
                        "authority_surface",
                        "SKILL.md must explicitly deny parallel ontology and stay an execution guide",
                    )
                )
            missing_scope_markers = missing_markers(skill, ("capability_scope", "project_scope", "self-hosting"))
            if missing_scope_markers:
                findings.append(
                    governance_finding(
                        "scope_binding",
                        "SKILL.md must explicitly bind self-hosting scope markers: "
                        + ", ".join(missing_scope_markers),
                    )
                )

        metadata = read_text_if_exists(project_root / "agents" / "openai.yaml")
        if metadata is None:
            findings.append(
                governance_finding("entrypoint", "agents/openai.yaml missing for self-hosting governance audit")
            )
        else:
            if "不要把 metadata 自己写成压缩版本体" not in metadata:
                findings.append(
                    governance_finding(
                        "authority_surface",
                        "agents/openai.yaml must explicitly avoid becoming compressed ontology",
                    )
                )
            missing_scope_markers = missing_markers(metadata, ("capability_scope", "project_scope", "self-hosting"))
            if missing_scope_markers:
                findings.append(
                    governance_finding(
                        "scope_binding",
                        "agents/openai.yaml must retain self-hosting scope markers: "
                        + ", ".join(missing_scope_markers),
                    )
                )

    elif downstream_governance_applicable(project_root):
        profile = "downstream_project_instance"

        readme = read_text_if_exists(project_root / "README.md")
        if readme is None:
            findings.append(governance_finding("entrypoint", "README.md missing for downstream governance audit"))
        else:
            missing_readme_markers = missing_markers(
                readme,
                (
                    "downstream project instance",
                    "BOUNDARY.md",
                    "governance/files.registry.json",
                    "governance/intent.routes.json",
                    "workflow.contract.json",
                ),
            )
            if missing_readme_markers:
                findings.append(
                    governance_finding(
                        "truth_source",
                        "README.md must route readers back to downstream truth assets: "
                        + ", ".join(missing_readme_markers),
                    )
                )

        for skill_path in downstream_skill_paths(project_root):
            skill_text = read_text_if_exists(skill_path)
            if skill_text is None:
                continue
            missing_skill_markers = missing_markers(
                skill_text,
                (
                    "BOUNDARY.md",
                    "governance/files.registry.json",
                    "governance/intent.routes.json",
                    "workflow.contract.json",
                ),
            )
            if missing_skill_markers:
                findings.append(
                    governance_finding(
                        "skill_entry",
                        f"{skill_path.relative_to(project_root).as_posix()} must route back to truth assets: "
                        + ", ".join(missing_skill_markers),
                    )
                )
            if not text_contains_any(
                skill_text,
                (
                    "不在 prose 中改写注册表或 route 合同",
                    "先登记注册表，再改 workflow 或运行态",
                ),
            ):
                findings.append(
                    governance_finding(
                        "authority_surface",
                        f"{skill_path.relative_to(project_root).as_posix()} must deny prose-level authority drift",
                    )
                )

        hooks_readme = read_text_if_exists(project_root / "tooling" / "hooks" / "README.md")
        if hooks_readme is not None:
            if "governance/hooks.policy.md" not in hooks_readme:
                findings.append(
                    governance_finding(
                        "hooks_adapter",
                        "tooling/hooks/README.md must point back to `governance/hooks.policy.md`",
                    )
                )
            if not text_contains_any(hooks_readme, ("不是 control truth", "不是真源")):
                findings.append(
                    governance_finding(
                        "authority_surface",
                        "tooling/hooks/README.md must explicitly deny becoming hook control truth",
                    )
                )

        status_projection = pack_validator.maybe_load(project_root / "status.projection.json")
        if status_projection:
            summary = status_projection.get("summary", "")
            if not projection_denies_authority(summary):
                findings.append(
                    governance_finding(
                        "status_projection",
                        "status.projection.json summary must stay derived/read-only and deny write authority",
                    )
                )

    else:
        payload = {
            "status": "not_applicable",
            "layer": "governance",
            "project_root": str(project_root),
            "message": (
                "当前目录没有暴露 self-hosting 或 downstream governance draft checker 所需的最小锚点；"
                "governance audit 暂不适用。"
            ),
            "next_refs": audit_routing_refs("governance"),
            "implemented": True,
        }
        print_payload(payload, fmt)
        return 0

    payload = {
        "status": "valid" if not findings else "invalid",
        "layer": "governance",
        "project_root": str(project_root),
        "profile": profile,
        "finding_count": len(findings),
        "findings": findings,
        "implemented": True,
    }
    print_payload(payload, fmt)
    return 0 if not findings else 1


def run_adoption_audit(project_root: Path, fmt: str) -> int:
    if not self_hosting_adoption_applicable(project_root):
        payload = {
            "status": "not_applicable",
            "layer": "adoption",
            "project_root": str(project_root),
            "message": (
                "当前目录没有暴露 self-hosting adoption draft checker 所需的最小入口锚点；"
                "adoption audit 暂不适用。"
            ),
            "next_refs": audit_routing_refs("adoption"),
            "implemented": True,
        }
        print_payload(payload, fmt)
        return 0

    findings: list[dict] = []

    readme = read_text_if_exists(project_root / "README.md")
    if readme is None:
        findings.append(adoption_finding("entrypoint", "README.md missing for adoption audit"))
    else:
        missing_readme_markers = missing_markers(
            readme,
            (
                "docs/非工程背景起步.md",
                "install / register / repair / audit",
                "docs/宿主化知识工作场景矩阵.md",
            ),
        )
        if missing_readme_markers:
            findings.append(
                adoption_finding(
                    "entrypoint",
                    "README.md must expose beginner path, first actions, and host-name-first routing anchors: "
                    + ", ".join(missing_readme_markers),
                )
            )

    beginner_guide = read_text_if_exists(project_root / "docs" / "非工程背景起步.md")
    if beginner_guide is None:
        findings.append(
            adoption_finding(
                "beginner_guide",
                "docs/非工程背景起步.md missing; adoption draft checker requires a beginner entrypoint",
            )
        )
    else:
        missing_beginner_markers = missing_markers(
            beginner_guide,
            (
                "哪份文件算数",
                "今天先做什么",
                "哪些文件先别改",
                "基础体检",
            ),
        )
        if missing_beginner_markers:
            findings.append(
                adoption_finding(
                    "beginner_guide",
                    "docs/非工程背景起步.md must keep low-bandwidth beginner anchors: "
                    + ", ".join(missing_beginner_markers),
                )
            )

    skill = read_text_if_exists(project_root / "SKILL.md")
    if skill is None:
        findings.append(adoption_finding("skill", "SKILL.md missing for adoption audit"))
    else:
        missing_skill_markers = missing_markers(
            skill,
            (
                "目标读者几乎没有软件工程基础",
                "先把 `Obsidian / Notion / Docs / Sheets / Slides` 视为宿主名",
                "先判断用户是在问治理问题还是工具操作问题",
            ),
        )
        if missing_skill_markers:
            findings.append(
                adoption_finding(
                    "skill",
                    "SKILL.md must preserve low-bandwidth and host-name-first triage markers: "
                    + ", ".join(missing_skill_markers),
                )
            )

    metadata = read_text_if_exists(project_root / "agents" / "openai.yaml")
    if metadata is None:
        findings.append(adoption_finding("metadata", "agents/openai.yaml missing for adoption audit"))
    else:
        missing_metadata_markers = missing_markers(
            metadata,
            (
                "哪份文件算数 / 今天先做哪一步 / 哪些先别改",
                "Obsidian / Notion / Docs / Sheets / Slides",
                "治理问题还是工具操作问题",
            ),
        )
        if missing_metadata_markers:
            findings.append(
                adoption_finding(
                    "metadata",
                    "agents/openai.yaml must preserve low-bandwidth and host-name-first routing markers: "
                    + ", ".join(missing_metadata_markers),
                )
            )

    hosted_matrix = read_text_if_exists(project_root / "docs" / "宿主化知识工作场景矩阵.md")
    if hosted_matrix is None:
        findings.append(
            adoption_finding(
                "hosted_matrix",
                "docs/宿主化知识工作场景矩阵.md missing; host-name-first adoption routing needs an official matrix",
            )
        )
    elif not text_contains_any(hosted_matrix, ("治理问题", "工具操作问题")):
        findings.append(
            adoption_finding(
                "hosted_matrix",
                "docs/宿主化知识工作场景矩阵.md must keep governance-vs-tool-operation triage markers",
            )
        )

    payload = {
        "status": "valid" if not findings else "invalid",
        "layer": "adoption",
        "project_root": str(project_root),
        "profile": "self_hosting_capability_repo",
        "finding_count": len(findings),
        "findings": findings,
        "implemented": True,
    }
    print_payload(payload, fmt)
    return 0 if not findings else 1


def run_runtime_audit(project_root: Path, fmt: str) -> int:
    workflow = pack_validator.maybe_load(project_root / "workflow.contract.json")
    if not workflow:
        payload = {
            "status": "invalid",
            "layer": "runtime",
            "project_root": str(project_root),
            "finding_count": 1,
            "findings": [
                runtime_finding("workflow_contract", "workflow.contract.json not found"),
            ],
            "implemented": True,
        }
        print_payload(payload, fmt)
        return 1

    if not runtime_chain_applicable(project_root, workflow):
        payload = {
            "status": "not_applicable",
            "layer": "runtime",
            "project_root": str(project_root),
            "message": (
                "当前 pack 没有暴露官方的 observation -> candidate -> activation runtime 链；"
                "runtime draft audit 暂不适用。"
            ),
            "next_refs": audit_routing_refs("runtime"),
            "implemented": True,
        }
        print_payload(payload, fmt)
        return 0

    findings: list[dict] = []

    active_observations = read_text_if_exists(project_root / "active-observations.md")
    if active_observations is None:
        findings.append(
            runtime_finding(
                "runtime_observation",
                "active-observations.md missing; runtime observation entry is required for this draft runtime audit",
            )
        )
    elif "不负责改写能力真源" not in active_observations and "not rewrite capability truth" not in active_observations:
        findings.append(
            runtime_finding(
                "runtime_observation",
                "active-observations.md must explicitly block hot-editing capability truth",
            )
        )

    candidate_trial = read_text_if_exists(project_root / "candidate_trial.md")
    if candidate_trial is None:
        findings.append(
            runtime_finding(
                "candidate_trial",
                "candidate_trial.md missing; runtime candidate trial page is required for this draft runtime audit",
            )
        )
    else:
        for required in ("failure_signals", "rollback_path"):
            if required not in candidate_trial:
                findings.append(
                    runtime_finding(
                        "candidate_trial",
                        f"candidate_trial.md missing `{required}`",
                    )
                )

    activation_decision = read_text_if_exists(project_root / "activation_decision.md")
    if activation_decision is None:
        findings.append(
            runtime_finding(
                "activation_decision",
                "activation_decision.md missing; activation or rollback landing page is required for this draft runtime audit",
            )
        )
    else:
        for marker in ("不是正式激活真源", "不能冒充正式激活"):
            if marker not in activation_decision:
                findings.append(
                    runtime_finding(
                        "activation_decision",
                        f"activation_decision.md missing `{marker}` runtime guard",
                    )
                )

    workflow_md = read_text_if_exists(project_root / "WORKFLOW.md")
    if workflow_md is None:
        findings.append(runtime_finding("workflow_markdown", "WORKFLOW.md missing"))
    else:
        if "activation_decision.md" not in workflow_md or "not a formal activation authority" not in workflow_md:
            findings.append(
                runtime_finding(
                    "workflow_markdown",
                    "WORKFLOW.md must state that activation_decision.md is not formal activation authority",
                )
            )
        if "failure signals, and rollback path" not in workflow_md:
            findings.append(
                runtime_finding(
                    "workflow_markdown",
                    "WORKFLOW.md must declare failure signals and rollback path before activation",
                )
            )

    policy = pack_validator.maybe_load(project_root / "rules.contract.json")
    rules = policy.get("rules", []) if policy else []
    if not any(rule.get("effect") == "require_rollback" for rule in rules):
        findings.append(
            runtime_finding(
                "rules_contract",
                "rules.contract.json must contain a `require_rollback` rule for runtime activation or rollback",
            )
        )
    if not any(
        "failure signals" in (rule.get("condition_ref") or "")
        and "rollback path" in (rule.get("condition_ref") or "")
        for rule in rules
    ):
        findings.append(
            runtime_finding(
                "rules_contract",
                "rules.contract.json must declare failure signals and rollback path before activation",
            )
        )

    state = pack_validator.maybe_load(project_root / "workflow.state.json")
    if state and state.get("current_node_id") == "node.activation_or_rollback" and state.get("missing_evidence_refs"):
        findings.append(
            runtime_finding(
                "workflow_state",
                "workflow.state.json reached activation_or_rollback while missing_evidence_refs is not empty",
            )
        )

    status_projection = pack_validator.maybe_load(project_root / "status.projection.json")
    summary = status_projection.get("summary", "") if status_projection else ""
    if not status_projection:
        findings.append(runtime_finding("status_projection", "status.projection.json missing"))
    elif "read-only" not in summary or "activation authority" not in summary:
        findings.append(
            runtime_finding(
                "status_projection",
                "status.projection.json summary must state read-only status and deny activation authority",
            )
        )

    events = read_events_if_exists(project_root / "workflow.events.jsonl")
    if not events:
        findings.append(runtime_finding("workflow_events", "workflow.events.jsonl missing or empty"))
    elif state and state.get("current_node_id") == "node.activation_or_rollback":
        last_event = events[-1]
        if last_event.get("subject_ref") != "transition.candidate-trial-to-activation-or-rollback":
            findings.append(
                runtime_finding(
                    "workflow_events",
                    "last runtime event must land through transition.candidate-trial-to-activation-or-rollback",
                )
            )
        if last_event.get("state_after", {}).get("current_node_id") != "node.activation_or_rollback":
            findings.append(
                runtime_finding(
                    "workflow_events",
                    "last runtime event must land on node.activation_or_rollback",
                )
            )

    payload = {
        "status": "valid" if not findings else "invalid",
        "layer": "runtime",
        "project_root": str(project_root),
        "finding_count": len(findings),
        "findings": findings,
        "implemented": True,
    }
    print_payload(payload, fmt)
    return 0 if not findings else 1


def audit_routing_refs(layer: str) -> list[str]:
    mapping = {
        "runtime": [
            "references/运行观察与能力晋升.md",
            "examples/capture-candidate-activation/README.md",
            "docs/体检分层矩阵.md",
        ],
        "governance": [
            "docs/项目治理能力模型.md",
            "docs/三层信息架构复盘.md",
            "references/工具适配对照表.md",
            "docs/体检分层矩阵.md",
        ],
        "adoption": [
            "docs/非工程背景起步.md",
            "docs/宿主化知识工作场景矩阵.md",
            "references/理解型输入与低带宽压缩包.md",
            "docs/体检分层矩阵.md",
        ],
    }
    return mapping[layer]


def run_routed_audit(project_root: Path, layer: str, fmt: str) -> int:
    payload = {
        "status": "routed",
        "layer": layer,
        "project_root": str(project_root),
        "message": (
            f"`audit --layer {layer}` 已完成层级判定，但当前还不是统一执行面；"
            "先按官方矩阵和 reference 做专项检查。"
        ),
        "next_refs": audit_routing_refs(layer),
        "implemented": False,
    }
    print_payload(payload, fmt)
    return 0


def build_repair_steps(findings: list[dict]) -> list[dict]:
    priorities = ["manifest", "hooks", "starter_profile", "registry", "routes", "scaffold"]
    summaries = {
        "manifest": "Fix starter topology and tracked-path declarations first",
        "hooks": "Restore project-level hook truth before wiring or keeping adapters",
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

    _, _, registry, routes, errors = scaffold.load_scaffold_assets(project_root)
    findings = scaffold.build_findings(errors)
    findings.extend(build_hook_findings(project_root, registry, routes))
    steps = build_repair_steps(findings)
    payload = {
        "status": "clean" if not steps else "repair_needed",
        "project_root": str(project_root),
        "step_count": len(steps),
        "steps": steps,
    }
    print_payload(payload, args.format)
    return 0 if not steps else 1


def run_capability_improve(args: argparse.Namespace) -> int:
    output_root = Path(args.output_root).expanduser().resolve()
    workspace_root = Path(args.workspace_root).expanduser().resolve()

    if not workspace_root.exists():
        print(f"error: workspace root does not exist: `{workspace_root}`", file=sys.stderr)
        return 1
    if not CAPABILITY_RUNNER.exists():
        print(f"error: capability runner not found: `{CAPABILITY_RUNNER}`", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        str(CAPABILITY_RUNNER),
        str(output_root),
        "--workspace-root",
        str(workspace_root),
        "--codex-bin",
        args.codex_bin,
        "--reasoning-effort",
        args.reasoning_effort,
    ]
    if args.model:
        command.extend(["--model", args.model])
    if args.profile:
        command.extend(["--profile", args.profile])
    if args.force:
        command.append("--force")
    for benchmark in args.benchmark:
        command.extend(["--benchmark", benchmark])

    result = subprocess.run(
        command,
        cwd=workspace_root,
        capture_output=True,
        text=True,
        check=False,
    )
    payload = {
        "status": "completed" if result.returncode == 0 else "failed",
        "output_root": str(output_root),
        "workspace_root": str(workspace_root),
        "command": command,
        "message": (
            f"capability improvement run completed at `{output_root}`"
            if result.returncode == 0
            else f"capability improvement run failed at `{output_root}`"
        ),
    }
    if result.stdout.strip():
        payload["stdout"] = result.stdout.strip()
    if result.stderr.strip():
        payload["stderr"] = result.stderr.strip()
    print_payload(payload, args.format)
    return result.returncode


def main() -> int:
    args = parse_args()
    if args.command == "register":
        return run_register(args)
    if args.command == "audit":
        return run_audit(args)
    if args.command == "repair":
        return run_repair(args)
    if args.command == "capability-improve":
        return run_capability_improve(args)
    print(f"error: unknown command `{args.command}`", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
