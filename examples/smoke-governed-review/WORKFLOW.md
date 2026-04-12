# Workflow

This pack models a governed review workflow.

Canonical control rule:

- `workflow.contract.json` is the control truth
- `workflow.state.json` and `workflow.events.jsonl` are execution instances
- `status.projection.json` is a derived summary only

Current gate state:

- `partial`

Current constraint:

- review can continue to gather evidence within the current node
- write and publish remain blocked by `workflow.contract.json` + `rules.contract.json` until required evidence is complete
- `status.projection.json` may summarize missing evidence and forbidden outputs, but it does not declare downstream authority
