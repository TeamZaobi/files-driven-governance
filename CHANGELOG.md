# 更新记录

本文记录 `files-driven` 的仓库层面重要变更。
它只负责记账：新增了什么、调整了什么、删掉了什么。
某一版为什么重要、改变了什么理解或使用方式，交给对应的 `docs/v*_版本说明.md`。

## Unreleased

### 新增

- 新增 [docs/语言体系规范.md](docs/语言体系规范.md)，把“中文优先、必要时补稳定键名”正式写成仓库级语言规范，用来约束后续 README、技能说明和参考件的写法。

### 调整

- 统一 `docs/` 与 `references/` 主要文档的中文命名与中文表达，替换早期英文文件名和中英混写表述，并同步修正仓库内链接与对外包装文案。
- 重写 [README.md](README.md)，把仓库入口改成面向人的项目说明，补充适用场景、不适用场景、首次阅读路线，以及 `README`、`SKILL`、`references`、`CHANGELOG`、版本说明之间的职责分工。
- 在 [README.md](README.md) 中补入 `mermaid` 图示，用可视化方式解释文档分层、治理流程和常见失真模式。
- 在 [README.md](README.md) 中补入简版“版本演进”脉络，作为理解入口；同时明确由 [CHANGELOG.md](CHANGELOG.md) 负责变更账本、由 `docs/v*_版本说明.md` 负责单版解读。

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
- 新增 [docs/文档膨胀质询记录_第1轮.md](docs/文档膨胀质询记录_第1轮.md)，记录第一轮文档膨胀质询与收敛。

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
