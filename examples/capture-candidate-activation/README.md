# capture-candidate-activation

This is the official first-pass example pack for the self-iterating capability chain.

Canonical path only:

1. `active-observations.md` as the entry page
2. `evidence_package.md`
3. `recall_note.md`
4. `split_decision.md`
5. `candidate_trial.md`
6. `activation_decision.md`

Canonical control truth:

- `workflow.contract.json` is the control truth
- `workflow.state.json` and `workflow.events.jsonl` are execution instances
- `status.projection.json` is derived read-only summary only

Main route:

`capture_evidence -> recall_history -> split_target -> candidate_trial -> activation_or_rollback`

This pack demonstrates how runtime observation becomes a candidate, how history is recalled before splitting, and how activation stays gated by trial conditions and rollback paths.
