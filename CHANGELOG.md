# 更新记录

本文记录 `files-driven` 的仓库层面重要变更。
它只负责记账：新增了什么、调整了什么、删掉了什么。
某一版为什么重要、改变了什么理解或使用方式，交给对应的 `docs/v*_版本说明.md`。

## Unreleased

### 新增

- 新增 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) `capability-improve` 子命令，把 `files-driven` 自己的 `self-hosting capability_scope` 改善 workflow 暴露成脚本调度、`Codex CLI` 节点执行的正式入口。
- 新增 [references/问题诊断与控制强度分级.md](references/问题诊断与控制强度分级.md)、[references/执行面判定与CLI生产策略.md](references/执行面判定与CLI生产策略.md)、[docs/外部项目Workflow改造脚手架.md](docs/外部项目Workflow改造脚手架.md)，把“先诊断问题、再选控制强度、再定宿主/CLI/runner 分工”补成正式脚手架。

### 调整

- 调整 [README.md](README.md)、[SKILL.md](SKILL.md) 与 [agents/openai.yaml](agents/openai.yaml)，把“脚本控制流程、Codex CLI 只做节点内产物”的 self-hosting 路由写进正式入口文案。
- 调整 [README.md](README.md)、[SKILL.md](SKILL.md)、[docs/项目治理能力模型.md](docs/项目治理能力模型.md) 与 [agents/openai.yaml](agents/openai.yaml)，把“帮助用户识别问题，解决问题”“长期路线是强化控制能力”收成正式口径，并明确控制面外移、Workflow 脚本化、CLI backend 化只是当前阶段的实现策略。
- 新增 [docs/v0.4.1_版本说明.md](docs/v0.4.1_版本说明.md)，系统解释这一版为什么强调强化控制能力、宿主原生能力优先，以及脚本/CLI 在当前阶段的补强角色。
- 调整 [README.md](README.md)、[SKILL.md](SKILL.md) 与 [docs/v0.4.1_版本说明.md](docs/v0.4.1_版本说明.md)，把新脚手架挂进正式入口和版本说明。
- 调整 [tests/test_entrypoint_consistency.py](tests/test_entrypoint_consistency.py) 与 [tests/test_files_engine_actions.py](tests/test_files_engine_actions.py)，把 `capability-improve` 的入口暴露和 `manage` CLI 包装执行补成回归。

## v0.4.0 - 2026-04-12

### 新增

- 新增 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)，把 `v1 -> v2 -> v2.1` 收成统一底层真源，并显式分开能力模型演进轴与 governed pack / contract `tranche v1`。
- 新增 `files engine` starter 与元 skill 执行动作闭环： [starters/minimal-files-engine/](starters/minimal-files-engine/)、[schemas/file.registration.schema.json](schemas/file.registration.schema.json)、[schemas/files.registry.schema.json](schemas/files.registry.schema.json)、[schemas/intent.routes.schema.json](schemas/intent.routes.schema.json)、[schemas/scaffold.manifest.schema.json](schemas/scaffold.manifest.schema.json)、[schemas/starter.profile.schema.json](schemas/starter.profile.schema.json)。
- 新增 [scripts/bootstrap_files_engine_starter.py](scripts/bootstrap_files_engine_starter.py)、[scripts/manage_files_engine.py](scripts/manage_files_engine.py)、[scripts/validate_files_engine_scaffold.py](scripts/validate_files_engine_scaffold.py)，把 `install / register / repair / audit` 从文档口径推进成真实动作入口。
- 新增 [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md) 与 [docs/files引擎元skill优化方案.md](docs/files引擎元skill优化方案.md)，把“制造引擎的脚手架资产”“registry identity core + annotations”“starter profile 与 manifest 解耦”正式写成仓库资产。
- 新增 [tests/test_end_to_end_governance_alignment.py](tests/test_end_to_end_governance_alignment.py)、[tests/test_files_engine_scaffold.py](tests/test_files_engine_scaffold.py)、[tests/test_files_engine_actions.py](tests/test_files_engine_actions.py)，把统一真源、starter 冷启动、register/audit/repair 流程与耦合边界冻结成回归。

### 调整

- 调整 [README.md](README.md)、[SKILL.md](SKILL.md)、[QUICKSTART.md](QUICKSTART.md)、[PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md)、[schemas/README.md](schemas/README.md)、[docs/完整说明书.md](docs/完整说明书.md) 与相关 references，把默认叙事从“结构说明”收回到“统一真源 + 动作入口 + 元 skill 执行闭环”。
- 调整 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py)、[schemas/workflow.state.schema.json](schemas/workflow.state.schema.json)、canonical examples 与相应测试，清出 legacy `schemas/` 路径、`allowed_next_step_refs` / `next_step` 旧授权语义，并把旧动作路径回流继续锁死。
- 调整 starter 与 registry 级联模型：`manifest` 只管拓扑，starter 专属形状约束移到 starter profile；`files.registry.json` 只保留 `file_id / path / family / layer / work_post` 身份核心，其余信息下沉到 annotations。
- 调整 [agents/openai.yaml](agents/openai.yaml) 与入口测试，使 runtime prompt、入口文案、故事和回归都显式理解 `install / register / repair / audit` 与 `reference implementation + regression fixture` 的定位。

## v0.3.1 - 2026-04-10

### 新增

- 新增 pack 级 [BOUNDARY.md](examples/smoke-governed-review/BOUNDARY.md) 约定，并在 smoke pack 中补出最小边界锚点：把首批场景、交付物、用户故事、测试用例、非目标、质量参考对象和验收责任人正式落成受控资产包入口。
- 新增仓库级 [PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md) 与 [tests/test_project_stories_and_tests.py](tests/test_project_stories_and_tests.py)，把本项目自己当前的具体用户故事、具体测试用例、非目标和验收责任人固定成可回归的入口资产。
- 新增 [references/AI-Native同构团队协作.md](references/AI-Native同构团队协作.md)，把“全员通过 AI 工具工作 + 项目级规则文件跟仓共享 + Git 目录级全量共享”这一协作前提正式收编为公开 reference。

### 调整

- 新增 [docs/v0.3.1_版本说明.md](docs/v0.3.1_版本说明.md)，并同步更新当前公开版本、发布元数据与说明书入口，使这轮补丁正式作为 `v0.3.1` 发布。
- 调整 [docs/v0.3.0_版本说明.md](docs/v0.3.0_版本说明.md)，补齐现有 `v0.3.0` 的历史说明文档。
- 调整 [README.md](README.md)、[docs/完整说明书.md](docs/完整说明书.md)、[docs/语言体系规范.md](docs/语言体系规范.md)、[docs/仓库元数据建议.md](docs/仓库元数据建议.md)、[references/官方读取顺序.md](references/官方读取顺序.md)、[references/工具适配对照表.md](references/工具适配对照表.md) 与 [references/结构家族定位约定.md](references/结构家族定位约定.md)，把 `AI-Native` 同构团队下的默认协作理解补清：先按“多个执行上下文共享同一 Git 存储”判断协作，再区分 runtime/工具入口与仓库级规则真源。
- 调整 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py)、[tests/test_validate_governance_assets.py](tests/test_validate_governance_assets.py)、[QUICKSTART.md](QUICKSTART.md) 与 [MIGRATION.md](MIGRATION.md)，让 validator 和入口文档开始强制要求 `BOUNDARY.md` 的最小 section tag、故事数量、测试数量以及至少一个失败/越界边界。
- 调整 [references/起步阶段_故事与测试对齐.md](references/起步阶段_故事与测试对齐.md)、[references/说人话需求确认工具包.md](references/说人话需求确认工具包.md) 与 [README.md](README.md)，把“先补故事和测试”从对话建议升级成 pack 级显式入口要求，并把仓库级项目故事/测试入口接进首次阅读路径。
- 调整 [SKILL.md](SKILL.md)、[references/起步阶段_故事与测试对齐.md](references/起步阶段_故事与测试对齐.md)、[docs/完整说明书.md](docs/完整说明书.md)、[README.md](README.md)、[PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md) 与 [tests/test_project_stories_and_tests.py](tests/test_project_stories_and_tests.py)，统一 `1-3` 个用户故事、`3-8` 个测试用例的数量口径，把仓库级故事/测试文档从 pack `BOUNDARY` 的固定 section contract 中解耦，并收窄首次阅读路径，减少入口溢出、规则漂移和过度设计。

## v0.3.0 - 2026-04-07

### 新增

- 新增 [docs/语言体系规范.md](docs/语言体系规范.md)，把“中文优先、必要时补稳定键名”正式写成仓库级语言规范，用来约束后续 README、技能说明和参考件的写法。
- 新增开发/运营并存治理的显式表达：在 [references/经典治理流程库.md](references/经典治理流程库.md) 中补入“运营信号分流”和“运行观察晋升关口”两条条件流程，在 [references/输出约定.md](references/输出约定.md) 中补入“开发/运营双治理结构”条件区块。
- 新增 [references/关口硬化与稳定放行.md](references/关口硬化与稳定放行.md)，把“该停没停、该问没问、`partial / blocked` 无法约束下游”正式收编成可复用的治理问题，并提供最小稳定解。
- 新增 [docs/项目治理能力模型_v1.md](docs/项目治理能力模型_v1.md)，把本轮重构对象正式上提为“项目治理设计能力”，而不只是一轮仓库文案调整。
- 新增 [docs/分支推进决策流程.md](docs/分支推进决策流程.md)，把 `main` 与 `codex/governance-capability-v1` 的职责、门槛和推进顺序正式写清。
- 新增 [schemas/README.md](schemas/README.md) 与四份 schema 草案： [workflow.contract.schema.json](schemas/workflow.contract.schema.json)、[object.contract.schema.json](schemas/object.contract.schema.json)、[policy.contract.schema.json](schemas/policy.contract.schema.json)、[agent.contract.schema.json](schemas/agent.contract.schema.json)。
- 新增 `gate_state` 的 canonical 三态冻结：在 [workflow.state.schema.json](schemas/workflow.state.schema.json)、[workflow.event.schema.json](schemas/workflow.event.schema.json) 与 [references/关口硬化与稳定放行.md](references/关口硬化与稳定放行.md) 中把最小枚举正式收口为 `blocked / partial / ready`。
- 新增 [schemas/status.projection.schema.json](schemas/status.projection.schema.json)，把 `status_projection` 的最小机读结构和“只能派生、不能放行”的边界正式写成 schema。
- 新增 [examples/smoke-governed-review](examples/smoke-governed-review)，把当前最小治理链做成可跑 smoke 资产包。
- 新增 [QUICKSTART.md](QUICKSTART.md)，把 governed pack 的最小入口、目录形状和 validator 用法收进入口层。
- 新增 [MIGRATION.md](MIGRATION.md)，说明从旧的 `schemas/*.json` / `statement` / 局部 check refs 迁到当前约定的步骤。
- 新增 [tests/test_validate_governance_assets.py](tests/test_validate_governance_assets.py)，把 smoke pack、authority key、rules、event actor、重复 event 与 legacy 兼容等关键边界固化成最小回归集。
- 新增 [governance-assets-ci.yml](.github/workflows/governance-assets-ci.yml)，把 JSON 语法检查、validator smoke run 和最小单元测试接入 GitHub Actions。
- 新增 [requirements-dev.txt](requirements-dev.txt)，把 validator 和测试所需的最小 Python 依赖显式化。

### 调整

- 收紧 [docs/语言体系规范.md](docs/语言体系规范.md) 与 [README.md](README.md) 的语言纪律：把入口层改回中文主叙事，新增“入口层 / 执行层 / 合同与实现层”的文档分层写法，并把英文稳定键名收回到第一次精确对齐和实现层文档中使用。
- 在 [SKILL.md](SKILL.md)、[references/经典治理流程库.md](references/经典治理流程库.md) 与 [references/跨层共享约定.md](references/跨层共享约定.md) 中收编 `process_projection`：把它定义成从 `execution_object` 派生的统一过程投影，用于多工具过程可见性和交接压缩，不新增分层，也不提升为真源。
- 进一步收紧 `process_projection` 的启用边界：默认只在多工具过程不透明时启用；若复杂性主要来自显式 `workflow` 或多 agent 协作，再条件补 `topology_supplement` 说明执行拓扑。
- 统一 `docs/` 与 `references/` 主要文档的中文命名与中文表达，替换早期英文文件名和中英混写表述，并同步修正仓库内链接与对外包装文案。
- 重写 [README.md](README.md)，把仓库入口改成面向人的项目说明，补充适用场景、不适用场景、首次阅读路线，以及 `README`、`SKILL`、`references`、`CHANGELOG`、版本说明之间的职责分工。
- 扩充 [README.md](README.md) 的方法学声明，补回 `Spec-Driven / Kanban / Agile` 与系统论、信息论、控制论的理论来源、重组关系和核心判断，使公开入口不只讲“怎么用”，也讲“为什么成立”。
- 在 [README.md](README.md) 中补入 `Prompt Engineering -> Context Engineering -> Harness / Agent-Native Engineering` 的外部演化线，并明确它与 `files-driven` 的关系是参照与重述，不是单向派生。
- 在 [README.md](README.md) 中补入 `mermaid` 图示，用可视化方式解释文档分层、治理流程和常见失真模式。
- 在 [README.md](README.md) 中补入简版“版本演进”脉络，作为理解入口；同时明确由 [CHANGELOG.md](CHANGELOG.md) 负责变更账本、由 `docs/v*_版本说明.md` 负责单版解读。
- 瘦身重排 [SKILL.md](SKILL.md)，把主技能收回到“执行导览 + 条件下钻”的结构，不再让主文件承担完整说明书职责。
- 重写 [README.md](README.md)，把入口面收成“项目说明 + 阅读路线 + 问题入口”，删去与主技能和完整说明书重复的大段展开。
- 收紧 [agents/openai.yaml](agents/openai.yaml) 的 `short_description` 与 `default_prompt`，使其与当前主技能的最小主流程保持一致。
- 调整 [references/场景手册.md](references/场景手册.md)，把三类起点的“最低交付物”压回核心最小集合，并把角色回路、意图触发、压缩顺序等改成条件补充项。
- 调整 [references/基本原则.md](references/基本原则.md) 与 [references/治理模式选择对照表.md](references/治理模式选择对照表.md)，补清各自的职责边界，避免与主技能和场景路由重复抢活。
- 调整 [references/结构家族定位约定.md](references/结构家族定位约定.md)、[references/官方读取顺序.md](references/官方读取顺序.md) 与 [references/跨层共享约定.md](references/跨层共享约定.md)，把三份执行 reference 收回到“定位 / 顺序 / 共享”的辅助职责，避免隐性变成第二主流程。
- 调整 [references/工具适配对照表.md](references/工具适配对照表.md)、[references/意图触发约定.md](references/意图触发约定.md) 与 [references/理解把握度与澄清规则.md](references/理解把握度与澄清规则.md)，补清启用前提与回退路由，避免默认全开或演化成第二套主流程。
- 调整 [SKILL.md](SKILL.md) 的 reference 路由语句，使“定位 / 顺序 / 适配 / 共享 / 意图 / 澄清”六类问题各自指向最合适的单一参考件，不再把多份 reference 一起当成隐性第二主流程。
- 调整剩余 routed references 的启用边界，包括 [references/起步阶段_故事与测试对齐.md](references/起步阶段_故事与测试对齐.md)、[references/说人话需求确认工具包.md](references/说人话需求确认工具包.md)、[references/理解型输入与低带宽压缩包.md](references/理解型输入与低带宽压缩包.md)、[references/经典治理流程库.md](references/经典治理流程库.md)、[references/跨工具团队实践.md](references/跨工具团队实践.md)、[references/文档生命周期与压缩.md](references/文档生命周期与压缩.md) 与 [references/跨项目共享模式提炼.md](references/跨项目共享模式提炼.md)，并同步细化主技能中的对应路由。
- 将带内部项目名的 routed reference 去专案化，同时上提 [references/跨项目共享模式提炼.md](references/跨项目共享模式提炼.md) 作为公开执行面的通用共享模式文件。
- 将研究过程留痕、计划账本和内部案例材料下沉到本地忽略区，公开树只保留可发布的技能、参考件和说明文档。
- 扩展 [SKILL.md](SKILL.md)、[references/治理模式选择对照表.md](references/治理模式选择对照表.md)、[docs/完整说明书.md](docs/完整说明书.md) 与 [docs/语言体系规范.md](docs/语言体系规范.md)，把“运行态叠加模式”“开发回路 / 运营回路”“运行观察”等中文主叫法和开发/运营双治理判断正式写清，并明确运营信号不能直接改写开发真源、技能沉淀不能自动晋升。
- 扩展 [SKILL.md](SKILL.md)、[references/经典治理流程库.md](references/经典治理流程库.md)、[references/输出约定.md](references/输出约定.md) 与 [README.md](README.md)，把 gate 失效收编为正式治理问题：补入 `route_gate -> evidence_gate -> write_gate -> stop_gate` 条件流程，并为正式输出增加“关口硬化方案”区块。
- 扩展 [README.md](README.md)，把 `schemas/` 正式纳入仓库职责分工与阅读路径，使 JSON 合同草案不再是游离实现尝试。
- 扩展 [SKILL.md](SKILL.md)、[references/结构家族定位约定.md](references/结构家族定位约定.md)、[references/官方读取顺序.md](references/官方读取顺序.md)、[references/跨层共享约定.md](references/跨层共享约定.md) 与 [references/输出约定.md](references/输出约定.md)，把“合同真源优先、共置不等于归属、`execution_object/status_projection/display_projection` 的写权边界”正式接入主流程与正式输出。
- 新增 [docs/治理能力模型_v1_下一阶段执行计划.md](docs/治理能力模型_v1_下一阶段执行计划.md)、[workflow.state.schema.json](schemas/workflow.state.schema.json)、[workflow.event.schema.json](schemas/workflow.event.schema.json) 与 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py)，把下一阶段的 P0 主链正式落到实例 schema、`checks` 协议和最小 validator 骨架。
- 在 [workflow.contract.schema.json](schemas/workflow.contract.schema.json)、[schemas/README.md](schemas/README.md)、[docs/项目治理能力模型_v1.md](docs/项目治理能力模型_v1.md) 与 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py) 中冻结 approval 语义：`node.approver_ref` 指向 agent role，`transition.approval_ref` 指向 `approval_type` object，并把 validator 从“未冻结警告”升级为最小强校验。
- 在 [schemas/README.md](schemas/README.md)、[docs/项目治理能力模型_v1.md](docs/项目治理能力模型_v1.md)、[docs/治理能力模型_v1_下一阶段执行计划.md](docs/治理能力模型_v1_下一阶段执行计划.md) 与 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py) 中补入 `status_projection` 的最小技术限制，并把 smoke asset pack 升成下一条直接执行线。
- 继续收口 governed pack 的入口边界：将 project-level object 资产从 `schemas/*.json` 调整为 `objects/*.json`，并在 [README.md](README.md)、[schemas/README.md](schemas/README.md)、[docs/项目治理能力模型_v1.md](docs/项目治理能力模型_v1.md) 与 smoke pack 中同步更新。
- 将 workflow 的 `checks` 收口为 v1 的唯一注册面：保留 workflow 顶层 `checks.route/evidence/write/stop`，删除 node / transition 层重复 check refs。
- 调整 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py) 的 pack 入口语义：显式使用 `pack_root`，优先读取 `objects/`，补最小 policy/event 校验，并为 legacy `schemas/` 布局保留兼容 warning。
- 继续收紧 pack 合同语义：`workflow.agent_refs` 固定指向 `agent.contract.json.agent_id`，`node.approver_ref` 继续指向 `roles[].role_id`，`workflow.events.jsonl.subject_ref` 固定为 `node_id / transition_id`。
- 调整 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py) 与 CI，使 pack 文件开始执行真实 schema 校验，不再只依赖 JSON 语法和语义 smoke。
- 继续收紧 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py) 的 schema enforcement：补入 `date-time` format 检查，并为 `generated_at / timestamp` 增加对应回归测试。
- 调整 [docs/分支推进决策流程.md](docs/分支推进决策流程.md)，去掉会快速过期的硬编码提交数，改成以实时 Git 命令结果为准。

## v0.2.7 - 2026-03-25

### 新增

- 新增 [references/意图触发约定.md](references/意图触发约定.md)，把短口令驱动工作正式写成可迁移的上游约定。

### 调整

- 扩展 `SKILL.md`，把短口令驱动工作纳入正式治理问题。
- 扩展 `references/输出约定.md` 与 `references/场景手册.md`，让输出可以显式包含意图触发约定。
- 同步更新 `README.md`、`docs/完整说明书.md`、`docs/仓库元数据建议.md` 与 `agents/openai.yaml`。

## v0.2.6 - 2026-03-25

### 新增

- 新增 [references/说人话需求确认工具包.md](references/说人话需求确认工具包.md)，提供默认问题集、故事模板、测试模板和最小完成规则。

### 调整

- 扩展 `SKILL.md`，要求在边界不稳时先问问题、先起草故事和测试，再进入治理设计。
- 扩展 `references/起步阶段_故事与测试对齐.md`、`references/输出约定.md` 与 `references/理解把握度与澄清规则.md`。
- 同步更新 `README.md`、`docs/完整说明书.md`、`docs/仓库元数据建议.md` 与 `agents/openai.yaml`。

## v0.2.5 - 2026-03-25

### 新增

- 新增 [references/起步阶段_故事与测试对齐.md](references/起步阶段_故事与测试对齐.md)，把起步阶段的方向与边界确认前置。

### 调整

- 扩展 `SKILL.md` 与 `references/输出约定.md`，把方向与边界锚点变成正式前置步骤。
- 扩展 `references/理解把握度与澄清规则.md` 与 `references/场景手册.md`。
- 同步更新 `README.md`、`docs/完整说明书.md`、`docs/仓库元数据建议.md` 与 `agents/openai.yaml`。

## v0.2.4 - 2026-03-24

### 新增

- 新增 [references/文档生命周期与压缩.md](references/文档生命周期与压缩.md)，把文档生命周期与压缩治理显式化。
- 补充一份文档膨胀质询与收敛记录，用于当时的内部收口。

### 调整

- 扩展 `SKILL.md`，把文档膨胀和读取成本纳入诊断维度。
- 扩展 `references/输出约定.md`、`references/经典治理流程库.md` 与 `references/场景手册.md`。
- 同步更新 `README.md`、`docs/完整说明书.md` 与 `docs/仓库元数据建议.md`。

## v0.2.3 - 2026-03-24

### 调整

- 把 `SKILL.md` 与 `references/输出约定.md` 的默认输出改成“核心必答 + 条件展开”。
- 同步更新 `README.md`、`docs/完整说明书.md`、`docs/仓库元数据建议.md` 与 `agents/openai.yaml`。

## v0.2.2 - 2026-03-24

### 新增

- 新增 [references/理解把握度与澄清规则.md](references/理解把握度与澄清规则.md)。

### 调整

- 扩展 `SKILL.md`，把理解把握度和澄清提问前置。
- 同步补齐 `OpenClaw` 在多工具适配语境中的定位。
- 扩展 `references/输出约定.md`、`references/基本原则.md`、`references/工具适配对照表.md`、`references/官方读取顺序.md` 与 `references/跨层共享约定.md`。

## v0.2.1 - 2026-03-24

### 新增

- 新增 [references/结构家族定位约定.md](references/结构家族定位约定.md)。
- 新增 [references/官方读取顺序.md](references/官方读取顺序.md)。
- 新增 [references/工具适配对照表.md](references/工具适配对照表.md)。

### 调整

- 扩展 `SKILL.md`、`README.md`、`docs/完整说明书.md`、`references/输出约定.md` 与 `references/基本原则.md`，把结构定位、读取顺序和工具适配正式写清。

## v0.2.0 - 2026-03-24

### 新增

- 新增 [references/经典治理流程库.md](references/经典治理流程库.md)，把可复用流程库正式化。
- 新增 [references/反方质询与收敛回路.md](references/反方质询与收敛回路.md)，把反方质询与收敛机制显式化。

### 调整

- 把 `SKILL.md` 从“只谈结构”升级成“结构 + 流程”的技能。
- 扩展输出约定与场景手册，使其能推荐默认流程和条件流程。
- 同步更新 `README.md`、`docs/完整说明书.md`、`docs/仓库元数据建议.md` 与 `agents/openai.yaml`。

## v0.1.0 - 2026-03-24

### 新增

- 首次公开发布 `files-driven`。
- 提供基本原则、治理模式对照表、跨层共享约定、输出约定、场景手册和多工具团队实践等基础文档。
