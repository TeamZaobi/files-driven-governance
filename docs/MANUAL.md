# Files-Driven Governance 完整说明书

## 1. 项目简介

`files-driven` 是一个“项目结构治理技能”，不是单纯的文件命名或目录规划工具。

它的目标是帮助团队把项目中的这些结构对象用文档显式治理起来：

- 规则与政策
- 对象模型
- 工作流
- 技能包
- 角色契约
- 执行对象
- 状态投影
- 展示投影

适用对象包括：

- 多 Agent 协作研发项目
- OpenClaw 类 AI 驱动项目
- 使用 `Spec + Kanban` 或类似流程的团队
- 同时使用 `Claude Code / Codex / AntiGravity` 等多个开发工具的团队

## 2. 解决的问题

这个技能主要解决以下问题：

1. `README`、状态页、任务卡、rules、agents、skills 等文件互相漂移。
2. 多工具并行使用时，工具入口被误当成 canonical source。
3. 项目里没有明确区分“规则”“流程”“角色”“方法”“状态摘要”。
4. 多人/多 Agent 协作时，不清楚谁能读、谁能写、谁能审批、谁只能投影。
5. 想借鉴 Spec-Driven、Kanban、敏捷等方法，但不想把项目搞成过重流程。

## 3. 底层方法论

### 3.1 系统论

系统论负责回答：

- 这个项目有哪些结构层次？
- 哪些 family 是慢变量，哪些是快变量？
- 哪些对象应该独立成 family？
- 哪些角色或工具共享同一组事实？

在本技能中，系统论主要用于：

- 设计 source family
- 设计 ownership
- 设计边界与耦合
- 决定目录优化的前置条件

### 3.2 信息论

信息论负责回答：

- 一个重要事实从哪里产生？
- 哪些文件在复制、投影或摘要它？
- 恢复上下文的最小路径是什么？
- 哪些页面“看起来权威”，但其实不是 canonical source？

在本技能中，信息论主要用于：

- source-of-truth 设计
- 引用链设计
- current-version locator 设计
- cross-layer sharing contract 设计

### 3.3 控制论

控制论负责回答：

- 谁观测当前状态？
- 谁做决策？
- 谁执行？
- 谁评审？
- 谁授权回滚或重分类？

在本技能中，控制论主要用于：

- 角色控制回路
- gate 设计
- review / rollback 路径
- change-control 强度设计

## 4. 核心结构模型

### 4.1 Source Family

本技能优先把项目划分为这些 family：

1. `policy_or_rules`
2. `object`
3. `workflow`
4. `skill`
5. `agent`
6. `execution_object`
7. `status_projection`
8. `display_projection`

这一步优先于目录规划。

### 4.2 四层文档视角

在 source family 之外，本技能还要求把文档系统按这四层观察：

1. `truth_source`
2. `execution_object`
3. `status_projection`
4. `display_projection`

这四层帮助团队判断：

- 哪些文件定义事实
- 哪些文件承载过程
- 哪些文件只负责低 token 接手
- 哪些文件只是对外投影

## 5. 诊断框架

本技能默认做七维诊断：

1. 项目阶段
2. 变更风险
3. 协作密度
4. Agent 自主度
5. 恢复压力
6. 协作拓扑
7. 工具异构度

### 5.1 协作拓扑

协作拓扑关注：

- 有多少人参与？
- 有多少 Agent 参与？
- 是否有人机混合审批？
- 是否存在平台团队、业务团队、审计团队等多层角色？

### 5.2 工具异构度

工具异构度关注：

- 是否同时用 `Claude Code / Codex / AntiGravity`
- 是否依赖 MCP、CLI、脚本、云端代理
- 是否工具之间共享一套规则与技能
- 是否把工具入口误写成 canonical role

## 6. 跨层共享矩阵

本技能要求为重要 family 设计共享矩阵，至少包含：

1. `producer`
2. `consumer`
3. `writable surface`
4. `projection surface`
5. `visibility scope`
6. `sync trigger`
7. `conflict rule`
8. `handoff packet`

### 6.1 示例理解

比如一个 `workflow` family：

- `producer`：流程治理负责人
- `consumer`：执行 Agent、状态层、展示层
- `writable surface`：canonical workflow 文档
- `projection surface`：README、状态页、网站展示页
- `visibility scope`：project / public
- `sync trigger`：流程 gate 变化、状态转换、回滚
- `conflict rule`：canonical source wins
- `handoff packet`：当前目标、当前版本、阻塞点、下一步动作

## 7. 角色控制回路

本技能要求至少描述一个显式回路：

1. `observe`
2. `decide`
3. `act`
4. `review`
5. `rollback_or_improve`

如果项目是多人/多 Agent 协作，建议把这些责任映射到角色，而不是只写工具名。

常见角色模式：

- `Spec Owner`
- `Agent Steward`
- `Quality Gate Owner`

这些是责任模式，不是必须照抄的标题。

## 8. 方法组合建议

### 8.1 Spec-Driven

适用于：

- 慢变量多
- 边界清晰
- 验收标准重要
- 错误代价高

### 8.2 Kanban

适用于：

- 连续流工作
- 并行任务多
- 需要显式 WIP 管理
- 审查吞吐是瓶颈

### 8.3 Agile / Sprint-like

适用于：

- 有迭代节奏
- 需要阶段性收口
- 需要里程碑 review

### 8.4 组合原则

本技能不把任何一种方法当成唯一答案。

推荐做法是：

- 用 Spec-Driven 稳住边界
- 用 Kanban 管理流动
- 视阶段需要叠加 Sprint-like review 节奏

## 9. 多工具环境的处理方式

本技能默认支持多工具并存，但要求：

1. 工具名不等于角色名。
2. 工具入口不等于 canonical source。
3. 工具特性只能影响 adapter 设计，不能反向定义项目制度。
4. 真正稳定的东西应写在：
   - `policy_or_rules`
   - `agent`
   - `workflow`
   - `skill`
   - `execution_object`
   - `status_projection`

### 9.1 Claude Code / Codex / AntiGravity 的正确位置

建议把它们理解为：

- 执行环境
- 工作台
- adapter 层
- 运行时入口

而不是：

- 持久角色身份
- 项目真源
- 永久治理结构

## 10. 使用方式

### 10.1 作为仓库诊断器

可直接使用：

```text
Use $files-driven to analyze this repo's rules, agents, workflows, skills, and documents, then design a right-sized project structure governance strategy.
```

### 10.2 作为新项目设计器

```text
请使用 $files-driven 为一个新的 AI Agent 项目设计项目结构治理方案，要求包含 source family、跨层共享矩阵、角色控制回路和最小恢复链。
```

### 10.3 作为治理收口器

```text
请使用 $files-driven 诊断这个项目里 rules、README、状态页、任务卡和 workflow 漂移的问题，先给止血顺序，再给终态治理结构。
```

## 11. 输出说明

标准输出区块如下：

1. `项目画像`
2. `项目结构家族图`
3. `跨层共享矩阵`
4. `当前主要失真或治理压力`
5. `推荐治理模式`
6. `推荐项目结构分层`
7. `推荐角色控制回路`
8. `推荐入口/恢复链`
9. `推荐版本与同步纪律`
10. `工具可移植性约束`
11. `推荐下一步实施顺序`
12. `明确不建议的做法`

## 12. 仓库内文件说明

### 12.1 核心真源

- [`SKILL.md`](../SKILL.md)
- [`agents/openai.yaml`](../agents/openai.yaml)

### 12.2 参考资料

- [`core-doctrine.md`](../references/core-doctrine.md)
- [`cross-layer-sharing-contract.md`](../references/cross-layer-sharing-contract.md)
- [`output-contract.md`](../references/output-contract.md)
- [`scenario-playbooks.md`](../references/scenario-playbooks.md)
- [`shared-patterns-from-aijournal-and-hqmdclaw.md`](../references/shared-patterns-from-aijournal-and-hqmdclaw.md)
- [`strategy-selection-matrix.md`](../references/strategy-selection-matrix.md)
- [`tool-portable-team-practices.md`](../references/tool-portable-team-practices.md)

## 13. 维护建议

建议按以下节奏维护：

1. 每次发现稳定的新误区或新模式，优先更新 `references/`。
2. 只有当触发条件、核心工作流、输出契约变化时，再改 `SKILL.md`。
3. 若对外定位变了，同步更新 `agents/openai.yaml`、`README.md`、GitHub 仓库元数据。
4. 若新增工具适配，不要把工具文案写进 canonical role，优先写进跨工具实践说明。

## 14. 发布建议

上传 GitHub 前，建议至少具备：

- `README.md`
- `LICENSE`
- `.gitignore`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/GITHUB_UPLOAD_CHECKLIST.md`
- `docs/REPO_METADATA.md`
- `.github` 模板

详见 [`docs/GITHUB_UPLOAD_CHECKLIST.md`](./GITHUB_UPLOAD_CHECKLIST.md)。
