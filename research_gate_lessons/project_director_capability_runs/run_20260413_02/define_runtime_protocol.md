## Objective

- Define the minimal runtime protocol for `node.define_runtime_protocol` so self-hosting improvement stays in `capability_scope`, keeps control with the external runner, and preserves the controlled `runtime -> candidate -> capability` chain. Sources: `task_packets/define_runtime_protocol.json`, `context/benchmarks.md`, `context/project_governance_model.md`, `WORKFLOW.md`.
- Keep this node operational and local: the worker produces `define_runtime_protocol.md` only and does not mutate workflow control files, contracts, or `objects/`. Sources: `task_packets/define_runtime_protocol.json`, `WORKFLOW.md`, `BOUNDARY.md`.

## Node Contract

- Run creation precondition: start inside a governed pack with the minimal controlled chain `BOUNDARY.md -> workflow.contract.json -> objects/*.json -> rules.contract.json + agent.contract.json -> workflow.state.json / workflow.events.jsonl -> status.projection.json(optional)`. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md`.
- Workflow binding: `node.define_runtime_protocol` is bound to `state.define_runtime_protocol`, `action.define_runtime_protocol`, `evidence.define_runtime_protocol`, policy `policy.capability.improvement.control`, and approver `role.governance_owner`. Sources: `workflow.contract.json`, `objects/state.define_runtime_protocol.json`, `objects/action.define_runtime_protocol.json`, `objects/evidence.define_runtime_protocol.json`, `agent.contract.json`.
- Current run state: the runner has `current_node_id` set to `node.define_runtime_protocol`, `gate_state` set to `partial`, and `evidence.define_runtime_protocol` is still missing. Sources: `workflow.state.json`, `status.projection.json`.
- Authority split: the runner owns runtime control files, while Codex CLI writes only the current node deliverable. Sources: `WORKFLOW.md`, `BOUNDARY.md`, `design_control_upgrade.md`.

## Task Packet

- The packet shape used here is already minimal and sufficient: `workflow_id`, `node_id`, `title`, `goal`, `deliverable_path`, `required_sections`, `context_paths`, `previous_artifacts`, `benchmark_anchors`, and `control_constraints`. Source: `task_packets/define_runtime_protocol.json`.
- The worker input contract is: read the task packet first, then the listed context files, then prior node artifacts; write only the requested deliverable. Sources: `task_packets/define_runtime_protocol.json`, `codex_runs/define_runtime_protocol/prompt.md`.
- The packet should keep benchmark anchors in the evidence lane only; anchor `019d859b-41f3-7752-bc49-ca9282c784ca` does not become control truth. Sources: `task_packets/define_runtime_protocol.json`, `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- The packet must carry explicit write prohibitions so the runner can enforce node-local output and protect contracts, runtime files, and `objects/`. Sources: `task_packets/define_runtime_protocol.json`, `WORKFLOW.md`, `BOUNDARY.md`.

## CLI Surface

- The proven invocation surface in this pack is `codex exec --full-auto -c model_reasoning_effort="high" --skip-git-repo-check --color never --json -C <run_pack> --output-last-message <codex_runs/.../last_message.md> -`, with the node prompt sent on stdin. Sources: `codex_runs/observe_gaps/command.json`, `codex_runs/map_capability_graph/command.json`, `codex_runs/design_control_upgrade/command.json`.
- Assumption: `node.define_runtime_protocol` should reuse the same `codex exec` envelope as the earlier nodes, because this node already has a matching prompt contract with `TASK_PACKET_PATH` and `DELIVERABLE_PATH`. Basis: `codex_runs/define_runtime_protocol/prompt.md`, `codex_runs/observe_gaps/command.json`, `codex_runs/map_capability_graph/command.json`, `codex_runs/design_control_upgrade/command.json`.
- The runner should set the working directory to the run pack and preserve `codex_runs/<node>/` traces as execution evidence; the worker-facing write surface remains the single deliverable file. Sources: `codex_runs/observe_gaps/command.json`, `codex_runs/map_capability_graph/command.json`, `codex_runs/design_control_upgrade/command.json`, `BOUNDARY.md`, `WORKFLOW.md`.

## Gate Checks

- Route check: only invoke this worker when `workflow.state.json.current_node_id` is `node.define_runtime_protocol`, and keep route changes on the runner side under the contract transition `node.design_control_upgrade -> node.define_runtime_protocol`. Sources: `workflow.contract.json`, `workflow.state.json`, `WORKFLOW.md`.
- Evidence check: prior evidence for `observe_gaps`, `map_capability_graph`, and `design_control_upgrade` must remain present, and this node completes only when `evidence.define_runtime_protocol` can point to `define_runtime_protocol.md`. Sources: `workflow.state.json`, `rules.contract.json`, `objects/evidence.define_runtime_protocol.json`.
- Write check: allow writes only to `define_runtime_protocol.md`; block edits to `workflow.contract.json`, `workflow.state.json`, `workflow.events.jsonl`, `status.projection.json`, `rules.contract.json`, `agent.contract.json`, and anything under `objects/`. Sources: `task_packets/define_runtime_protocol.json`, `WORKFLOW.md`, `BOUNDARY.md`.
- Stop check: halt if self-hosting `capability_scope` is not treated as the active frame, if required sections are missing, or if projections, benchmark anchors, or tool adapters are being used as control authority. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md`, `context/tool_adapter_matrix.md`, `observe_gaps.md`, `design_control_upgrade.md`, `status.projection.json`.

## Recovery Model

- Recovery truth stays in runner-written `workflow.state.json` and `workflow.events.jsonl`; `status.projection.json` is useful for restoring context but cannot authorize progression. Sources: `WORKFLOW.md`, `context/project_governance_model.md`, `context/repo_readme.md`, `context/capture_candidate_workflow.md`, `status.projection.json`.
- If this node run fails before evidence capture, rerun the same node from the packet/context set and regenerate only `define_runtime_protocol.md`; do not hot-edit capability truth during the round. Sources: `task_packets/define_runtime_protocol.json`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `WORKFLOW.md`.
- If the node output is rejected at the next gate, the contract rollback target is `node.design_control_upgrade`; if a later benchmark pilot fails, the contract rolls back to `node.define_runtime_protocol`. Sources: `workflow.contract.json`.
- Promotion remains outside this node: any later activation must still pass a candidate trial with declared success criteria, failure signals, and rollback path. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `design_control_upgrade.md`.
