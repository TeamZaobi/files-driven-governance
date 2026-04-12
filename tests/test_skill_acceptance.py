import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
OUTPUT_CONVENTION = ROOT / "references" / "输出约定.md"
BASELINE = ROOT / "tests" / "fixtures" / "skill_acceptance_baseline.json"


def section_slice(text: str, start_heading: str, end_heading: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[start:end]


class SkillAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        cls.skill_text = SKILL.read_text(encoding="utf-8")
        cls.output_text = OUTPUT_CONVENTION.read_text(encoding="utf-8")

    def test_trigger_families_still_have_anchors(self) -> None:
        for family in self.baseline["trigger_families"]:
            for check in family["checks"]:
                path = ROOT / check["file"]
                text = path.read_text(encoding="utf-8")
                self.assertIn(
                    check["contains"],
                    text,
                    f"missing trigger anchor `{check['contains']}` for `{family['id']}`",
                )

    def test_skill_default_path_is_four_steps_and_puts_ownership_before_layers(self) -> None:
        targets = self.baseline["lightness_targets"]
        for heading in targets["required_skill_sections"]:
            self.assertIn(heading, self.skill_text)

        default_section = section_slice(
            self.skill_text,
            "## 默认主路径",
            "## 条件升级包",
        )
        headings = [line for line in default_section.splitlines() if line.startswith("### ")]
        self.assertEqual(len(headings), targets["skill_default_step_headings"])

        for phrase in targets["required_skill_phrases"]:
            self.assertIn(phrase, self.skill_text)

        for phrase in targets["absent_skill_phrases_in_default_section"]:
            self.assertNotIn(phrase, default_section)

    def test_output_convention_uses_four_block_default_skeleton(self) -> None:
        targets = self.baseline["lightness_targets"]
        for heading in targets["required_output_sections"]:
            self.assertIn(heading, self.output_text)

        default_section = section_slice(
            self.output_text,
            "## 默认回答骨架",
            "## 条件加段",
        )
        headings = [line for line in default_section.splitlines() if line.startswith("### ")]
        self.assertEqual(len(headings), targets["output_default_block_headings"])

        for phrase in targets["required_output_phrases"]:
            self.assertIn(phrase, self.output_text)

        for heading in targets["absent_output_headings"]:
            self.assertNotIn(heading, self.output_text)


if __name__ == "__main__":
    unittest.main()
