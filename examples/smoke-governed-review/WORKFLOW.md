# Workflow

This pack models a governed review workflow.

Canonical control rule:

- `workflow.contract.json` is the control truth
- `workflow.state.json` and `workflow.events.jsonl` are execution instances
- `status.projection.json` is a derived summary only

Current gate state:

- `partial`

Current constraint:

- review can continue to gather evidence
- write and publish remain blocked
