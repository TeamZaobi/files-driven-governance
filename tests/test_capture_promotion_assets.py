import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "references" / "运行观察与能力晋升.md"
EXAMPLE_ROOT = ROOT / "examples" / "capture-candidate-activation"
VALIDATOR = ROOT / "scripts" / "validate_governance_assets.py"
README = ROOT / "README.md"
MANUAL = ROOT / "docs" / "使用手册.md"
SKILL = ROOT / "SKILL.md"
OUTPUT_CONVENTION = ROOT / "references" / "输出约定.md"
PLAN = ROOT / "docs" / "当前阶段补完计划.md"


class CapturePromotionAssetsTests(unittest.TestCase):
    def make_pack_copy(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        pack_root = Path(temp_dir.name) / "pack"
        shutil.copytree(EXAMPLE_ROOT, pack_root)
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

    def read_events(self, path: Path) -> list[dict]:
        events = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
        return events

    def test_reference_answers_core_questions(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("只记运行观察", text)
        self.assertIn("做证据包", text)
        self.assertIn("召回历史", text)
        self.assertIn("拆成项目出口与能力候选", text)
        self.assertIn("进入待试验", text)
        self.assertIn("允许激活或回退", text)
        self.assertIn("不热改能力真源", text)
        self.assertIn("展示页不能冒充正式激活", text)

    def test_example_contains_main_path_files(self) -> None:
        expected = {
            "README.md",
            "BOUNDARY.md",
            "WORKFLOW.md",
            "active-observations.md",
            "evidence_package.md",
            "recall_note.md",
            "split_decision.md",
            "candidate_trial.md",
            "activation_decision.md",
            "workflow.contract.json",
            "workflow.state.json",
            "workflow.events.jsonl",
            "status.projection.json",
            "rules.contract.json",
            "agent.contract.json",
        }
        actual = {path.name for path in EXAMPLE_ROOT.iterdir() if path.is_file()}
        self.assertTrue(expected.issubset(actual))
        self.assertTrue((EXAMPLE_ROOT / "objects").is_dir())

    def test_workflow_contract_and_stage_pages_surface_key_fields(self) -> None:
        workflow = self.read_json(EXAMPLE_ROOT / "workflow.contract.json")
        state = self.read_json(EXAMPLE_ROOT / "workflow.state.json")
        projection = self.read_json(EXAMPLE_ROOT / "status.projection.json")
        workflow_md = (EXAMPLE_ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        trial = (EXAMPLE_ROOT / "candidate_trial.md").read_text(encoding="utf-8")
        activation = (EXAMPLE_ROOT / "activation_decision.md").read_text(encoding="utf-8")

        self.assertEqual(workflow["workflow_id"], "workflow.capture.candidate.activation")
        self.assertEqual(workflow["entry_intents"][0]["entry_node"], "node.capture_evidence")
        self.assertEqual(
            [node["node_id"] for node in workflow["nodes"]],
            [
                "node.capture_evidence",
                "node.recall_history",
                "node.split_target",
                "node.candidate_trial",
                "node.activation_or_rollback",
            ],
        )
        self.assertEqual(
            [transition["transition_id"] for transition in workflow["transitions"]],
            [
                "transition.capture-evidence-to-recall-history",
                "transition.recall-history-to-split-target",
                "transition.split-target-to-candidate-trial",
                "transition.candidate-trial-to-activation-or-rollback",
            ],
        )
        self.assertIn(
            "capture_evidence -> recall_history -> split_target -> candidate_trial -> activation_or_rollback",
            workflow_md,
        )
        self.assertEqual(state["current_node_id"], "node.activation_or_rollback")
        self.assertEqual(projection["family"], "status_projection")
        self.assertIn("failure_signals", trial)
        self.assertIn("rollback_path", trial)
        self.assertIn("展示页", activation)
        self.assertIn("正式激活真源", activation)

    def test_object_contracts_and_event_chain_are_present(self) -> None:
        objects = {
            "state.capture.evidence.json",
            "action.capture.evidence.json",
            "evidence.capture.evidence.json",
            "state.recall.note.json",
            "action.recall.note.json",
            "evidence.recall.note.json",
            "state.split.decision.json",
            "action.split.decision.json",
            "evidence.split.decision.json",
            "state.candidate.trial.json",
            "action.candidate.trial.json",
            "evidence.candidate.trial.json",
            "state.activation.decision.json",
            "action.activation.decision.json",
            "evidence.activation.decision.json",
            "approval.capture.candidate.activation.json",
        }
        actual_objects = {path.name for path in (EXAMPLE_ROOT / "objects").iterdir() if path.is_file()}
        self.assertTrue(objects.issubset(actual_objects))

        capture_state = self.read_json(EXAMPLE_ROOT / "objects" / "state.candidate.trial.json")
        activation_state = self.read_json(EXAMPLE_ROOT / "objects" / "state.activation.decision.json")
        self.assertEqual(capture_state["fields"][1]["field_id"], "trial_status")
        self.assertEqual(activation_state["fields"][1]["field_id"], "decision_kind")

        events = self.read_events(EXAMPLE_ROOT / "workflow.events.jsonl")
        self.assertEqual(events[-1]["state_after"]["current_node_id"], "node.activation_or_rollback")
        self.assertEqual(events[-1]["state_after"]["gate_state"], "ready")
        self.assertEqual(events[-1]["subject_ref"], "transition.candidate-trial-to-activation-or-rollback")

    def test_example_pack_passes_validator(self) -> None:
        result = self.run_validator(EXAMPLE_ROOT)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_entry_docs_and_plan_point_to_official_path(self) -> None:
        readme = README.read_text(encoding="utf-8")
        manual = MANUAL.read_text(encoding="utf-8")
        skill = SKILL.read_text(encoding="utf-8")
        output = OUTPUT_CONVENTION.read_text(encoding="utf-8")
        plan = PLAN.read_text(encoding="utf-8")

        for text in (readme, manual, skill, output):
            self.assertIn("运行观察与能力晋升", text)
            self.assertIn("capture-candidate-activation", text)

        self.assertIn("runtime -> candidate -> capability", plan)
        self.assertIn("starter / manage 接入", plan)
        self.assertIn("validator / audit 加深", plan)
        self.assertIn("不接受什么", plan)


if __name__ == "__main__":
    unittest.main()
