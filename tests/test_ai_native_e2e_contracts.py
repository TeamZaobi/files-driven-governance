import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "ai_native_e2e"

SCHEMA_FILES = {
    "case": SCHEMA_DIR / "ai-native-e2e.case.schema.json",
    "replay_artifact": SCHEMA_DIR / "ai-native-e2e.replay-artifact.schema.json",
    "assertion_report": SCHEMA_DIR / "ai-native-e2e.assertion-report.schema.json",
    "run_metadata": SCHEMA_DIR / "ai-native-e2e.run-metadata.schema.json",
    "adapter_contract": SCHEMA_DIR / "ai-native-e2e.adapter-contract.schema.json",
}

FIXTURE_FILES = {
    "case": FIXTURE_DIR / "case.conversation_replay.json",
    "replay_artifact": FIXTURE_DIR / "replay_artifact.conversation_replay.json",
    "assertion_report": FIXTURE_DIR / "assertion_report.conversation_replay.json",
    "run_metadata": FIXTURE_DIR / "run_metadata.conversation_replay.json",
    "adapter_contract": FIXTURE_DIR / "adapter_contract.unittest.json",
    "adapter_contract_live": FIXTURE_DIR / "adapter_contract.kimicc_glm.json",
    "adapter_contract_mock": FIXTURE_DIR / "adapter_contract.mock_cli.json",
}


class AINativeE2EContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            name: json.loads(path.read_text(encoding="utf-8"))
            for name, path in SCHEMA_FILES.items()
        }
        cls.fixtures = {
            name: json.loads(path.read_text(encoding="utf-8"))
            for name, path in FIXTURE_FILES.items()
        }
        cls.validators = {
            name: Draft202012Validator(schema, format_checker=FormatChecker())
            for name, schema in cls.schemas.items()
        }

    def test_schema_documents_are_valid_json_schema(self) -> None:
        for name, schema in self.schemas.items():
            with self.subTest(schema=name):
                try:
                    Draft202012Validator.check_schema(schema)
                except SchemaError as exc:  # pragma: no cover - defensive branch
                    self.fail(f"{name} schema is not a valid JSON Schema document: {exc}")

    def test_fixture_set_validates_against_declared_schemas(self) -> None:
        for name, validator in self.validators.items():
            with self.subTest(fixture=name):
                fixture_key = name
                if name == "adapter_contract":
                    validator.validate(self.fixtures[fixture_key])
                    validator.validate(self.fixtures["adapter_contract_live"])
                    validator.validate(self.fixtures["adapter_contract_mock"])
                    continue
                validator.validate(self.fixtures[fixture_key])

    def test_contract_chain_is_self_consistent(self) -> None:
        case = self.fixtures["case"]
        replay_artifact = self.fixtures["replay_artifact"]
        assertion_report = self.fixtures["assertion_report"]
        run_metadata = self.fixtures["run_metadata"]
        adapter = self.fixtures["adapter_contract"]

        self.assertEqual(case["adapter_ref"], adapter["adapter_id"])
        self.assertEqual(replay_artifact["case_ref"], case["case_id"])
        self.assertEqual(replay_artifact["adapter_ref"], adapter["adapter_id"])
        self.assertEqual(replay_artifact["run_ref"], run_metadata["run_id"])
        self.assertEqual(assertion_report["case_ref"], case["case_id"])
        self.assertEqual(assertion_report["replay_artifact_ref"], replay_artifact["replay_artifact_id"])
        self.assertEqual(assertion_report["run_ref"], run_metadata["run_id"])
        self.assertEqual(run_metadata["case_ref"], case["case_id"])
        self.assertEqual(run_metadata["adapter_ref"], adapter["adapter_id"])

        self.assertEqual(
            set(case["expected_assertions"].keys()),
            {
                "route_assertions",
                "read_assertions",
                "write_assertions",
                "boundary_assertions",
                "projection_assertions",
                "recovery_assertions",
                "trajectory_assertions",
            },
        )
        self.assertEqual(
            {item["category"] for item in assertion_report["assertions"]},
            {"route", "read", "write", "boundary", "projection", "recovery", "trajectory"},
        )
        self.assertEqual(
            {item["status"] for item in assertion_report["assertions"]},
            {"pass"},
        )

    def test_case_requires_all_assertion_buckets(self) -> None:
        broken = deepcopy(self.fixtures["case"])
        broken["expected_assertions"].pop("route_assertions")

        with self.assertRaises(ValidationError):
            self.validators["case"].validate(broken)


if __name__ == "__main__":
    unittest.main()
