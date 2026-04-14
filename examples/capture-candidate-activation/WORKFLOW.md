# Workflow

This pack models the self-iterating capability chain.

Canonical control truth:

- `workflow.contract.json` is the control truth
- `workflow.state.json` and `workflow.events.jsonl` are execution instances
- `status.projection.json` is a derived summary only

Current route:

`capture_evidence -> recall_history -> split_target -> candidate_trial -> activation_or_rollback`

Current state:

- `gate_state`: `ready`
- `current_node_id`: `node.activation_or_rollback`
- required evidence has already been collected for the chain
- this projection does not authorize any new write, publish, or activation action

Human entry:

- `active-observations.md` is the reading entry, not the control truth

Hard constraints:

- current round does not hot-edit capability truth
- `activation_decision.md` is a display landing page, not a formal activation authority
- candidate trial must declare success criteria, failure signals, and rollback path before activation is allowed
