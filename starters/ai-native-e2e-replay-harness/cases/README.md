# cases

这里存放 replay case 定义。

## 期望内容

- 输入对话或输入事件。
- 初始工作区状态或最小上下文。
- 预期断言，例如 route、read set、write set、boundary、projection、recovery、trajectory。
- 回放边界和失败条件。

## 当前合同锚点

- `schemas/ai-native-e2e.case.schema.json`
- `schemas/ai-native-e2e.adapter-contract.schema.json`

## 命名建议

- `*.case.json`：适合机器可读的 case 定义。
- `*.case.md`：适合先做人工说明，再逐步收敛成机器合同。

## 不放什么

- 不放运行产物。
- 不放 fixture 原始数据。
- 不把 case 目录当成报告目录。
