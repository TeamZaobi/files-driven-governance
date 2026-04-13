## Objective

- Validate whether the upgraded project-director capability graph and runtime protocol are ready for benchmark trial in self-hosting `capability_scope`, with control kept by the external runner rather than model-internal reasoning. Sources: `task_packets/pilot_on_benchmarks.json`, `context/benchmarks.md`, `design_control_upgrade.md`, `define_runtime_protocol.md`.
- Keep this node in the pilot/evidence lane: use benchmark anchors and observed failure patterns to judge trial readiness, but do not treat this artifact as promotion authority. Sources: `context/benchmarks.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `WORKFLOW.md`, `BOUNDARY.md`.

## Benchmark Matrix

| Check focus | Benchmark basis | Expected signal in this pack | Current pilot read |
| --- | --- | --- | --- |
| Externalized control | Anchor `019d859b-41f3-7752-bc49-ca9282c784ca` is the strongest positive sample, and it showed best adherence under script-controlled execution. Sources: `context/benchmarks.md`. | Route, gate, and runtime control stay with the runner; the worker writes only the node deliverable. Sources: `WORKFLOW.md`, `define_runtime_protocol.md`. | Ready: the upgraded design matches the benchmark direction. Sources: `design_control_upgrade.md`, `define_runtime_protocol.md`. |
| Self-hosting scope binding | Failure mode FM-2 says self-hosting work deforms when `capability_scope` is not declared early. Sources: `observe_gaps.md`, `context/project_governance_model.md`, `context/skill.md`. | Pilot must stay in self-hosting `capability_scope`, not default `project_scope`. Sources: `map_capability_graph.md`, `design_control_upgrade.md`. | Ready in design; still needs enforcement in each benchmark run. Sources: `design_control_upgrade.md`, `define_runtime_protocol.md`. |
| Authority boundary | Failure modes FM-3 and FM-5 show drift when projections, benchmark anchors, or adapters act like control truth. Sources: `observe_gaps.md`, `context/tool_adapter_matrix.md`, `WORKFLOW.md`, `BOUNDARY.md`. | Benchmark anchors stay in evidence only; projections and adapters do not authorize route, gate, or activation. Sources: `context/benchmarks.md`, `WORKFLOW.md`, `define_runtime_protocol.md`. | Ready: the protocol states explicit stop checks against hidden authority surfaces. Sources: `define_runtime_protocol.md`. |
| Trial discipline | Capability promotion requires success criteria, failure signals, and rollback before activation. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`. | Pilot result must remain a trial judgment, with rollback to `node.define_runtime_protocol` if the benchmark pilot fails. Sources: `workflow.contract.json`, `define_runtime_protocol.md`. | Partial: rollback path exists, but this pack does not yet contain a post-upgrade benchmark verdict. Sources: `workflow.contract.json`, `status.projection.json`, `design_control_upgrade.md`. |

## Pilot Result

- Pilot conclusion: the pack is fit to continue a controlled benchmark trial, but not yet fit for capability promotion. Sources: `context/benchmarks.md`, `design_control_upgrade.md`, `define_runtime_protocol.md`, `context/runtime_promotion.md`, `status.projection.json`.
- Positive signal: the proposed control split directly matches the strongest benchmark sample by moving control from model-internal reasoning to the runner and keeping worker output node-local. Sources: `context/benchmarks.md`, `WORKFLOW.md`, `design_control_upgrade.md`, `define_runtime_protocol.md`.
- Open condition: the current workflow state for `node.pilot_on_benchmarks` is still `partial`, and the run pack does not contain a completed post-upgrade benchmark comparison beyond the positive anchor and diagnosed failure modes. Sources: `workflow.state.json`, `status.projection.json`, `observe_gaps.md`, `context/benchmarks.md`.
- Operational decision: proceed to benchmark evaluation only if the run keeps scope binding, evidence-only benchmark usage, and rollback readiness explicit; otherwise stop and roll back to `node.define_runtime_protocol`. Sources: `define_runtime_protocol.md`, `workflow.contract.json`, `context/runtime_promotion.md`.

## Residual Risks

- Complex workflows may still show low adherence if the runner contract is present on paper but not enforced during invocation. Sources: user-established conclusions for this run, `context/benchmarks.md`, `design_control_upgrade.md`.
- Self-hosting scope drift remains possible if a benchmark run falls back to default `project_scope` framing instead of declared `capability_scope`. Sources: `context/project_governance_model.md`, `map_capability_graph.md`, `design_control_upgrade.md`.
- Hidden authority drift remains possible if a projection page, benchmark anchor, or tool wrapper is used to justify advancement outside the runner-owned gate chain. Sources: `observe_gaps.md`, `context/tool_adapter_matrix.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- Assumption: one strong positive anchor plus documented failure patterns is enough to justify a pilot, but not enough to claim stable cross-case improvement; the pack does not include additional raw benchmark transcripts or a quantified adherence delta. Basis: `context/benchmarks.md`, `observe_gaps.md`, `status.projection.json`.

## Follow-up Checks

- Re-run the benchmark under the runner-owned protocol and confirm the worker only writes `pilot_on_benchmarks.md` while runtime control stays in runner-managed files. Sources: `WORKFLOW.md`, `BOUNDARY.md`, `define_runtime_protocol.md`.
- Verify the benchmark run begins with explicit self-hosting `capability_scope` binding before any graph or artifact classification. Sources: `context/project_governance_model.md`, `map_capability_graph.md`, `design_control_upgrade.md`.
- Verify the pilot records success criteria, failure signals, and rollback path before any promotion-facing decision. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- If the pilot fails, roll back to `node.define_runtime_protocol`; if the pilot passes, carry the evidence into `node.promote_or_rollback` without treating this document as activation authority. Sources: `workflow.contract.json`, `define_runtime_protocol.md`, `BOUNDARY.md`.
