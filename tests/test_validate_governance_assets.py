import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"
SMOKE_PACK = ROOT / "examples" / "smoke-governed-review"


class ValidateGovernanceAssetsCliTests(unittest.TestCase):
    def make_pack(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        pack_root = Path(temp_dir.name) / "pack"
        shutil.copytree(SMOKE_PACK, pack_root)
        return pack_root

    def run_validator(self, pack_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(pack_root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json(self, path: Path, data: dict) -> None:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def read_events(self, path: Path) -> list[dict]:
        events = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
        return events

    def write_events(self, path: Path, events: list[dict]) -> None:
        payload = "\n".join(json.dumps(event, ensure_ascii=False) for event in events)
        path.write_text(payload + "\n", encoding="utf-8")

    def test_smoke_pack_passes(self) -> None:
        result = self.run_validator(SMOKE_PACK)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_status_projection_authority_key_fails(self) -> None:
        pack_root = self.make_pack()
        projection_path = pack_root / "status.projection.json"
        projection = self.read_json(projection_path)
        projection["allowed_next_step_refs"] = ["transition.review-to-review"]
        self.write_json(projection_path, projection)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("forbidden authority key `allowed_next_step_refs`", result.stderr)

    def test_rules_contract_missing_effect_fails(self) -> None:
        pack_root = self.make_pack()
        rules_path = pack_root / "rules.contract.json"
        rules = self.read_json(rules_path)
        rules["rules"][0].pop("effect")
        self.write_json(rules_path, rules)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rules[1] missing required key `effect`", result.stderr)

    def test_workflow_contract_missing_checks_fails_schema(self) -> None:
        pack_root = self.make_pack()
        workflow_path = pack_root / "workflow.contract.json"
        workflow = self.read_json(workflow_path)
        workflow.pop("checks", None)
        self.write_json(workflow_path, workflow)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workflow.contract.json: schema violation", result.stderr)
        self.assertIn("'checks' is a required property", result.stderr)

    def test_object_contract_missing_kind_fails_schema(self) -> None:
        pack_root = self.make_pack()
        object_path = pack_root / "objects" / "state.review.partial.json"
        object_contract = self.read_json(object_path)
        object_contract.pop("kind", None)
        self.write_json(object_path, object_contract)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("objects/state.review.partial.json: schema violation", result.stderr)
        self.assertIn("'kind' is a required property", result.stderr)

    def test_duplicate_event_id_fails(self) -> None:
        pack_root = self.make_pack()
        events_path = pack_root / "workflow.events.jsonl"
        events = self.read_events(events_path)
        duplicated = dict(events[0])
        duplicated["timestamp"] = "2026-04-03T09:05:00+08:00"
        events.append(duplicated)
        self.write_events(events_path, events)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate event_id `event.review.001`", result.stderr)

    def test_unknown_actor_id_fails(self) -> None:
        pack_root = self.make_pack()
        events_path = pack_root / "workflow.events.jsonl"
        events = self.read_events(events_path)
        events[0]["actor_id"] = "agent.unknown"
        self.write_events(events_path, events)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("actor_id `agent.unknown` not found", result.stderr)

    def test_unknown_agent_ref_fails(self) -> None:
        pack_root = self.make_pack()
        workflow_path = pack_root / "workflow.contract.json"
        workflow = self.read_json(workflow_path)
        workflow["agent_refs"] = ["agent.unknown"]
        self.write_json(workflow_path, workflow)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("workflow.agent_refs: missing target `agent.unknown`", result.stderr)

    def test_node_transition_id_collision_fails(self) -> None:
        pack_root = self.make_pack()
        workflow_path = pack_root / "workflow.contract.json"
        workflow = self.read_json(workflow_path)
        workflow["transitions"][0]["transition_id"] = "node.review"
        self.write_json(workflow_path, workflow)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("node_ids and transition_ids must not overlap", result.stderr)

    def test_event_subject_ref_must_stay_on_node_or_transition(self) -> None:
        pack_root = self.make_pack()
        events_path = pack_root / "workflow.events.jsonl"
        events = self.read_events(events_path)
        events[0]["subject_ref"] = "evidence.review.note"
        self.write_events(events_path, events)

        result = self.run_validator(pack_root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("subject_ref `evidence.review.note` not found in node/transition ids", result.stderr)

    def test_legacy_schemas_directory_warns_but_passes(self) -> None:
        pack_root = self.make_pack()
        (pack_root / "objects").rename(pack_root / "schemas")

        result = self.run_validator(pack_root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("object contracts loaded from legacy schemas/ directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
