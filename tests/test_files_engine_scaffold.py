import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MODEL = ROOT / "docs" / "项目治理能力模型.md"
STARTER_DOC = ROOT / "docs" / "files引擎脚手架工程.md"
STORIES = ROOT / "PROJECT_STORIES_AND_TESTS.md"
STARTER_ROOT = ROOT / "starters" / "minimal-files-engine"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_files_engine_starter.py"
MANAGE = ROOT / "scripts" / "manage_files_engine.py"
SCAFFOLD_VALIDATOR = ROOT / "scripts" / "validate_files_engine_scaffold.py"
PACK_VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"


class FilesEngineScaffoldTests(unittest.TestCase):
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

    def write_json(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def bootstrap(self, project_id: str = "demo-project") -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        target = Path(temp_dir.name) / "starter"
        result = self.run_cmd(str(BOOTSTRAP), str(target), "--project-id", project_id)
        self.assertEqual(result.returncode, 0, result.stderr)
        return target

    def test_docs_surface_meta_skill_layers_and_new_story_chain(self) -> None:
        readme = README.read_text(encoding="utf-8")
        model = MODEL.read_text(encoding="utf-8")
        starter_doc = STARTER_DOC.read_text(encoding="utf-8")
        stories = STORIES.read_text(encoding="utf-8")

        self.assertIn("meta-skill capability", readme)
        self.assertIn("downstream project instance", readme)
        self.assertIn("meta-skill capability", model)
        self.assertIn("downstream project instance", model)
        self.assertIn("官方最小 starter", starter_doc)
        self.assertIn("US-9", stories)
        self.assertIn("US-10", stories)
        self.assertIn("US-11", stories)
        self.assertIn("US-12", stories)
        self.assertIn("TC-10", stories)
        self.assertIn("TC-11", stories)
        self.assertIn("TC-12", stories)
        self.assertIn("TC-13", stories)
        self.assertIn("manage_files_engine.py", readme)
        self.assertIn("`manage` CLI", starter_doc)
        self.assertIn("starter profile", starter_doc)

    def test_bootstrap_creates_valid_starter_for_both_scaffold_and_pack(self) -> None:
        target = self.bootstrap()

        manifest = self.read_json(target / "governance" / "scaffold.manifest.json")
        profile = self.read_json(target / "governance" / "starter.profile.json")
        registry = self.read_json(target / "governance" / "files.registry.json")
        routes = self.read_json(target / "governance" / "intent.routes.json")
        self.assertEqual(manifest["project_id"], "demo-project")
        self.assertEqual(manifest["manifest_id"], "scaffold.demo-project")
        self.assertEqual(profile["project_id"], "demo-project")
        self.assertEqual(profile["profile_id"], "starter.demo-project")
        self.assertEqual(registry["project_id"], "demo-project")
        self.assertEqual(routes["project_id"], "demo-project")

        scaffold = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))
        pack = self.run_cmd(str(PACK_VALIDATOR), str(target))

        self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
        self.assertEqual(pack.returncode, 0, pack.stderr)

    def test_unregistered_tracked_file_fails_scaffold_validation(self) -> None:
        target = self.bootstrap()
        stray = target / "objects" / "state.review.ready.json"
        stray.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "object_id": "state.review.ready",
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

        result = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("objects/state.review.ready.json", result.stderr)
        self.assertIn("tracked files must be registered", result.stderr)

    def test_unknown_route_reference_fails_scaffold_validation(self) -> None:
        target = self.bootstrap()
        routes_path = target / "governance" / "intent.routes.json"
        routes = self.read_json(routes_path)
        routes["routes"][0]["write_targets"].append("unknown.file")
        self.write_json(routes_path, routes)

        result = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown file_id `unknown.file`", result.stderr)

    def test_audit_cli_reports_registry_findings(self) -> None:
        target = self.bootstrap()
        stray = target / "objects" / "state.review.ready.json"
        stray.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "object_id": "state.review.ready",
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

        result = self.run_cmd(str(MANAGE), "audit", str(target), "--format", "json")

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "invalid")
        self.assertIn("registry", {finding["category"] for finding in payload["findings"]})
        self.assertIn("objects/state.review.ready.json", json.dumps(payload, ensure_ascii=False))

    def test_register_cli_adds_new_tracked_file(self) -> None:
        target = self.bootstrap()
        new_file = target / "objects" / "output.publish.review.extra.json"
        new_file.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "object_id": "output.publish.review.extra",
                    "family": "object",
                    "version_anchor": "v1",
                    "kind": "output_type",
                    "fields": [
                        {
                            "field_id": "summary",
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

        register = self.run_cmd(
            str(MANAGE),
            "register",
            str(target),
            "--file-id",
            "output.object.publish.review.extra",
            "--path",
            "objects/output.publish.review.extra.json",
            "--family",
            "object",
            "--layer",
            "truth_source",
            "--work-post",
            "output_contract",
            "--evidence-type",
            "output_type",
            "--truth-status",
            "canonical",
            "--write-role",
            "maintainer",
            "--consumed-as",
            "output_contract",
        )

        self.assertEqual(register.returncode, 0, register.stderr)
        registry = self.read_json(target / "governance" / "files.registry.json")
        entry = next(
            item for item in registry["entries"] if item["file_id"] == "output.object.publish.review.extra"
        )
        self.assertEqual(entry["path"], "objects/output.publish.review.extra.json")
        self.assertNotIn("evidence_type", entry)
        self.assertEqual(entry["annotations"]["evidence_type"], "output_type")

        scaffold = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))
        self.assertEqual(scaffold.returncode, 0, scaffold.stderr)

    def test_route_rename_does_not_require_registry_edit(self) -> None:
        target = self.bootstrap()
        routes_path = target / "governance" / "intent.routes.json"
        routes = self.read_json(routes_path)
        routes["routes"][0]["route_id"] = "route.bootstrap.files-engine.v2"
        self.write_json(routes_path, routes)

        result = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_manifest_controls_required_paths(self) -> None:
        target = self.bootstrap()
        manifest_path = target / "governance" / "scaffold.manifest.json"
        manifest = self.read_json(manifest_path)
        manifest["required_paths"].append("docs/missing.md")
        self.write_json(manifest_path, manifest)

        result = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required path missing `docs/missing.md`", result.stderr)

    def test_repair_cli_orders_manifest_before_routes(self) -> None:
        target = self.bootstrap()
        manifest_path = target / "governance" / "scaffold.manifest.json"
        routes_path = target / "governance" / "intent.routes.json"

        manifest = self.read_json(manifest_path)
        manifest["required_paths"].append("docs/missing.md")
        self.write_json(manifest_path, manifest)

        routes = self.read_json(routes_path)
        routes["routes"][0]["write_targets"].append("unknown.file")
        self.write_json(routes_path, routes)

        result = self.run_cmd(str(MANAGE), "repair", str(target), "--format", "json")

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "repair_needed")
        self.assertGreaterEqual(payload["step_count"], 2)
        self.assertEqual(payload["steps"][0]["category"], "manifest")
        self.assertEqual(payload["steps"][1]["category"], "routes")

    def test_family_layer_drift_is_rejected(self) -> None:
        target = self.bootstrap()
        registry_path = target / "governance" / "files.registry.json"
        registry = self.read_json(registry_path)
        for entry in registry["entries"]:
            if entry["file_id"] == "workflow.contract.review":
                entry["layer"] = "execution_object"
                break
        self.write_json(registry_path, registry)

        result = self.run_cmd(str(SCAFFOLD_VALIDATOR), str(target))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("incompatible family/layer `workflow` + `execution_object`", result.stderr)

    def test_bootstrap_refuses_nonempty_target_directory(self) -> None:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        target = Path(temp_dir.name) / "starter"
        target.mkdir(parents=True)
        (target / "keep.txt").write_text("occupied\n", encoding="utf-8")

        result = self.run_cmd(str(BOOTSTRAP), str(target))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("target directory must not already contain files", result.stderr)


if __name__ == "__main__":
    unittest.main()
