# Files-Driven Governance `v0.2.2`

发布日期：`2026-03-24`

## 本次补丁做了什么

`v0.2.2` 解决了两个具体遗漏：

1. 把 `OpenClaw` 从“项目类型示例”提升为显式多工具入口，补进 adapter guidance、共享规则和检索语境。
2. 把“理解置信度 -> 主动澄清提问”升为前置诊断规则，避免 skill 在项目基本情况未对齐时过早冻结治理蓝图。

## 主要变化

1. 更新 [`SKILL.md`](../SKILL.md)
   - 明确 `OpenClaw` 与 `Claude Code / Codex / AntiGravity` 一样，应默认视为 tool adapter 或 launcher，而不是 canonical role
   - 在锁定诊断前加入理解置信度判断与澄清提问规则

2. 新增 [`references/understanding-confidence-and-clarification.md`](../references/understanding-confidence-and-clarification.md)
   - 定义 `high / medium / low` 三档理解置信度
   - 规定何时应先向用户提问，何时可以带假设继续推进

3. 更新多工具参考件
   - [`references/tool-adapter-matrix.md`](../references/tool-adapter-matrix.md)
   - [`references/official-retrieval-orders.md`](../references/official-retrieval-orders.md)
   - [`references/cross-layer-sharing-contract.md`](../references/cross-layer-sharing-contract.md)

4. 更新输出与说明文档
   - [`references/output-contract.md`](../references/output-contract.md)
   - [`references/core-doctrine.md`](../references/core-doctrine.md)
   - [`README.md`](../README.md)
   - [`docs/MANUAL.md`](./MANUAL.md)
   - [`docs/REPO_METADATA.md`](./REPO_METADATA.md)
   - [`agents/openai.yaml`](../agents/openai.yaml)

## 为什么这次补丁重要

在多工具项目里，`OpenClaw` 经常会成为真实的一线工作入口。如果 skill 只抽象地说“多工具”，但不显式覆盖 `OpenClaw`，就容易在适配设计里漏掉关键 entry surface。

同时，如果 skill 在项目边界、canonical source、工具入口或目标治理强度还不清楚时直接输出蓝图，建议很容易跑偏。把“理解置信度”写成正式规则后，skill 会更倾向于先提少量高杠杆问题，提高对齐质量。

## 适用场景

这次补丁尤其适合：

- `OpenClaw + 其他工具` 混合协作的项目
- 入口文件多、adapter surface 多、真源不清楚的仓库
- 用户目标还不够明确、需要先澄清再诊断的治理设计任务

## 推荐发布标题

`v0.2.2 - OpenClaw and alignment patch`
