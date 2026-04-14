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
WORKFLOW_ID = "workflow.repo.treatment.rollout"
POLICY_ID = "policy.repo.treatment.rollout"
AGENT_ID = "agent.repo.treatment.rollout"
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_FINAL_CHECKS = ("python3 -m unittest discover -s tests -p 'test_*.py'",)

CONTEXT_SOURCES = (
    ("README.md", "context/repo_readme.md"),
    ("SKILL.md", "context/skill.md"),
    ("agents/openai.yaml", "context/agent_surface.yaml"),
    ("docs/当前阶段补完计划.md", "context/current_tranche_plan.md"),
    ("docs/非工程背景起步.md", "context/non_engineering_onramp.md"),
    ("docs/使用手册.md", "context/manual.md"),
    ("scripts/manage_files_engine.py", "context/manage_files_engine.py"),
    ("scripts/validate_files_engine_scaffold.py", "context/validate_files_engine_scaffold.py"),
    ("scripts/validate_governance_assets.py", "context/validate_governance_assets.py"),
    ("tests/test_entrypoint_consistency.py", "context/test_entrypoint_consistency.py"),
    ("tests/test_files_engine_scaffold.py", "context/test_files_engine_scaffold.py"),
    ("tests/test_files_engine_actions.py", "context/test_files_engine_actions.py"),
    ("tests/test_validate_governance_assets.py", "context/test_validate_governance_assets.py"),
    ("tests/test_capture_promotion_assets.py", "context/test_capture_promotion_assets.py"),
    ("tests/test_agent_facing_e2e.py", "context/test_agent_facing_e2e.py"),
)


@dataclass(frozen=True)
class StepSpec:
    key: str
    title: str
    actor_id: str
    approver_role: str
    report_path: str
    event_type: str
    goal: str
    required_sections: tuple[str, ...]
    workspace_targets: tuple[str, ...]

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
        key="align_identity_surface",
        title="Align Identity Surface",
        actor_id="role.governance_owner",
        approver_role="role.governance_owner",
        report_path="reports/align_identity_surface.md",
        event_type="align",
        goal=(
            "Align the repo's host-facing identity with the current canonical `files-driven` naming, "
            "without overstating current audit capability."
        ),
        required_sections=(
            "## Objective",
            "## Owned Paths",
            "## Planned Changes",
            "## Verification",
        ),
        workspace_targets=("agents/openai.yaml",),
    ),
    StepSpec(
        key="rewrite_entrypoint_language",
        title="Rewrite Entrypoint Language",
        actor_id="role.docs_owner",
        approver_role="role.docs_owner",
        report_path="reports/rewrite_entrypoint_language.md",
        event_type="rewrite",
        goal=(
            "Rewrite the user-facing onramp with the agreed medical translation layer "
            "(`体检 -> 诊断 -> 治疗 -> 复查 -> 随访`) while keeping canonical governance terms intact underneath."
        ),
        required_sections=(
            "## Objective",
            "## Owned Paths",
            "## Planned Changes",
            "## Verification",
        ),
        workspace_targets=(
            "README.md",
            "docs/非工程背景起步.md",
            "docs/使用手册.md",
        ),
    ),
    StepSpec(
        key="split_audit_capabilities",
        title="Split Audit Capabilities",
        actor_id="role.implementation_owner",
        approver_role="role.implementation_owner",
        report_path="reports/split_audit_capabilities.md",
        event_type="audit",
        goal=(
            "Make the audit surface honest: keep current scaffold audit working, but encode the next-step split "
            "toward scaffold / pack / runtime tiers instead of implying a complete downstream system check."
        ),
        required_sections=(
            "## Objective",
            "## Owned Paths",
            "## Planned Changes",
            "## Verification",
        ),
        workspace_targets=(
            "scripts/manage_files_engine.py",
            "tests/test_files_engine_actions.py",
            "tests/test_files_engine_scaffold.py",
        ),
    ),
    StepSpec(
        key="harden_memory_audit",
        title="Harden Memory Audit",
        actor_id="role.runtime_owner",
        approver_role="role.runtime_owner",
        report_path="reports/harden_memory_audit.md",
        event_type="harden",
        goal=(
            "Strengthen the runtime-memory audit seam so validator coverage can catch broken reason/artifact references "
            "and missing controlled-upgrade evidence."
        ),
        required_sections=(
            "## Objective",
            "## Owned Paths",
            "## Planned Changes",
            "## Verification",
        ),
        workspace_targets=(
            "scripts/validate_governance_assets.py",
            "tests/test_validate_governance_assets.py",
            "tests/test_capture_promotion_assets.py",
        ),
    ),
    StepSpec(
        key="add_adoption_regressions",
        title="Add Adoption Regressions",
        actor_id="role.test_owner",
        approver_role="role.test_owner",
        report_path="reports/add_adoption_regressions.md",
        event_type="test",
        goal=(
            "Freeze the adoption-facing identity and onboarding path in regression tests so future iterations do not "
            "reintroduce drift between host surface, README, and low-bandwidth entrypoint language."
        ),
        required_sections=(
            "## Objective",
            "## Owned Paths",
            "## Planned Changes",
            "## Verification",
        ),
        workspace_targets=(
            "tests/test_entrypoint_consistency.py",
            "tests/test_agent_facing_e2e.py",
        ),
    ),
    StepSpec(
        key="verify_and_close",
        title="Verify And Close",
        actor_id="role.capability_owner",
        approver_role="role.capability_owner",
        report_path="reports/verify_and_close.md",
        event_type="close",
        goal=(
            "Write the closeout note for this rollout, summarize what changed, record residual risks, "
            "and hand control back to the runner for final verification."
        ),
        required_sections=(
            "## Objective",
            "## Changed Areas",
            "## Final Checks",
            "## Residual Risks",
            "## Next Actions",
        ),
        workspace_targets=(),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the agreed files-driven rollout as a script-controlled Codex CLI workflow that edits the target workspace "
            "and writes governed runtime artifacts."
        )
    )
    parser.add_argument("output_root", help="Directory where the rollout run pack should be written.")
    parser.add_argument(
        "--workspace-root",
        default=str(ROOT),
        help="Workspace root to edit. Defaults to the current repository root.",
    )
    parser.add_argument(
        "--codex-bin",
        default="codex",
        help="Codex CLI binary to call. Defaults to `codex`.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model passed to `codex exec`. Defaults to `{DEFAULT_MODEL}`.",
    )
    parser.add_argument("--profile", help="Optional Codex profile passed to `codex exec`.")
    parser.add_argument(
        "--reasoning-effort",
        default="high",
        choices=("minimal", "low", "medium", "high"),
        help="Codex reasoning effort override. Defaults to `high`.",
    )
    parser.add_argument(
        "--allow-dirty-workspace",
        action="store_true",
        help="Allow running against a git workspace that already has local modifications.",
    )
    parser.add_argument(
        "--no-default-final-checks",
        action="store_true",
        help="Disable the built-in final verification command list.",
    )
    parser.add_argument(
        "--final-check",
        action="append",
        default=[],
        help="Additional shell command to run at the end of the rollout from the workspace root.",
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


def ensure_workspace_ready(workspace_root: Path, allow_dirty: bool) -> None:
    git_dir = workspace_root / ".git"
    if not git_dir.exists():
        return
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=workspace_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return
    if result.stdout.strip() and not allow_dirty:
        raise RuntimeError(
            "workspace has local modifications; rerun with `--allow-dirty-workspace` if this is intentional"
        )


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
    return copied


def approval_ref(index: int) -> str:
    return f"approval.transition.{index + 1}"


def transition_id(current_index: int) -> str:
    current = STEP_SPECS[current_index].key.replace("_", "-")
    nxt = STEP_SPECS[current_index + 1].key.replace("_", "-")
    return f"transition.{current}-to-{nxt}"


def build_objects() -> list[dict]:
    payloads: list[dict] = []
    for index, step in enumerate(STEP_SPECS):
        payloads.append(
            {
                "schema_version": "1.0",
                "object_id": step.state_ref,
                "family": "object",
                "version_anchor": "v1",
                "kind": "state_profile",
                "fields": [
                    {"field_id": "goal", "type": "string", "required": True},
                    {"field_id": "workspace_targets", "type": "array<string>", "required": True},
                    {"field_id": "completion_signal", "type": "string", "required": True},
                ],
            }
        )
        payloads.append(
            {
                "schema_version": "1.0",
                "object_id": step.action_ref,
                "family": "object",
                "version_anchor": "v1",
                "kind": "action_class",
                "fields": [
                    {"field_id": "report_path", "type": "string", "required": True},
                    {"field_id": "workspace_targets", "type": "array<string>", "required": True},
                    {"field_id": "task_packet_path", "type": "string", "required": True},
                ],
            }
        )
        payloads.append(
            {
                "schema_version": "1.0",
                "object_id": step.evidence_ref,
                "family": "object",
                "version_anchor": "v1",
                "kind": "evidence_type",
                "fields": [
                    {"field_id": "report_path", "type": "string", "required": True},
                    {"field_id": "summary", "type": "string", "required": True},
                    {"field_id": "workspace_targets", "type": "array<string>", "required": False},
                ],
            }
        )
        if index < len(STEP_SPECS) - 1:
            payloads.append(
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
    return payloads


def write_static_pack_assets(pack_root: Path, final_checks: tuple[str, ...]) -> None:
    object_dir = pack_root / "objects"
    object_dir.mkdir(parents=True, exist_ok=True)
    (pack_root / "task_packets").mkdir(parents=True, exist_ok=True)
    (pack_root / "codex_runs").mkdir(parents=True, exist_ok=True)
    (pack_root / "reports").mkdir(parents=True, exist_ok=True)

    boundary = pack_root / "BOUNDARY.md"
    final_check_lines = [f"- `{command}`" for command in final_checks] if final_checks else ["- none"]
    boundary.write_text(
        "\n".join(
            [
                "# 方向与边界锚点",
                "",
                "这个文件是 repo treatment rollout run pack 的边界入口。",
                "先读它，再读 `WORKFLOW.md`、`workflow.contract.json` 和阶段报告。",
                "",
                "## 首批真实使用场景 [scenarios]",
                "",
                "- 维护者已经收敛出一轮推进方案，希望用受控脚本调度 Codex CLI 一次性落地。",
                "- 需要先止住命名漂移和能力承诺漂移，再把审计能力和入口语言收回到真实可执行边界。",
                "- 需要把运行时记忆轴和采用体验测试纳入正式回归，而不是继续只靠说明文或人工提醒。",
                "",
                "## 首批交付物 [deliverable]",
                "",
                "- 一个可直接运行的 rollout runner，能调度 Codex CLI 对目标 workspace 执行分阶段修改，并在 run pack 中留下任务包、事件流、状态页、阶段报告和最终校验结果。",
                "",
                "## 用户故事 [user_stories]",
                "",
                "### 用户故事 US-1",
                "",
                "- 谁在用：维护 `files-driven` 的 capability owner。",
                "- 在什么场景下：已经完成一轮系统诊断，需要把推进方案编码成一次受控执行。",
                "- 他/她现在想完成什么：把 agreed rollout 变成一条可复跑、可审计、可回放的 Codex CLI 执行链。",
                "- 为什么这件事对当前阶段重要：如果推进方案仍停在对话里，后续实现会重新散回局部修补。",
                "- 这次完成后，用户应该看到什么变化：存在一条受控脚本路径，可以一次性推动命名收口、入口重写、audit 收口和记忆轴硬化。",
                "- 这次明确不包含什么：不要求这一轮自动完成全部未来 tranche。",
                "",
                "### 用户故事 US-2",
                "",
                "- 谁在用：负责采用体验和宿主入口的人。",
                "- 在什么场景下：需要把用户侧语言压回可理解的“体检 -> 诊断 -> 治疗 -> 复查 -> 随访”，同时避免污染底层合同键名。",
                "- 他/她现在想完成什么：让用户入口和宿主显示面不再夸大当前 audit 能力，也不再继续漂移。",
                "- 为什么这件事对当前阶段重要：如果入口语言和真实实现继续错位，采用成本会持续上升。",
                "- 这次完成后，用户应该看到什么变化：入口语言更清楚，能力承诺与实现边界更一致。",
                "- 这次明确不包含什么：不要求把 schema、contract 和 validator 全部改写成医学语言。",
                "",
                "### 用户故事 US-3",
                "",
                "- 谁在用：负责 runtime / validator / regression 的维护者。",
                "- 在什么场景下：需要把记忆轴和采用体验纳入受控回归，而不是继续作为条件说明留在文档层。",
                "- 他/她现在想完成什么：把 `reason_refs / artifact_refs`、候选链边界和 adoption-facing regression 纳入正式修改路径。",
                "- 为什么这件事对当前阶段重要：如果这部分继续留在软约定层，系统体检能力仍会落空。",
                "- 这次完成后，用户应该看到什么变化：validator / tests 能明确捕捉这类退化。",
                "- 这次明确不包含什么：不要求一轮做成平台级全量体检器。",
                "",
                "## 测试用例 [test_cases]",
                "",
                "### 测试用例 TC-1",
                "",
                "- 对应故事：US-1",
                "- 前提：使用者只拿到这个 run pack 和目标 workspace。",
                "- 当：按 `BOUNDARY.md -> WORKFLOW.md -> task_packets/ -> reports/` 阅读。",
                "- 那么：应能看清 rollout 的节点顺序、写权边界和最终校验方式。",
                "- 通过条件：runner、worker、runtime files 和 workspace 改动边界清楚。",
                "- 这次明确不要求：不要求 run pack 解释全部底层方法学。",
                "- 失败/越界边界：如果阶段报告可以替代 workflow 控制文件，说明控制面重新滑回说明文。",
                "",
                "### 测试用例 TC-2",
                "",
                "- 对应故事：US-2",
                "- 前提：目标 workspace 至少包含宿主入口、README 和起步文档。",
                "- 当：runner 顺序执行命名收口与入口语言改写节点。",
                "- 那么：应能保持 `files-driven` 主名，并把医学语言限制在用户入口层。",
                "- 通过条件：入口语言变清晰，但 schema / contract 语义不被误改。",
                "- 这次明确不要求：不要求这一轮完成所有后续用户教育资产。",
                "- 失败/越界边界：如果医学语言直接侵入 contract 或 validator canonical 键名，说明翻译层越界。",
                "",
                "### 测试用例 TC-3",
                "",
                "- 对应故事：US-3",
                "- 前提：runner 已完成全部节点并进入 final checks。",
                "- 当：检查 `workflow.state.json`、`workflow.events.jsonl`、`status.projection.json`、`reports/` 和 final check 报告。",
                "- 那么：应能确认 worker 只写节点报告与目标 workspace，runner 才推进 runtime control，并执行最终验证。",
                "- 通过条件：失败时会停在 blocked，成功时 ready 且留有 final check 结果。",
                "- 这次明确不要求：不要求 final checks 默认覆盖所有外部工具集成。",
                "- 失败/越界边界：如果 final check 失败后状态仍然 ready，说明闭环不可信。",
                "",
                "## 非目标 [non_goals]",
                "",
                "- 不把医学语言写进 schema、workflow 合同或 validator 的 canonical 键名。",
                "- 不让 Codex worker 直接写 runtime control files。",
                "- 不把当前 runner 冒充为已经完成的平台级全量体检器。",
                "",
                "## 质量参考对象 [quality_references]",
                "",
                "- `context/repo_readme.md`",
                "- `context/current_tranche_plan.md`",
                "- `context/validate_governance_assets.py`",
                "",
                "## 验收责任人 [acceptance_owner]",
                "",
                "- `files-driven` capability maintainer",
                "",
                "## Final Checks",
                "",
                *final_check_lines,
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
                "This pack encodes the agreed rollout as a script-controlled Codex CLI run.",
                "",
                "Control truth:",
                "- `workflow.contract.json` is the control truth",
                "- `workflow.state.json` and `workflow.events.jsonl` are execution instances",
                "- `status.projection.json` is derived only",
                "",
                "Current route:",
                "`align_identity_surface -> rewrite_entrypoint_language -> split_audit_capabilities -> harden_memory_audit -> add_adoption_regressions -> verify_and_close`",
                "",
                "Control rules:",
                "- the runner writes runtime control files and final verification reports",
                "- the Codex worker edits only the current node's owned workspace paths and report",
                "- final checks happen after the closeout node and can still block the rollout",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    readme = pack_root / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# repo-treatment-rollout",
                "",
                "Generated by `scripts/run_repo_treatment_rollout.py`.",
                "",
                "Main reports:",
                *[f"- `{step.report_path}`" for step in STEP_SPECS],
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    object_contracts = build_objects()
    for payload in object_contracts:
        write_json(object_dir / f"{payload['object_id']}.json", payload)

    policy = {
        "schema_version": "1.0",
        "policy_id": POLICY_ID,
        "family": "policy_or_rules",
        "version_anchor": "v1",
        "scope": "workflow",
        "rules": [
            {
                "rule_id": "rule.runner.controls.runtime",
                "effect": "require_evidence",
                "target_refs": [step.evidence_ref for step in STEP_SPECS],
                "required_refs": [step.evidence_ref for step in STEP_SPECS],
            },
            {
                "rule_id": "rule.worker.writes.only.node.scope",
                "effect": "deny",
                "target_refs": [
                    "workflow.contract.json",
                    "workflow.state.json",
                    "workflow.events.jsonl",
                    "status.projection.json",
                    "rules.contract.json",
                    "agent.contract.json",
                ],
            },
        ],
    }
    write_json(pack_root / "rules.contract.json", policy)

    transition_approvals = [approval_ref(index) for index in range(len(STEP_SPECS) - 1)]
    roles = [
        "role.governance_owner",
        "role.docs_owner",
        "role.implementation_owner",
        "role.runtime_owner",
        "role.test_owner",
        "role.capability_owner",
    ]
    executions = {
        role: [step.action_ref for step in STEP_SPECS if step.actor_id == role]
        for role in roles
    }
    reviews = {
        role: [step.action_ref for step in STEP_SPECS if step.approver_role == role]
        for role in roles
    }
    agent = {
        "schema_version": "1.0",
        "agent_id": AGENT_ID,
        "family": "agent",
        "version_anchor": "v1",
        "roles": [
            {
                "role_id": role,
                "can_execute_refs": executions[role],
                "can_review_refs": reviews[role],
                "can_approve_refs": transition_approvals,
                "blocked_action_refs": [],
            }
            for role in roles
        ],
    }
    write_json(pack_root / "agent.contract.json", agent)

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
                "intent_id": "intent.repo.treatment.rollout",
                "entry_node": STEP_SPECS[0].node_id,
                "aliases": [
                    "run files-driven treatment rollout",
                    "implement agreed rollout with codex",
                    "apply the agreed treatment plan",
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
            "route": ["check.route.repo.treatment.rollout"],
            "evidence": ["check.evidence.repo.treatment.rollout"],
            "write": ["check.write.repo.treatment.rollout"],
            "stop": ["check.stop.repo.treatment.rollout"],
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
        "projection_id": "projection.repo.treatment.rollout.status",
        "family": "status_projection",
        "workflow_id": state["workflow_id"],
        "run_id": state["run_id"],
        "contract_version": state["contract_version"],
        "source_last_event_id": state["last_event_id"],
        "current_node_id": state["current_node_id"],
        "gate_state": state["gate_state"],
        "summary": (
            f"Current node `{state['current_node_id']}` with gate_state `{state['gate_state']}`. "
            "This projection is runner-derived only and does not authorize workspace edits by itself."
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
    workspace_root: Path,
    step: StepSpec,
    previous_reports: list[str],
    final_checks: tuple[str, ...],
) -> tuple[Path, dict]:
    packet = {
        "workflow_id": WORKFLOW_ID,
        "node_id": step.node_id,
        "title": step.title,
        "goal": step.goal,
        "workspace_root": str(workspace_root),
        "report_path": str((pack_root / step.report_path).resolve()),
        "required_sections": list(step.required_sections),
        "workspace_targets": list(step.workspace_targets),
        "context_paths": [
            "context/repo_readme.md",
            "context/skill.md",
            "context/agent_surface.yaml",
            "context/current_tranche_plan.md",
            "context/non_engineering_onramp.md",
            "context/manual.md",
            "context/manage_files_engine.py",
            "context/validate_files_engine_scaffold.py",
            "context/validate_governance_assets.py",
            "context/test_entrypoint_consistency.py",
            "context/test_files_engine_scaffold.py",
            "context/test_files_engine_actions.py",
            "context/test_validate_governance_assets.py",
            "context/test_capture_promotion_assets.py",
            "context/test_agent_facing_e2e.py",
        ],
        "previous_reports": previous_reports,
        "final_checks": list(final_checks),
        "control_constraints": [
            "The runner owns workflow.state.json, workflow.events.jsonl, and status.projection.json.",
            "Do not modify workflow contracts, runtime files, task packets, object contracts, rules.contract.json, or agent.contract.json.",
            "Only edit the current node's owned workspace paths.",
            "Always write the node report.",
        ],
    }
    path = pack_root / "task_packets" / f"{step.key}.json"
    write_json(path, packet)
    return path, packet


def build_prompt(task_packet_path: Path, packet: dict) -> str:
    owned_paths = packet["workspace_targets"] or ["(no workspace edits for this node)"]
    lines = [
        f"You are the Codex CLI worker for node `{packet['node_id']}` in a script-controlled rollout.",
        "",
        f"TASK_PACKET_PATH: {task_packet_path}",
        f"WORKSPACE_ROOT: {packet['workspace_root']}",
        f"REPORT_PATH: {packet['report_path']}",
        "",
        "Read the task packet first, then the listed context files.",
        "Work in the workspace root, but only modify the owned workspace paths for this node.",
        "Do not edit workflow control files, contracts, objects, or other task packets.",
        "Always write the node report to REPORT_PATH.",
        "",
        "Owned workspace paths:",
        *[f"- {item}" for item in owned_paths],
        "",
        "The agreed rollout priorities are:",
        "- stop naming drift on the host-facing identity surface",
        "- rewrite the onboarding layer with `体检 -> 诊断 -> 治疗 -> 复查 -> 随访` as user translation only",
        "- keep `audit` honest about current capability",
        "- harden runtime memory checks",
        "- freeze adoption-facing behavior in regression tests",
        "",
        "Deliverable requirements:",
        *[f"- include section `{section}`" for section in packet["required_sections"]],
        "- describe concrete file edits or explain why no workspace edit was needed for this node",
        "- preserve existing repo direction instead of reopening the worldview",
        "",
        "Write the report and perform the workspace edits now.",
    ]
    return "\n".join(lines) + "\n"


def codex_command(args: argparse.Namespace, workspace_root: Path, last_message_path: Path) -> list[str]:
    command = [
        args.codex_bin,
        "exec",
        "--model",
        args.model,
        "--full-auto",
        "-c",
        f"model_reasoning_effort={json.dumps(args.reasoning_effort)}",
        "--skip-git-repo-check",
        "--color",
        "never",
        "--json",
        "-C",
        str(workspace_root),
        "--output-last-message",
        str(last_message_path),
        "-",
    ]
    if args.profile:
        command[2:2] = ["--profile", args.profile]
    return command


def validate_report(path: Path, required_sections: tuple[str, ...]) -> None:
    if not path.exists():
        raise RuntimeError(f"Codex worker did not create report: `{path}`")
    text = path.read_text(encoding="utf-8")
    for section in required_sections:
        if section not in text:
            raise RuntimeError(f"report `{path.name}` missing required section `{section}`")


def run_worker(
    args: argparse.Namespace,
    pack_root: Path,
    workspace_root: Path,
    step: StepSpec,
    task_packet_path: Path,
    packet: dict,
) -> Path:
    run_dir = pack_root / "codex_runs" / step.key
    run_dir.mkdir(parents=True, exist_ok=True)
    last_message_path = run_dir / "last_message.md"
    prompt_path = run_dir / "prompt.md"
    prompt = build_prompt(task_packet_path, packet)
    prompt_path.write_text(prompt, encoding="utf-8")

    command = codex_command(args, workspace_root, last_message_path)
    result = subprocess.run(
        command,
        input=prompt,
        cwd=workspace_root,
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

    report_path = pack_root / step.report_path
    validate_report(report_path, step.required_sections)
    return report_path


def run_pack_validator(pack_root: Path) -> None:
    if not VALIDATOR.exists():
        return
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(pack_root)],
        cwd=ROOT,
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
        raise RuntimeError(f"generated run pack failed governance validator:\n{result.stderr}")


def run_final_checks(pack_root: Path, workspace_root: Path, commands: tuple[str, ...]) -> None:
    report_dir = pack_root / "final_checks"
    report_dir.mkdir(parents=True, exist_ok=True)
    aggregate: list[dict] = []
    for index, command in enumerate(commands, start=1):
        result = subprocess.run(
            command,
            cwd=workspace_root,
            shell=True,
            text=True,
            capture_output=True,
            check=False,
        )
        payload = {
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        aggregate.append(payload)
        write_json(report_dir / f"check_{index:02d}.json", payload)
        if result.returncode != 0:
            raise RuntimeError(f"final check failed: `{command}`")
    write_json(report_dir / "summary.json", {"checks": aggregate})


def write_summary(pack_root: Path, workspace_root: Path, args: argparse.Namespace, final_checks: tuple[str, ...]) -> None:
    summary = pack_root / "summary.md"
    final_check_lines = [f"- `{command}`" for command in final_checks] if final_checks else ["- none"]
    lines = [
        "# Summary",
        "",
        f"- `workflow_id`: `{WORKFLOW_ID}`",
        f"- `workspace_root`: `{workspace_root}`",
        f"- `model`: `{args.model}`",
        f"- `reasoning_effort`: `{args.reasoning_effort}`",
        "",
        "Reports:",
        *[f"- `{step.report_path}`" for step in STEP_SPECS],
        "",
        "Final checks:",
        *final_check_lines,
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def final_checks_tuple(args: argparse.Namespace) -> tuple[str, ...]:
    commands = [] if args.no_default_final_checks else list(DEFAULT_FINAL_CHECKS)
    commands.extend(args.final_check)
    return tuple(commands)


def next_event_id(index: int) -> str:
    return f"event.rollout.{index:03d}"


def main() -> int:
    args = parse_args()
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    output_root = Path(args.output_root).expanduser().resolve()
    final_checks = final_checks_tuple(args)

    if not workspace_root.exists():
        print(f"error: workspace root does not exist: `{workspace_root}`", file=sys.stderr)
        return 1

    try:
        ensure_workspace_ready(workspace_root, args.allow_dirty_workspace)
        ensure_output_root(output_root, args.force)
        copy_context(workspace_root, output_root)
        write_static_pack_assets(output_root, final_checks)

        run_id = f"run.repo.treatment.rollout.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state = initialize_state(output_root, run_id)
        initial_event = build_event(
            event_id=next_event_id(1),
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

        previous_reports: list[str] = []
        for index, step in enumerate(STEP_SPECS):
            task_packet_path, packet = build_task_packet(
                output_root,
                workspace_root,
                step,
                previous_reports,
                final_checks,
            )
            try:
                report_path = run_worker(args, output_root, workspace_root, step, task_packet_path, packet)
                if index == len(STEP_SPECS) - 1 and final_checks:
                    run_final_checks(output_root, workspace_root, final_checks)
            except Exception as exc:
                blocked_event = build_event(
                    event_id=next_event_id(index + 2),
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

            previous_reports.append(step.report_path)
            remaining = [item for item in state["missing_evidence_refs"] if item != step.evidence_ref]
            if index < len(STEP_SPECS) - 1:
                event = build_event(
                    event_id=next_event_id(index + 2),
                    run_id=run_id,
                    actor_id=step.actor_id,
                    event_type=step.event_type,
                    subject_ref=transition_id(index),
                    reason_refs=[str(task_packet_path.relative_to(output_root))],
                    artifact_refs=[str(report_path.relative_to(output_root))],
                    current_node_id=STEP_SPECS[index + 1].node_id,
                    gate_state="partial",
                    missing_evidence_refs=remaining,
                )
            else:
                event = build_event(
                    event_id=next_event_id(index + 2),
                    run_id=run_id,
                    actor_id=step.actor_id,
                    event_type="land",
                    subject_ref=step.node_id,
                    reason_refs=[str(task_packet_path.relative_to(output_root))],
                    artifact_refs=[str(report_path.relative_to(output_root))],
                    current_node_id=step.node_id,
                    gate_state="ready",
                    missing_evidence_refs=[],
                )
            append_event(output_root, event, state)

        write_summary(output_root, workspace_root, args, final_checks)
        run_pack_validator(output_root)
        print(f"repo treatment rollout completed: {output_root}")
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
