import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references" / "讨论收口与晋升.md"
EXAMPLE_ROOT = ROOT / "examples" / "discussion-decision-task"
VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"


class DiscussionPromotionAssetsTests(unittest.TestCase):
    def test_reference_exists_and_answers_core_questions(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("什么时候开 discussion", text)
        self.assertIn("最低要留什么", text)
        self.assertIn("何时升级到质询", text)
        self.assertIn("何时压成 decision_package", text)
        self.assertIn("何时压成 task", text)
        self.assertIn("何时压成 decision", text)
        self.assertIn("何时归档", text)

    def test_example_contains_main_path_files(self) -> None:
        expected = {
            "README.md",
            "discussion.md",
            "decision_package.md",
            "task_or_decision.md",
            "active-discussions.md",
        }
        actual = {path.name for path in EXAMPLE_ROOT.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(actual))
        self.assertNotIn("decision-package.md", actual)
        self.assertNotIn("task.md", actual)

    def test_discussion_example_contains_promotion_fields(self) -> None:
        text = (EXAMPLE_ROOT / "discussion.md").read_text(encoding="utf-8")
        self.assertIn("`issue_ledger`", text)
        self.assertIn("`promotion_target`", text)
        self.assertIn("`closure_authority`", text)
        self.assertIn("## Promotion Judgment", text)

    def test_final_landing_example_contains_owner_object_and_stop_condition(self) -> None:
        text = (EXAMPLE_ROOT / "task_or_decision.md").read_text(encoding="utf-8")
        self.assertIn("`owner`", text)
        self.assertIn("`current_object`", text)
        self.assertIn("`stop_condition`", text)
        self.assertIn("## Owner Handoff", text)

    def test_active_discussions_keeps_boundary_thread_visible(self) -> None:
        text = (EXAMPLE_ROOT / "active-discussions.md").read_text(encoding="utf-8")
        self.assertIn("`why_active`", text)
        self.assertIn("`next_action`", text)
        self.assertIn("`promote_to`", text)
        self.assertIn("controlled promotion path", text)

    def test_discussion_and_entry_page_use_same_canonical_promotion_route(self) -> None:
        discussion = (EXAMPLE_ROOT / "discussion.md").read_text(encoding="utf-8")
        active = (EXAMPLE_ROOT / "active-discussions.md").read_text(encoding="utf-8")
        decision_package = (EXAMPLE_ROOT / "decision_package.md").read_text(encoding="utf-8")

        self.assertIn("decision_package -> task_or_decision", discussion)
        self.assertIn("decision_package -> task_or_decision", active)
        self.assertIn("task_or_decision.md", decision_package)

    def test_discussion_pack_passes_validator(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(EXAMPLE_ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
