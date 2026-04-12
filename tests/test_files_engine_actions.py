import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "scripts" / "bootstrap_files_engine_starter.py"
MANAGE = ROOT / "scripts" / "manage_files_engine.py"
SCAFFOLD_VALIDATOR = ROOT / "scripts" / "validate_files_engine_scaffold.py"


class FilesEngineActionTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
