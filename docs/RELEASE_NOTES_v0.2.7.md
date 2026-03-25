# Files-Driven Governance `v0.2.7`

发布日期：`2026-03-25`

## 本次补丁做了什么

`v0.2.7` 把“继续开发”“开始审计”“反思”“推进”这类自然语言短口令，提升成了一个可移植的 intent-trigger contract。

这次补丁解决的问题是：

- 许多项目希望操作者少说废话，直接用短口令推动开发、审计、反思和推进
- 这些词如果只存在于聊天习惯或工具启动 prompt 里，语义很容易随工具、人员或上下文漂移
- 只加同义词会提高表面易用性，但不会让系统真正知道该读哪些状态、启用哪个 Agent、走哪条 workflow

## 主要变化

1. 新增 [`references/intent-trigger-contract.md`](../references/intent-trigger-contract.md)
   - 规定 `canonical intent + alias layer + modifier layer`
   - 区分 `direct_action_intent` 与 `route_intent`
   - 规定口令触发后的读取顺序、workflow 绑定、Agent 选择、歧义规则和状态回写

2. 更新 [`SKILL.md`](../SKILL.md)
   - 要求在项目需要口令驱动操作时，显式设计意图触发与执行契约
   - 要求把口令易用性扩展留在 alias 和 modifier 层，而不是偷偷扩展语义

3. 更新 [`references/output-contract.md`](../references/output-contract.md) 与 [`references/scenario-playbooks.md`](../references/scenario-playbooks.md)
   - 为治理蓝图增加 `意图触发与执行契约` 条件区块
   - 把 trigger contract 接入既有仓库、绿地项目和 recovery 场景

4. 更新 [`README.md`](../README.md)、[`docs/MANUAL.md`](./MANUAL.md)、[`docs/REPO_METADATA.md`](./REPO_METADATA.md)、[`agents/openai.yaml`](../agents/openai.yaml) 和 [`CHANGELOG.md`](../CHANGELOG.md)
   - 同步版本定位、默认 prompt 和对外发布文案

## 为什么这次补丁重要

如果项目真的想做到“我只说一句继续开发，系统就能自己接着干”，关键不是词表更长，而是下面这些 contract 是否存在：

1. 这个词到底映射到哪个 canonical intent
2. 默认先读哪里
3. 状态不全时怎么办
4. 该走哪条 workflow
5. 该启用哪个 Agent
6. 做完后必须回写什么

没有这些 contract，所谓“自然口令”只是更隐蔽的猜测。

这次补丁的核心是：

1. 把短口令从 prompt 习惯提升成治理对象
2. 用少量稳定 intent 承载大量自然说法
3. 让这套能力可以跨工具、跨 handoff、跨项目复用

## 推荐发布标题

`v0.2.7 - Portable intent-trigger contract`
