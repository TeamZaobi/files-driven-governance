# Files-Driven Governance 完整说明书

当前版本：`v0.2.5`

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
- 同时使用 `Claude Code / Codex / AntiGravity / OpenClaw` 等多个开发工具的团队

## 2. 解决的问题

这个技能主要解决以下问题：

1. `README`、状态页、任务卡、rules、agents、skills 等文件互相漂移。
2. 多工具并行使用时，工具入口被误当成 canonical source。
3. 项目里没有明确区分“规则”“流程”“角色”“方法”“状态摘要”。
4. 多人/多 Agent 协作时，不清楚谁能读、谁能写、谁能审批、谁只能投影。
5. 想借鉴 Spec-Driven、Kanban、敏捷等方法，但不想把项目搞成过重流程。
6. 需要按项目实际情况给出精确方案，而不是默认输出完整治理大图。
7. 项目运行一段时间后，active docs 膨胀，恢复链和当前态判断成本越来越高。
8. 项目起始阶段如果用户故事、使用场景或交付预期有小漂移，后续结构设计和开发范围会被连带放大。

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

### 4.0 起始对齐包：方向与边界锚点

在讨论 source family、目录分层或工具适配前，本技能现在要求先落一个最小的“方向与边界锚点”。

这个起始对齐包至少要明确：

1. 首批真实使用场景
2. 首批交付物
3. `1-3` 个核心用户故事
4. `3-7` 个验收/测试用例
5. 明确不做的范围或延后项
6. 仅用于质量校准的参考样例

对于早期项目或边界有漂移迹象的项目，本技能不再满足于一两个笼统问题，而是应先用一组简短但完整的问题确认：

1. 谁在什么场景里使用
2. 第一阶段到底交付什么
3. 什么算成功，什么虽然相关但不算本次交付
4. 哪些输入/资料必须先支持
5. 哪些能力暂时明确不做
6. 哪些参考对象只是风格或质量基线

这些确认必须尽量说人话，而不是先抛架构黑话给用户翻译。
用户故事和测试用例也不能只写标题，至少要细到能判断：

1. 谁在什么情境下使用
2. 希望得到什么结果
3. 什么结果算通过
4. 什么虽然相关，但这次明确不交付

如果这一步不稳定，就不应继续放大到结构治理蓝图。

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

### 4.1.1 Agent 与 Skill 的设计公理

本技能对 `agent` 和 `skill` 的区分采用一条明确公理：

1. `Agent` 以角色来定义
   - 定义职责
   - 定义 authority
   - 定义输入输出边界
   - 定义它在控制回路里的位置
2. `Skill` 以任务技能来定义
   - 定义可复用 procedure
   - 定义任务方法
   - 定义执行 checklist、references、assets
   - 定义适用边界与触发条件

因此：

1. 不应用工具名来定义长期 `Agent`
2. 不应用单次任务名来定义长期 `Agent`
3. 不应用人格或角色名来定义 `Skill`
4. 不应让 `Skill` 反向承担角色 authority
5. 不应让 `Agent` 收纳过多互不相关的任务技能

### 4.1.2 五类核心对象的检索公理

对 `policy_or_rules / object / workflow / skill / agent`，本技能默认要求：

1. 有 canonical locator
2. 有 current-version anchor
3. 有跨工具稳定的 official retrieval order
4. 有明确的 tool adapter surface

如果一个项目只能通过某个工具入口才能找到这些对象，这说明治理还不够稳定。

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

在正式锁定诊断前，本技能还会判断“对项目基本情况的理解置信度”。

### 5.0 理解置信度与澄清提问

本技能会先检查自己是否真正理解了这些基本项：

1. 项目边界与当前目标
2. 主要角色、Agent 和工具入口
3. 当前 canonical source 与 current-version anchor
4. 当前协作形态与风险
5. 用户真正想要的使用场景与首批交付物
6. 用户真正想要的输出、验收边界和治理强度

置信度分成：

- `high`
- `medium`
- `low`

当置信度是 `low` 时，应先向用户提问，再冻结诊断。
当置信度是 `medium` 且不确定点会影响 family 划分、OpenClaw/其他工具适配、控制回路设计，或首批交付物边界时，也应先做少量澄清提问。
如果项目仍处在起始边界确认阶段，应优先用一组短问题确认使用场景和交付预期，而不是先问架构偏好。

### 5.1 协作拓扑

协作拓扑关注：

- 有多少人参与？
- 有多少 Agent 参与？
- 是否有人机混合审批？
- 是否存在平台团队、业务团队、审计团队等多层角色？

### 5.2 工具异构度

工具异构度关注：

- 是否同时用 `Claude Code / Codex / AntiGravity / OpenClaw`
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

## 6.2 对象家族检索与适配

本技能现在会单独检查五类核心对象的检索准备度：

1. `policy_or_rules`
2. `object`
3. `workflow`
4. `skill`
5. `agent`

每类对象都应回答：

1. 真源在哪里
2. 当前版本锚点在哪里
3. 官方读取顺序是什么
4. 哪些文件只是 tool adapter
5. 哪些 adapter 只能 summarize，不能 define

如果项目使用 `OpenClaw`，还应额外回答：

1. `OpenClaw` 在这个项目里是 launcher、adapter、projection，还是被明确提升为 canonical entrypoint
2. 如果没有 `OpenClaw`，这五类核心对象是否仍然可稳定检索

## 6.3 文档生命周期与压缩

当项目进入运行态后，本技能会把“文档膨胀”视为治理问题而不是排版问题。

推荐最小生命周期状态：

1. `active`
2. `stable_reference`
3. `projection`
4. `history`
5. `archive`

推荐优先动作：

1. 先识别哪些 active 页面其实只是 projection 或 history
2. 先压缩 `status_projection` 和 overloaded `README`
3. 再拆分 overloaded `discussion / task / review`
4. 最后才归档或降级旧页

只有当膨胀、检索成本、stale page 或历史越权明显时，才展开这块设计。

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

补充约束：

1. 角色模式应优先落到 `Agent`
2. 任务能力模式应优先落到 `Skill`
3. 如果一个设计同时像“角色说明书”又像“任务说明书”，默认先拆分，而不是继续混写

## 8. 方法组合建议

### 8.1 Spec-Driven

适用于：

- 慢变量多
- 边界清晰
- 验收标准重要
- 错误代价高

其中“边界清晰”和“验收标准重要”应优先由起始对齐包中的用户故事与测试用例来支撑，而不是仅靠抽象目标描述。

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

## 9. 经典流程库

这一版 skill 不再只输出“结构图”，还会输出“建议沉淀的流程库”。

这些流程分成两层：

### 9.1 默认流程

默认流程是大多数 AI Agent 项目都值得优先建立的最小治理回路：

1. `low_token_recovery_chain`
   - `status entry -> active object -> canonical source -> history on demand`
2. `discussion -> decision_package -> task_or_decision`
3. `truth_source -> execution_object -> status_projection -> display_projection`
4. `mechanism_review -> repair_or_split`

### 9.2 条件升级流程

条件升级流程只有在项目风险、分歧、自动化程度或治理强度足够高时才建议启用：

1. `adversarial_inquiry -> defense -> convergence`
2. `isolated_multi_role_deliberation`
3. `proposal -> validation -> shadow/canary -> activation_or_rollback`
4. `skill_seed -> package_contract -> active_package`
5. `contract_gap -> closure_topic -> downstream_resume`

### 9.3 为什么要把流程也纳入 skill

因为你要治理的不是静态目录，而是：

- 主题如何从未决进入执行
- 高风险争议如何被打磨到可接受
- 机制缺口如何被独立拆出而不是偷偷补洞
- 新 procedure 如何从 seed 变成 active package

也就是说，结构设计和流程设计必须一起给。

### 9.4 敌意质询的定位

`敌意质询 -> 答辩 -> 收敛` 在本技能里已被升为显式高级流程。

它适用于：

1. 重要主题分歧较大
2. 讨论结果将直接晋升为 `task / decision`
3. 需要制度性反方或用户价值标杆位
4. 团队已有“太快达成礼貌共识”的倾向

其最小要求是：

1. `question_id`
2. 逐条应答
3. `resolved / accepted / downgraded / deferred`
4. 明确的 `closure_authority`

## 10. 多工具环境的处理方式

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

同时要求：

1. 五类核心对象要有稳定的 official retrieval order
2. tool adapter 只能作为 bootstrap、launcher、projection 或 compatibility shim
3. tool adapter 不能成为唯一 locator

### 10.1 Claude Code / Codex / AntiGravity / OpenClaw 的正确位置

建议把它们理解为：

- 执行环境
- 工作台
- adapter 层
- 运行时入口

而不是：

- 持久角色身份
- 项目真源
- 永久治理结构

## 11. 使用方式

### 11.1 作为仓库诊断器

可直接使用：

```text
Use $files-driven to analyze this repo's rules, agents, workflows, skills, and documents, then design a right-sized project structure governance strategy.
```

### 11.2 作为新项目设计器

```text
请使用 $files-driven 为一个新的 AI Agent 项目设计项目结构治理方案，要求包含 source family、跨层共享矩阵、角色控制回路和最小恢复链。
```

```text
请先用几个问题确认这个项目的使用场景、首批交付物、用户故事和测试用例，再使用 $files-driven 给治理方案。
```

### 11.3 作为治理收口器

```text
请使用 $files-driven 诊断这个项目里 rules、README、状态页、任务卡和 workflow 漂移的问题，先给止血顺序，再给终态治理结构。
```

## 12. 输出说明

标准输出采用“两层结构”：

### 12.1 核心必答区块

1. `方向与边界锚点`
2. `项目画像`
3. `当前主要失真或治理压力`
4. `推荐治理模式`
5. `推荐经典流程库`
6. `项目结构家族图`
7. `推荐入口/恢复链`
8. `推荐下一步实施顺序`
9. `明确不建议的做法`

### 12.2 条件展开区块

当且仅当诊断表明这些主题是当前主要矛盾时，再展开：

1. `跨层共享矩阵`
2. `推荐项目结构分层`
3. `推荐角色控制回路`
4. `推荐版本与同步纪律`
5. `对象家族检索与适配策略`
6. `工具可移植性约束`
7. `文档生命周期与压缩策略`

例如：

- 有多人、多 Agent、多工具共享同一事实时，再展开 `跨层共享矩阵`
- 有角色责任或自治风险时，再展开 `推荐角色控制回路`
- 有 retrieval ambiguity 或 tool entrypoint 越权时，再展开 `对象家族检索与适配策略`
- 存在迁移风险或明确多工具协同时，再展开 `工具可移植性约束`
- 有 active docs 膨胀、recovery cost 上升或 stale page 积累时，再展开 `文档生命周期与压缩策略`

如果理解置信度较低，或首批交付物仍在漂移，技能应先提出一组说人话的确认问题，并把用户故事和测试用例写清楚，而不是直接输出完整蓝图。

## 13. 仓库内文件说明

### 13.1 核心真源

- [`SKILL.md`](../SKILL.md)
- [`agents/openai.yaml`](../agents/openai.yaml)
- [`CHANGELOG.md`](../CHANGELOG.md)

### 13.2 参考资料

- [`adversarial-convergence-loop.md`](../references/adversarial-convergence-loop.md)
- [`classic-governance-flows.md`](../references/classic-governance-flows.md)
- [`core-doctrine.md`](../references/core-doctrine.md)
- [`cross-layer-sharing-contract.md`](../references/cross-layer-sharing-contract.md)
- [`family-locator-contract.md`](../references/family-locator-contract.md)
- [`official-retrieval-orders.md`](../references/official-retrieval-orders.md)
- [`output-contract.md`](../references/output-contract.md)
- [`startup-alignment-through-stories-and-tests.md`](../references/startup-alignment-through-stories-and-tests.md)
- [`scenario-playbooks.md`](../references/scenario-playbooks.md)
- [`shared-patterns-from-aijournal-and-hqmdclaw.md`](../references/shared-patterns-from-aijournal-and-hqmdclaw.md)
- [`strategy-selection-matrix.md`](../references/strategy-selection-matrix.md)
- [`tool-adapter-matrix.md`](../references/tool-adapter-matrix.md)
- [`tool-portable-team-practices.md`](../references/tool-portable-team-practices.md)
- [`understanding-confidence-and-clarification.md`](../references/understanding-confidence-and-clarification.md)
- [`document-lifecycle-and-compaction.md`](../references/document-lifecycle-and-compaction.md)

### 13.3 发布说明

- [`RELEASE_NOTES_v0.2.0.md`](./RELEASE_NOTES_v0.2.0.md)
- [`RELEASE_NOTES_v0.2.1.md`](./RELEASE_NOTES_v0.2.1.md)
- [`RELEASE_NOTES_v0.2.2.md`](./RELEASE_NOTES_v0.2.2.md)
- [`RELEASE_NOTES_v0.2.3.md`](./RELEASE_NOTES_v0.2.3.md)
- [`RELEASE_NOTES_v0.2.4.md`](./RELEASE_NOTES_v0.2.4.md)
- [`RELEASE_NOTES_v0.2.5.md`](./RELEASE_NOTES_v0.2.5.md)
- [`DOCUMENT_BLOAT_INQUIRY_ROUND_1.md`](./DOCUMENT_BLOAT_INQUIRY_ROUND_1.md)

## 14. 维护建议

建议按以下节奏维护：

1. 每次发现稳定的新误区或新模式，优先更新 `references/`。
2. 只有当触发条件、核心工作流、输出契约变化时，再改 `SKILL.md`。
3. 若对外定位变了，同步更新 `agents/openai.yaml`、`README.md`、GitHub 仓库元数据。
4. 若新增工具适配，不要把工具文案写进 canonical role，优先写进跨工具实践说明。
5. 若经典流程库发生变化，同步更新 `references/classic-governance-flows.md`、`references/adversarial-convergence-loop.md` 与 `CHANGELOG.md`。

## 15. 发布建议

上传 GitHub 前，建议至少具备：

- `README.md`
- `CHANGELOG.md`
- `LICENSE`
- `.gitignore`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/RELEASE_NOTES_v0.2.0.md`
- `docs/RELEASE_NOTES_v0.2.1.md`
- `docs/RELEASE_NOTES_v0.2.2.md`
- `docs/RELEASE_NOTES_v0.2.3.md`
- `docs/RELEASE_NOTES_v0.2.4.md`
- `docs/RELEASE_NOTES_v0.2.5.md`
- `docs/DOCUMENT_BLOAT_INQUIRY_ROUND_1.md`
- `docs/GITHUB_UPLOAD_CHECKLIST.md`
- `docs/REPO_METADATA.md`
- `.github` 模板

详见 [`docs/GITHUB_UPLOAD_CHECKLIST.md`](./GITHUB_UPLOAD_CHECKLIST.md)。
