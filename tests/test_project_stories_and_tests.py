import unittest
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_STORIES_AND_TESTS = ROOT / "PROJECT_STORIES_AND_TESTS.md"
REQUIRED_HEADINGS = [
    "## 当前使用场景",
    "## 当前交付物",
    "## 项目用户故事",
    "## 项目测试用例",
    "## 当前非目标",
    "## 质量判断参考",
    "## 验收责任人",
]
STORY_RE = re.compile(r"^###\s+用户故事\b.*$", re.MULTILINE)
TEST_RE = re.compile(r"^###\s+测试用例\b.*$", re.MULTILINE)
FAILURE_RE = re.compile(r"失败/越界边界", re.MULTILINE)


class ProjectStoriesAndTestsDocTests(unittest.TestCase):
    def test_project_stories_and_tests_doc_is_complete(self) -> None:
        text = PROJECT_STORIES_AND_TESTS.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            self.assertIn(heading, text, f"missing heading: {heading}")

        stories = STORY_RE.findall(text)
        tests = TEST_RE.findall(text)

        self.assertGreaterEqual(len(stories), 1)
        self.assertGreaterEqual(len(tests), 1)
        self.assertIn("验收责任人", text)
        self.assertIn("当前非目标", text)
        self.assertTrue(FAILURE_RE.search(text))


if __name__ == "__main__":
    unittest.main()
