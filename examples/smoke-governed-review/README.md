# smoke-governed-review

This is a minimal smoke asset pack for `files-driven` governed workflow validation.

It demonstrates:

1. `BOUNDARY.md` as the explanation-layer boundary anchor for scenarios, stories, tests, non-goals, quality references, and acceptance ownership
2. `route / evidence / write / stop` gate coverage
3. agent-level participation through `agent_refs`, plus approval coverage through `approver_ref` and `approval_ref`
4. canonical `gate_state` usage with a valid `partial` state
5. a derived `status_projection` that does not introduce new release authority
6. `objects/*.json` as the project-level home for object contracts, distinct from repository schema drafts

The pack is intentionally small so it can be used as a validator smoke test and as a reference shape for future project packs.

Run the validator against this directory as the `pack_root`, not against the repository root.
