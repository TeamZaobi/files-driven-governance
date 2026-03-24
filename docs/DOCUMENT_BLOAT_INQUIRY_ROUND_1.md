# Document Bloat Inquiry Round 1

日期：`2026-03-24`

主题：`files-driven` 是否需要把“文档生命周期与压缩治理”升成显式机制

## Claim

当前 skill 已经有分层、恢复链、projection demotion 和 minimum output shaping，但还缺少一份显式的“文档生命周期与压缩策略”。
如果不补这一层，项目运行过程中出现的文档膨胀只能靠临场判断，缺少稳定的触发器和收口动作。

## Hostile Questions

### `Q1`

问题：
这是不是又在给 skill 增加一份参考件，反而让 skill 自己更膨胀？

答辩：
如果只是再加一份泛化说明，确实会加重包装层。
但这里补的是缺失的治理闭环：它定义的是何时 `split / compact / demote / archive`，并且直接约束 active surface，而不是再加一个泛泛概念层。

状态：`resolved`

### `Q2`

问题：
文档压缩会不会导致历史信息丢失，反而让回溯更困难？

答辩：
方案不是“删历史”，而是“把历史降级为 `history` 或 `archive`，并保持 trusted reentry path”。
压缩对象优先是 overloaded projection 和 active notes，而不是 canonical facts。

状态：`resolved`

### `Q3`

问题：
是不是每个项目都要上完整的 lifecycle policy，反而过度设计？

答辩：
不是。它被设计成条件展开机制，只有在 active docs 膨胀、retrieval cost 上升、stale pages 积累时才激活。
对早期小项目，只需要一条简单规则：“status 保持短、历史按需读、过期页降级为 history”。

状态：`resolved`

### `Q4`

问题：
现有的 `low_token_recovery_chain` 和 `mechanism_review` 不是已经够了吗？

答辩：
还不够。它们说明“怎么恢复”和“出了机制问题怎么办”，但没有回答“什么时候该把一个活动文档从 active 降级为 history/projection”。
生命周期策略补的是中间这层。

状态：`resolved`

### `Q5`

问题：
如果项目成员对“当前页是否该归档”意见不一致，怎么收敛？

答辩：
这里不需要对每个低风险页面都跑重型敌意质询。
只有当压缩动作会改变 canonical source、恢复链或 public surface 时，才进入正式 `adversarial_inquiry -> defense -> convergence`。
普通页面可由 lifecycle review owner 按既定规则执行。

状态：`accepted`
接受风险：
不同项目对归档阈值仍会有差异，需要在具体 repo 里做一次本地化收口。

## Reflection

这轮质询说明两点：

1. 文档膨胀治理本身是必要的，但必须作为“条件触发机制”存在，不能再变成新的默认重流程。
2. 真正需要被压缩的通常不是 canonical source，而是过长的 status、README、discussion、重复摘要和仍被误当成当前页的旧页面。

## Convergence

本轮收敛结论：

1. 将“文档生命周期与压缩策略”补入 skill 是合理的。
2. 它应以条件展开区块和条件 flow 的形式存在，而不是默认强制展开。
3. 推荐 flow 形状为：
   `growth_signal -> lifecycle_review -> compact_or_archive -> trusted_reentry`
4. 推荐优先压缩：
   - `status_projection`
   - overloaded `README`
   - overloaded `discussion`
   - stale projections pretending to be current

## Closure Authority

当前轮次闭合级别：`provisional convergence`

closure_authority：
`repo maintainer pending final acceptance`
