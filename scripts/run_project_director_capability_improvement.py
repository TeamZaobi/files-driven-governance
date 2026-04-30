#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"
WORKFLOW_ID = "workflow.project.director.capability.improvement"
POLICY_ID = "policy.capability.improvement.control"
AGENT_ID = "agent.capability.governor"


@dataclass(frozen=True)
class StepSpec:
    key: str
    title: str
    actor_id: str
    approver_role: str
    deliverable: str
    event_type: str
    goal: str
    required_sections: tuple[str, ...]

    @property
    def node_id(self) -> str:
        return f"node.{self.key}"

    @property
    def state_ref(self) -> str:
        return f"state.{self.key}"

    @property
    def action_ref(self) -> str:
        return f"action.{self.key}"

    @property
    def evidence_ref(self) -> str:
        return f"evidence.{self.key}"


STEP_SPECS = (
    StepSpec(
        key="observe_gaps",
        title="Observe Gaps",
        actor_id="role.governance_owner",
        approver_role="role.governance_owner",
        deliverable="observe_gaps.md",
        event_type="observe",
        goal=(
            "Collect the concrete failure modes behind low complex-workflow adherence in Mobius, "
            "using the current repository as the canonical source and the benchmark anchors as external evidence."
        ),
        required_sections=(
            "## Objective",
            "## Evidence Inventory",
            "## Failure Modes",
            "## Baseline Claims",
        ),
    ),
    StepSpec(
        key="map_capability_graph",
        title="Map Capability Graph",
        actor_id="role.governance_owner",
        approver_role="role.governance_owner",
        deliverable="map_capability_graph.md",
        event_type="map",
        goal=(
            "Map the current project-director capability graph, separating what the model already does well "
            "from what still lives as implicit runtime control."
        ),
        required_sections=(
            "## Objective",
            "## Current Graph",
            "## Strengths",
            "## Capability Gaps",
            "## Boundary Corrections",
        ),
    ),
    StepSpec(
        key="design_control_upgrade",
        title="Design Control Upgrade",
        actor_id="role.governance_owner",
        approver_role="role.governance_owner",
        deliverable="design_control_upgrade.md",
        event_type="design",
        goal=(
            "Reallocate control responsibilities away from the model and into the runner, Codex CLI worker surface, "
            "and explicit approval points."
        ),
        required_sections=(
            "## Objective",
            "## Control Reallocation",
            "## Runtime Governor Duties",
            "## LLM Boundary",
            "## Risks If Not Adopted",
        ),
    ),
    StepSpec(
        key="define_runtime_protocol",
        title="Define Runtime Protocol",
        actor_id="role.governance_owner",
        approver_role="role.governance_owner",
        deliverable="define_runtime_protocol.md",
        event_type="protocol",
        goal=(
            "Define the minimal runtime protocol for the improved control method: run creation, task packet shape, "
            "CLI invocation surface, gate checks, and recovery points."
        ),
        required_sections=(
            "## Objective",
            "## Node Contract",
            "## Task Packet",
            "## CLI Surface",
            "## Gate Checks",
            "## Recovery Model",
        ),
    ),
    StepSpec(
        key="pilot_on_benchmarks",
        title="Pilot On Benchmarks",
        actor_id="role.test_owner",
        approver_role="role.test_owner",
        deliverable="pilot_on_benchmarks.md",
        event_type="pilot",
        goal=(
            "Use the improved capability graph and runtime protocol to design benchmark-based validation, "
            "anchored on the strong positive sample and additional failure patterns."
        ),
        required_sections=(
            "## Objective",
            "## Benchmark Matrix",
            "## Pilot Result",
            "## Residual Risks",
            "## Follow-up Checks",
        ),
    ),
    StepSpec(
        key="promote_or_rollback",
        title="Promote Or Rollback",
        actor_id="role.capability_owner",
        approver_role="role.capability_owner",
        deliverable="promote_or_rollback.md",
        event_type="promote",
        goal=(
            "Decide whether the improved project-director capability graph is ready for promotion, "
            "needs another controlled pilot, or should be rolled back."
        ),
        required_sections=(
            "## Objective",
            "## Promotion Decision",
            "## Reasons",
            "## Rollback Conditions",
            "## Next Actions",
        ),
    ),
)

CONTEXT_SOURCES = (
    ("docs/项目治理能力模型.md", "context/project_governance_model.md"),
    ("README.md", "context/repo_readme.md"),
    ("SKILL.md", "context/skill.md"),
    ("references/工具适配对照表.md", "context/tool_adapter_matrix.md"),
    ("references/经典治理流程库.md", "context/runtime_promotion.md"),
    ("examples/discussion-decision-task/WORKFLOW.md", "context/capture_candidate_workflow.md"),
)

BENCHMARK_NOTES = (
    "The benchmark conversation `019d859b-41f3-7752-bc49-ca9282c784ca` is the strongest positive sample.",
    "Its value is not just better content quality. It proved that script-controlled execution produced the best workflow adherence.",
    "The new control method must therefore move control responsibility from model-internal reasoning to the external runner.",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the experimental L4 project-director capability-improvement workflow as a script-controlled recovery pack, "
            "calling Codex CLI as the node worker and writing governed runtime artifacts only after lighter governance has failed."
        )
    )
    parser.add_argument(
        "output_root",
        help="Directory where the generated governed run pack should be written.",
    )
    parser.add_argument(
        "--workspace-root",
        default=str(ROOT),
        help="Workspace root whose canonical docs should be snapshotted into the run pack.",
    )
    parser.add_argument(
        "--benchmark",
        action="append",
        default=[],
        help="Benchmark anchor or conversation id. Repeat for multiple anchors.",
    )
    parser.add_argument(
        "--codex-bin",
        default="codex",
        help="Codex CLI binary to call. Defaults to `codex`.",
    )
    parser.add_argument("--model", help="Optional model override passed to `codex exec`.")
    parser.add_argument("--profile", help="Optional Codex profile passed to `codex exec`.")
    parser.add_argument(
        "--reasoning-effort",
        default="high",
        choices=("minimal", "low", "medium", "high"),
        help="Safe Codex reasoning effort override. Defaults to `high` to avoid incompatible local defaults.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing output directory by clearing it first.",
    )
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def ensure_output_root(output_root: Path, force: bool) -> None:
    if output_root.exists():
        if force:
            shutil.rmtree(output_root)
        elif any(output_root.iterdir()):
            raise RuntimeError(f"output directory must be empty or pass --force: `{output_root}`")
    output_root.mkdir(parents=True, exist_ok=True)


def copy_context(workspace_root: Path, pack_root: Path) -> list[str]:
    copied: list[str] = []
    for source_rel, dest_rel in CONTEXT_SOURCES:
        source = workspace_root / source_rel
        if not source.exists():
            raise RuntimeError(f"context source missing: `{source}`")
        destination = pack_root / dest_rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        copied.append(dest_rel)

    benchmarks = pack_root / "context" / "benchmarks.md"
    benchmark_lines = ["# Benchmarks", ""]
    for line in BENCHMARK_NOTES:
        benchmark_lines.append(f"- {line}")
    benchmarks.write_text("\n".join(benchmark_lines) + "\n", encoding="utf-8")
    copied.append("context/benchmarks.md")
    return copied


def approval_ref(index: int) -> str:
    return f"approval.transition.{index + 1}"


def transition_id(current_index: int) -> str:
    current = STEP_SPECS[current_index].key.replace("_", "-")
    nxt = STEP_SPECS[current_index + 1].key.replace("_", "-")
    return f"transition.{current}-to-{nxt}"


def build_objects() -> list[dict]:
    objects: list[dict] = []
    for index, step in enumerate(STEP_SPECS):
        objects.append(
            {
                "schema_version": "1.0",
                "object_id": step.state_ref,
                "family": "object",
                "version_anchor": "v1",
                "kind": "state_profile",
                "fields": [
                    {"field_id": "objective", "type": "string", "required": True},
                    {"field_id": "completion_signal", "type": "string", "required": True},
                ],
            }
        )
        objects.append(
            {
                "schema_version": "1.0",
                "object_id": step.action_ref,
                "family": "object",
                "version_anchor": "v1",
                "kind": "action_class",
                "fields": [
                    {"field_id": "deliverable_path", "type": "string", "required": True},
                    {"field_id": "required_sections", "type": "array", "required": True},
                    {"field_id": "task_packet_path", "type": "string", "required": True},
                ],
            }
        )
        objects.append(
            {
                "schema_version": "1.0",
                "object_id": step.evidence_ref,
                "family": "object",
                "version_anchor": "v1",
                "kind": "evidence_type",
                "fields": [
                    {"field_id": "artifact_path", "type": "string", "required": True},
                    {"field_id": "summary", "type": "string", "required": True},
                    {"field_id": "benchmark_anchor", "type": "string", "required": False},
                ],
            }
        )
        if index < len(STEP_SPECS) - 1:
            objects.append(
                {
                    "schema_version": "1.0",
                    "object_id": approval_ref(index),
                    "family": "object",
                    "version_anchor": "v1",
                    "kind": "approval_type",
                    "fields": [
                        {"field_id": "approval_id", "type": "string", "required": True},
                        {"field_id": "transition_ref", "type": "string", "required": True},
                        {"field_id": "approver_role_ref", "type": "string", "required": True},
                    ],
                }
            )
    return objects


def write_static_pack_assets(pack_root: Path, benchmark_ids: list[str]) -> None:
    object_dir = pack_root / "objects"
    object_dir.mkdir(parents=True, exist_ok=True)
    task_packet_dir = pack_root / "task_packets"
    task_packet_dir.mkdir(parents=True, exist_ok=True)
    codex_run_dir = pack_root / "codex_runs"
    codex_run_dir.mkdir(parents=True, exist_ok=True)

    boundary = pack_root / "BOUNDARY.md"
    benchmark_lines = [f"- `{value}`" for value in benchmark_ids] or ["- none provided"]
    boundary.write_text(
        "\n".join(
            [
                "# 方向与边界锚点",
                "",
                "这个文件是 project-director capability improvement run pack 的边界入口。",
                "先读它，再读 `WORKFLOW.md`、`workflow.contract.json` 和阶段产物。",
                "",
                "## 首批真实使用场景 [scenarios]",
                "",
                "- 维护者需要把“项目总监能力图谱改善”从自由讨论改成受控 run，而不是继续依赖长对话里的隐式记忆。",
                "- 需要一条脚本控制、`codex cli` 节点执行的官方路径，验证控制权重分配是否真的能提升复杂流程遵循度。",
                "- 负责基线与回归的人，需要一个能直接复跑、回放和校验的 capability-scope 自改造包。",
                "",
                "## 首批交付物 [deliverable]",
                "",
                "- 一个可直接运行、可直接校验的 self-hosting governed pack，包含边界页、workflow 合同、运行实例、对象合同、阶段产物和 Codex 调用留痕。",
                "",
                "## 用户故事 [user_stories]",
                "",
                "### 用户故事 US-1",
                "",
                "- 谁在用：维护 `files-driven` 能力模型的人。",
                "- 在什么场景下：需要把前面的讨论收口成一条真正受控的能力改善链。",
                "- 他/她现在想完成什么：先看清能力缺口，再由脚本控制整个改善过程，并让 Codex CLI 只做节点内操作。",
                "- 为什么这件事对当前阶段重要：如果控制权还留在模型内部，复杂流程遵循度仍然会持续偏低。",
                "- 这次完成后，用户应该看到什么变化：改善链能够一次跑完，并留下可审计的 runtime artifacts。",
                "- 这次明确不包含什么：不要求这一轮就把所有下游项目一起升级。",
                "",
                "### 用户故事 US-2",
                "",
                "- 谁在用：负责 benchmark 与回归的人。",
                "- 在什么场景下：需要验证脚本控制方法是否真的比 prompt-only 工作流更稳。",
                "- 他/她现在想完成什么：把 benchmark anchor 放进同一个受控 run 里，形成可复盘的 pilot 结论。",
                "- 为什么这件事对当前阶段重要：没有 benchmark，改善结论很容易退回感受层。",
                "- 这次完成后，用户应该看到什么变化：pilot 结果能清楚指出哪些能力已改善、哪些还需回退或补试。",
                "- 这次明确不包含什么：不要求这里直接修改对话平台或外部业务系统。",
                "",
                "### 用户故事 US-3",
                "",
                "- 谁在用：负责 capability promotion/rollback 的维护者。",
                "- 在什么场景下：需要决定这轮改善能否进入能力真源，还是应继续试验。",
                "- 他/她现在想完成什么：在受控终点明确 promotion decision、rollback 条件和下一步动作。",
                "- 为什么这件事对当前阶段重要：如果终点没有裁定面，改善会重新滑回开放式讨论。",
                "- 这次完成后，用户应该看到什么变化：终点页能清楚说明 promote / continue pilot / rollback 的结论。",
                "- 这次明确不包含什么：不要求这一轮直接发明新的世界观层或新的结构家族。",
                "",
                "## 测试用例 [test_cases]",
                "",
                "### 测试用例 TC-1",
                "",
                "- 对应故事：US-1",
                "- 前提：使用者只拿到这个 run pack。",
                "- 当：先读 `BOUNDARY.md`，再读 `WORKFLOW.md`、`workflow.contract.json` 和阶段产物。",
                "- 那么：应能按固定顺序看清整条能力改善链。",
                "- 通过条件：入口、合同、实例和阶段产物角色清楚，不互相冒充。",
                "- 这次明确不要求：不要求这里覆盖所有下游项目场景。",
                "- 失败/越界边界：如果阶段产物能反过来替代 `workflow.contract.json` 或 runtime 文件，说明控制权还没有真正外移。",
                "",
                "### 测试用例 TC-2",
                "",
                "- 对应故事：US-2",
                "- 前提：benchmark anchor 已作为证据输入 run pack。",
                "- 当：检查 `observe_gaps.md`、`pilot_on_benchmarks.md` 和 `promote_or_rollback.md`。",
                "- 那么：应能看到 benchmark 被当成证据，而不是被当成控制真源。",
                "- 通过条件：benchmark 只进入分析、pilot 和裁定，不直接改写 workflow 合同。",
                "- 这次明确不要求：不要求 benchmark 本身在包内完整复现原始会话内容。",
                "- 失败/越界边界：如果 benchmark anchor 被直接当成运行时放行依据，而不是分析证据，说明方法仍在滑形。",
                "",
                "### 测试用例 TC-3",
                "",
                "- 对应故事：US-1",
                "- 前提：脚本已经调用完 Codex CLI。",
                "- 当：检查 `workflow.state.json`、`workflow.events.jsonl`、`status.projection.json` 和 `codex_runs/`。",
                "- 那么：应能确认 runtime 由 runner 维护，Codex CLI 只留下节点内产物和执行留痕。",
                "- 通过条件：控制文件由脚本写，节点产物由 worker 写，分工稳定。",
                "- 这次明确不要求：不要求节点 worker 具备审批权或状态推进权。",
                "- 失败/越界边界：如果节点 worker 可以直接改 runtime control files，说明控制面还没有从模型手里拿出来。",
                "",
                "## 非目标 [non_goals]",
                "",
                "- 不让 Codex CLI 直接拥有 workflow state 的写权。",
                "- 不在这一轮引入新的顶层结构家族。",
                "- 不把 benchmark anchor 直接当成 control truth。",
                "",
                "## 质量参考对象 [quality_references]",
                "",
                "- [project_governance_model](context/project_governance_model.md)",
                "- [tool_adapter_matrix](context/tool_adapter_matrix.md)",
                "- [runtime_promotion](context/runtime_promotion.md)",
                "",
                "## 验收责任人 [acceptance_owner]",
                "",
                "- `files-driven` capability maintainer",
                "",
                "## Benchmark Anchors",
                "",
                *benchmark_lines,
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    workflow_md = pack_root / "WORKFLOW.md"
    workflow_md.write_text(
        "\n".join(
            [
                "# Workflow",
                "",
                "This pack uses a script-controlled, Codex-assisted workflow.",
                "",
                "Control truth:",
                "- `workflow.contract.json` is the control truth",
                "- `workflow.state.json` and `workflow.events.jsonl` are execution instances",
                "- `status.projection.json` is derived only",
                "",
                "Current route:",
                "`observe_gaps -> map_capability_graph -> design_control_upgrade -> define_runtime_protocol -> pilot_on_benchmarks -> promote_or_rollback`",
                "",
                "Control rules:",
                "- the runner writes runtime control files",
                "- Codex CLI only writes the current node deliverable",
                "- benchmark anchors are evidence, not control authority",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    readme = pack_root / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# project-director-capability-improvement",
                "",
                "Generated by `scripts/run_project_director_capability_improvement.py`.",
                "",
                "Main path:",
                *[f"{index + 1}. `{step.deliverable}`" for index, step in enumerate(STEP_SPECS)],
                "",
                "Use this pack to inspect how control was externalized from the model into a runner and Codex CLI task packets.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    object_contracts = build_objects()

    policy = {
        "schema_version": "1.0",
        "policy_id": POLICY_ID,
        "family": "policy_or_rules",
        "version_anchor": "v1",
        "risk_level": "high",
        "scope": "workflow",
        "applies_to_refs": [WORKFLOW_ID],
        "rules": [
            {
                "rule_id": "rule.runner.controls.runtime",
                "effect": "require_evidence",
                "target_refs": [step.evidence_ref for step in STEP_SPECS],
                "required_refs": [step.evidence_ref for step in STEP_SPECS],
            }
        ],
    }
    write_json(pack_root / "rules.contract.json", policy)

    agent = {
        "schema_version": "1.0",
        "agent_id": AGENT_ID,
        "family": "agent",
        "version_anchor": "v1",
        "roles": [
            {
                "role_id": "role.governance_owner",
                "can_execute_refs": [
                    step.action_ref
                    for step in STEP_SPECS
                    if step.actor_id == "role.governance_owner"
                ],
                "can_review_refs": [
                    step.action_ref
                    for step in STEP_SPECS
                    if step.approver_role == "role.governance_owner"
                ],
                "can_approve_refs": [approval_ref(index) for index in range(4)],
                "blocked_action_refs": [],
            },
            {
                "role_id": "role.test_owner",
                "can_execute_refs": [STEP_SPECS[4].action_ref],
                "can_review_refs": [STEP_SPECS[4].action_ref],
                "can_approve_refs": [approval_ref(4)],
                "blocked_action_refs": [],
            },
            {
                "role_id": "role.capability_owner",
                "can_execute_refs": [STEP_SPECS[5].action_ref],
                "can_review_refs": [STEP_SPECS[5].action_ref],
                "can_approve_refs": [],
                "blocked_action_refs": [],
            },
        ],
    }
    write_json(pack_root / "agent.contract.json", agent)

    for payload in object_contracts:
        write_json(object_dir / f"{payload['object_id']}.json", payload)

    workflow = {
        "schema_version": "1.0",
        "workflow_id": WORKFLOW_ID,
        "family": "workflow",
        "governance_level": "controlled",
        "execution_mode": "gated",
        "version_anchor": "v1",
        "explanation_ref": "WORKFLOW.md",
        "policy_refs": [POLICY_ID],
        "object_refs": [payload["object_id"] for payload in object_contracts],
        "agent_refs": [AGENT_ID],
        "entry_intents": [
            {
                "intent_id": "intent.project.director.capability.improvement",
                "entry_node": STEP_SPECS[0].node_id,
                "aliases": [
                    "improve project director capability graph",
                    "externalize workflow control",
                    "run capability improvement workflow",
                ],
            }
        ],
        "nodes": [
            {
                "node_id": step.node_id,
                "state_ref": step.state_ref,
                "action_ref": step.action_ref,
                "evidence_refs": [step.evidence_ref],
                "output_policy_refs": [POLICY_ID],
                "approver_ref": step.approver_role,
            }
            for step in STEP_SPECS
        ],
        "transitions": [
            {
                "transition_id": transition_id(index),
                "from_node": STEP_SPECS[index].node_id,
                "to_node": STEP_SPECS[index + 1].node_id,
                "guard_policy_refs": [POLICY_ID],
                "approval_ref": approval_ref(index),
                "rollback_to": STEP_SPECS[max(0, index - 1)].node_id,
            }
            for index in range(len(STEP_SPECS) - 1)
        ],
        "checks": {
            "route": ["check.route.capability.improvement"],
            "evidence": ["check.evidence.capability.improvement"],
            "write": ["check.write.capability.improvement"],
            "stop": ["check.stop.capability.improvement"],
        },
    }
    write_json(pack_root / "workflow.contract.json", workflow)


def initialize_state(pack_root: Path, run_id: str) -> dict:
    state = {
        "schema_version": "1.0",
        "run_id": run_id,
        "workflow_id": WORKFLOW_ID,
        "contract_version": "v1",
        "current_node_id": STEP_SPECS[0].node_id,
        "gate_state": "blocked",
        "required_evidence_refs": [step.evidence_ref for step in STEP_SPECS],
        "missing_evidence_refs": [step.evidence_ref for step in STEP_SPECS],
        "forbidden_output_refs": [],
        "updated_at": now_iso(),
        "last_event_id": "",
    }
    write_json(pack_root / "workflow.state.json", state)
    return state


def write_projection(pack_root: Path, state: dict) -> None:
    projection = {
        "schema_version": "1.0",
        "projection_id": "projection.project.director.capability.improvement.status",
        "family": "status_projection",
        "workflow_id": state["workflow_id"],
        "run_id": state["run_id"],
        "contract_version": state["contract_version"],
        "source_last_event_id": state["last_event_id"],
        "current_node_id": state["current_node_id"],
        "gate_state": state["gate_state"],
        "summary": (
            f"Current node `{state['current_node_id']}` with gate_state `{state['gate_state']}`. "
            "This projection is derived from runner-written state and does not authorize any promotion by itself."
        ),
        "missing_evidence_refs": state["missing_evidence_refs"],
        "forbidden_output_refs": state["forbidden_output_refs"],
        "generated_at": now_iso(),
    }
    write_json(pack_root / "status.projection.json", projection)


def append_event(pack_root: Path, event: dict, state: dict) -> None:
    append_jsonl(pack_root / "workflow.events.jsonl", event)
    state["last_event_id"] = event["event_id"]
    state["updated_at"] = event["timestamp"]
    state["current_node_id"] = event["state_after"]["current_node_id"]
    state["gate_state"] = event["state_after"]["gate_state"]
    state["missing_evidence_refs"] = event["state_after"].get("missing_evidence_refs", [])
    write_json(pack_root / "workflow.state.json", state)
    write_projection(pack_root, state)


def build_event(
    event_id: str,
    run_id: str,
    actor_id: str,
    event_type: str,
    subject_ref: str,
    reason_refs: list[str],
    artifact_refs: list[str],
    current_node_id: str,
    gate_state: str,
    missing_evidence_refs: list[str],
) -> dict:
    payload = {
        "schema_version": "1.0",
        "event_id": event_id,
        "run_id": run_id,
        "workflow_id": WORKFLOW_ID,
        "contract_version": "v1",
        "timestamp": now_iso(),
        "actor_id": actor_id,
        "event_type": event_type,
        "subject_ref": subject_ref,
        "state_after": {
            "current_node_id": current_node_id,
            "gate_state": gate_state,
            "missing_evidence_refs": missing_evidence_refs,
        },
    }
    if reason_refs:
        payload["reason_refs"] = reason_refs
    if artifact_refs:
        payload["artifact_refs"] = artifact_refs
    return payload


def build_task_packet(
    pack_root: Path,
    step: StepSpec,
    previous_artifacts: list[str],
    benchmark_ids: list[str],
) -> tuple[Path, dict]:
    packet = {
        "workflow_id": WORKFLOW_ID,
        "node_id": step.node_id,
        "title": step.title,
        "goal": step.goal,
        "deliverable_path": step.deliverable,
        "required_sections": list(step.required_sections),
        "context_paths": [
            "context/project_governance_model.md",
            "context/repo_readme.md",
            "context/skill.md",
            "context/tool_adapter_matrix.md",
            "context/runtime_promotion.md",
            "context/capture_candidate_workflow.md",
            "context/benchmarks.md",
        ],
        "previous_artifacts": previous_artifacts,
        "benchmark_anchors": benchmark_ids,
        "control_constraints": [
            "The runner owns workflow.state.json, workflow.events.jsonl, and status.projection.json.",
            "Do not modify control contracts, agent contracts, policy contracts, or object contracts.",
            "Only write the requested deliverable.",
        ],
    }
    path = pack_root / "task_packets" / f"{step.key}.json"
    write_json(path, packet)
    return path, packet


def build_prompt(task_packet_path: Path, packet: dict) -> str:
    lines = [
        f"You are the Codex CLI worker for node `{packet['node_id']}` in a script-controlled workflow.",
        "",
        f"TASK_PACKET_PATH: {task_packet_path}",
        f"DELIVERABLE_PATH: {packet['deliverable_path']}",
        "",
        "Use only the files inside the current run pack.",
        "Read the task packet and the listed context files first.",
        "Do not modify workflow.contract.json, workflow.state.json, workflow.events.jsonl, status.projection.json, rules.contract.json, agent.contract.json, or any files under objects/.",
        "Only write the requested deliverable file.",
        "",
        "The user-established conclusions for this run are:",
        "- complex workflows in Mobius still show low adherence when control stays inside the model",
        "- script-controlled execution produced the best recent result",
        "- the improvement target is the project-director capability graph in self-hosting capability_scope",
        "",
        "Deliverable requirements:",
        *[f"- include section `{section}`" for section in packet["required_sections"]],
        "- ground every claim in the run pack context or label it as an assumption",
        "- keep the document concise and operational",
        "",
        "Write the deliverable now.",
    ]
    return "\n".join(lines) + "\n"


def codex_command(args: argparse.Namespace, pack_root: Path, last_message_path: Path) -> list[str]:
    command = [
        args.codex_bin,
        "exec",
        "--full-auto",
        "-c",
        f"model_reasoning_effort={json.dumps(args.reasoning_effort)}",
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
        "-C",
        str(pack_root),
        "--output-last-message",
        str(last_message_path),
        "-",
    ]
    if args.model:
        command[2:2] = ["--model", args.model]
    if args.profile:
        command[2:2] = ["--profile", args.profile]
    return command


def validate_deliverable(path: Path, required_sections: tuple[str, ...]) -> None:
    if not path.exists():
        raise RuntimeError(f"Codex worker did not create deliverable: `{path}`")
    text = path.read_text(encoding="utf-8")
    for section in required_sections:
        if section not in text:
            raise RuntimeError(f"deliverable `{path.name}` missing required section `{section}`")


def run_worker(
    args: argparse.Namespace,
    pack_root: Path,
    step: StepSpec,
    task_packet_path: Path,
    packet: dict,
) -> tuple[Path, subprocess.CompletedProcess[str]]:
    run_dir = pack_root / "codex_runs" / step.key
    run_dir.mkdir(parents=True, exist_ok=True)
    last_message_path = run_dir / "last_message.md"
    prompt_path = run_dir / "prompt.md"
    prompt = build_prompt(task_packet_path, packet)
    prompt_path.write_text(prompt, encoding="utf-8")

    command = codex_command(args, pack_root, last_message_path)
    result = subprocess.run(
        command,
        input=prompt,
        cwd=pack_root,
        text=True,
        capture_output=True,
        check=False,
    )
    (run_dir / "stdout.jsonl").write_text(result.stdout, encoding="utf-8")
    (run_dir / "stderr.log").write_text(result.stderr, encoding="utf-8")
    (run_dir / "command.json").write_text(
        json.dumps(command, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Codex CLI failed for `{step.key}` with exit code {result.returncode}. See `{run_dir}`."
        )

    deliverable_path = pack_root / step.deliverable
    validate_deliverable(deliverable_path, step.required_sections)
    return deliverable_path, result


def run_validator(workspace_root: Path, pack_root: Path) -> None:
    if not VALIDATOR.exists():
        return
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(pack_root)],
        cwd=workspace_root,
        capture_output=True,
        text=True,
        check=False,
    )
    report = {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    write_json(pack_root / "validation.report.json", report)
    if result.returncode != 0:
        raise RuntimeError(f"generated pack failed governance validator:\n{result.stderr}")


def write_summary(pack_root: Path, run_id: str, benchmark_ids: list[str]) -> None:
    summary = pack_root / "summary.md"
    lines = [
        "# Summary",
        "",
        f"- `run_id`: `{run_id}`",
        f"- `workflow_id`: `{WORKFLOW_ID}`",
        f"- `pack_root`: `{pack_root}`",
        f"- `benchmarks`: {', '.join(f'`{item}`' for item in benchmark_ids) if benchmark_ids else '`none`'}",
        "",
        "Generated deliverables:",
        *[f"- `{step.deliverable}`" for step in STEP_SPECS],
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    output_root = Path(args.output_root).expanduser().resolve()
    benchmark_ids = args.benchmark or ["019d859b-41f3-7752-bc49-ca9282c784ca"]

    if not workspace_root.exists():
        print(f"error: workspace root does not exist: `{workspace_root}`", file=sys.stderr)
        return 1

    try:
        ensure_output_root(output_root, args.force)
        copy_context(workspace_root, output_root)
        write_static_pack_assets(output_root, benchmark_ids)

        run_id = f"run.project.director.capability.improvement.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state = initialize_state(output_root, run_id)
        initial_event = build_event(
            event_id="event.capability.001",
            run_id=run_id,
            actor_id=STEP_SPECS[0].actor_id,
            event_type="enter",
            subject_ref=STEP_SPECS[0].node_id,
            reason_refs=["BOUNDARY.md", "WORKFLOW.md"],
            artifact_refs=[],
            current_node_id=STEP_SPECS[0].node_id,
            gate_state="blocked",
            missing_evidence_refs=[step.evidence_ref for step in STEP_SPECS],
        )
        append_event(output_root, initial_event, state)

        previous_artifacts: list[str] = []
        for index, step in enumerate(STEP_SPECS):
            task_packet_path, packet = build_task_packet(output_root, step, previous_artifacts, benchmark_ids)
            try:
                deliverable_path, _ = run_worker(args, output_root, step, task_packet_path, packet)
            except Exception as exc:
                blocked_event = build_event(
                    event_id=f"event.capability.{index + 2:03d}",
                    run_id=run_id,
                    actor_id=step.actor_id,
                    event_type="blocked",
                    subject_ref=step.node_id,
                    reason_refs=[str(task_packet_path.relative_to(output_root))],
                    artifact_refs=[],
                    current_node_id=step.node_id,
                    gate_state="blocked",
                    missing_evidence_refs=state["missing_evidence_refs"],
                )
                append_event(output_root, blocked_event, state)
                raise RuntimeError(str(exc)) from exc

            previous_artifacts.append(step.deliverable)
            remaining = [item for item in state["missing_evidence_refs"] if item != step.evidence_ref]
            if index < len(STEP_SPECS) - 1:
                event = build_event(
                    event_id=f"event.capability.{index + 2:03d}",
                    run_id=run_id,
                    actor_id=step.actor_id,
                    event_type=step.event_type,
                    subject_ref=transition_id(index),
                    reason_refs=[str(task_packet_path.relative_to(output_root))],
                    artifact_refs=[str(deliverable_path.relative_to(output_root))],
                    current_node_id=STEP_SPECS[index + 1].node_id,
                    gate_state="partial",
                    missing_evidence_refs=remaining,
                )
            else:
                event = build_event(
                    event_id=f"event.capability.{index + 2:03d}",
                    run_id=run_id,
                    actor_id=step.actor_id,
                    event_type="land",
                    subject_ref=step.node_id,
                    reason_refs=[str(task_packet_path.relative_to(output_root))],
                    artifact_refs=[str(deliverable_path.relative_to(output_root))],
                    current_node_id=step.node_id,
                    gate_state="ready",
                    missing_evidence_refs=[],
                )
            append_event(output_root, event, state)

        write_summary(output_root, run_id, benchmark_ids)
        run_validator(workspace_root, output_root)
        print(f"capability improvement run completed: {output_root}")
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
