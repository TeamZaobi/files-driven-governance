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
BOOTSTRAP = ROOT / "scripts" / "bootstrap_files_engine_starter.py"
MANAGE = ROOT / "scripts" / "manage_files_engine.py"
SCAFFOLD_VALIDATOR = ROOT / "scripts" / "validate_files_engine_scaffold.py"


class FilesEngineActionTests(unittest.TestCase):
    def make_mock_codex(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        script_path = Path(temp_dir.name) / "mock_codex.py"
        script_path.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env python3
                import json
                import re
                import sys
                from pathlib import Path

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
                    if not packet_match:
                        print('{"type":"error","message":"missing packet"}')
                        return 2
                    packet_path = Path(packet_match.group(1).strip())
                    packet = json.loads(packet_path.read_text(encoding="utf-8"))
                    deliverable = packet_path.parents[1] / packet["deliverable_path"]
                    lines = [f"# {packet['title']}", ""]
                    for section in packet["required_sections"]:
                        lines.extend([section, "", f"Generated for {packet['node_id']}.", ""])
                    lines.append("Benchmark anchors: " + ", ".join(packet["benchmark_anchors"]))
                    deliverable.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
                    print('{"type":"message","message":"mock complete"}')
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

    def bootstrap(self, project_id: str = "demo-project") -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        target = Path(temp_dir.name) / "starter"
        result = self.run_cmd(str(BOOTSTRAP), str(target), "--project-id", project_id)
        self.assertEqual(result.returncode, 0, result.stderr)
        return target

    def test_install_register_and_audit_round_trip(self) -> None:
        target = self.bootstrap()
        new_file = target / "objects" / "state.review.extra.json"
        new_file.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "object_id": "state.review.extra",
                    "family": "object",
                    "version_anchor": "v1",
                    "kind": "state_profile",
                    "fields": [
                        {
                            "field_id": "gate_state",
                            "type": "string",
                            "required": True
                        }
                    ]
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        invalid_audit = self.run_cmd(str(MANAGE), "audit", str(target), "--format", "json")
        self.assertNotEqual(invalid_audit.returncode, 0)

        register = self.run_cmd(
            str(MANAGE),
            "register",
            str(target),
            "--file-id",
            "state.object.review.extra",
            "--path",
            "objects/state.review.extra.json",
            "--family",
            "object",
            "--layer",
            "truth_source",
            "--work-post",
            "state_contract",
            "--truth-status",
            "canonical",
            "--write-role",
            "maintainer",
        )
        self.assertEqual(register.returncode, 0, register.stderr)

        valid_audit = self.run_cmd(str(MANAGE), "audit", str(target), "--format", "json")
        self.assertEqual(valid_audit.returncode, 0, valid_audit.stderr)
        self.assertEqual(json.loads(valid_audit.stdout)["status"], "valid")

        scaffold = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))
        self.assertEqual(scaffold.returncode, 0, scaffold.stderr)

    def test_register_replace_overwrites_existing_entry(self) -> None:
        target = self.bootstrap()
        result = self.run_cmd(
            str(MANAGE),
            "register",
            str(target),
            "--file-id",
            "boundary.root",
            "--path",
            "BOUNDARY.md",
            "--family",
            "policy_or_rules",
            "--layer",
            "truth_source",
            "--work-post",
            "boundary_anchor",
        )
        self.assertNotEqual(result.returncode, 0)

        replace = self.run_cmd(
            str(MANAGE),
            "register",
            str(target),
            "--file-id",
            "boundary.root",
            "--path",
            "BOUNDARY.md",
            "--family",
            "policy_or_rules",
            "--layer",
            "truth_source",
            "--work-post",
            "boundary_anchor",
            "--evidence-type",
            "boundary_evidence",
            "--replace",
        )
        self.assertEqual(replace.returncode, 0, replace.stderr)
        registry = self.read_json(target / "governance" / "files.registry.json")
        entry = next(item for item in registry["entries"] if item["file_id"] == "boundary.root")
        self.assertEqual(entry["annotations"]["evidence_type"], "boundary_evidence")

    def test_capability_improve_runs_runner_via_manage_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack_root = Path(temp_dir) / "capability-pack"
            mock_codex = self.make_mock_codex()

            previous_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{mock_codex.parent}:{previous_path}"
            self.addCleanup(lambda: os.environ.__setitem__("PATH", previous_path))

            result = self.run_cmd(
                str(MANAGE),
                "capability-improve",
                str(pack_root),
                "--workspace-root",
                str(ROOT),
                "--codex-bin",
                str(mock_codex),
                "--benchmark",
                "019d859b-41f3-7752-bc49-ca9282c784ca",
                "--format",
                "json",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "completed")
            self.assertIn("capability improvement run completed", payload["stdout"])

            state = self.read_json(pack_root / "workflow.state.json")
            report = self.read_json(pack_root / "validation.report.json")
            self.assertEqual(state["gate_state"], "ready")
            self.assertEqual(report["returncode"], 0)


if __name__ == "__main__":
    unittest.main()
