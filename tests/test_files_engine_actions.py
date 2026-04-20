import json
import os
import shutil
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
RUNTIME_EXAMPLE = ROOT / "examples" / "capture-candidate-activation"


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

    def init_git_repo(self, root: Path) -> None:
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=root, check=True, capture_output=True, text=True)
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        if branch and branch != "main":
            subprocess.run(["git", "branch", "-m", "main"], cwd=root, check=True, capture_output=True, text=True)

    def read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def bootstrap(self, project_id: str = "demo-project") -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        target = Path(temp_dir.name) / "starter"
        result = self.run_cmd(str(BOOTSTRAP), str(target), "--project-id", project_id)
        self.assertEqual(result.returncode, 0, result.stderr)
        return target

    def make_self_hosting_fixture(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        target = Path(temp_dir.name) / "capability-repo"
        (target / "docs").mkdir(parents=True)
        (target / "agents").mkdir(parents=True)

        (target / "README.md").write_text(
            "# files-driven fixture\n\n"
            "入口回到 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。\n"
            "README 只做入口、执行导览、迭代边界或合同说明，不与这份真源平行定义本体。\n"
            "先明确当前对象到底是 capability_scope、repo.files-driven 还是某个下游项目实例；在 self-hosting 场景下也不例外。\n",
            encoding="utf-8",
        )
        (target / "docs" / "项目治理能力模型.md").write_text(
            "# 模型\n\n唯一的底层真源。\n",
            encoding="utf-8",
        )
        (target / "SKILL.md").write_text(
            "# files-driven\n\n"
            "底层能力模型回到 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。\n"
            "`SKILL.md` 只负责执行导览，不与真源平行定义本体。\n"
            "当前要显式区分 capability_scope、project_scope 和 self-hosting。\n",
            encoding="utf-8",
        )
        (target / "agents" / "openai.yaml").write_text(
            "interface:\n"
            '  display_name: "files-driven"\n'
            "  default_prompt: >-\n"
            "    先判断 capability_scope、project_scope 和 self-hosting；不要把 metadata 自己写成压缩版本体。\n",
            encoding="utf-8",
        )
        return target

    def make_self_hosting_adoption_fixture(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        target = Path(temp_dir.name) / "capability-repo"
        (target / "docs").mkdir(parents=True)
        (target / "agents").mkdir(parents=True)

        (target / "README.md").write_text(
            "# files-driven fixture\n\n"
            "先读 [docs/非工程背景起步.md](docs/非工程背景起步.md)。\n"
            "默认动作是 install / register / repair / audit。\n"
            "宿主名先行时回 [docs/宿主化知识工作场景矩阵.md](docs/宿主化知识工作场景矩阵.md)。\n",
            encoding="utf-8",
        )
        (target / "SKILL.md").write_text(
            "# files-driven\n\n"
            "目标读者几乎没有软件工程基础时，先降到低带宽解释。\n"
            "先把 `Obsidian / Notion / Docs / Sheets / Slides` 视为宿主名。\n"
            "先判断用户是在问治理问题还是工具操作问题。\n",
            encoding="utf-8",
        )
        (target / "agents" / "openai.yaml").write_text(
            "interface:\n"
            '  display_name: "files-driven"\n'
            "  default_prompt: >-\n"
            "    先回哪份文件算数 / 今天先做哪一步 / 哪些先别改；再判断 `Obsidian / Notion / Docs / Sheets / Slides` 是治理问题还是工具操作问题。\n",
            encoding="utf-8",
        )
        (target / "docs" / "非工程背景起步.md").write_text(
            "# 起步\n\n"
            "先记住哪份文件算数、今天先做什么、哪些文件先别改。\n"
            "如果听到 audit，先把它理解成基础体检。\n",
            encoding="utf-8",
        )
        (target / "docs" / "宿主化知识工作场景矩阵.md").write_text(
            "# 宿主矩阵\n\n"
            "先区分治理问题和工具操作问题。\n",
            encoding="utf-8",
        )
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

    def test_pack_layer_uses_governance_validator(self) -> None:
        target = self.bootstrap()
        status_projection_path = target / "status.projection.json"
        status_projection = self.read_json(status_projection_path)
        status_projection["allowed_next_step_refs"] = []
        status_projection_path.write_text(
            json.dumps(status_projection, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "pack",
            "--format",
            "json",
        )
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["layer"], "pack")
        self.assertEqual(payload["status"], "invalid")
        self.assertTrue(any(item["category"] == "status_projection" for item in payload["findings"]))

    def test_runtime_layer_is_not_applicable_for_plain_starter(self) -> None:
        target = self.bootstrap()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "runtime",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "not_applicable")
        self.assertEqual(payload["layer"], "runtime")
        self.assertTrue(payload["implemented"])
        self.assertGreaterEqual(len(payload["next_refs"]), 1)

    def test_runtime_layer_validates_official_runtime_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "runtime-pack"
            shutil.copytree(RUNTIME_EXAMPLE, target)

            result = self.run_cmd(
                str(MANAGE),
                "audit",
                str(target),
                "--layer",
                "runtime",
                "--format",
                "json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "valid")
            self.assertEqual(payload["layer"], "runtime")
            self.assertTrue(payload["implemented"])

            candidate_trial_path = target / "candidate_trial.md"
            candidate_trial = candidate_trial_path.read_text(encoding="utf-8").replace("failure_signals", "trial_failures")
            candidate_trial_path.write_text(candidate_trial, encoding="utf-8")

            invalid = self.run_cmd(
                str(MANAGE),
                "audit",
                str(target),
                "--layer",
                "runtime",
                "--format",
                "json",
            )
            self.assertNotEqual(invalid.returncode, 0)
            invalid_payload = json.loads(invalid.stdout)
            self.assertEqual(invalid_payload["status"], "invalid")
            self.assertTrue(any(item["category"] == "candidate_trial" for item in invalid_payload["findings"]))

    def test_runtime_layer_requires_recall_and_event_trace_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "runtime-pack"
            shutil.copytree(RUNTIME_EXAMPLE, target)

            recall_note_path = target / "recall_note.md"
            recall_note = recall_note_path.read_text(encoding="utf-8").replace("decision_memory", "decision_trace")
            recall_note_path.write_text(recall_note, encoding="utf-8")

            events_path = target / "workflow.events.jsonl"
            events_text = events_path.read_text(encoding="utf-8").replace('"reason_refs"', '"reason_trace_refs"', 1)
            events_path.write_text(events_text, encoding="utf-8")

            result = self.run_cmd(
                str(MANAGE),
                "audit",
                str(target),
                "--layer",
                "runtime",
                "--format",
                "json",
            )
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "invalid")
            categories = {item["category"] for item in payload["findings"]}
            self.assertIn("recall_note", categories)
            self.assertIn("workflow_events", categories)

    def test_runtime_layer_requires_traceable_event_chain_alignment(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "runtime-pack"
            shutil.copytree(RUNTIME_EXAMPLE, target)

            events_path = target / "workflow.events.jsonl"
            lines = events_path.read_text(encoding="utf-8").splitlines()
            mutated_lines = []
            for line in lines:
                if '"event_id":"event.capture.003"' in line:
                    line = line.replace('"reason_refs":["recall_note.md"]', '"reason_refs":["split_decision.md"]')
                mutated_lines.append(line)
            events_path.write_text("\n".join(mutated_lines) + "\n", encoding="utf-8")

            result = self.run_cmd(
                str(MANAGE),
                "audit",
                str(target),
                "--layer",
                "runtime",
                "--format",
                "json",
            )
            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "invalid")
            categories = {item["category"] for item in payload["findings"]}
            self.assertIn("workflow_events", categories)

    def test_governance_layer_validates_downstream_authority_boundaries(self) -> None:
        target = self.bootstrap()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["layer"], "governance")
        self.assertEqual(payload["profile"], "downstream_project_instance")
        self.assertTrue(payload["implemented"])

        hooks_readme_path = target / "tooling" / "hooks" / "README.md"
        hooks_readme = hooks_readme_path.read_text(encoding="utf-8")
        hooks_readme = hooks_readme.replace("不是 control truth", "是 control truth")
        hooks_readme = hooks_readme.replace("不是真源", "是真源")
        hooks_readme_path.write_text(hooks_readme, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        self.assertTrue(any(item["category"] == "authority_surface" for item in invalid_payload["findings"]))

    def test_governance_layer_warns_when_git_workspace_is_missing(self) -> None:
        target = self.bootstrap()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        categories = {item["category"] for item in payload.get("warnings", [])}
        self.assertIn("git_workspace", categories)

    def test_governance_layer_warns_on_dirty_stable_branch_without_upstream(self) -> None:
        target = self.bootstrap()
        self.init_git_repo(target)

        readme_path = target / "README.md"
        readme_path.write_text(readme_path.read_text(encoding="utf-8") + "\nDirty branch test.\n", encoding="utf-8")

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        categories = {item["category"] for item in payload.get("warnings", [])}
        self.assertIn("git_branch_strategy", categories)
        self.assertIn("git_tracking", categories)

    def test_governance_layer_validates_downstream_readme_scope_and_authority(self) -> None:
        target = self.bootstrap()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["profile"], "downstream_project_instance")
        self.assertTrue(payload["implemented"])

        readme_path = target / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8")
        readme_text = readme_text.replace("project_scope", "runtime_scope")
        readme_text = readme_text.replace("不与治理真源平行定义本体", "与治理真源平行定义本体")
        readme_path.write_text(readme_text, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        categories = {item["category"] for item in invalid_payload["findings"]}
        self.assertIn("scope_binding", categories)
        self.assertIn("authority_surface", categories)

    def test_governance_layer_validates_downstream_skill_scope_and_authority(self) -> None:
        target = self.bootstrap()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["profile"], "downstream_project_instance")
        self.assertTrue(payload["implemented"])

        skill_path = target / "skills" / "review-skill" / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8")
        skill_text = skill_text.replace("project_scope", "runtime_scope")
        skill_text = skill_text.replace("不与治理真源平行定义本体", "与治理真源平行定义本体")
        skill_path.write_text(skill_text, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        categories = {item["category"] for item in invalid_payload["findings"]}
        self.assertIn("scope_binding", categories)
        self.assertIn("authority_surface", categories)

    def test_governance_layer_validates_self_hosting_scope_binding(self) -> None:
        target = self.make_self_hosting_fixture()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["layer"], "governance")
        self.assertEqual(payload["profile"], "self_hosting_capability_repo")
        self.assertTrue(payload["implemented"])

        skill_path = target / "SKILL.md"
        skill_text = skill_path.read_text(encoding="utf-8").replace(" 和 self-hosting", "")
        skill_path.write_text(skill_text, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        self.assertTrue(any(item["category"] == "scope_binding" for item in invalid_payload["findings"]))

    def test_governance_layer_validates_self_hosting_readme_authority_denial(self) -> None:
        target = self.make_self_hosting_fixture()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["profile"], "self_hosting_capability_repo")
        self.assertTrue(payload["implemented"])

        readme_path = target / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8").replace("不与这份真源平行定义本体", "与这份真源平行定义本体")
        readme_path.write_text(readme_text, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        self.assertTrue(any(item["category"] == "authority_surface" for item in invalid_payload["findings"]))

    def test_governance_layer_validates_self_hosting_readme_scope_binding(self) -> None:
        target = self.make_self_hosting_fixture()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["profile"], "self_hosting_capability_repo")
        self.assertTrue(payload["implemented"])

        readme_path = target / "README.md"
        readme_text = readme_path.read_text(encoding="utf-8").replace("capability_scope", "runtime_scope")
        readme_path.write_text(readme_text, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "governance",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        self.assertTrue(any(item["category"] == "scope_binding" for item in invalid_payload["findings"]))

    def test_adoption_layer_is_not_applicable_for_downstream_starter(self) -> None:
        target = self.bootstrap()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "adoption",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "not_applicable")
        self.assertEqual(payload["layer"], "adoption")
        self.assertTrue(payload["implemented"])
        self.assertGreaterEqual(len(payload["next_refs"]), 1)

    def test_adoption_layer_validates_self_hosting_entrypoints(self) -> None:
        target = self.make_self_hosting_adoption_fixture()

        result = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "adoption",
            "--format",
            "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "valid")
        self.assertEqual(payload["profile"], "self_hosting_capability_repo")
        self.assertTrue(payload["implemented"])

        beginner_path = target / "docs" / "非工程背景起步.md"
        beginner_text = beginner_path.read_text(encoding="utf-8").replace("哪些文件先别改", "哪些文件以后再说")
        beginner_path.write_text(beginner_text, encoding="utf-8")

        invalid = self.run_cmd(
            str(MANAGE),
            "audit",
            str(target),
            "--layer",
            "adoption",
            "--format",
            "json",
        )
        self.assertNotEqual(invalid.returncode, 0)
        invalid_payload = json.loads(invalid.stdout)
        self.assertEqual(invalid_payload["status"], "invalid")
        self.assertTrue(any(item["category"] == "beginner_guide" for item in invalid_payload["findings"]))

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
