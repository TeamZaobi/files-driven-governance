import json
import os
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_project_director_capability_improvement.py"
VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"


class ProjectDirectorCapabilityImprovementRunnerTests(unittest.TestCase):
    def make_mock_codex(self, mode: str = "success") -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        script_path = Path(temp_dir.name) / "mock_codex.py"
        script_path.write_text(
            textwrap.dedent(
                f"""\
                #!/usr/bin/env python3
                import json
                import re
                import sys
                from pathlib import Path

                MODE = {mode!r}

                def extract(flag, argv):
                    if flag in argv:
                        return argv[argv.index(flag) + 1]
                    return None

                def main() -> int:
                    stdin_text = sys.stdin.read()
                    last_message = extract("--output-last-message", sys.argv)
                    packet_match = re.search(r"^TASK_PACKET_PATH: (.+)$", stdin_text, re.MULTILINE)
                    if last_message:
                        Path(last_message).write_text("mock last message\\n", encoding="utf-8")
                    if MODE == "exit-1":
                        print('{{"type":"error","message":"forced failure"}}')
                        return 1
                    if not packet_match:
                        print('{{"type":"error","message":"missing packet"}}')
                        return 2
                    packet_path = Path(packet_match.group(1).strip())
                    packet = json.loads(packet_path.read_text(encoding="utf-8"))
                    deliverable = packet_path.parents[1] / packet["deliverable_path"]
                    if MODE != "missing-deliverable":
                        lines = [f"# {{packet['title']}}", ""]
                        for section in packet["required_sections"]:
                            lines.extend([section, "", f"Generated for {{packet['node_id']}}.", ""])
                        lines.append("Benchmark anchors: " + ", ".join(packet["benchmark_anchors"]))
                        deliverable.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
                    print('{{"type":"message","message":"mock complete"}}')
                    return 0

                if __name__ == "__main__":
                    raise SystemExit(main())
                """
            ),
            encoding="utf-8",
        )
        script_path.chmod(script_path.stat().st_mode | stat.S_IXUSR)
        return script_path

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

    def test_runner_generates_valid_governed_pack_with_mock_codex(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack_root = Path(temp_dir) / "capability-pack"
            mock_codex = self.make_mock_codex()

            result = self.run_cmd(
                str(RUNNER),
                str(pack_root),
                "--workspace-root",
                str(ROOT),
                "--codex-bin",
                str(mock_codex),
                "--benchmark",
                "019d859b-41f3-7752-bc49-ca9282c784ca",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((pack_root / "workflow.contract.json").exists())
            self.assertTrue((pack_root / "workflow.state.json").exists())
            self.assertTrue((pack_root / "workflow.events.jsonl").exists())
            self.assertTrue((pack_root / "status.projection.json").exists())
            self.assertTrue((pack_root / "summary.md").exists())

            state = self.read_json(pack_root / "workflow.state.json")
            projection = self.read_json(pack_root / "status.projection.json")
            self.assertEqual(state["current_node_id"], "node.promote_or_rollback")
            self.assertEqual(state["gate_state"], "ready")
            self.assertEqual(projection["gate_state"], "ready")
            self.assertEqual(len(state["missing_evidence_refs"]), 0)

            events = [
                json.loads(line)
                for line in (pack_root / "workflow.events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(events), 7)

            for deliverable in (
                "observe_gaps.md",
                "map_capability_graph.md",
                "design_control_upgrade.md",
                "define_runtime_protocol.md",
                "pilot_on_benchmarks.md",
                "promote_or_rollback.md",
            ):
                self.assertTrue((pack_root / deliverable).exists(), deliverable)

            packet = self.read_json(pack_root / "task_packets" / "observe_gaps.json")
            self.assertIn("019d859b-41f3-7752-bc49-ca9282c784ca", packet["benchmark_anchors"])

            validate = self.run_cmd(str(VALIDATOR), str(pack_root))
            self.assertEqual(validate.returncode, 0, validate.stderr)

    def test_runner_stops_and_marks_blocked_when_codex_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack_root = Path(temp_dir) / "capability-pack"
            mock_codex = self.make_mock_codex(mode="exit-1")

            result = self.run_cmd(
                str(RUNNER),
                str(pack_root),
                "--workspace-root",
                str(ROOT),
                "--codex-bin",
                str(mock_codex),
                "--benchmark",
                "019d859b-41f3-7752-bc49-ca9282c784ca",
            )

            self.assertNotEqual(result.returncode, 0)
            state = self.read_json(pack_root / "workflow.state.json")
            self.assertEqual(state["gate_state"], "blocked")
            events = [
                json.loads(line)
                for line in (pack_root / "workflow.events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(events[-1]["event_type"], "blocked")


if __name__ == "__main__":
    unittest.main()
