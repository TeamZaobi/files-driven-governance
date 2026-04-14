import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SKILL = ROOT / "SKILL.md"
METADATA = ROOT / "agents" / "openai.yaml"
OUTPUT_CONVENTION = ROOT / "references" / "输出约定.md"
STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"
PLAN = ROOT / "docs" / "当前阶段补完计划.md"
FIXTURE = ROOT / "tests" / "fixtures" / "agent_facing_e2e_cases.json"


class AgentFacingE2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.texts = {
            "README.md": README.read_text(encoding="utf-8"),
            "SKILL.md": SKILL.read_text(encoding="utf-8"),
            "agents/openai.yaml": METADATA.read_text(encoding="utf-8"),
            "references/输出约定.md": OUTPUT_CONVENTION.read_text(encoding="utf-8"),
            "references/理解型输入与低带宽压缩包.md": (
                ROOT / "references" / "理解型输入与低带宽压缩包.md"
            ).read_text(encoding="utf-8"),
        }

    def test_agent_interface_contract_is_explicit(self) -> None:
        metadata = self.texts["agents/openai.yaml"]
        readme = self.texts["README.md"]
        stories = STORIES.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")

        for phrase in self.fixture["global_contract"]["metadata_required_phrases"]:
            self.assertIn(phrase, metadata)

        for phrase in self.fixture["global_contract"]["readme_required_phrases"]:
            self.assertIn(phrase, readme)

        self.assertIn("用户故事 US-14", stories)
        self.assertIn("测试用例 TC-15", stories)
        self.assertIn("Agent-facing", stories)
        self.assertIn("agent-facing", plan)
        self.assertIn("真实 runtime 黑盒级 agent e2e", plan)
        self.assertIn("外部 workflow 个案 benchmark", plan)
        self.assertIn("不把一次外部 workflow 改造经验直接抬成仓库级通用模板", plan)
        self.assertIn("AI-Native 与 Skill 驱动 E2E 验收矩阵", plan)

    def test_common_agent_requests_route_to_expected_assets_and_output_shapes(self) -> None:
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                request_anchor = case["request_anchor"]
                self.assertIn(
                    request_anchor["contains"],
                    self.texts[request_anchor["file"]],
                )

                for check in case["route_checks"]:
                    self.assertIn(check["contains"], self.texts[check["file"]])

                for check in case["output_checks"]:
                    self.assertIn(check["contains"], self.texts[check["file"]])

    def test_agent_default_prompt_keeps_output_before_conditional_expansion(self) -> None:
        metadata = self.texts["agents/openai.yaml"]
        output = self.texts["references/输出约定.md"]

        self.assertIn("正式回答时先按最小骨架组织", metadata)
        self.assertIn("只在需要时", metadata)
        self.assertIn("运行观察 -> 候选保留 -> 能力晋升", metadata)
        self.assertIn("## 默认回答骨架", output)
        self.assertIn("## 条件加段", output)


if __name__ == "__main__":
    unittest.main()
