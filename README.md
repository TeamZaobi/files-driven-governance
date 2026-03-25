# Files-Driven Governance

当前版本：`v0.2.7`

`files-driven` 是一个面向 `AI Agent` / `OpenClaw` / AI 驱动 workflow 项目的项目结构治理技能。

它不把“文件管理”当成简单的目录规划问题，而是把文档视为项目治理的承载介质，用来设计和诊断：

- `policy_or_rules`
- `object`
- `workflow`
- `skill`
- `agent`
- `execution_object`
- `status_projection`
- `display_projection`

之间的真源、投影、同步顺序、共享协议、控制回路与经典流程库。

## v0.2.7 触发口令契约补丁

这一版把“继续开发”“开始审计”“反思”“推进”这类自然语言短口令，提升成了一个可移植、可部署的正式治理契约。

本次补丁重点包括：

1. 新增 `intent-trigger-contract` 参考件。
2. 把口令体系拆成 `canonical intent + alias layer + modifier layer`。
3. 要求区分 `direct action` 与 `route intent`，避免“推进”这类词偷偷改义。
4. 为输出契约增加 `意图触发与执行契约` 条件区块。
5. 更新说明书、默认 prompt、版本文档和场景剧本，使这一能力能服务通用项目部署。

## v0.2.6 需求确认工具包补丁

这一版把“说人话确认需求”继续往前推进了一步：不只要求先确认边界，还给出默认的需求确认问题集、用户故事模板和测试用例模板，让 skill 能直接落出可复述、可纠偏、可测试的起始对齐包。

本次补丁重点包括：

1. 新增需求确认工具包参考件。
2. 固化默认的人话问题集、故事模板和测试模板。
3. 要求边界未稳时，先给问题集和草案，再谈治理蓝图。
4. 把 acceptance owner / audience 纳入起始对齐包。
5. 更新输出契约、说明书、默认 prompt 和版本文档。

## v0.2.5 起始对齐补丁

这一版把“项目起始阶段的方向与边界确认”提升成正式前置步骤。skill 在输出治理蓝图前，会先用一组简短但更完整、但必须说人话的问题确认使用场景、交付预期、用户故事、测试用例和非目标。

本次补丁重点包括：

1. 新增 `方向与边界锚点` 核心区块。
2. 要求绿地或边界漂移项目先确认 usage scenario 和 first deliverable。
3. 新增起始对齐参考件，显式约束问题设计、漂移信号和纠偏动作。
4. 要求用户故事和测试用例写得足够细，能直接判断通过、失败和越界。
5. 更新输出契约、场景剧本、默认 prompt 和版本文档。

## v0.2.4 文档膨胀治理补丁

这一版把“文档膨胀管理”从隐含机制提升成显式治理能力，并为它启动了一轮正式的质询-反思-收敛。

本次补丁重点包括：

1. 新增文档生命周期与压缩策略参考件。
2. 把 `growth_signal -> lifecycle_review -> compact_or_archive` 加入条件流程库。
3. 为输出契约增加 `文档生命周期与压缩策略` 条件区块。
4. 落下一份本主题的质询-反思-收敛记录。

## v0.2.3 精确求解补丁

这一版不删方法库，但把默认输出从“全量蓝图”改成“核心必答 + 条件展开”，让 skill 根据项目实际情况输出更精确的方案。

本次补丁重点包括：

1. 将输出契约改成核心区块与条件区块两层。
2. 要求 skill 不再默认展开全部治理模块。
3. 为 `跨层共享矩阵`、`角色控制回路`、`检索与适配策略`、`工具可移植性约束` 增加诊断触发条件。
4. 强调“不要把简单项目膨胀成完整治理 dossier”。

## v0.2.2 补丁重点

这一版补上了两个治理细节：一是把 `OpenClaw` 明确纳入多工具适配层，而不只是项目类型示例；二是把“理解置信度 -> 主动澄清提问”升成前置诊断规则。

本次补丁重点包括：

1. 把 `OpenClaw` 明确加入多工具 adapter 语境，并补到适配矩阵、共享规则和检索说明。
2. 新增理解置信度与澄清提问参考件。
3. 要求 skill 在锁定诊断前先判断自己对项目基本情况的理解置信度。
4. 当关键前提不清楚时，鼓励 skill 先提少量高杠杆问题，再给治理蓝图。

## v0.2.1 补丁重点

这一版补齐了前一轮遗漏的“对象家族检索与工具适配”层，把 `policy_or_rules / object / workflow / skill / agent` 的 locator、current-version anchor、official retrieval order 和 tool adapter surface 明确写成了正式 contract。

本次补丁重点包括：

1. 新增 family locator contract。
2. 新增五类核心对象的官方检索顺序。
3. 新增 tool adapter matrix，显式区分 canonical source 和 adapter surface。
4. 把 `对象家族检索与适配策略` 升为输出必答区块。

## v0.2.0 升级重点

这一版新增了“流程库”层，不再只回答“结构应该怎么分”，也会回答“哪些经典流程要默认沉淀，哪些只在高风险场景启用”。

本次升级重点包括：

1. 把 `AIJournal` 与 `HQMDClaw` 中反复出现的经典流程提炼成可复用 flow library。
2. 将 `敌意质询 -> 答辩 -> 收敛` 升级为显式一等机制。
3. 将 `proposal -> validation -> shadow/canary -> activation/rollback` 纳入条件升级流程，而不是零散建议。
4. 将 `skill_seed -> package_contract -> active_package` 和 `contract_gap -> closure_topic -> downstream_resume` 固化为可推荐模式。
5. 为本次升级补齐 `CHANGELOG` 和 `v0.2.0` 发布说明。

## 核心定位

这个技能适合三类典型场景：

1. 已有仓库诊断：梳理现有项目的文档体系、角色边界、状态层与漂移点。
2. 新项目搭建：为 AI Agent 项目设计最小可运行的项目治理结构。
3. 漂移后收口：当 `rules / agents / workflows / skills / README / status` 互相漂移时，给出止血和迁移顺序。

它默认支持多工具协作环境，包括但不限于：

- `Claude Code`
- `Codex`
- `AntiGravity`
- `OpenClaw`

但不会把任何工具名当成项目里的 canonical role。
同时，它现在会把“先确认首批真实使用场景和首批交付物”视为治理设计的前置条件，而不是可选补充。
当项目希望用自然语言短口令高效触发开发、审计、反思、推进等动作时，它也会把口令层设计成显式 contract，而不是隐含在聊天习惯里。

## 设计原则

本技能基于三套底层方法论：

1. 系统论：设计项目结构、边界、层次、耦合和 ownership。
2. 信息论：设计事实源、信息流、共享链、恢复链和版本定位。
3. 控制论：设计角色回路、review gate、rollback path 和 change-control intensity。

它默认采用“中等治理强度”：

- 强调 source-of-truth、分层、shared contract、status recovery
- 不默认引入重审批流
- 不默认复制成熟大项目的复杂目录
- 不默认展开完整治理蓝图

同时坚持一个明确的对象设计原则：

1. `Agent` 以角色来定义
   - 角色要明确
   - 边界要清晰
   - 不用工具名或单次任务名定义持久角色
2. `Skill` 以任务技能来定义
   - 绑定可复用 procedure
   - 绑定任务能力和操作方法
   - 不伪装成角色本体

并增加一个显式的检索原则：

1. `policy_or_rules / object / workflow / skill / agent` 都应有稳定 locator
2. 先找 canonical family source，再看 tool adapter
3. 官方读取顺序应跨工具保持稳定
4. `OpenClaw` 入口默认属于 adapter surface，除非项目明确把它提升为 canonical source

## 主要能力

使用 `files-driven` 时，技能会优先完成这些工作：

1. 锁定方向与边界锚点：
   - 使用场景
   - 首批交付物
   - 1-3 个核心用户故事
   - 3-7 个验收/测试用例
   - 非目标与延后项
   - acceptance owner / audience
2. 使用需求确认工具包：
   - 默认问题集
   - 默认用户故事模板
   - 默认测试用例模板
3. 建立七维诊断：
   - 项目阶段
   - 变更风险
   - 协作密度
   - Agent 自主度
   - 恢复压力
   - 协作拓扑
   - 工具异构度
4. 划分 source family：
   - `policy_or_rules`
   - `object`
   - `workflow`
   - `skill`
   - `agent`
   - `execution_object`
   - `status_projection`
   - `display_projection`
5. 建立四层文档视角：
   - `truth_source`
   - `execution_object`
   - `status_projection`
   - `display_projection`
6. 设计跨层共享矩阵：
   - producer
   - consumer
   - writable surface
   - projection surface
   - visibility scope
   - sync trigger
   - conflict rule
   - handoff packet
7. 设计角色控制回路：
   - `observe`
   - `decide`
   - `act`
   - `review`
   - `rollback_or_improve`
8. 组合治理方法：
   - `Spec-Driven`
   - `Kanban`
   - `Agile/Sprint-like`
   - `decision / review / change-control gate`
9. 选择经典流程库：
   - `low_token_recovery_chain`
   - `discussion -> decision_package -> task_or_decision`
   - `mechanism_review`
   - `adversarial_inquiry -> defense -> convergence`
   - `proposal -> validation -> shadow/canary -> activation_or_rollback`
   - `skill_seed -> package_contract -> active_package`
   - `contract_gap -> closure_topic -> downstream_resume`
   - `growth_signal -> lifecycle_review -> compact_or_archive`
10. 设计对象家族检索与适配策略：
   - family locator
   - current-version anchor
   - official retrieval order
   - tool adapter surface
11. 判断理解置信度并按需澄清：
   - `high / medium / low`
   - compact startup question set for usage scenario and delivery expectation
   - default story and test drafts when the boundary is still moving
   - targeted clarification questions
   - explicit assumptions when ambiguity remains
12. 设计意图触发与执行契约：
   - canonical intent set
   - alias layer
   - modifier layer
   - workflow and agent binding
   - ambiguity and fallback rules

## 仓库结构

```text
.
├── CHANGELOG.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── adversarial-convergence-loop.md
│   ├── classic-governance-flows.md
│   ├── core-doctrine.md
│   ├── cross-layer-sharing-contract.md
│   ├── family-locator-contract.md
│   ├── intent-trigger-contract.md
│   ├── official-retrieval-orders.md
│   ├── output-contract.md
│   ├── plain-language-requirements-confirmation-kit.md
│   ├── startup-alignment-through-stories-and-tests.md
│   ├── scenario-playbooks.md
│   ├── shared-patterns-from-aijournal-and-hqmdclaw.md
│   ├── strategy-selection-matrix.md
│   ├── tool-adapter-matrix.md
│   ├── document-lifecycle-and-compaction.md
│   ├── understanding-confidence-and-clarification.md
│   └── tool-portable-team-practices.md
├── docs/
│   ├── DOCUMENT_BLOAT_INQUIRY_ROUND_1.md
│   ├── MANUAL.md
│   ├── GITHUB_UPLOAD_CHECKLIST.md
│   ├── RELEASE_NOTES_v0.2.0.md
│   ├── RELEASE_NOTES_v0.2.1.md
│   ├── RELEASE_NOTES_v0.2.2.md
│   ├── RELEASE_NOTES_v0.2.3.md
│   ├── RELEASE_NOTES_v0.2.4.md
│   ├── RELEASE_NOTES_v0.2.5.md
│   ├── RELEASE_NOTES_v0.2.6.md
│   ├── RELEASE_NOTES_v0.2.7.md
│   └── REPO_METADATA.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── .gitignore
```

## 快速使用

### 1. 作为 Skill 使用

将本目录安装或接入你的 skill 搜索路径后，可以直接用类似提示调用：

```text
Use $files-driven to analyze this repo's rules, agents, workflows, skills, and documents, then design a right-sized project structure governance strategy.
```

也可以直接用中文：

```text
请使用 $files-driven 分析这个多 Agent 项目的 rules、agents、workflows、skills、status 和 README，设计一套适合当前阶段的项目结构治理策略。
```

如果项目还在起始阶段，也可以直接要求技能先确认边界：

```text
请先用需求确认问题集把这个项目的使用场景、首批交付物、用户故事和测试用例说清楚，再使用 $files-driven 设计项目治理方案。
```

如果你希望项目支持更自然的触发口令，也可以直接要求技能设计通用触发契约：

```text
请使用 $files-driven 为这个多 Agent 项目设计一套通用的意图触发与执行契约，让“继续开发”“开始审计”“反思”“推进”这类口令都能稳定定位状态、选择 Agent 并开始工作。
```

### 2. 典型触发句

- “分析这个多 Agent 仓库的现有文档体系，判断哪些文件是事实源、哪些只是状态页，并给出重构方案。”
- “我要做一个 AI Agent 驱动的 OpenClaw 项目，请为它设计一套适合早期阶段的文档管理策略，要求不过重，但要能支撑后续扩展。”
- “这个项目现在 discussion、任务、状态页和 README 已经互相漂移，请诊断主要问题，并给出收口和迁移顺序。”
- “我希望操作者只说‘继续开发’‘开始审计’‘推进’之类短口令，系统就能读状态、选 Agent、开始执行，请设计一套通用部署规范。”

## 输出约定

技能现在采用“核心必答 + 条件展开”：

核心必答区块：

1. `方向与边界锚点`
2. `项目画像`
3. `当前主要失真或治理压力`
4. `推荐治理模式`
5. `推荐经典流程库`
6. `项目结构家族图`
7. `推荐入口/恢复链`
8. `推荐下一步实施顺序`
9. `明确不建议的做法`

条件展开区块：

1. `跨层共享矩阵`
2. `推荐项目结构分层`
3. `推荐角色控制回路`
4. `推荐版本与同步纪律`
5. `对象家族检索与适配策略`
6. `工具可移植性约束`
7. `意图触发与执行契约`
8. `文档生命周期与压缩策略`

只有当诊断显示这些问题确实重要时，skill 才会展开它们。
如果对项目基本情况的理解置信度不足，或者首批交付物仍在漂移，技能会先提出一组简短但更完整的问题，优先确认使用场景与交付预期，而不是直接输出失真的蓝图。
这些问题和对应的用户故事、测试用例必须尽量说人话，并写到足够清晰，避免后续开发时出现“看起来都对，但其实已经偏题”的扩 scope。
如果边界仍未稳定，skill 应先给出问题集、故事草案和测试草案，而不是假装已经确认完成。

## 文档导航

- 技能真源：[`SKILL.md`](./SKILL.md)
- 版本记录：[`CHANGELOG.md`](./CHANGELOG.md)
- 完整说明书：[`docs/MANUAL.md`](./docs/MANUAL.md)
- `v0.2.0` 发布说明：[`docs/RELEASE_NOTES_v0.2.0.md`](./docs/RELEASE_NOTES_v0.2.0.md)
- `v0.2.1` 发布说明：[`docs/RELEASE_NOTES_v0.2.1.md`](./docs/RELEASE_NOTES_v0.2.1.md)
- `v0.2.2` 发布说明：[`docs/RELEASE_NOTES_v0.2.2.md`](./docs/RELEASE_NOTES_v0.2.2.md)
- `v0.2.3` 发布说明：[`docs/RELEASE_NOTES_v0.2.3.md`](./docs/RELEASE_NOTES_v0.2.3.md)
- `v0.2.4` 发布说明：[`docs/RELEASE_NOTES_v0.2.4.md`](./docs/RELEASE_NOTES_v0.2.4.md)
- `v0.2.5` 发布说明：[`docs/RELEASE_NOTES_v0.2.5.md`](./docs/RELEASE_NOTES_v0.2.5.md)
- `v0.2.6` 发布说明：[`docs/RELEASE_NOTES_v0.2.6.md`](./docs/RELEASE_NOTES_v0.2.6.md)
- `v0.2.7` 发布说明：[`docs/RELEASE_NOTES_v0.2.7.md`](./docs/RELEASE_NOTES_v0.2.7.md)
- 文档膨胀质询记录：[`docs/DOCUMENT_BLOAT_INQUIRY_ROUND_1.md`](./docs/DOCUMENT_BLOAT_INQUIRY_ROUND_1.md)
- 上传 GitHub 清单：[`docs/GITHUB_UPLOAD_CHECKLIST.md`](./docs/GITHUB_UPLOAD_CHECKLIST.md)
- 仓库元数据建议：[`docs/REPO_METADATA.md`](./docs/REPO_METADATA.md)
- 贡献方式：[`CONTRIBUTING.md`](./CONTRIBUTING.md)
- 安全说明：[`SECURITY.md`](./SECURITY.md)

## 许可证

当前仓库默认附带 `MIT` 许可证，见 [`LICENSE`](./LICENSE)。

如果你准备改成更严格或更商业化的许可模式，优先修改 `LICENSE`，并同步更新 [`docs/REPO_METADATA.md`](./docs/REPO_METADATA.md) 与 GitHub 仓库设置。
