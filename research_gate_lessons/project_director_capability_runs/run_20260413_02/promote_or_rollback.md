## Objective

- Decide whether the improved project-director capability graph in self-hosting `capability_scope` is ready for promotion, should continue under controlled pilot, or should roll back. Sources: `task_packets/promote_or_rollback.json`, user-established conclusions for this run.
- Keep this document as a decision artifact inside the governed chain, not as standalone activation authority. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `status.projection.json`.

## Promotion Decision

- Decision: do **not** promote the improved capability graph to capability truth in this run; continue a controlled pilot under runner-owned workflow control. Sources: `pilot_on_benchmarks.md`, `context/runtime_promotion.md`, `workflow.state.json`.
- Decision: do **not** roll back the design immediately, because the proposed control split matches the strongest positive benchmark direction. Sources: `context/benchmarks.md`, `design_control_upgrade.md`, `define_runtime_protocol.md`.

## Reasons

- The strongest benchmark anchor says the best recent adherence came from script-controlled execution, so the direction of change is supported. Sources: `context/benchmarks.md`.
- The diagnosed root failure is model-internal control in complex workflows; the upgraded design moves scope, route, gate, and runtime control to the external runner. Sources: user-established conclusions for this run, `observe_gaps.md`, `design_control_upgrade.md`.
- The runtime protocol already limits the worker to node-local output and keeps control files with the runner, which is the intended control split. Sources: `define_runtime_protocol.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- The latest pilot result is explicitly “fit to continue a controlled benchmark trial, but not yet fit for capability promotion.” Sources: `pilot_on_benchmarks.md`.
- Promotion conditions are still incomplete in this pack: `workflow.state.json` and `status.projection.json` both show `gate_state` = `partial`, and the promotion chain requires a completed trial result before activation. Sources: `workflow.state.json`, `status.projection.json`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- Self-hosting still carries active deformation risk if `capability_scope` is not enforced at run start, so the improvement is not yet safe to promote as stable capability truth. Sources: `map_capability_graph.md`, `design_control_upgrade.md`, `pilot_on_benchmarks.md`.

## Rollback Conditions

- Roll back to `node.define_runtime_protocol` if a benchmark run fails to keep control with the external runner and instead lets the worker influence route, gate, or runtime control files. Sources: `pilot_on_benchmarks.md`, `define_runtime_protocol.md`, `WORKFLOW.md`.
- Roll back to `node.define_runtime_protocol` if self-hosting `capability_scope` is not explicitly bound before graph or artifact classification. Sources: `map_capability_graph.md`, `design_control_upgrade.md`, `define_runtime_protocol.md`.
- Roll back to `node.define_runtime_protocol` if benchmark anchors, projections, or tool adapters are used as control authority rather than evidence or display surfaces. Sources: `observe_gaps.md`, `define_runtime_protocol.md`, `pilot_on_benchmarks.md`.
- Roll back if promotion is requested without a completed trial judgment that includes success criteria, failure signals, and a declared rollback path. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `pilot_on_benchmarks.md`.

## Next Actions

- Run the next benchmark pass under the runner-owned protocol and verify that the worker writes only the node deliverable while the runner maintains runtime control artifacts. Sources: `pilot_on_benchmarks.md`, `define_runtime_protocol.md`, `BOUNDARY.md`.
- Enforce explicit `self-hosting` + `capability_scope` binding at invocation time, before any capability-graph reasoning. Sources: `design_control_upgrade.md`, `define_runtime_protocol.md`, `context/project_governance_model.md`.
- Collect a post-upgrade benchmark verdict that compares actual adherence under the new control split, then re-open promotion only with that evidence. Sources: `pilot_on_benchmarks.md`, `context/runtime_promotion.md`.
- If the next pilot fails any rollback condition, send the chain back to `node.define_runtime_protocol`; if it passes, return to promotion review with completed trial evidence. Sources: `define_runtime_protocol.md`, `pilot_on_benchmarks.md`, `workflow.contract.json`.
