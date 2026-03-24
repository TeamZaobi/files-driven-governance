# Files-Driven Governance `v0.2.4`

发布日期：`2026-03-24`

## 本次补丁做了什么

`v0.2.4` 把“文档膨胀管理”从隐含机制提升成显式治理能力。

这次补丁解决的问题是：

- 项目运行一段时间后，active docs 越来越长
- status 和 README 开始混入历史叙事
- stale page 看起来仍然像 current truth
- recovery cost 和检索成本不断升高

## 主要变化

1. 新增 [`references/document-lifecycle-and-compaction.md`](../references/document-lifecycle-and-compaction.md)
   - 定义 `active / stable_reference / projection / history / archive`
   - 定义 `split / compact / demote / archive / index_only`
   - 定义何时触发生命周期 review

2. 更新 [`references/classic-governance-flows.md`](../references/classic-governance-flows.md)
   - 新增条件流程：
     `growth_signal -> lifecycle_review -> compact_or_archive -> trusted_reentry`

3. 更新 [`references/output-contract.md`](../references/output-contract.md)
   - 新增条件区块：
     `文档生命周期与压缩策略`

4. 更新 [`references/scenario-playbooks.md`](../references/scenario-playbooks.md)
   - 把文档膨胀纳入 existing repo / recovery 场景的显式处理项

5. 新增 [`docs/DOCUMENT_BLOAT_INQUIRY_ROUND_1.md`](./DOCUMENT_BLOAT_INQUIRY_ROUND_1.md)
   - 启动本主题的一轮正式 `质询 -> 反思 -> 收敛`

## 为什么这次补丁重要

没有文档生命周期规则时，团队通常会：

- 保留所有历史页为 active
- 让 status/README 吸纳越来越多解释
- 继续追加文档，而不降级 stale projection

结果不是“信息更全”，而是“当前态更难找、误判更常见、恢复更贵”。

这次补丁的核心是：

1. 不删历史，但要降级历史
2. 不压缩 canonical facts，先压缩 derivative surfaces
3. 让 repo 在膨胀时有明确的 compaction trigger 和 trusted reentry path

## 推荐发布标题

`v0.2.4 - Document lifecycle and compaction`
