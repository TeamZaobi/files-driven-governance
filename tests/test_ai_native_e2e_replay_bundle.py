import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "ai_native_e2e"
VALIDATOR = ROOT / "scripts" / "validate_ai_native_e2e_bundle.py"


class AINativeE2EReplayBundleTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_self_hosting_conversation_replay_bundle_validates(self) -> None:
        result = self.run_cmd(
            str(VALIDATOR),
            "--case",
            str(FIXTURE_DIR / "case.conversation_replay.json"),
            "--replay-artifact",
            str(FIXTURE_DIR / "replay_artifact.conversation_replay.json"),
            "--assertion-report",
            str(FIXTURE_DIR / "assertion_report.conversation_replay.json"),
            "--run-metadata",
            str(FIXTURE_DIR / "run_metadata.conversation_replay.json"),
            "--adapter-contract",
            str(FIXTURE_DIR / "adapter_contract.unittest.json"),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["scenario_kind"], "conversation_replay")
        self.assertEqual(payload["execution_mode"], "conversation_replay")
        self.assertIn("trajectory", payload["checked_categories"])

    def test_missing_trajectory_category_fails_bundle_validation(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        workspace = Path(temp_dir.name)

        case_path = workspace / "case.json"
        replay_path = workspace / "replay.json"
        report_path = workspace / "report.json"
        run_path = workspace / "run.json"
        adapter_path = workspace / "adapter.json"

        case_path.write_text(
            (FIXTURE_DIR / "case.conversation_replay.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        replay_path.write_text(
            (FIXTURE_DIR / "replay_artifact.conversation_replay.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        run_path.write_text(
            (FIXTURE_DIR / "run_metadata.conversation_replay.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        adapter_path.write_text(
            (FIXTURE_DIR / "adapter_contract.unittest.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )

        report = json.loads(
            (FIXTURE_DIR / "assertion_report.conversation_replay.json").read_text(encoding="utf-8")
        )
        report["assertions"] = [
            item for item in report["assertions"] if item["category"] != "trajectory"
        ]
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result = self.run_cmd(
            str(VALIDATOR),
            "--case",
            str(case_path),
            "--replay-artifact",
            str(replay_path),
            "--assertion-report",
            str(report_path),
            "--run-metadata",
            str(run_path),
            "--adapter-contract",
            str(adapter_path),
        )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "invalid")
        self.assertIn("category `trajectory`", json.dumps(payload, ensure_ascii=False))

    def test_blocked_bundle_is_structurally_valid(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        workspace = Path(temp_dir.name)

        case_path = workspace / "case.json"
        replay_path = workspace / "replay.json"
        report_path = workspace / "report.json"
        run_path = workspace / "run.json"
        adapter_path = workspace / "adapter.json"

        for source, target in [
            (FIXTURE_DIR / "case.conversation_replay.json", case_path),
            (FIXTURE_DIR / "replay_artifact.conversation_replay.json", replay_path),
            (FIXTURE_DIR / "adapter_contract.unittest.json", adapter_path),
        ]:
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

        report = json.loads(
            (FIXTURE_DIR / "assertion_report.conversation_replay.json").read_text(encoding="utf-8")
        )
        report["overall_status"] = "blocked"
        report["assertions"][0]["status"] = "blocked"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        run_metadata = json.loads(
            (FIXTURE_DIR / "run_metadata.conversation_replay.json").read_text(encoding="utf-8")
        )
        run_metadata["result"] = "blocked"
        run_path.write_text(json.dumps(run_metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        result = self.run_cmd(
            str(VALIDATOR),
            "--case",
            str(case_path),
            "--replay-artifact",
            str(replay_path),
            "--assertion-report",
            str(report_path),
            "--run-metadata",
            str(run_path),
            "--adapter-contract",
            str(adapter_path),
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")


if __name__ == "__main__":
    unittest.main()
