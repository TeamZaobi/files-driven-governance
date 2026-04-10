import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADVERSARIAL_ROOT = ROOT / "examples" / "adversarial-convergence"
PROCESS_ROOT = ROOT / "examples" / "multi-tool-process-projection"
README = ROOT / "README.md"
MANUAL = ROOT / "docs" / "使用手册.md"
STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"


class DiscussionBranchAssetsTests(unittest.TestCase):
    def test_adversarial_example_contains_minimum_files(self) -> None:
        expected = {
            "README.md",
            "claim.md",
            "question-ledger.md",
            "defense.md",
            "convergence.md",
        }
        actual = {path.name for path in ADVERSARIAL_ROOT.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(actual))

    def test_question_ledger_and_convergence_keep_inquiry_closure_fields(self) -> None:
        ledger = (ADVERSARIAL_ROOT / "question-ledger.md").read_text(encoding="utf-8")
        convergence = (ADVERSARIAL_ROOT / "convergence.md").read_text(encoding="utf-8")

        self.assertIn("`question_id`", ledger)
        self.assertIn("`response_ref`", ledger)
        self.assertIn("`closure_authority`", ledger)
        self.assertIn("`result`", convergence)
        self.assertIn("`next_step`", convergence)
        self.assertIn("partial_accept", convergence)

    def test_process_projection_example_contains_required_assets(self) -> None:
        expected = {
            "README.md",
            "primary-trace.md",
            "review-trace.md",
            "decision-note.md",
            "process-projection.md",
            "topology-supplement.md",
            "status.projection.json",
        }
        actual = {path.name for path in PROCESS_ROOT.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(actual))

    def test_process_projection_and_status_projection_keep_handoff_fields(self) -> None:
        process_projection = (PROCESS_ROOT / "process-projection.md").read_text(
            encoding="utf-8"
        )
        topology = (PROCESS_ROOT / "topology-supplement.md").read_text(encoding="utf-8")
        status_projection = json.loads(
            (PROCESS_ROOT / "status.projection.json").read_text(encoding="utf-8")
        )

        for field in (
            "`goal`",
            "`actions`",
            "`findings`",
            "`decisions`",
            "`artifacts`",
            "`status`",
            "`next_step`",
        ):
            self.assertIn(field, process_projection)

        self.assertIn("## 节点", topology)
        self.assertIn("## 流转", topology)
        self.assertIn("## 关口", topology)
        self.assertEqual(status_projection["family"], "status_projection")
        self.assertIn("summary", status_projection)
        self.assertIn("gate_state", status_projection)
        self.assertNotIn("allowed_next_step_refs", status_projection)

    def test_entry_docs_surface_main_path_and_branch_routes(self) -> None:
        readme = README.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        stories = STORIES.read_text(encoding="utf-8")

        self.assertIn("议题还没到 `task / decision`", readme)
        self.assertIn("examples/adversarial-convergence/README.md", readme)
        self.assertIn("examples/multi-tool-process-projection/README.md", readme)
        self.assertIn("### 5.9 讨论一直停在聊天层", manual)
        self.assertIn("### 6.3 如果一个议题还没到 task 或 decision", manual)
        self.assertIn("discussion 什么时候开、什么时候晋升", manual)
        self.assertIn("### 想直接看 discussion 和收口样例", manual)
        self.assertIn("### 用户故事 US-8", stories)
        self.assertIn("### 测试用例 TC-8", stories)


if __name__ == "__main__":
    unittest.main()
