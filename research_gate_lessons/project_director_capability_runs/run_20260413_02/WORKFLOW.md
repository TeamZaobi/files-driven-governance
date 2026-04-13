# Workflow

This pack uses a script-controlled, Codex-assisted workflow.

Control truth:
- `workflow.contract.json` is the control truth
- `workflow.state.json` and `workflow.events.jsonl` are execution instances
- `status.projection.json` is derived only

Current route:
`observe_gaps -> map_capability_graph -> design_control_upgrade -> define_runtime_protocol -> pilot_on_benchmarks -> promote_or_rollback`

Control rules:
- the runner writes runtime control files
- Codex CLI only writes the current node deliverable
- benchmark anchors are evidence, not control authority
