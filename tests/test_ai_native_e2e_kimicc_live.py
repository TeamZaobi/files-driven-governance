import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "ai_native_e2e"
LIVE_RUNNER = ROOT / "scripts" / "run_ai_native_e2e_cli_judge.py"
VALIDATOR = ROOT / "scripts" / "validate_ai_native_e2e_bundle.py"
KIMICC_CONFIG = Path.home() / ".kimicc.json"


def has_live_kimicc_profile(profile: str) -> bool:
    if os.environ.get("RUN_LIVE_AI_NATIVE_E2E") != "1":
        return False
    if shutil.which("kimicc") is None or not KIMICC_CONFIG.exists():
        return False
    try:
        config = json.loads(KIMICC_CONFIG.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    payload = config.get("profiles", {}).get(profile, {})
    key = payload.get("key", "")
    return isinstance(key, str) and key and "YOUR_" not in key and "sk-kimi-YOUR" not in key


@unittest.skipUnless(has_live_kimicc_profile("glm"), "requires RUN_LIVE_AI_NATIVE_E2E=1 and a usable kimicc glm profile")
class AINativeE2EKimiccLiveTests(unittest.TestCase):
    def run_cmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_kimicc_example_live_judge_emits_valid_bundle(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        output_dir = Path(temp_dir.name) / "live-run"

        command = json.dumps(
            ["kimicc", "--profile", "glm", "--print", "--output-format", "json", "--tools="],
            ensure_ascii=False,
        )

        live = self.run_cmd(
            str(LIVE_RUNNER),
            "--case",
            str(FIXTURE_DIR / "case.conversation_replay.json"),
            "--observed-replay-artifact",
            str(FIXTURE_DIR / "replay_artifact.conversation_replay.json"),
            "--observed-run-metadata",
            str(FIXTURE_DIR / "run_metadata.conversation_replay.json"),
            "--adapter-contract",
            str(FIXTURE_DIR / "adapter_contract.kimicc_glm.json"),
            "--output-dir",
            str(output_dir),
            "--cli-command-json",
            command,
            "--runtime-name",
            "kimicc:glm",
            "--runtime-version",
            "glm-4.7",
        )
        self.assertEqual(live.returncode, 0, live.stdout + live.stderr)

        summary = json.loads(live.stdout)
        self.assertEqual(summary["status"], "ok")
        self.assertEqual(summary["runtime_name"], "kimicc:glm")

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
            str(FIXTURE_DIR / "adapter_contract.kimicc_glm.json"),
        )
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

        report = json.loads((output_dir / "assertion_report.json").read_text(encoding="utf-8"))
        replay = json.loads((output_dir / "replay_artifact.json").read_text(encoding="utf-8"))
        run_metadata = json.loads((output_dir / "run_metadata.json").read_text(encoding="utf-8"))

        self.assertEqual(report["case_ref"], "case.ai-native-e2e.scope-routing.smoke")
        self.assertEqual(run_metadata["runtime_name"], "kimicc:glm")
        self.assertEqual({item["category"] for item in report["assertions"]}, {
            "route",
            "read",
            "write",
            "boundary",
            "projection",
            "recovery",
            "trajectory",
        })
        self.assertEqual(replay["transcript"][-1]["tool_name"], "kimicc:glm")
        self.assertIn(run_metadata["result"], {"pass", "fail", "blocked"})


if __name__ == "__main__":
    unittest.main()
