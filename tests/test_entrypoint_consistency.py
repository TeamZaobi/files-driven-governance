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
VERSION_NEXT = ROOT / "docs" / "v0.4.1_版本说明.md"
CONTROL_STRENGTH = ROOT / "references" / "问题诊断与控制强度分级.md"
EXECUTION_SURFACE = ROOT / "references" / "执行面判定与CLI生产策略.md"
EXTERNAL_WORKFLOW = ROOT / "docs" / "外部项目Workflow改造脚手架.md"
MANUAL = ROOT / "docs" / "使用手册.md"
PLAN = ROOT / "docs" / "当前阶段补完计划.md"
PROJECT_STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"
INFO_ARCH_REVIEW = ROOT / "docs" / "三层信息架构复盘.md"
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
        version_next = VERSION_NEXT.read_text(encoding="utf-8")
        control_strength = CONTROL_STRENGTH.read_text(encoding="utf-8")
        execution_surface = EXECUTION_SURFACE.read_text(encoding="utf-8")
        external_workflow = EXTERNAL_WORKFLOW.read_text(encoding="utf-8")
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
        self.assertIn("帮助用户识别问题，解决问题", readme)
        self.assertIn("强化控制能力", readme)
        self.assertIn("世界观轴", readme)
        self.assertIn("控制强度轴", readme)
        self.assertIn("执行面轴", readme)
        self.assertIn("动作触发 -> 一级关口 -> 二级升级", skill)
        self.assertIn("帮助用户识别问题，解决问题", skill)
        self.assertIn("强化控制能力", skill)
        self.assertIn("世界观轴", skill)
        self.assertIn("控制强度轴", skill)
        self.assertIn("执行面轴", skill)
        self.assertIn("唯一的底层真源", model)
        self.assertIn("能力模型演进层", model)
        self.assertIn("受控合同链 tranche", model)
        self.assertIn("v1 -> v2 -> v2.1", model)
        self.assertIn("帮助用户识别问题，解决问题", model)
        self.assertIn("强化控制能力", model)
        self.assertIn("真源层", INFO_ARCH_REVIEW.read_text(encoding="utf-8"))
        self.assertIn("README / SKILL / metadata", INFO_ARCH_REVIEW.read_text(encoding="utf-8"))
        self.assertIn("未发布方向说明", version_next)
        self.assertIn("强化控制能力", version_next)
        self.assertIn("宿主原生能力优先", version_next)
        self.assertIn("CLI", version_next)
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
        self.assertIn("capability-improve", readme)
        self.assertIn("capability-improve", skill)
        self.assertIn("run_project_director_capability_improvement.py", readme)
        self.assertIn("run_project_director_capability_improvement.py", skill)
        self.assertIn("Codex CLI", readme)
        self.assertIn("Codex CLI", skill)
        self.assertIn("问题诊断与控制强度分级", readme)
        self.assertIn("执行面判定与CLI生产策略", readme)
        self.assertIn("外部项目Workflow改造脚手架", readme)
        self.assertIn("问题诊断与控制强度分级", skill)
        self.assertIn("执行面判定与CLI生产策略", skill)
        self.assertIn("外部项目Workflow改造脚手架", skill)
        self.assertIn("L0", control_strength)
        self.assertIn("L4", control_strength)
        self.assertIn("CLI", execution_surface)
        self.assertIn("producer", execution_surface)
        self.assertIn("不是新的顶层结构家族", execution_surface)
        self.assertIn("最小 starter 模板", external_workflow)
        self.assertIn("不是 `manage` CLI 的正式子命令", external_workflow)
        self.assertIn("最小 benchmark 模板", external_workflow)
        self.assertIn("运行观察与能力晋升", skill)
        self.assertIn("capture-candidate-activation", skill)
        self.assertIn("运行观察与能力晋升", manual)
        self.assertIn("capture-candidate-activation", manual)
        self.assertIn("runtime -> candidate -> capability", plan)
        self.assertIn("补完顺序", plan)
        self.assertIn("不接受什么", plan)
        self.assertIn("运行观察与能力晋升", skill)
        self.assertIn("capture-candidate-activation", skill)
        self.assertIn("运行观察与能力晋升", manual)
        self.assertIn("capture-candidate-activation", manual)
        self.assertIn("runtime -> candidate -> capability", plan)
        self.assertIn("补完顺序", plan)
        self.assertIn("不接受什么", plan)
        self.assertIn("docs/宿主化知识工作场景矩阵.md", skill)
        self.assertIn("docs/体检分层矩阵.md", skill)
        self.assertIn("先判断用户是在问治理问题还是工具操作问题", skill)
        self.assertIn("scaffold / pack / runtime / governance / adoption", skill)
        self.assertIn("draft checker", skill)

    def test_readme_front_page_prioritizes_routing_before_theory(self) -> None:
        readme = README.read_text(encoding="utf-8")

        self.assertIn("## 目录", readme)
        self.assertIn("## 先看你是哪种场景", readme)
        self.assertIn("## 首屏动作", readme)
        self.assertIn("继续开发本仓库", readme)
        self.assertIn("哪份文件算数", readme)
        self.assertIn("默认也先用新手能接住的颗粒度来讲", readme)
        self.assertIn("docs/三层信息架构复盘.md", readme)
        self.assertIn("入口层", readme)
        self.assertIn("说明层", readme)
        self.assertIn("真源层", readme)
        self.assertNotIn("不再只回答“文档怎么分层”", readme)

        self.assertLess(readme.index("## 目录"), readme.index("## 第一性原理与当前版本方向"))
        self.assertLess(readme.index("## 先看你是哪种场景"), readme.index("## 第一性原理与当前版本方向"))
        self.assertLess(readme.index("## 首屏动作"), readme.index("## 第一性原理与当前版本方向"))

    def test_skill_front_page_starts_from_problem_then_control_model(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")

        self.assertIn("现在哪份文件算数", skill)
        self.assertIn("今天先做哪一步", skill)
        self.assertIn("这次到底需不需要更强控制", skill)
        self.assertIn("如果当前主要想知道怎么处理现有问题，优先按下面的“默认主路径”执行", skill)
        self.assertIn("如果主要想系统理解为什么这样判断，读 [docs/完整说明书.md]", skill)
        self.assertIn("如果要改底层本体，回 [docs/项目治理能力模型.md]", skill)
        self.assertNotIn("不再把自己写成“结构治理顾问”", skill)
        self.assertLess(skill.index("现在哪份文件算数"), skill.index("世界观轴"))

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
        self.assertIn("capability-improve", metadata)
        self.assertIn("Codex CLI", metadata)
        self.assertIn("识别问题并按需强化控制能力", metadata)
        self.assertIn("强化控制能力", metadata)
        self.assertIn("哪份文件算数 / 今天先做哪一步 / 哪些先别改", metadata)
        self.assertIn("install / register / repair / audit", metadata)
        self.assertIn("若当前主要是在处理现有问题，优先给最小动作", metadata)
        self.assertIn("Obsidian / Notion / Docs / Sheets / Slides", metadata)
        self.assertIn("治理问题还是工具操作问题", metadata)
        self.assertIn("真源、写权、投影、漂移、恢复或读取顺序", metadata)
        self.assertIn("scaffold / pack / runtime / governance / adoption", metadata)
        self.assertIn("当前统一动作面已覆盖 `scaffold`、`pack`、`runtime`、`governance`、`adoption` 五层", metadata)
        self.assertIn("如果用户需要系统理解为什么这样判断，再补完整说明", metadata)
        self.assertIn("不要把 metadata 自己写成压缩版本体", metadata)

    def test_markdown_entry_links_resolve(self) -> None:
        for path in [
            README,
            QUICKSTART,
            MIGRATION,
            SKILL,
            MANUAL,
            PLAN,
            VERSION_NEXT,
            CONTROL_STRENGTH,
            EXECUTION_SURFACE,
            EXTERNAL_WORKFLOW,
            *EXAMPLE_READMES,
        ]:
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
