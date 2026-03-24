# v0.2.1 Release Notes

发布日期：`2026-03-24`

## 这次补丁修了什么

`v0.2.1` 不是新的方向升级，而是把 `v0.2.0` 里遗漏的一层补齐：  
把 `policy_or_rules / object / workflow / skill / agent` 这五类核心对象的检索与工具适配正式写成 contract。

## 新增内容

1. 新增 [`references/family-locator-contract.md`](../references/family-locator-contract.md)
   - 规定五类核心对象各自的 canonical source、current-version anchor、fallback retrieval order 和 adapter surface
2. 新增 [`references/official-retrieval-orders.md`](../references/official-retrieval-orders.md)
   - 固定五类核心对象的官方读取顺序
3. 新增 [`references/tool-adapter-matrix.md`](../references/tool-adapter-matrix.md)
   - 明确各 family 在多工具环境中的 canonical source 与 adapter surface 边界

## 主要改动

1. [SKILL.md](../SKILL.md)
   - 新增 family locator / official retrieval order / tool adapter 设计要求
2. [`references/output-contract.md`](../references/output-contract.md)
   - 新增必答区块 `对象家族检索与适配策略`
3. [README.md](../README.md)
   - 当前版本改为 `v0.2.1`
   - 补入补丁重点和新发布说明入口
4. [MANUAL.md](./MANUAL.md)
   - 补入五类核心对象的检索公理与多工具适配要求
5. [CHANGELOG.md](../CHANGELOG.md)
   - 记录本次补丁内容

## 这版解决的核心问题

在 `v0.2.0` 之前，skill 已经能判断：

- 结构怎么分
- 流程怎么选
- Agent 和 Skill 怎么区分

但还缺：

- 五类核心对象怎么稳定找到
- 当前版本锚点怎么固定
- 多工具环境里哪些只是 adapter，哪些才是 canonical source

`v0.2.1` 就是专门补这层。

## 推荐发布标题

`v0.2.1 - Retrieval and adapter patch`

## 推荐一句话摘要

`v0.2.1` adds official retrieval rules and tool-adapter contracts for the five core project-governance families.
