import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "docs" / "项目治理能力模型.md"
README = ROOT / "README.md"
QUICKSTART = ROOT / "QUICKSTART.md"
SKILL = ROOT / "SKILL.md"
MANUAL = ROOT / "docs" / "使用手册.md"
BEGINNER_GUIDE = ROOT / "docs" / "非工程背景起步.md"
FULL_GUIDE = ROOT / "docs" / "完整说明书.md"
LANGUAGE = ROOT / "docs" / "语言体系规范.md"
INFO_ARCH_REVIEW = ROOT / "docs" / "三层信息架构复盘.md"
STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"
MIGRATION = ROOT / "MIGRATION.md"
SCHEMA_README = ROOT / "schemas" / "README.md"
STARTER_DOC = ROOT / "docs" / "files引擎脚手架工程.md"
STARTER_ROOT = ROOT / "starters" / "minimal-files-engine"
STATE_SCHEMA = ROOT / "schemas" / "workflow.state.schema.json"
SHARED_REF = ROOT / "references" / "跨层共享约定.md"
CROSS_PROJECT_REF = ROOT / "references" / "跨项目共享模式提炼.md"
OUTPUT_CONVENTION = ROOT / "references" / "输出约定.md"
LOW_BANDWIDTH_REF = ROOT / "references" / "理解型输入与低带宽压缩包.md"
SCENE_MANUAL_REF = ROOT / "references" / "场景手册.md"
HOMOGENEOUS_TEAM_REF = ROOT / "references" / "AI-Native同构团队协作.md"
STRUCTURE_FAMILY_REF = ROOT / "references" / "结构家族定位约定.md"
READING_ORDER_REF = ROOT / "references" / "官方读取顺序.md"
TOOL_ADAPTER_REF = ROOT / "references" / "工具适配对照表.md"
HOSTED_KNOWLEDGE_MATRIX = ROOT / "docs" / "宿主化知识工作场景矩阵.md"
AUDIT_MATRIX = ROOT / "docs" / "体检分层矩阵.md"
COVERAGE_DIFF = ROOT / "docs" / "能力覆盖矩阵与历史差分.md"
E2E_MATRIX = ROOT / "docs" / "AI-Native与Skill驱动E2E验收矩阵.md"
EXTERNAL_WORKFLOW_RETROFIT = ROOT / "docs" / "外部项目Workflow改造脚手架.md"
CHECKPOINT_DOC = ROOT / "docs" / "阶段状态检查点_2026-04-14.md"
HOSTED_FIXTURE_ROOT = ROOT / "examples" / "hosted-knowledge-governance"
DISCUSSION_ROOT = ROOT / "examples" / "discussion-decision-task"
PROCESS_ROOT = ROOT / "examples" / "multi-tool-process-projection"
SMOKE_ROOT = ROOT / "examples" / "smoke-governed-review"
ADVERSARIAL_ROOT = ROOT / "examples" / "adversarial-convergence"


class EndToEndGovernanceAlignmentTests(unittest.TestCase):
    def test_entry_docs_route_back_to_canonical_source(self) -> None:
        required = {
            README: "docs/项目治理能力模型.md",
            MANUAL: "项目治理能力模型.md",
            FULL_GUIDE: "项目治理能力模型.md",
            STORIES: "docs/项目治理能力模型.md",
            MIGRATION: "docs/项目治理能力模型.md",
            SCHEMA_README: "docs/项目治理能力模型.md",
            STARTER_DOC: "项目治理能力模型.md",
        }

        for path, anchor in required.items():
            text = path.read_text(encoding="utf-8")
            self.assertIn(anchor, text, f"{path.name} must point back to canonical source")

        model = MODEL.read_text(encoding="utf-8")
        self.assertIn("唯一的底层真源", model)
        self.assertIn("后续多角度、多轮审计", model)
        self.assertIn("meta-skill capability", model)
        self.assertIn("downstream project instance", model)

    def test_scope_first_path_replaces_family_first_boot(self) -> None:
        manual = MANUAL.read_text(encoding="utf-8")
        full_guide = FULL_GUIDE.read_text(encoding="utf-8")
        shared = SHARED_REF.read_text(encoding="utf-8")
        cross_project = CROSS_PROJECT_REF.read_text(encoding="utf-8")
        structure_family = STRUCTURE_FAMILY_REF.read_text(encoding="utf-8")
        reading_order = READING_ORDER_REF.read_text(encoding="utf-8")
        language = LANGUAGE.read_text(encoding="utf-8")

        self.assertIn("先判动作、scope 和一级关口", manual)
        self.assertIn("默认判断顺序不是先分四层，也不是先分结构家族", full_guide)
        self.assertIn("先判当前动作、`scope` 和一级关口", shared)
        self.assertIn("先看当前动作、`scope` 和一级关口", cross_project)
        self.assertIn("先把主诉答清，再决定是否需要下钻结构家族标签", structure_family)
        self.assertIn("先把当前可信真源、最小下一步和暂时不要动的地方说清", reading_order)
        self.assertIn("先确认这次到底要做什么、站在哪个 `scope`、先过哪个一级关口", language)

        self.assertNotIn("### 4.1 先分四层", manual)
        self.assertNotIn("### 2. 先分结构家族，再谈文档层", cross_project)
        self.assertNotIn("先按结构家族判归属，再谈共享矩阵", shared)

    def test_beginner_entrypoints_offer_low_bandwidth_path(self) -> None:
        readme = README.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        beginner = BEGINNER_GUIDE.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        output = OUTPUT_CONVENTION.read_text(encoding="utf-8")
        low_bandwidth = LOW_BANDWIDTH_REF.read_text(encoding="utf-8")
        scene_manual = SCENE_MANUAL_REF.read_text(encoding="utf-8")
        homogeneous_team = HOMOGENEOUS_TEAM_REF.read_text(encoding="utf-8")
        structure_family = STRUCTURE_FAMILY_REF.read_text(encoding="utf-8")
        reading_order = READING_ORDER_REF.read_text(encoding="utf-8")
        tool_adapter = TOOL_ADAPTER_REF.read_text(encoding="utf-8")
        full_guide = FULL_GUIDE.read_text(encoding="utf-8")
        stories = STORIES.read_text(encoding="utf-8")

        self.assertIn("非工程背景起步.md", readme)
        self.assertIn("非工程背景起步", manual)
        self.assertIn("哪份文件算数", beginner)
        self.assertIn("今天先做什么", beginner)
        self.assertIn("哪些文件先别改", beginner)
        self.assertIn("如果用户明确说“看不懂”或明显不是工程背景", skill)
        self.assertIn("这次要做什么 / 先别做什么 / 卡住时找哪里", output)
        self.assertIn("先把回答翻回“哪份文件算数、今天先做什么、哪些先别改”", output)
        self.assertIn("给非工程背景读者的最小压缩形状", low_bandwidth)
        self.assertIn("如果你第一次读这份说明书，先只抓四件事", full_guide)
        self.assertIn("这份说明书不替代动作路径", full_guide)
        self.assertIn("这一节只保留够用的动作顺序，不重新展开完整模型总论", manual)
        self.assertIn("现有项目 / 新项目 / 止血收口", scene_manual)
        self.assertIn("先不要从这里起讲；先把主诉答清", homogeneous_team)
        self.assertIn("哪份文件算数、今天先做什么、哪些先别改", structure_family)
        self.assertIn("哪份文件算数、今天先做什么、哪些先别改", reading_order)
        self.assertIn("先不要从品牌差异或适配表开始讲", tool_adapter)
        self.assertIn("哪份文件算数", SHARED_REF.read_text(encoding="utf-8"))
        self.assertIn("docs/非工程背景起步.md", stories)

    def test_hosted_knowledge_work_matrix_is_wired_into_docs(self) -> None:
        readme = README.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        info_arch = INFO_ARCH_REVIEW.read_text(encoding="utf-8")
        tool_adapter = TOOL_ADAPTER_REF.read_text(encoding="utf-8")
        matrix = HOSTED_KNOWLEDGE_MATRIX.read_text(encoding="utf-8")
        output = OUTPUT_CONVENTION.read_text(encoding="utf-8")

        self.assertIn("docs/宿主化知识工作场景矩阵.md", readme)
        self.assertIn("宿主化知识工作场景矩阵", info_arch)
        self.assertIn("宿主化知识工作场景矩阵", tool_adapter)
        self.assertIn("Obsidian", matrix)
        self.assertIn("Notion", matrix)
        self.assertIn("Docs / Sheets / Slides", matrix)
        self.assertIn("治理问题", matrix)
        self.assertIn("工具操作问题", matrix)
        self.assertIn("MOC", matrix)
        self.assertIn("Canvas", matrix)
        self.assertIn("database view", matrix)
        self.assertIn("Obsidian Markdown 内链的最低协议", matrix)
        self.assertIn("[[笔记名]]", matrix)
        self.assertIn("桌面端可点击文件链接", matrix)
        self.assertIn("宿主化 Markdown 链接分流", tool_adapter)
        self.assertIn("### I. 对话链接 / 宿主内链分流", output)
        self.assertIn("不要把桌面端可点击绝对路径文件链接直接落盘进项目 Markdown", output)
        self.assertIn("默认都先按索引、状态或展示处理", manual)

    def test_hosted_knowledge_fixture_is_wired_and_machine_checked(self) -> None:
        matrix = HOSTED_KNOWLEDGE_MATRIX.read_text(encoding="utf-8")
        fixture_readme = (HOSTED_FIXTURE_ROOT / "README.md").read_text(encoding="utf-8")
        expected = json.loads((HOSTED_FIXTURE_ROOT / "classification.expected.json").read_text(encoding="utf-8"))

        self.assertIn("examples/hosted-knowledge-governance/README.md", matrix)
        self.assertIn("host-name-first governance triage", fixture_readme)
        self.assertIn("Obsidian", fixture_readme)
        self.assertIn("Notion", fixture_readme)
        self.assertIn("Docs, Sheets, or Slides", fixture_readme)
        self.assertEqual(expected["fixture_id"], "hosted-knowledge-governance")
        self.assertGreaterEqual(len(expected["checks"]), 8)
        self.assertGreaterEqual(len(expected["tool_operation_non_goals"]), 5)
        for item in expected["checks"]:
            self.assertTrue((HOSTED_FIXTURE_ROOT / item["path"]).exists(), item["path"])

    def test_audit_layer_matrix_is_wired_into_docs(self) -> None:
        readme = README.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        info_arch = INFO_ARCH_REVIEW.read_text(encoding="utf-8")
        radar = (ROOT / "docs" / "能力雷达与版本演进盘点.md").read_text(encoding="utf-8")
        matrix = AUDIT_MATRIX.read_text(encoding="utf-8")

        self.assertIn("docs/体检分层矩阵.md", readme)
        self.assertIn("体检分层矩阵", info_arch)
        self.assertIn("体检分层矩阵", radar)
        self.assertIn("scaffold", matrix)
        self.assertIn("pack", matrix)
        self.assertIn("runtime", matrix)
        self.assertIn("governance", matrix)
        self.assertIn("adoption", matrix)
        self.assertIn("默认 `audit = scaffold 基础体检`", matrix)
        self.assertIn("manage audit --layer pack", matrix)
        self.assertIn("manage audit --layer runtime", matrix)
        self.assertIn("manage audit --layer governance", matrix)
        self.assertIn("manage audit --layer adoption", matrix)
        self.assertIn("manage audit --layer pack", manual)
        self.assertIn("manage audit --layer runtime", manual)
        self.assertIn("manage audit --layer governance", manual)
        self.assertIn("manage audit --layer adoption", manual)

    def test_coverage_diff_matrix_is_wired_into_docs(self) -> None:
        readme = README.read_text(encoding="utf-8")
        info_arch = INFO_ARCH_REVIEW.read_text(encoding="utf-8")
        radar = (ROOT / "docs" / "能力雷达与版本演进盘点.md").read_text(encoding="utf-8")
        full_guide = FULL_GUIDE.read_text(encoding="utf-8")
        matrix = COVERAGE_DIFF.read_text(encoding="utf-8")

        self.assertIn("docs/能力覆盖矩阵与历史差分.md", readme)
        self.assertIn("能力覆盖矩阵与历史差分", info_arch)
        self.assertIn("能力覆盖矩阵与历史差分", radar)
        self.assertIn("能力覆盖矩阵与历史差分", full_guide)
        self.assertIn("v1 -> v2 -> v2.1", matrix)
        self.assertIn("v0.2.0 -> v0.5.0", matrix)
        self.assertIn("tranche v1", matrix)
        self.assertIn("README / SKILL / metadata / 手册", matrix)
        self.assertIn("真源 / 说明 / 执行 / 闭环", matrix)
        self.assertIn("宿主化知识工作场景", matrix)
        self.assertIn("audit` 五层体检", matrix)

    def test_external_workflow_retrofit_benchmark_is_explicit(self) -> None:
        readme = README.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        metadata = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        radar = (ROOT / "docs" / "能力雷达与版本演进盘点.md").read_text(encoding="utf-8")
        coverage = COVERAGE_DIFF.read_text(encoding="utf-8")
        plan = (ROOT / "docs" / "当前阶段补完计划.md").read_text(encoding="utf-8")
        retrofit = EXTERNAL_WORKFLOW_RETROFIT.read_text(encoding="utf-8")
        checkpoint = CHECKPOINT_DOC.read_text(encoding="utf-8")

        self.assertIn("docs/外部项目Workflow改造脚手架.md", readme)
        self.assertIn("workflow-control-plane / model-routing / hook-policy / state / events", skill)
        self.assertIn("human authority", metadata)
        self.assertIn("machine-readable control plane", metadata)
        self.assertIn("candidate benchmark", retrofit)
        self.assertIn("个案 benchmark", retrofit)
        self.assertIn("benchmark 晋升原则", retrofit)
        self.assertIn("薄共同骨架", retrofit)
        self.assertIn("workflow 是这次的实例", retrofit)
        self.assertIn("下次可能是 hooks 或 scaffolding", retrofit)
        self.assertIn("变量槽位", retrofit)
        self.assertIn("不少于 `2-3` 个外部项目样本", retrofit)
        self.assertIn("human authority", retrofit)
        self.assertIn("machine-readable control plane", retrofit)
        self.assertIn("config/workflow-control-plane.json", retrofit)
        self.assertIn("config/model-routing.json", retrofit)
        self.assertIn("config/hook-policy.json", retrofit)
        self.assertIn("逻辑角色", retrofit)
        self.assertIn("Gemini / Codex / Claude", retrofit)
        self.assertIn("外部 workflow 改造 benchmark", radar)
        self.assertIn("个案 benchmark", radar)
        self.assertIn("benchmark family", coverage)
        self.assertIn("薄共同骨架 + 变量槽位", coverage)
        self.assertIn("外部 workflow 控制面合同化 benchmark", coverage)
        self.assertIn("human authority layer", checkpoint)
        self.assertIn("薄共同骨架 + 变量槽位", plan)
        self.assertIn("hooks 或 scaffolding", plan)

    def test_ai_native_skill_e2e_matrix_is_wired_into_docs(self) -> None:
        readme = README.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        plan = (ROOT / "docs" / "当前阶段补完计划.md").read_text(encoding="utf-8")
        matrix = E2E_MATRIX.read_text(encoding="utf-8")

        self.assertIn("docs/AI-Native与Skill驱动E2E验收矩阵.md", readme)
        self.assertIn("AI-Native 与 Skill 驱动 E2E 验收矩阵", skill)
        self.assertIn("AI-Native 与 Skill 驱动 E2E 验收矩阵", plan)
        self.assertIn("agent-facing skill route", matrix)
        self.assertIn("downstream starter governance", matrix)
        self.assertIn("host-name-first triage", matrix)
        self.assertIn("runtime promotion chain", matrix)
        self.assertIn("self-hosting control capability", matrix)
        self.assertIn("CLI / runner", matrix)
        self.assertIn("模拟真实生产场景", matrix)
        self.assertIn("route contract", matrix)
        self.assertIn("宿主 CLI 或 runner", matrix)
        self.assertIn("reason_refs / artifact_refs / recall chain", matrix)
        self.assertIn("真实在线模型 + 多 agent + 外部工具的黑盒 runtime", matrix)
        self.assertIn("测试目标直达协议（下游默认）", matrix)
        self.assertIn("E2E 通过 = 真实入口触发 + 真源读取正确 + 写权受控执行 + 冷启动可恢复重放 + 结果 oracle 一致。", matrix)
        self.assertIn("truth_source_allowlist", matrix)
        self.assertIn("projection_denylist", matrix)
        self.assertIn("write_allowlist", matrix)
        self.assertIn("write_role", matrix)
        self.assertIn("oracle", matrix)
        self.assertIn("replay_seed", matrix)
        self.assertIn("failure_boundary", matrix)
        self.assertIn("下游如果反馈“测试目标不够直接”", skill)

    def test_examples_close_entry_to_contract_to_handoff_chain(self) -> None:
        discussion_boundary = (DISCUSSION_ROOT / "BOUNDARY.md").read_text(encoding="utf-8")
        discussion_workflow = (DISCUSSION_ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        discussion_contract = json.loads(
            (DISCUSSION_ROOT / "workflow.contract.json").read_text(encoding="utf-8")
        )
        process_projection = (PROCESS_ROOT / "process-projection.md").read_text(
            encoding="utf-8"
        )
        smoke_boundary = (SMOKE_ROOT / "BOUNDARY.md").read_text(encoding="utf-8")
        smoke_workflow = (SMOKE_ROOT / "WORKFLOW.md").read_text(encoding="utf-8")

        self.assertIn("先读它，再读 `active-discussions.md`、`WORKFLOW.md`", discussion_boundary)
        self.assertEqual(discussion_contract["explanation_ref"], "WORKFLOW.md")
        self.assertIn("`workflow.contract.json` is the control truth", discussion_workflow)

        self.assertIn("`handoff_focus`", process_projection)
        self.assertNotIn("`next_step`", process_projection)
        self.assertIn("不生成新的 gate、next-step 或放行结论", process_projection)

        self.assertIn("先读它，再读 `workflow.contract.json` 和运行实例", smoke_boundary)
        self.assertIn("`workflow.contract.json` + `rules.contract.json`", smoke_workflow)
        self.assertNotIn("allowed_next_step_refs: []", smoke_workflow)

    def test_story_chain_and_version_axes_stay_split(self) -> None:
        stories = STORIES.read_text(encoding="utf-8")
        migration = MIGRATION.read_text(encoding="utf-8")
        schema = SCHEMA_README.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")

        for text in (stories, migration, schema, skill, readme):
            self.assertIn("tranche v1", text)

        self.assertIn("能力模型阶段判断只认", stories)
        self.assertIn("只保留为历史兼容与迁移背景", stories)
        self.assertIn("如果你还没按前面的“先看你是哪种场景”分过一次诊", readme)
        self.assertIn("如果你是继续开发本仓库，或需要先建立统一基线，再用这 3 份建立共同口径", readme)
        self.assertIn("共享存储治理能力基线", stories)
        self.assertIn("这份手册只解释“怎么用这套", manual)
        self.assertIn("你希望把协作建立在共享存储上", manual)
        self.assertIn("如果你今天主要想知道怎么处理，先读 [docs/使用手册.md]", readme)
        self.assertIn("不要把 `README` 当成压缩版本体", readme)
        self.assertIn(
            "即使需要讲方法学，也默认优先用新手能接住的颗粒度来解释",
            FULL_GUIDE.read_text(encoding="utf-8"),
        )
        self.assertIn("只要 pack 里还保留 `pack_root/schemas/*.json`，validator 就会直接报迁移错误", readme)
        self.assertIn("`workflow.events.jsonl.subject_ref`", skill)
        self.assertIn("仓库根的 `schemas/` 目录是 repo 级 schema 草案目录", schema)

    def test_model_audit_baseline_is_reflected_into_skill_audit_path(self) -> None:
        model = MODEL.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")

        self.assertIn("派生文档约束", model)
        self.assertIn("后续审计基线", model)
        self.assertIn("### H. 真源对照与反向审计", skill)
        self.assertIn("派生文档约束", skill)
        self.assertIn("后续审计基线", skill)
        self.assertIn("没有把自己写成并列本体", skill)
        self.assertIn("contract tranche v1", skill)
        self.assertIn("误读成世界观版本", skill)
        self.assertIn("project_scope", skill)
        self.assertIn("capability_scope", skill)
        self.assertIn("self-hosting", skill)
        self.assertIn("repo.files-driven / skill.files-driven / meta-skill capability / downstream project instance", skill)
        self.assertIn("runtime -> candidate -> capability", skill)

    def test_downstream_starter_sources_keep_scope_drift_guards(self) -> None:
        starter_readme = (STARTER_ROOT / "README.md").read_text(encoding="utf-8")
        starter_skill = (STARTER_ROOT / "skills" / "review-skill" / "SKILL.md").read_text(encoding="utf-8")
        hooks_readme = (STARTER_ROOT / "tooling" / "hooks" / "README.md").read_text(encoding="utf-8")

        self.assertIn("project_scope", starter_readme)
        self.assertIn("不与治理真源平行定义本体", starter_readme)
        self.assertIn("project_scope", starter_skill)
        self.assertIn("不与治理真源平行定义本体", starter_skill)
        self.assertIn("不是 control truth", hooks_readme)
        self.assertIn("不是真源", hooks_readme)

    def test_execution_state_and_contract_examples_do_not_carry_legacy_next_step_authority(self) -> None:
        state_schema = json.loads(STATE_SCHEMA.read_text(encoding="utf-8"))
        smoke_state = json.loads((SMOKE_ROOT / "workflow.state.json").read_text(encoding="utf-8"))
        discussion_state = json.loads(
            (DISCUSSION_ROOT / "workflow.state.json").read_text(encoding="utf-8")
        )
        task_or_decision_action = json.loads(
            (DISCUSSION_ROOT / "objects" / "action.task.or.decision.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertNotIn("allowed_next_step_refs", state_schema["required"])
        self.assertNotIn("allowed_next_step_refs", state_schema["properties"])
        self.assertNotIn("allowed_next_step_refs", smoke_state)
        self.assertNotIn("allowed_next_step_refs", discussion_state)
        self.assertIn("handoff_focus", {field["field_id"] for field in task_or_decision_action["fields"]})
        self.assertNotIn("next_step", {field["field_id"] for field in task_or_decision_action["fields"]})

    def test_portable_entry_and_example_docs_avoid_workspace_absolute_paths(self) -> None:
        files = [
            README,
            QUICKSTART,
            STORIES,
            MIGRATION,
            SCHEMA_README,
            DISCUSSION_ROOT / "discussion.md",
            DISCUSSION_ROOT / "decision_package.md",
            DISCUSSION_ROOT / "task_or_decision.md",
            ADVERSARIAL_ROOT / "question-ledger.md",
            PROCESS_ROOT / "topology-supplement.md",
        ]

        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("/Users/jixiaokang/.agents/skills/files-driven", text, path.name)


if __name__ == "__main__":
    unittest.main()
