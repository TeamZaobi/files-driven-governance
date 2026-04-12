# discussion

- `object_id`: `DISC-EXAMPLE-20260410-001`
- `status`: `active`
- `topic`: `把一个有争议的协作问题收口为稳定、可晋升的主路径`
- `scope`: `只收主路径，不扩到质询分支和 process projection`
- `related_truth_sources`:
  - `references/讨论收口与晋升.md`
- `required_roles`:
  - `maintainer`
  - `reviewer`
- `issue_ledger`: [issue_ledger.md](issue_ledger.md)
- `promotion_target`: `decision_package -> task_or_decision`
- `closure_authority`: `project-maintainer`
- `next_action`: `先压 decision_package，再决定进入 task 还是 decision`

## Summary

把 discussion 从聊天层提升成正式未决对象，并把出口收窄到可执行落点。

## Known Facts

1. 当前争议还没有窄到可以直接下 `decision`。
2. 当前内容已经不适合继续留在聊天记录里。
3. 当前最合适的下一步是先压 `issue_ledger` 和 `decision_package`。

## Open Issues

1. 哪些问题还只是边界不清，不能直接进入执行。
2. 哪些问题已经足够稳定，可以交给 `decision_package`。
3. 最终落点应该是 `task`、`decision`，还是继续保留 discussion。

## Role Inputs

### Maintainer

当前要先证明这件事不该继续停在聊天里，并且已经有了受控出口。

### Reviewer

如果 discussion 还不能回答“下一步去哪”，就还不算完成收口。

## Promotion Judgment

当前 discussion 已具备晋升条件：

1. 主要问题已经可以登记成 `issue_ledger`
2. 需要一个压缩后的裁定面
3. 后续落点已经收窄到 `task_or_decision`
