#!/usr/bin/env python3
from __future__ import annotations

import argparse
import functools
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - exercised through CLI in tests
    Draft202012Validator = None

# Schemas remain the source of field shape. This validator focuses on
# cross-file semantics, pack hygiene, and a small compatibility surface.

SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas"


REQUIRED_STATE_KEYS = {
    "schema_version",
    "run_id",
    "workflow_id",
    "contract_version",
    "current_node_id",
    "gate_state",
    "required_evidence_refs",
    "missing_evidence_refs",
    "allowed_next_step_refs",
    "forbidden_output_refs",
    "updated_at",
    "last_event_id",
}

REQUIRED_EVENT_KEYS = {
    "schema_version",
    "event_id",
    "run_id",
    "workflow_id",
    "contract_version",
    "timestamp",
    "actor_id",
    "event_type",
    "subject_ref",
    "state_after",
}

REQUIRED_STATUS_PROJECTION_KEYS = {
    "schema_version",
    "projection_id",
    "family",
    "workflow_id",
    "run_id",
    "contract_version",
    "source_last_event_id",
    "current_node_id",
    "gate_state",
    "missing_evidence_refs",
    "forbidden_output_refs",
    "summary",
    "generated_at",
}

REQUIRED_POLICY_KEYS = {
    "schema_version",
    "policy_id",
    "family",
    "version_anchor",
    "scope",
    "rules",
}

REQUIRED_POLICY_RULE_KEYS = {
    "rule_id",
    "effect",
}

POLICY_EFFECTS = {
    "allow",
    "deny",
    "require_review",
    "require_evidence",
    "require_rollback",
}

GATE_STATES = {
    "blocked",
    "partial",
    "ready",
}

FORBIDDEN_STATUS_PROJECTION_KEYS = {
    "allowed_next_step_refs",
    "approval_ref",
    "approver_ref",
    "guard_policy_refs",
    "output_policy_refs",
    "required_check_refs",
    "release_decision",
    "next_step",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def maybe_load(path: Path) -> dict | None:
    if not path.exists():
        return None
    return load_json(path)


def object_contract_paths(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))


@functools.lru_cache(maxsize=None)
def schema_validator(schema_filename: str) -> Draft202012Validator:
    if Draft202012Validator is None:
        raise RuntimeError("jsonschema package is required to validate governance packs")
    schema = load_json(SCHEMA_ROOT / schema_filename)
    return Draft202012Validator(schema)


def format_schema_path(path: list[object]) -> str:
    if not path:
        return "$"
    buffer = "$"
    for item in path:
        if isinstance(item, int):
            buffer += f"[{item}]"
        else:
            buffer += f".{item}"
    return buffer


def validate_against_schema(
    instance: dict,
    schema_filename: str,
    label: str,
    errors: list[str],
) -> None:
    validator = schema_validator(schema_filename)
    for issue in sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path)):
        errors.append(
            f"{label}: schema violation at {format_schema_path(list(issue.absolute_path))}: {issue.message}"
        )


def ensure_pack_directory(directory: Path, pack_root: Path, label: str, errors: list[str]) -> bool:
    if not directory.exists():
        return False
    if directory.is_symlink():
        errors.append(f"{label}: symlink directories are not allowed")
        return False
    try:
        resolved = directory.resolve()
    except OSError as exc:
        errors.append(f"{label}: failed to resolve directory ({exc})")
        return False
    try:
        resolved.relative_to(pack_root)
    except ValueError:
        errors.append(f"{label}: resolved path `{resolved}` escapes pack_root `{pack_root}`")
        return False
    return True


def collect_object_contracts(root: Path, warnings: list[str], errors: list[str]) -> list[dict]:
    object_dir = root / "objects"
    legacy_dir = root / "schemas"
    if ensure_pack_directory(object_dir, root, "objects/", errors):
        contracts = []
        for path in object_contract_paths(object_dir):
            if path.is_symlink():
                errors.append(f"objects/: symlink files are not allowed (`{path.name}`)")
                continue
            data = load_json(path)
            validate_against_schema(data, "object.contract.schema.json", f"objects/{path.name}", errors)
            if data.get("family") == "object":
                contracts.append(data)
        legacy_contracts = []
        if ensure_pack_directory(legacy_dir, root, "schemas/", errors):
            for path in object_contract_paths(legacy_dir):
                if path.is_symlink():
                    errors.append(f"schemas/: symlink files are not allowed (`{path.name}`)")
                    continue
                data = load_json(path)
                validate_against_schema(data, "object.contract.schema.json", f"schemas/{path.name}", errors)
                if data.get("family") == "object":
                    legacy_contracts.append(path.name)
        if legacy_contracts:
            warnings.append(
                f"legacy object contracts under schemas/ were ignored; move them to objects/ ({', '.join(sorted(legacy_contracts))})"
            )
        return contracts

    if not legacy_dir.exists():
        return []
    if not ensure_pack_directory(legacy_dir, root, "schemas/", errors):
        return []

    contracts = []
    for path in object_contract_paths(legacy_dir):
        if path.is_symlink():
            errors.append(f"schemas/: symlink files are not allowed (`{path.name}`)")
            continue
        data = load_json(path)
        validate_against_schema(data, "object.contract.schema.json", f"schemas/{path.name}", errors)
        if data.get("family") == "object":
            contracts.append(data)
    if contracts:
        warnings.append("object contracts loaded from legacy schemas/ directory; prefer objects/")
    return contracts


def object_ids(contracts: list[dict]) -> set[str]:
    ids: set[str] = set()
    for contract in contracts:
        object_id = contract.get("object_id")
        if object_id:
            ids.add(object_id)
    return ids


def object_kinds(contracts: list[dict]) -> dict[str, str]:
    registry: dict[str, str] = {}
    for contract in contracts:
        object_id = contract.get("object_id")
        if object_id:
            registry[object_id] = contract.get("kind", "generic")
    return registry


def role_ids(agent_contract: dict | None) -> set[str]:
    ids: set[str] = set()
    if not agent_contract:
        return ids
    for role in agent_contract.get("roles", []):
        role_id = role.get("role_id")
        if role_id:
            ids.add(role_id)
    return ids


def role_approval_refs(agent_contract: dict | None) -> dict[str, set[str]]:
    approvals: dict[str, set[str]] = {}
    if not agent_contract:
        return approvals
    for role in agent_contract.get("roles", []):
        role_id = role.get("role_id")
        if role_id:
            approvals[role_id] = set(role.get("can_approve_refs", []))
    return approvals


def actor_ids(agent_contract: dict | None) -> set[str]:
    ids = role_ids(agent_contract)
    if agent_contract and agent_contract.get("agent_id"):
        ids.add(agent_contract["agent_id"])
    return ids


def contract_agent_ids(agent_contract: dict | None) -> set[str]:
    ids: set[str] = set()
    if agent_contract and agent_contract.get("agent_id"):
        ids.add(agent_contract["agent_id"])
    return ids


def missing_ref(target: str, registry: set[str], label: str, errors: list[str]) -> None:
    if target and target not in registry:
        errors.append(f"{label}: missing target `{target}`")


def expect_object_kind(
    target: str,
    object_kinds: dict[str, str],
    expected_kind: str,
    label: str,
    errors: list[str],
) -> None:
    if not target:
        return
    actual_kind = object_kinds.get(target)
    if actual_kind is None:
        errors.append(f"{label}: missing target `{target}`")
        return
    if actual_kind != expected_kind:
        errors.append(
            f"{label}: kind mismatch for `{target}` (expected `{expected_kind}`, got `{actual_kind}`)"
        )


def validate_workflow_contract(
    workflow: dict,
    policy_ids: set[str],
    object_refs: set[str],
    object_kind_registry: dict[str, str],
    contract_agent_ids: set[str],
    agent_roles: set[str],
    role_approval_registry: dict[str, set[str]],
    errors: list[str],
) -> tuple[set[str], set[str]]:
    node_ids: set[str] = set()
    transition_ids: set[str] = set()
    node_approvers: dict[str, str] = {}

    for ref in workflow.get("policy_refs", []):
        missing_ref(ref, policy_ids, "workflow.policy_refs", errors)
    for ref in workflow.get("object_refs", []):
        missing_ref(ref, object_refs, "workflow.object_refs", errors)

    if workflow.get("agent_refs") and not contract_agent_ids:
        errors.append("workflow.agent_refs present but no agent.contract.json agent_id was loaded")
    for ref in workflow.get("agent_refs", []):
        if not contract_agent_ids:
            break
        missing_ref(ref, contract_agent_ids, "workflow.agent_refs", errors)

    for node in workflow.get("nodes", []):
        node_id = node.get("node_id")
        if node_id:
            node_ids.add(node_id)
        for key in ("state_ref", "action_ref"):
            missing_ref(node.get(key, ""), object_refs, f"node.{key}", errors)
        for ref in node.get("evidence_refs", []):
            missing_ref(ref, object_refs, "node.evidence_refs", errors)
        for ref in node.get("output_policy_refs", []):
            missing_ref(ref, policy_ids, "node.output_policy_refs", errors)
        approver_ref = node.get("approver_ref")
        missing_ref(approver_ref, agent_roles, "node.approver_ref", errors)
        if node_id and approver_ref:
            node_approvers[node_id] = approver_ref

    for transition in workflow.get("transitions", []):
        transition_id = transition.get("transition_id")
        if transition_id:
            transition_ids.add(transition_id)
        for ref in transition.get("guard_policy_refs", []):
            missing_ref(ref, policy_ids, "transition.guard_policy_refs", errors)
        approval_ref = transition.get("approval_ref")
        expect_object_kind(
            approval_ref,
            object_kind_registry,
            "approval_type",
            "transition.approval_ref",
            errors,
        )
        from_node = transition.get("from_node")
        to_node = transition.get("to_node")
        if from_node and from_node not in node_ids:
            errors.append(f"transition.from_node: missing node `{from_node}`")
        if to_node and to_node not in node_ids:
            errors.append(f"transition.to_node: missing node `{to_node}`")
        if approval_ref:
            adjacent_approvers = {
                role
                for role in (
                    node_approvers.get(from_node, ""),
                    node_approvers.get(to_node, ""),
                )
                if role
            }
            if not adjacent_approvers:
                errors.append(
                    f"transition.approval_ref `{approval_ref}` has no adjacent node.approver_ref coverage"
                )
            elif not any(
                approval_ref in role_approval_registry.get(role_id, set())
                for role_id in adjacent_approvers
            ):
                errors.append(
                    f"transition.approval_ref `{approval_ref}` not covered by adjacent approver roles {sorted(adjacent_approvers)}"
                )

    colliding_ids = node_ids.intersection(transition_ids)
    if colliding_ids:
        errors.append(
            f"workflow contract: node_ids and transition_ids must not overlap ({sorted(colliding_ids)})"
        )

    return node_ids, transition_ids


def validate_policy_contract(policy: dict | None, errors: list[str]) -> None:
    if not policy:
        return

    validate_against_schema(policy, "policy.contract.schema.json", "rules.contract.json", errors)

    missing = REQUIRED_POLICY_KEYS.difference(policy.keys())
    for key in sorted(missing):
        errors.append(f"rules.contract.json: missing required key `{key}`")

    if policy.get("family") != "policy_or_rules":
        errors.append("rules.contract.json: family must be `policy_or_rules`")

    for index, rule in enumerate(policy.get("rules", []), start=1):
        missing_rule_keys = REQUIRED_POLICY_RULE_KEYS.difference(rule.keys())
        for key in sorted(missing_rule_keys):
            errors.append(f"rules.contract.json: rules[{index}] missing required key `{key}`")
        effect = rule.get("effect")
        if effect and effect not in POLICY_EFFECTS:
            errors.append(
                f"rules.contract.json: rules[{index}].effect `{effect}` must be one of {sorted(POLICY_EFFECTS)}"
            )


def validate_state(
    state: dict | None,
    workflow: dict,
    node_ids: set[str],
    errors: list[str],
) -> None:
    if not state:
        return
    validate_against_schema(state, "workflow.state.schema.json", "workflow.state.json", errors)
    missing = REQUIRED_STATE_KEYS.difference(state.keys())
    for key in sorted(missing):
        errors.append(f"workflow.state.json: missing required key `{key}`")
    if state.get("workflow_id") != workflow.get("workflow_id"):
        errors.append("workflow.state.json: workflow_id does not match workflow.contract.json")
    current_node_id = state.get("current_node_id")
    if current_node_id and current_node_id not in node_ids:
        errors.append(f"workflow.state.json: current_node_id `{current_node_id}` not found in workflow nodes")
    gate_state = state.get("gate_state")
    if gate_state and gate_state not in GATE_STATES:
        errors.append(
            f"workflow.state.json: gate_state `{gate_state}` must be one of {sorted(GATE_STATES)}"
        )


def validate_events(
    events_path: Path,
    workflow: dict,
    node_ids: set[str],
    transition_ids: set[str],
    valid_actor_ids: set[str],
    warnings: list[str],
    errors: list[str],
) -> set[str]:
    event_ids: set[str] = set()
    if not events_path.exists():
        return event_ids
    with events_path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                event = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"workflow.events.jsonl:{line_no}: invalid JSON ({exc})")
                continue
            validate_against_schema(
                event,
                "workflow.event.schema.json",
                f"workflow.events.jsonl:{line_no}",
                errors,
            )
            missing = REQUIRED_EVENT_KEYS.difference(event.keys())
            for key in sorted(missing):
                errors.append(f"workflow.events.jsonl:{line_no}: missing required key `{key}`")
            event_id = event.get("event_id")
            if event_id:
                if event_id in event_ids:
                    errors.append(f"workflow.events.jsonl:{line_no}: duplicate event_id `{event_id}`")
                event_ids.add(event_id)
            if event.get("workflow_id") != workflow.get("workflow_id"):
                errors.append(f"workflow.events.jsonl:{line_no}: workflow_id mismatch")
            actor_id = event.get("actor_id")
            if valid_actor_ids and actor_id and actor_id not in valid_actor_ids:
                errors.append(
                    f"workflow.events.jsonl:{line_no}: actor_id `{actor_id}` not found in agent.contract.json"
                )
            elif actor_id and not valid_actor_ids:
                warnings.append(
                    f"workflow.events.jsonl:{line_no}: actor_id `{actor_id}` cannot be checked because no agent.contract.json was loaded"
                )
            state_after = event.get("state_after", {})
            current_node_id = state_after.get("current_node_id")
            if current_node_id and current_node_id not in node_ids:
                errors.append(
                    f"workflow.events.jsonl:{line_no}: state_after.current_node_id `{current_node_id}` not found"
                )
            gate_state = state_after.get("gate_state")
            if gate_state and gate_state not in GATE_STATES:
                errors.append(
                    f"workflow.events.jsonl:{line_no}: state_after.gate_state `{gate_state}` must be one of {sorted(GATE_STATES)}"
                )
            subject_ref = event.get("subject_ref", "")
            if subject_ref and subject_ref not in node_ids and subject_ref not in transition_ids:
                errors.append(
                    f"workflow.events.jsonl:{line_no}: subject_ref `{subject_ref}` not found in node/transition ids"
                )
    return event_ids


def compare_ref_lists(label: str, actual: list[str], expected: list[str], errors: list[str]) -> None:
    if sorted(actual) != sorted(expected):
        errors.append(
            f"{label}: expected {sorted(expected)}, got {sorted(actual)}"
        )


def validate_status_projection(
    projection: dict | None,
    state: dict | None,
    workflow: dict,
    node_ids: set[str],
    errors: list[str],
) -> None:
    if not projection:
        return
    if not state:
        errors.append("status.projection.json requires workflow.state.json to exist")
        return

    validate_against_schema(
        projection,
        "status.projection.schema.json",
        "status.projection.json",
        errors,
    )

    missing = REQUIRED_STATUS_PROJECTION_KEYS.difference(projection.keys())
    for key in sorted(missing):
        errors.append(f"status.projection.json: missing required key `{key}`")

    forbidden = set(projection.keys()).intersection(FORBIDDEN_STATUS_PROJECTION_KEYS)
    for key in sorted(forbidden):
        errors.append(
            f"status.projection.json: forbidden authority key `{key}`; projections must stay derived and read-only"
        )

    extra_keys = set(projection.keys()).difference(REQUIRED_STATUS_PROJECTION_KEYS)
    for key in sorted(extra_keys):
        errors.append(
            f"status.projection.json: unexpected key `{key}`; keep the projection minimal and derived"
        )

    if projection.get("family") != "status_projection":
        errors.append("status.projection.json: family must be `status_projection`")
    if projection.get("workflow_id") != workflow.get("workflow_id"):
        errors.append("status.projection.json: workflow_id mismatch")
    if projection.get("workflow_id") != state.get("workflow_id"):
        errors.append("status.projection.json: workflow_id does not match workflow.state.json")
    if projection.get("run_id") != state.get("run_id"):
        errors.append("status.projection.json: run_id does not match workflow.state.json")
    if projection.get("contract_version") != state.get("contract_version"):
        errors.append("status.projection.json: contract_version does not match workflow.state.json")
    if projection.get("source_last_event_id") != state.get("last_event_id"):
        errors.append("status.projection.json: source_last_event_id does not match workflow.state.json")

    current_node_id = projection.get("current_node_id")
    if current_node_id and current_node_id not in node_ids:
        errors.append(f"status.projection.json: current_node_id `{current_node_id}` not found in workflow nodes")
    if current_node_id != state.get("current_node_id"):
        errors.append("status.projection.json: current_node_id does not match workflow.state.json")

    gate_state = projection.get("gate_state")
    if gate_state and gate_state not in GATE_STATES:
        errors.append(
            f"status.projection.json: gate_state `{gate_state}` must be one of {sorted(GATE_STATES)}"
        )
    if gate_state != state.get("gate_state"):
        errors.append("status.projection.json: gate_state does not match workflow.state.json")

    compare_ref_lists(
        "status.projection.json: missing_evidence_refs",
        projection.get("missing_evidence_refs", []),
        state.get("missing_evidence_refs", []),
        errors,
    )
    compare_ref_lists(
        "status.projection.json: forbidden_output_refs",
        projection.get("forbidden_output_refs", []),
        state.get("forbidden_output_refs", []),
        errors,
    )


def validate_markdown_tokens(root: Path, warnings: list[str]) -> None:
    workflow_md = root / "WORKFLOW.md"
    if not workflow_md.exists():
        return
    text = workflow_md.read_text(encoding="utf-8")
    for token in ("entry gate", "transition gate", "entry/transition/stop"):
        if token in text:
            warnings.append(
                f"WORKFLOW.md contains legacy gate token `{token}`; prefer route/evidence/write/stop canonical terms"
            )


def main() -> int:
    if Draft202012Validator is None:
        print(
            "error: jsonschema package is required; install it with `python3 -m pip install -r requirements-dev.txt`",
            file=sys.stderr,
        )
        return 2

    parser = argparse.ArgumentParser(
        description="Validate a files-driven governance asset pack for ref integrity and minimal instance consistency."
    )
    parser.add_argument("pack_root", type=Path, help="Root directory of one governance asset pack")
    args = parser.parse_args()

    pack_root = args.pack_root.resolve()
    workflow = maybe_load(pack_root / "workflow.contract.json")
    if not workflow:
        print("error: workflow.contract.json not found", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    policy = maybe_load(pack_root / "rules.contract.json")
    agent = maybe_load(pack_root / "agent.contract.json")
    state = maybe_load(pack_root / "workflow.state.json")
    status_projection = maybe_load(pack_root / "status.projection.json")
    object_contracts = collect_object_contracts(pack_root, warnings, errors)

    validate_against_schema(
        workflow,
        "workflow.contract.schema.json",
        "workflow.contract.json",
        errors,
    )
    if agent:
        validate_against_schema(agent, "agent.contract.schema.json", "agent.contract.json", errors)

    policy_ids = {policy["policy_id"]} if policy and policy.get("policy_id") else set()
    object_ref_ids = object_ids(object_contracts)
    object_kind_registry = object_kinds(object_contracts)
    agent_contract_ids = contract_agent_ids(agent)
    agent_role_ids = role_ids(agent)
    valid_actor_ids = actor_ids(agent)
    role_approval_registry = role_approval_refs(agent)

    validate_policy_contract(policy, errors)
    node_ids, transition_ids = validate_workflow_contract(
        workflow,
        policy_ids,
        object_ref_ids,
        object_kind_registry,
        agent_contract_ids,
        agent_role_ids,
        role_approval_registry,
        errors,
    )
    validate_state(state, workflow, node_ids, errors)
    event_ids = validate_events(
        pack_root / "workflow.events.jsonl",
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
    validate_status_projection(status_projection, state, workflow, node_ids, errors)
    validate_markdown_tokens(pack_root, warnings)

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
