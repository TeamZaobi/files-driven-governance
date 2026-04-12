import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "ai_native_e2e"
RUNNER = ROOT / "scripts" / "run_ai_native_e2e_cli_judge.py"
VALIDATOR = ROOT / "scripts" / "validate_ai_native_e2e_bundle.py"


class AINativeE2ECliRunnerTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_generic_cli_runner_emits_valid_bundle_from_observed_replay(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        output_dir = Path(temp_dir.name) / "cli-run"

        command = json.dumps(
            [
                sys.executable,
                str(FIXTURE_DIR / "mock_runtime_cli.py"),
            ],
            ensure_ascii=False,
        )
        run = self.run_cmd(
            str(RUNNER),
            "--case",
            str(FIXTURE_DIR / "case.conversation_replay.json"),
            "--observed-replay-artifact",
            str(FIXTURE_DIR / "replay_artifact.conversation_replay.json"),
            "--observed-run-metadata",
            str(FIXTURE_DIR / "run_metadata.conversation_replay.json"),
            "--adapter-contract",
            str(FIXTURE_DIR / "adapter_contract.mock_cli.json"),
            "--output-dir",
            str(output_dir),
            "--cli-command-json",
            command,
            "--runtime-name",
            "mock-cli",
            "--runtime-version",
            "fixture-v1",
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

        summary = json.loads(run.stdout)
        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["overall_status"], "pass")

        validate = self.run_cmd(
            str(VALIDATOR),
            "--case",
            str(FIXTURE_DIR / "case.conversation_replay.json"),
            "--replay-artifact",
            str(output_dir / "replay_artifact.json"),
            "--assertion-report",
            str(output_dir / "assertion_report.json"),
            "--run-metadata",
            str(output_dir / "run_metadata.json"),
            "--adapter-contract",
            str(FIXTURE_DIR / "adapter_contract.mock_cli.json"),
        )
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

        report = json.loads((output_dir / "assertion_report.json").read_text(encoding="utf-8"))
        replay = json.loads((output_dir / "replay_artifact.json").read_text(encoding="utf-8"))
        run_metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))

        self.assertEqual(run_metadata["runtime_name"], "mock-cli")
        self.assertEqual(run_metadata["result"], "pass")
        self.assertEqual(report["overall_status"], "pass")
        self.assertEqual(replay["transcript"][-1]["tool_name"], "mock-cli")
        self.assertEqual({item["category"] for item in report["assertions"]}, {
            "route",
            "read",
            "write",
            "boundary",
            "projection",
            "recovery",
            "trajectory",
        })


if __name__ == "__main__":
    unittest.main()
