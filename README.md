# Files-Driven Governance

当前版本：`v0.2.1`

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

但不会把任何工具名当成项目里的 canonical role。

## 设计原则

本技能基于三套底层方法论：

1. 系统论：设计项目结构、边界、层次、耦合和 ownership。
2. 信息论：设计事实源、信息流、共享链、恢复链和版本定位。
3. 控制论：设计角色回路、review gate、rollback path 和 change-control intensity。

它默认采用“中等治理强度”：

- 强调 source-of-truth、分层、shared contract、status recovery
- 不默认引入重审批流
- 不默认复制成熟大项目的复杂目录

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

## 主要能力

使用 `files-driven` 时，技能会优先完成这些工作：

1. 建立七维诊断：
   - 项目阶段
   - 变更风险
   - 协作密度
   - Agent 自主度
   - 恢复压力
   - 协作拓扑
   - 工具异构度
2. 划分 source family：
   - `policy_or_rules`
   - `object`
   - `workflow`
   - `skill`
   - `agent`
   - `execution_object`
   - `status_projection`
   - `display_projection`
3. 建立四层文档视角：
   - `truth_source`
   - `execution_object`
   - `status_projection`
   - `display_projection`
4. 设计跨层共享矩阵：
   - producer
   - consumer
   - writable surface
   - projection surface
   - visibility scope
   - sync trigger
   - conflict rule
   - handoff packet
5. 设计角色控制回路：
   - `observe`
   - `decide`
   - `act`
   - `review`
   - `rollback_or_improve`
6. 组合治理方法：
   - `Spec-Driven`
   - `Kanban`
   - `Agile/Sprint-like`
   - `decision / review / change-control gate`
7. 选择经典流程库：
   - `low_token_recovery_chain`
   - `discussion -> decision_package -> task_or_decision`
   - `mechanism_review`
   - `adversarial_inquiry -> defense -> convergence`
   - `proposal -> validation -> shadow/canary -> activation_or_rollback`
   - `skill_seed -> package_contract -> active_package`
   - `contract_gap -> closure_topic -> downstream_resume`
8. 设计对象家族检索与适配策略：
   - family locator
   - current-version anchor
   - official retrieval order
   - tool adapter surface

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
│   ├── official-retrieval-orders.md
│   ├── output-contract.md
│   ├── scenario-playbooks.md
│   ├── shared-patterns-from-aijournal-and-hqmdclaw.md
│   ├── strategy-selection-matrix.md
│   ├── tool-adapter-matrix.md
│   └── tool-portable-team-practices.md
├── docs/
│   ├── MANUAL.md
│   ├── GITHUB_UPLOAD_CHECKLIST.md
│   ├── RELEASE_NOTES_v0.2.0.md
│   ├── RELEASE_NOTES_v0.2.1.md
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

### 2. 典型触发句

- “分析这个多 Agent 仓库的现有文档体系，判断哪些文件是事实源、哪些只是状态页，并给出重构方案。”
- “我要做一个 AI Agent 驱动的 OpenClaw 项目，请为它设计一套适合早期阶段的文档管理策略，要求不过重，但要能支撑后续扩展。”
- “这个项目现在 discussion、任务、状态页和 README 已经互相漂移，请诊断主要问题，并给出收口和迁移顺序。”

## 输出约定

技能默认输出以下区块：

1. `项目画像`
2. `项目结构家族图`
3. `跨层共享矩阵`
4. `当前主要失真或治理压力`
5. `推荐治理模式`
6. `推荐经典流程库`
7. `推荐项目结构分层`
8. `推荐角色控制回路`
9. `推荐入口/恢复链`
10. `推荐版本与同步纪律`
11. `对象家族检索与适配策略`
12. `工具可移植性约束`
13. `推荐下一步实施顺序`
14. `明确不建议的做法`

## 文档导航

- 技能真源：[`SKILL.md`](./SKILL.md)
- 版本记录：[`CHANGELOG.md`](./CHANGELOG.md)
- 完整说明书：[`docs/MANUAL.md`](./docs/MANUAL.md)
- `v0.2.0` 发布说明：[`docs/RELEASE_NOTES_v0.2.0.md`](./docs/RELEASE_NOTES_v0.2.0.md)
- `v0.2.1` 发布说明：[`docs/RELEASE_NOTES_v0.2.1.md`](./docs/RELEASE_NOTES_v0.2.1.md)
- 上传 GitHub 清单：[`docs/GITHUB_UPLOAD_CHECKLIST.md`](./docs/GITHUB_UPLOAD_CHECKLIST.md)
- 仓库元数据建议：[`docs/REPO_METADATA.md`](./docs/REPO_METADATA.md)
- 贡献方式：[`CONTRIBUTING.md`](./CONTRIBUTING.md)
- 安全说明：[`SECURITY.md`](./SECURITY.md)

## 许可证

当前仓库默认附带 `MIT` 许可证，见 [`LICENSE`](./LICENSE)。

如果你准备改成更严格或更商业化的许可模式，优先修改 `LICENSE`，并同步更新 [`docs/REPO_METADATA.md`](./docs/REPO_METADATA.md) 与 GitHub 仓库设置。
