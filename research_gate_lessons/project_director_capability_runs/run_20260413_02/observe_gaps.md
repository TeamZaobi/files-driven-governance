## Objective

- Record the control-related gaps behind low complex-workflow adherence and establish the baseline for improving the project-director capability graph in self-hosting `capability_scope`. Sources: `task_packets/observe_gaps.json`, `context/benchmarks.md`, user-established conclusion for this run.
- Keep this node at the observation layer: collect evidence and failure modes, but do not hot-edit capability truth or treat this document as activation authority. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `WORKFLOW.md`.
- Use the repository governance model as canonical source and the benchmark anchor `019d859b-41f3-7752-bc49-ca9282c784ca` as external evidence, not as control truth. Sources: `task_packets/observe_gaps.json`, `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`.

## Evidence Inventory

| Evidence | Direct signal | Operational implication |
| --- | --- | --- |
| `task_packets/observe_gaps.json` | The node goal is to collect concrete failure modes behind low complex-workflow adherence, using the repo as canonical source and benchmark anchors as external evidence. | This node should diagnose gaps, not redesign the whole system yet. |
| `context/benchmarks.md` | The benchmark anchor is the strongest positive sample; script-controlled execution produced the best workflow adherence; control should move from model-internal reasoning to the external runner. | The primary control hypothesis is externalized control, not better prompting alone. |
| `WORKFLOW.md` | This pack is script-controlled; the runner writes runtime control files; Codex CLI only writes the current node deliverable; benchmark anchors are evidence only. | Route, gate, and authority must stay outside the model. |
| `BOUNDARY.md` | The run exists to replace free discussion with a controlled run and verify whether script-controlled execution improves adherence. TC-1 and TC-3 define failure as artifacts or workers replacing workflow control. | The current pack treats control drift itself as the problem to solve. |
| `workflow.contract.json` + `README.md` | The official path starts at `node.observe_gaps` and is explicitly framed as “externalize workflow control” / “improve project director capability graph”. | The improvement target is a governed capability-improvement chain, not an ad hoc prompt tweak. |
| `workflow.state.json` + `status.projection.json` | The run is currently `blocked` at `node.observe_gaps` until evidence exists; the projection explicitly says it does not authorize promotion. | Gate state is intended to be binding and projection pages are not authority. |
| `context/project_governance_model.md` + `context/skill.md` + `context/repo_readme.md` | Self-hosting must explicitly declare scope; `project_scope` four-part defaults do not automatically apply to `capability_scope`; runtime must not overwrite capability truth. | A major risk is scope confusion during self-improvement. |
| `context/runtime_promotion.md` + `context/capture_candidate_workflow.md` | Current-round observations should stay in runtime/evidence/candidate layers; activation requires success criteria, failure signals, and rollback. | Observations must not be mistaken for promoted capability changes. |
| `context/tool_adapter_matrix.md` | Tool adapters may expose or execute truth, but must not rewrite rules, workflow semantics, or object structure. | Multi-tool entry points can amplify drift if they become hidden control authorities. |

## Failure Modes

- **FM-1: Control remains inside the model.** When route, gate, or write decisions are left to model-internal reasoning, adherence drops; the benchmark explicitly points to external runner control as the best recent result. Sources: `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- **FM-2: Self-hosting scope is not declared early enough.** When the run improves `files-driven` itself without first pinning `self-hosting` and `capability_scope`, capability assets, project facts, and runtime artifacts can be mixed. Sources: `context/project_governance_model.md`, `context/skill.md`, `context/repo_readme.md`.
- **FM-3: Runtime observations are treated as capability truth.** If current-round observations, summaries, or candidate notes are allowed to act like final capability updates, the controlled `runtime -> candidate -> capability` chain collapses. Sources: `context/project_governance_model.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- **FM-4: Gate outputs are advisory instead of binding.** The canonical docs explicitly call out the recurring failure where a state is already `blocked` / `partial` but downstream modification or advancement still happens. Sources: `context/repo_readme.md`, `context/skill.md`, `workflow.state.json`, `status.projection.json`.
- **FM-5: Projections, benchmarks, or adapters masquerade as authority.** If derived pages, benchmark conclusions, or tool wrappers start acting like control truth, the system silently rewrites governance semantics outside the runner-owned chain. Sources: `WORKFLOW.md`, `BOUNDARY.md`, `status.projection.json`, `context/tool_adapter_matrix.md`.
- **Assumption — FM-6: Mobius likely exhibits one or more of FM-1 to FM-5 rather than a content-only quality issue.** This pack provides benchmark and governance evidence for the control hypothesis, but it does not include raw Mobius incident logs inside the run pack. Basis: `task_packets/observe_gaps.json`, `context/benchmarks.md`, `BOUNDARY.md`.

## Baseline Claims

- The control baseline for the next node is **runner-owned workflow control with node-local worker writes**, not stronger prompt wording. Sources: `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- The improvement target for this run is **the project-director capability graph under self-hosting `capability_scope`**. Sources: user-established conclusion for this run, `workflow.contract.json`, `README.md`, `context/project_governance_model.md`.
- The current node should produce **diagnostic evidence only**; it does not authorize promotion, activation, or truth-source edits. Sources: `task_packets/observe_gaps.json`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `status.projection.json`.
- Any later upgrade path must preserve **explicit scope declaration, evidence gates, success criteria, failure signals, and rollback path** before activation. Sources: `context/project_governance_model.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
