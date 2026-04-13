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
STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"
MIGRATION = ROOT / "MIGRATION.md"
SCHEMA_README = ROOT / "schemas" / "README.md"
STARTER_DOC = ROOT / "docs" / "files引擎脚手架工程.md"
STATE_SCHEMA = ROOT / "schemas" / "workflow.state.schema.json"
SHARED_REF = ROOT / "references" / "跨层共享约定.md"
CROSS_PROJECT_REF = ROOT / "references" / "跨项目共享模式提炼.md"
OUTPUT_CONVENTION = ROOT / "references" / "输出约定.md"
LOW_BANDWIDTH_REF = ROOT / "references" / "理解型输入与低带宽压缩包.md"
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
        language = LANGUAGE.read_text(encoding="utf-8")

        self.assertIn("先判动作、scope 和一级关口", manual)
        self.assertIn("默认判断顺序不是先分四层，也不是先分结构家族", full_guide)
        self.assertIn("先判当前动作、`scope` 和一级关口", shared)
        self.assertIn("先看当前动作、`scope` 和一级关口", cross_project)
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
        stories = STORIES.read_text(encoding="utf-8")

        self.assertIn("非工程背景起步.md", readme)
        self.assertIn("非工程背景起步", manual)
        self.assertIn("哪份文件算数", beginner)
        self.assertIn("今天先做什么", beginner)
        self.assertIn("哪些文件先别改", beginner)
        self.assertIn("如果用户明确说“看不懂”或明显不是工程背景", skill)
        self.assertIn("这次要做什么 / 先别做什么 / 卡住时找哪里", output)
        self.assertIn("给非工程背景读者的最小压缩形状", low_bandwidth)
        self.assertIn("docs/非工程背景起步.md", stories)

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
        readme = README.read_text(encoding="utf-8")

        for text in (stories, migration, schema, skill, readme):
            self.assertIn("tranche v1", text)

        self.assertIn("能力模型阶段判断只认", stories)
        self.assertIn("只保留为历史兼容与迁移背景", stories)
        self.assertIn("无论你是什么场景，先用这 3 份建立共同口径", readme)
        self.assertIn("只要 pack 里还保留 `pack_root/schemas/*.json`，validator 就会直接报迁移错误", readme)
        self.assertIn("`workflow.events.jsonl.subject_ref`", skill)
        self.assertIn("仓库根的 `schemas/` 目录是 repo 级 schema 草案目录", schema)

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
