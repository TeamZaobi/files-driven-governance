import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "starters" / "ai-native-e2e-replay-harness"
SCAFFOLD_VALIDATOR = ROOT / "scripts" / "validate_files_engine_scaffold.py"


class AINativeE2EStarterTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_replay_harness_starter_validates_against_existing_scaffold_contracts(self) -> None:
        result = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(STARTER))
        self.assertEqual(result.returncode, 0, result.stderr)

        manifest = self.read_json(STARTER / "governance" / "scaffold.manifest.json")
        profile = self.read_json(STARTER / "governance" / "starter.profile.json")
        routes = self.read_json(STARTER / "governance" / "intent.routes.json")

        self.assertEqual(manifest["workflow_contract_path"], "harness.contract.json")
        self.assertEqual(
            set(profile["required_family_entries"]),
            {"policy_or_rules", "workflow", "display_projection"},
        )
        self.assertEqual(
            {route["primary_gate"] for route in routes["routes"]},
            {"boundary", "registry", "recovery"},
        )

    def test_replay_harness_docs_keep_ai_native_e2e_boundary_clear(self) -> None:
        readme = (STARTER / "README.md").read_text(encoding="utf-8")
        boundary = (STARTER / "BOUNDARY.md").read_text(encoding="utf-8")
        case_readme = (STARTER / "cases" / "README.md").read_text(encoding="utf-8")
        fixture_readme = (STARTER / "fixtures" / "README.md").read_text(encoding="utf-8")
        report_readme = (STARTER / "reports" / "README.md").read_text(encoding="utf-8")

        self.assertIn("并列关系", readme)
        self.assertIn("workflow_contract_path", readme)
        self.assertIn("不负责业务 runtime", boundary)
        self.assertIn("trajectory", boundary)
        self.assertIn("trajectory", case_readme)
        self.assertIn("replay-artifact", fixture_readme)
        self.assertIn("assertion-report", report_readme)


if __name__ == "__main__":
    unittest.main()
