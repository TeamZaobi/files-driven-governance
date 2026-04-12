# ai-native e2e replay harness starter

这是一份独立的 AI-Native E2E replay / harness starter 骨架。
它的目标不是承载业务 workflow，而是把回放、断言和报告的最小目录形状固定下来，方便下游项目从一开始就把 `cases / fixtures / reports` 分开管理。

这个 starter 和 `minimal-files-engine` 是并列关系，不是嵌回去的附属结构。
为了兼容当前 `contract tranche v1` 的 validator，这里继续复用 `workflow_contract_path` 字段来承接 `harness.contract.json`，并继续使用现有 `primary_gate` 枚举；这只是兼容面复用，不表示把 replay starter 误写成业务 workflow。

## 目录职责

- `cases/`：存放回放用例定义，描述输入、初始状态、预期断言与回放边界。
- `fixtures/`：存放回放输入和基准材料，例如对话转写、workspace 快照、golden 数据和最小上下文。
- `reports/`：存放执行产物，例如断言报告、diff、运行元数据和失败摘要。
- `governance/`：存放 starter 自身的注册、路由与拓扑约束。

## 读法

先读 `BOUNDARY.md`，再读 `governance/scaffold.manifest.json`、`governance/files.registry.json`、`governance/intent.routes.json`，最后看 `cases/`、`fixtures/`、`reports/` 的说明页。

## 非目标

- 不在这里放业务 workflow runtime。
- 不在这里复用 `minimal-files-engine` 的 objects / status / workflow 运行态。
- 不在这一层引入执行脚本或自动化 runner。
