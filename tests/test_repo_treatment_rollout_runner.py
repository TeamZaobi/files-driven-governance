import json
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_repo_treatment_rollout.py"
VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"


class RepoTreatmentRolloutRunnerTests(unittest.TestCase):
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
                    packet_match = re.search(r"^TASK_PACKET_PATH: (.+)$", stdin_text, re.MULTILINE)
                    last_message = extract("--output-last-message", sys.argv)
                    if last_message:
                        Path(last_message).write_text("mock last message\\n", encoding="utf-8")
                    if MODE == "exit-1":
                        print('{{"type":"error","message":"forced failure"}}')
                        return 1
                    if not packet_match:
                        print('{{"type":"error","message":"missing packet"}}')
                        return 2
                    packet = json.loads(Path(packet_match.group(1).strip()).read_text(encoding="utf-8"))
                    for relative in packet.get("workspace_targets", []):
                        target = Path(packet["workspace_root"]) / relative
                        target.parent.mkdir(parents=True, exist_ok=True)
                        existing = target.read_text(encoding="utf-8") if target.exists() else ""
                        target.write_text(existing + f"\\n# touched by {{packet['node_id']}}\\n", encoding="utf-8")
                    report = Path(packet["report_path"])
                    report.parent.mkdir(parents=True, exist_ok=True)
                    lines = [f"# {{packet['title']}}", ""]
                    for section in packet["required_sections"]:
                        lines.extend([section, "", f"Generated for {{packet['node_id']}}.", ""])
                    if packet.get("workspace_targets"):
                        lines.append("Touched: " + ", ".join(packet["workspace_targets"]))
                    report.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
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

    def scaffold_workspace(self, root: Path) -> None:
        files = {
            "README.md": "# files-driven\n",
            "SKILL.md": "# files-driven\n",
            "agents/openai.yaml": 'interface:\\n  display_name: "old name"\\n',
            "docs/当前阶段补完计划.md": "# 当前阶段补完计划\n",
            "docs/非工程背景起步.md": "# 起步\n",
            "docs/使用手册.md": "# 使用手册\n",
            "scripts/manage_files_engine.py": "print('manage')\n",
            "scripts/validate_files_engine_scaffold.py": "print('scaffold')\n",
            "scripts/validate_governance_assets.py": "print('governance')\n",
            "tests/test_entrypoint_consistency.py": "print('entrypoint')\n",
            "tests/test_files_engine_scaffold.py": "print('files_engine_scaffold')\n",
            "tests/test_files_engine_actions.py": "print('files_engine_actions')\n",
            "tests/test_validate_governance_assets.py": "print('validate_governance_assets')\n",
            "tests/test_capture_promotion_assets.py": "print('capture_promotion_assets')\n",
            "tests/test_agent_facing_e2e.py": "print('agent_facing_e2e')\n",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def init_git_repo(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=root, check=True, capture_output=True, text=True)

    def test_runner_generates_valid_pack_and_touches_workspace_with_mock_codex(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            output_root = Path(temp_dir) / "run-pack"
            workspace_root.mkdir()
            self.scaffold_workspace(workspace_root)
            mock_codex = self.make_mock_codex()

            result = self.run_cmd(
                str(RUNNER),
                str(output_root),
                "--workspace-root",
                str(workspace_root),
                "--codex-bin",
                str(mock_codex),
                "--no-default-final-checks",
                "--final-check",
                "python3 -c \"from pathlib import Path; assert Path('README.md').exists()\"",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_root / "workflow.contract.json").exists())
            self.assertTrue((output_root / "workflow.state.json").exists())
            self.assertTrue((output_root / "workflow.events.jsonl").exists())
            self.assertTrue((output_root / "status.projection.json").exists())
            self.assertTrue((output_root / "summary.md").exists())
            self.assertTrue((output_root / "reports" / "verify_and_close.md").exists())

            state = self.read_json(output_root / "workflow.state.json")
            projection = self.read_json(output_root / "status.projection.json")
            self.assertEqual(state["current_node_id"], "node.verify_and_close")
            self.assertEqual(state["gate_state"], "ready")
            self.assertEqual(projection["gate_state"], "ready")
            self.assertEqual(len(state["missing_evidence_refs"]), 0)

            command = self.read_json(output_root / "codex_runs" / "align_identity_surface" / "command.json")
            self.assertIn("--model", command)
            self.assertIn("gpt-5.4", command)

            touched = (workspace_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn("node.align_identity_surface", touched)

            validate = self.run_cmd(str(VALIDATOR), str(output_root))
            self.assertEqual(validate.returncode, 0, validate.stderr)

    def test_runner_stops_and_marks_blocked_when_codex_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            output_root = Path(temp_dir) / "run-pack"
            workspace_root.mkdir()
            self.scaffold_workspace(workspace_root)
            mock_codex = self.make_mock_codex(mode="exit-1")

            result = self.run_cmd(
                str(RUNNER),
                str(output_root),
                "--workspace-root",
                str(workspace_root),
                "--codex-bin",
                str(mock_codex),
                "--no-default-final-checks",
            )

            self.assertNotEqual(result.returncode, 0)
            state = self.read_json(output_root / "workflow.state.json")
            self.assertEqual(state["gate_state"], "blocked")
            events = [
                json.loads(line)
                for line in (output_root / "workflow.events.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(events[-1]["event_type"], "blocked")

    def test_runner_rejects_dirty_workspace_without_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir) / "workspace"
            output_root = Path(temp_dir) / "run-pack"
            workspace_root.mkdir()
            self.scaffold_workspace(workspace_root)
            self.init_git_repo(workspace_root)
            (workspace_root / "README.md").write_text("# dirty\n", encoding="utf-8")
            mock_codex = self.make_mock_codex()

            result = self.run_cmd(
                str(RUNNER),
                str(output_root),
                "--workspace-root",
                str(workspace_root),
                "--codex-bin",
                str(mock_codex),
                "--no-default-final-checks",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--allow-dirty-workspace", result.stderr)


if __name__ == "__main__":
    unittest.main()
