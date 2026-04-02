# smoke-governed-review

This is a minimal smoke asset pack for `files-driven` governed workflow validation.

It demonstrates:

1. `route / evidence / write / stop` gate coverage
2. approval coverage through `approver_ref` plus `approval_ref`
3. canonical `gate_state` usage with a valid `partial` state
4. a derived `status_projection` that does not introduce new release authority

The pack is intentionally small so it can be used as a validator smoke test and as a reference shape for future project packs.
