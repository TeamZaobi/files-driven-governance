## Objective

- Upgrade the self-hosting project-director capability graph so complex-workflow adherence no longer depends on model-internal control; the new baseline is runner-owned workflow control, node-local Codex output, and explicit approval checkpoints for promotion decisions. Sources: `task_packets/design_control_upgrade.json`, `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- Keep this document at the design layer only; it does not authorize activation, promotion, or truth-source edits. Sources: `WORKFLOW.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.

## Control Reallocation

| Control area | New owner | Operational rule |
| --- | --- | --- |
| Scope binding | Runner | Require `self-hosting` and `capability_scope` to be declared before any graph step, because the default four-part split is for `project_scope`, not capability self-improvement. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md`. |
| Route and gate | Runner | Keep `workflow.contract.json` as control truth, `workflow.state.json` and `workflow.events.jsonl` as runner-owned execution state, and `status.projection.json` as derived only. Sources: `WORKFLOW.md`, `context/repo_readme.md`, `context/capture_candidate_workflow.md`. |
| Node write surface | Codex CLI worker | Limit the worker to the current node deliverable and do not grant write authority over control files, contracts, or objects. Sources: `task_packets/design_control_upgrade.json`, `WORKFLOW.md`, `BOUNDARY.md`. |
| Evidence and display surfaces | Runner-governed evidence lane | Treat benchmark anchors, projections, and tool adapters as evidence/display inputs only, never as route, gate, or activation authority. Sources: `context/benchmarks.md`, `context/tool_adapter_matrix.md`, `WORKFLOW.md`, `BOUNDARY.md`, `map_capability_graph.md`. |
| Promotion decision | Explicit approval checkpoint outside the model | Only open activation or rollback after evidence exists and the candidate declares success criteria, failure signals, and rollback path. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `BOUNDARY.md`. |

## Runtime Governor Duties

- The runtime governor should be the external runner/script surface that already owns runtime control files in this pack. Sources: `WORKFLOW.md`, `BOUNDARY.md`, `README.md`.
- Enforce preflight scope binding, current-node identity, allowed context set, and single-deliverable write scope before invoking the worker. Sources: `task_packets/design_control_upgrade.json`, `context/project_governance_model.md`, `context/skill.md`.
- Refuse downstream advance when gate state is blocked or when required evidence is missing, because projections are summaries and cannot authorize progression. Sources: `BOUNDARY.md`, `context/capture_candidate_workflow.md`, `context/repo_readme.md`.
- Record route, transition, and status changes in runner-owned runtime files instead of inferring them from prose artifacts. Sources: `WORKFLOW.md`, `context/repo_readme.md`.
- Preserve the hard chain `runtime -> evidence/candidate -> trial -> capability` and block any direct `runtime -> capability` write path. Sources: `context/project_governance_model.md`, `context/runtime_promotion.md`, `map_capability_graph.md`.
- On promotion-facing nodes, require explicit stop/go approval material rather than letting the worker text act as activation authority. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `BOUNDARY.md`.

## LLM Boundary

- The LLM may read the task packet, listed context, and prior node artifacts, then produce the current node deliverable. Sources: `task_packets/design_control_upgrade.json`, `WORKFLOW.md`.
- The LLM must not own route selection, gate changes, approval decisions, activation, or capability-truth mutation. Sources: `task_packets/design_control_upgrade.json`, `WORKFLOW.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- The LLM must not reinterpret benchmark anchors, `status.projection.json`, or tool wrappers as control truth. Sources: `context/benchmarks.md`, `context/tool_adapter_matrix.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- In self-hosting work, the LLM must reason in `capability_scope` asset types such as taxonomy, reading order, upgrade rules, schema, validator, and template, instead of reusing the default `project_scope` four-part split unchanged. Sources: `context/project_governance_model.md`, `map_capability_graph.md`.
- Assumption: keeping the LLM inside node-local drafting and analysis will improve adherence further once the graph is upgraded; the pack proves externalized control is better than prompt-only control, but it does not yet contain post-upgrade pilot results. Basis: `context/benchmarks.md`, `README.md`.

## Risks If Not Adopted

- Complex workflows in Mobius-like conditions will likely keep low adherence when control stays inside the model. Sources: user-established conclusions for this run, `context/benchmarks.md`, `observe_gaps.md`.
- Self-hosting runs will keep mixing capability assets, project facts, and runtime artifacts unless scope binding is enforced first. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md`, `observe_gaps.md`.
- Runtime observations or summaries can be mistaken for promoted capability changes, collapsing the required trial and rollback chain. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `observe_gaps.md`.
- Derived projections, benchmark anchors, or tool adapters can become hidden control authorities, recreating control drift outside the runner. Sources: `context/tool_adapter_matrix.md`, `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`, `map_capability_graph.md`.
- Promotion outcomes will stay discussion-heavy instead of auditable, because success criteria, failure signals, and rollback will not be enforced at a distinct checkpoint. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `BOUNDARY.md`.
