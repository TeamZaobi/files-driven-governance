import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
QUICKSTART = ROOT / "QUICKSTART.md"
MIGRATION = ROOT / "MIGRATION.md"
SCHEMA_README = ROOT / "schemas" / "README.md"
SKILL = ROOT / "SKILL.md"
METADATA = ROOT / "agents" / "openai.yaml"
EXAMPLE_READMES = [
    ROOT / "examples" / "smoke-governed-review" / "README.md",
    ROOT / "examples" / "discussion-decision-task" / "README.md",
    ROOT / "examples" / "adversarial-convergence" / "README.md",
    ROOT / "examples" / "multi-tool-process-projection" / "README.md",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class EntrypointConsistencyTests(unittest.TestCase):
    def test_governed_pack_entrypoints_keep_canonical_terms(self) -> None:
        quickstart = QUICKSTART.read_text(encoding="utf-8")
        migration = MIGRATION.read_text(encoding="utf-8")
        schema = SCHEMA_README.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")

        for text in (quickstart, migration, skill):
            self.assertIn("BOUNDARY.md", text)

        self.assertIn("objects/*.json", quickstart)
        self.assertIn("objects/*.json", migration)
        self.assertIn("workflow 顶层 `checks.route/evidence/write/stop`", quickstart)
        self.assertIn("route / evidence / write / stop", quickstart)
        self.assertIn("route / evidence / write / stop", schema)
        self.assertIn("route / evidence / write / stop", skill)
        self.assertIn("status.projection.json", schema)
        self.assertIn("不允许携带新的放行字段", schema)

    def test_metadata_matches_skill_default_path_language(self) -> None:
        metadata = METADATA.read_text(encoding="utf-8")
        self.assertIn("四层", metadata)
        self.assertIn("只在需要时", metadata)
        self.assertIn("governed-pack/harness", metadata)
        self.assertIn("discussion 晋升", metadata)

    def test_markdown_entry_links_resolve(self) -> None:
        for path in [README, QUICKSTART, MIGRATION, SKILL, *EXAMPLE_READMES]:
            text = path.read_text(encoding="utf-8")
            for raw_target in LINK_RE.findall(text):
                if raw_target.startswith(("http://", "https://", "mailto:", "app://", "#")):
                    continue

                target = raw_target.split("#", 1)[0]
                if not target:
                    continue

                if target.startswith("/"):
                    resolved = Path(target)
                else:
                    resolved = (path.parent / target).resolve()

                self.assertTrue(
                    resolved.exists(),
                    f"broken link in {path.relative_to(ROOT)} -> {raw_target}",
                )


if __name__ == "__main__":
    unittest.main()
