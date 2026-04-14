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
MODEL = ROOT / "docs" / "项目治理能力模型.md"
MODEL_V1 = ROOT / "docs" / "项目治理能力模型_v1.md"
MANUAL = ROOT / "docs" / "使用手册.md"
PLAN = ROOT / "docs" / "当前阶段补完计划.md"
PROJECT_STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"
EXAMPLE_READMES = [
    ROOT / "examples" / "smoke-governed-review" / "README.md",
    ROOT / "examples" / "discussion-decision-task" / "README.md",
    ROOT / "examples" / "adversarial-convergence" / "README.md",
    ROOT / "examples" / "multi-tool-process-projection" / "README.md",
    ROOT / "examples" / "capture-candidate-activation" / "README.md",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class EntrypointConsistencyTests(unittest.TestCase):
    def test_governed_pack_entrypoints_keep_canonical_terms(self) -> None:
        readme = README.read_text(encoding="utf-8")
        quickstart = QUICKSTART.read_text(encoding="utf-8")
        migration = MIGRATION.read_text(encoding="utf-8")
        schema = SCHEMA_README.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        model = MODEL.read_text(encoding="utf-8")
        model_v1 = MODEL_V1.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")
        stories = PROJECT_STORIES.read_text(encoding="utf-8")

        self.assertTrue(readme.startswith("# files-driven\n"))
        self.assertIn("\n# files-driven\n", skill)
        self.assertIn("入口规则", readme)
        self.assertIn("能力规则", readme)
        self.assertIn("项目实体", readme)
        self.assertIn("v2.1", readme)
        self.assertIn("作用域绑定与防变形规则", readme)
        self.assertIn("docs/项目治理能力模型.md", readme)
        self.assertIn("动作触发 -> 一级关口 -> 二级升级", skill)
        self.assertIn("唯一的底层真源", model)
        self.assertIn("能力模型演进层", model)
        self.assertIn("受控合同链 tranche", model)
        self.assertIn("v1 -> v2 -> v2.1", model)
        self.assertIn("历史阶段入口", model_v1)
        self.assertIn("统一底层真源", stories)
        self.assertNotIn("skill 驱动 AI-Native 项目治理（files-driven）", readme)
        self.assertNotIn("skill 驱动 AI-Native 项目治理（files-driven）", skill)

        for text in (quickstart, migration, skill):
            self.assertIn("BOUNDARY.md", text)

        self.assertIn("docs/项目治理能力模型.md", quickstart)
        self.assertIn("docs/files引擎脚手架工程.md", readme)
        self.assertIn("bootstrap_files_engine_starter.py", readme)
        self.assertIn("manage_files_engine.py", readme)
        self.assertIn("validate_files_engine_scaffold.py", readme)
        self.assertIn("scaffold.manifest.json", readme)
        self.assertIn("starter profile", readme)
        self.assertIn("运行观察与能力晋升", readme)
        self.assertIn("capture-candidate-activation", readme)
        self.assertIn("bootstrap_files_engine_starter.py", quickstart)
        self.assertIn("objects/*.json", quickstart)
        self.assertIn("objects/*.json", migration)
        self.assertIn("workflow 顶层 `checks.route/evidence/write/stop`", quickstart)
        self.assertIn("route / evidence / write / stop", quickstart)
        self.assertIn("route / evidence / write / stop", schema)
        self.assertIn("route / evidence / write / stop", skill)
        self.assertIn("status.projection.json", schema)
        self.assertIn("file.registration.schema.json", schema)
        self.assertIn("files.registry.schema.json", schema)
        self.assertIn("intent.routes.schema.json", schema)
        self.assertIn("scaffold.manifest.schema.json", schema)
        self.assertIn("starter.profile.schema.json", schema)
        self.assertIn("hooks使用方法论与脚手架", readme)
        self.assertIn("hooks使用方法论与脚手架", skill)
        self.assertIn("hooks使用方法论与脚手架", manual)
        self.assertIn("文件身份核心", schema)
        self.assertIn("annotations", schema)
        self.assertIn("不允许携带新的放行字段", schema)
        self.assertIn("install / register / repair / audit", readme)
        self.assertIn("`manage` CLI", skill)
        self.assertIn("运行观察与能力晋升", skill)
        self.assertIn("capture-candidate-activation", skill)
        self.assertIn("运行观察与能力晋升", manual)
        self.assertIn("capture-candidate-activation", manual)
        self.assertIn("runtime -> candidate -> capability", plan)
        self.assertIn("补完顺序", plan)
        self.assertIn("不接受什么", plan)

    def test_metadata_matches_skill_default_path_language(self) -> None:
        metadata = METADATA.read_text(encoding="utf-8")
        self.assertIn('display_name: "files-driven"', metadata)
        self.assertIn("capability_scope、project_scope", metadata)
        self.assertIn("入口规则、能力规则、项目规则、项目实体", metadata)
        self.assertIn("一级关口", metadata)
        self.assertIn("self-hosting", metadata)
        self.assertIn("只在需要时", metadata)
        self.assertIn("governed-pack/harness", metadata)
        self.assertIn("discussion 晋升", metadata)

    def test_markdown_entry_links_resolve(self) -> None:
        for path in [README, QUICKSTART, MIGRATION, SKILL, MANUAL, PLAN, *EXAMPLE_READMES]:
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
