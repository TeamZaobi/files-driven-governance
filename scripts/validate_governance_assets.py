#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


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

GATE_STATES = {
    "blocked",
    "partial",
    "ready",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def maybe_load(path: Path) -> dict | None:
    if not path.exists():
        return None
    return load_json(path)


def collect_object_contracts(root: Path) -> list[dict]:
    schema_dir = root / "schemas"
    if not schema_dir.exists():
        return []
    contracts = []
    for path in sorted(schema_dir.glob("*.json")):
        data = load_json(path)
        if data.get("family") == "object":
            contracts.append(data)
    return contracts


def collect_check_ids(workflow: dict) -> set[str]:
    check_ids: set[str] = set()
    for gate in ("route", "evidence", "write", "stop"):
        for item in workflow.get("checks", {}).get(gate, []):
            if isinstance(item, str):
                check_ids.add(item)
            elif isinstance(item, dict) and item.get("check_id"):
                check_ids.add(item["check_id"])
    return check_ids


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
    agent_roles: set[str],
    role_approval_registry: dict[str, set[str]],
    errors: list[str],
    warnings: list[str],
) -> tuple[set[str], set[str]]:
    node_ids: set[str] = set()
    transition_ids: set[str] = set()
    node_approvers: dict[str, str] = {}

    for ref in workflow.get("policy_refs", []):
        missing_ref(ref, policy_ids, "workflow.policy_refs", errors)
    for ref in workflow.get("object_refs", []):
        missing_ref(ref, object_refs, "workflow.object_refs", errors)

    if workflow.get("agent_refs") and not agent_roles:
        warnings.append("workflow.agent_refs present but no agent roles were loaded")
    for ref in workflow.get("agent_refs", []):
        if not agent_roles:
            break
        if ref not in agent_roles:
            warnings.append(
                f"workflow.agent_refs contains `{ref}`; current validator only knows role ids, so this may be a role/agent mismatch"
            )

    check_ids = collect_check_ids(workflow)

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
        for ref in node.get("check_refs", []):
            missing_ref(ref, check_ids, "node.check_refs", errors)
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
        for ref in transition.get("required_check_refs", []):
            missing_ref(ref, check_ids, "transition.required_check_refs", errors)
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

    return node_ids, transition_ids


def validate_state(
    state: dict | None,
    workflow: dict,
    node_ids: set[str],
    errors: list[str],
) -> None:
    if not state:
        return
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
    errors: list[str],
) -> None:
    if not events_path.exists():
        return
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
            missing = REQUIRED_EVENT_KEYS.difference(event.keys())
            for key in sorted(missing):
                errors.append(f"workflow.events.jsonl:{line_no}: missing required key `{key}`")
            if event.get("workflow_id") != workflow.get("workflow_id"):
                errors.append(f"workflow.events.jsonl:{line_no}: workflow_id mismatch")
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
                # P0 only validates node/transition refs. Evidence/policy refs stay to contract checks.
                errors.append(
                    f"workflow.events.jsonl:{line_no}: subject_ref `{subject_ref}` not found in node/transition ids"
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
    parser = argparse.ArgumentParser(
        description="Validate files-driven governance assets for ref integrity and minimal instance consistency."
    )
    parser.add_argument("root", type=Path, help="Root directory of a governance asset pack")
    args = parser.parse_args()

    root = args.root.resolve()
    workflow = maybe_load(root / "workflow.contract.json")
    if not workflow:
        print("error: workflow.contract.json not found", file=sys.stderr)
        return 1

    policy = maybe_load(root / "rules.contract.json")
    agent = maybe_load(root / "agent.contract.json")
    state = maybe_load(root / "workflow.state.json")
    object_contracts = collect_object_contracts(root)

    errors: list[str] = []
    warnings: list[str] = []

    policy_ids = {policy["policy_id"]} if policy and policy.get("policy_id") else set()
    object_ref_ids = object_ids(object_contracts)
    object_kind_registry = object_kinds(object_contracts)
    agent_role_ids = role_ids(agent)
    role_approval_registry = role_approval_refs(agent)

    node_ids, transition_ids = validate_workflow_contract(
        workflow,
        policy_ids,
        object_ref_ids,
        object_kind_registry,
        agent_role_ids,
        role_approval_registry,
        errors,
        warnings,
    )
    validate_state(state, workflow, node_ids, errors)
    validate_events(root / "workflow.events.jsonl", workflow, node_ids, transition_ids, errors)
    validate_markdown_tokens(root, warnings)

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
