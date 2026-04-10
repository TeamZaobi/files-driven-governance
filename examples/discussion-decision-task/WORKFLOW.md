# Workflow

This pack models the discussion promotion path.

Canonical control truth:

- `workflow.contract.json` is the control truth
- `workflow.state.json` and `workflow.events.jsonl` are execution instances
- `status.projection.json` is a derived summary only

Current route:

`discussion -> issue_ledger -> decision_package -> task_or_decision`

Current state:

- `gate_state`: `ready`
- `current_node_id`: `node.task_or_decision`
- required evidence has already been collected for the chain
- this projection does not authorize any new write or publish action

Human entry:

- `active-discussions.md` is the reading entry, not the control truth
