# fixtures

这里存放 replay 的输入材料和基准材料。

## 期望内容

- 对话转写。
- workspace 快照。
- golden 数据。
- 回放需要的最小上下文。
- replay artifact、run metadata 和 adapter contract 的样例或基线。

## 当前合同锚点

- `schemas/ai-native-e2e.replay-artifact.schema.json`
- `schemas/ai-native-e2e.run-metadata.schema.json`
- `schemas/ai-native-e2e.adapter-contract.schema.json`

## 命名建议

- `transcripts/`：对话或事件转写。
- `snapshots/`：工作区或现场快照。
- `goldens/`：基准输出和稳定参考。

## 不放什么

- 不放 case 级断言说明。
- 不放生成后的 report。
- 不把 fixture 目录当成手工维护的真源目录。
