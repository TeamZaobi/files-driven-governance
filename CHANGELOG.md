# 更新记录

本文记录 `files-driven` 的仓库层面重要变更。
它只负责记账：新增了什么、调整了什么、删掉了什么。
某一版为什么重要、改变了什么理解或使用方式，交给对应的 `docs/v*_版本说明.md`。

## Unreleased

### 新增

- 新增 [docs/语言体系规范.md](docs/语言体系规范.md)，把“中文优先、必要时补稳定键名”正式写成仓库级语言规范，用来约束后续 README、技能说明和参考件的写法。
- 新增开发/运营并存治理的显式表达：在 [references/经典治理流程库.md](references/经典治理流程库.md) 中补入“运营信号分流”和“运行观察晋升关口”两条条件流程，在 [references/输出约定.md](references/输出约定.md) 中补入“开发/运营双治理结构”条件区块。
- 新增 [references/关口硬化与稳定放行.md](references/关口硬化与稳定放行.md)，把“该停没停、该问没问、`partial / blocked` 无法约束下游”正式收编成可复用的治理问题，并提供最小稳定解。
- 新增 [docs/项目治理能力模型_v1.md](docs/项目治理能力模型_v1.md)，把本轮重构对象正式上提为“项目治理设计能力”，而不只是一轮仓库文案调整。
- 新增 [schemas/README.md](schemas/README.md) 与四份 schema 草案： [workflow.contract.schema.json](schemas/workflow.contract.schema.json)、[object.contract.schema.json](schemas/object.contract.schema.json)、[policy.contract.schema.json](schemas/policy.contract.schema.json)、[agent.contract.schema.json](schemas/agent.contract.schema.json)。
- 新增 `gate_state` 的 canonical 三态冻结：在 [workflow.state.schema.json](schemas/workflow.state.schema.json)、[workflow.event.schema.json](schemas/workflow.event.schema.json) 与 [references/关口硬化与稳定放行.md](references/关口硬化与稳定放行.md) 中把最小枚举正式收口为 `blocked / partial / ready`。

### 调整

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
