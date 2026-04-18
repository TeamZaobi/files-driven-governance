## Objective

- Map the current project-director capability graph for self-hosting `capability_scope`, separating stable capability from runner/runtime control. Sources: `task_packets/map_capability_graph.json`, `context/project_governance_model.md`, `README.md`.
- Keep this artifact diagnostic only; it does not authorize activation, promotion, or truth-source edits. Sources: `WORKFLOW.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.

## Current Graph

| Cluster | What is explicit now | What still lives outside model capability | Sources |
| --- | --- | --- | --- |
| Governance core | `files-driven` is defined as the project director, speaking from `capability_scope` and governing work that normally lives in `project_scope`. | In self-hosting, this must be re-declared explicitly before reuse; otherwise the default `project_scope` framing can deform the analysis. | `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md` |
| Scope and routing | The model already has a scope-first router: first identify `capability_scope / project_scope / runtime_scope`, then decide action and boundary. | The rule is present, but enforcement in this run is carried by the controlled workflow and node packets rather than by a promoted capability asset. | `context/project_governance_model.md`, `context/skill.md`, `WORKFLOW.md`, `README.md` |
| Structure model | The graph already contains stable classification assets: `truth_source / execution_object / status_projection / display_projection`, plus the project-side four-part split. | The four-part split is default only for `project_scope`; self-hosting capability work still needs an explicit remap into capability assets such as taxonomy, reading order, upgrade rules, schema, validator, and template. | `context/project_governance_model.md`, `context/repo_readme.md` |
| Control spine | Control truth is explicit: `workflow.contract.json` is authoritative; the runner owns `workflow.state.json` and `workflow.events.jsonl`; `status.projection.json` is derived only; Codex writes only the current deliverable. | Route, gate, and write authority are intentionally outside the model and therefore are not yet part of the model's own reusable capability graph inside this pack. | `WORKFLOW.md`, `workflow.contract.json`, `task_packets/map_capability_graph.json`, `context/benchmarks.md` |
| Promotion spine | The upgrade path is explicit as `runtime -> candidate -> capability`, and activation requires success criteria, failure signals, and rollback. | This run is still in diagnostic/mapping stages; promotion logic is defined as a rule, but not yet instantiated as a completed capability upgrade. | `context/project_governance_model.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `README.md` |
| Tool surface | Tool adapters may expose truth, provide entry commands, and run checks. | Adapters, benchmark anchors, and projections are not allowed to become control authorities; this remains an active boundary to defend. | `context/tool_adapter_matrix.md`, `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md` |

## Strengths

- The governance worldview is already strong and explicit: role, work object, scope order, and anti-deformation rules are all defined in the canonical model. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md`.
- This run pack already proves a cleaner control split than prompt-only control: the benchmark says script-controlled execution produced the best recent adherence, and the workflow keeps authority with the runner. Sources: `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`.
- The graph already includes a disciplined promotion theory: runtime observations do not hot-edit capability truth, and activation requires predeclared evaluation and rollback conditions. Sources: `context/project_governance_model.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- Adapter boundaries are already stated clearly enough to prevent most obvious authority drift: tools may enter, summarize, and execute checks, but must not rewrite rules, object structure, or workflow semantics. Sources: `context/tool_adapter_matrix.md`.

## Capability Gaps

- The self-hosting entry condition is a rule, but not yet a first-class graph node: the docs require explicit `self-hosting` and `capability_scope`, yet the current improvement graph begins with diagnosis rather than a dedicated scope-binding handshake. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `workflow.contract.json`, `README.md`.
- Externalized workflow control is currently implemented as run-specific control artifacts and task packets; in this pack it is not yet promoted as a reusable capability-scope asset of the project director itself. Sources: `README.md`, `WORKFLOW.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- The graph does not yet show per-capability trial criteria: success criteria, failure signals, and rollback are mandatory for activation, but those details are still deferred to later nodes in the path. Sources: `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`, `workflow.contract.json`, `README.md`.
- Hidden-authority surfaces remain the main drift risk: projection pages, benchmark anchors, and tool wrappers are explicitly non-authoritative, which means the capability graph still needs stronger negative boundaries around them. Sources: `context/tool_adapter_matrix.md`, `context/benchmarks.md`, `WORKFLOW.md`, `BOUNDARY.md`, `observe_gaps.md`.
- Assumption: the low adherence seen in Mobius is mainly a control-graph problem rather than a content-quality problem. The task framing and benchmark direction support this hypothesis, but the pack does not include raw Mobius incident traces. Basis: `task_packets/observe_gaps.json`, `context/benchmarks.md`, `observe_gaps.md`.

## Boundary Corrections

- Make `self-hosting declared` and `scope = capability_scope` the mandatory first node of the graph before any four-part classification or gap analysis. Sources: `context/project_governance_model.md`, `context/repo_readme.md`, `context/skill.md`.
- Split the graph into four explicit authority zones: `capability truth`, `runner-controlled workflow`, `runtime evidence/candidates`, and `tool/display adapters`. Sources: `context/project_governance_model.md`, `WORKFLOW.md`, `context/tool_adapter_matrix.md`, `context/capture_candidate_workflow.md`.
- Add a hard no-bypass edge: `runtime observation -> evidence/candidate -> trial -> capability`, with no direct `runtime -> capability` write path. Sources: `context/project_governance_model.md`, `context/runtime_promotion.md`, `context/capture_candidate_workflow.md`.
- Mark `status.projection.json`, benchmark anchors, and adapter entrypoints as evidence/display surfaces only, never as route, gate, or activation authorities. Sources: `WORKFLOW.md`, `context/benchmarks.md`, `context/tool_adapter_matrix.md`, `BOUNDARY.md`.
- When mapping self-hosting capability work, use capability-scope asset types (`taxonomy`, `reading order`, `upgrade rules`, `schema`, `validator`, `template`) instead of applying the default `project_scope` four-part split unchanged. Sources: `context/project_governance_model.md`.
