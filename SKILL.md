---
name: files-driven
description: 用于 AI、多代理和文档密集项目的结构治理与收口设计：判断真源、结构家族、四层分层、协作关口与恢复链，适用于现有仓库诊断、新项目搭建和漂移重整；必要时补跨层共享、短口令约定和解释型摩擦处理。
---

# 文档驱动治理（files-driven）

## 核心定位

把文档当成项目治理的承载介质，而不是被动备注。
对“全员通过 AI 工具工作 + 项目级规则文件跟仓共享 + Git 目录级全量共享”的项目，
默认先把多人协作理解成共享存储问题。
这个技能主要回答三类问题：

1. 项目的事实到底写在哪
2. 哪些文件在定义事实，哪些只是在推进执行、总结状态或对外展示
3. 多人、多代理、多工具并行时，谁先读、谁能写、谁负责复核与恢复

适用场景：

- 现有仓库开始出现规则、流程、状态页和说明页互相漂移
- 新项目需要一套够用但不过重的治理结构
- 项目已经失真，需要先止血、再收口、再重整
- governed pack 或 harness 需要从 prose-first 说明推进到最小可执行合同链
- 议题还没到 `task / decision`，需要判断 discussion 何时收口、何时晋升

## 默认主路径

### 1. 先定起点与边界

先判断当前问题属于哪个起点：

- `existing_repo`
- `greenfield`
- `recovery_or_realignment`

如果情况是混合的，优先按用户眼下最急的问题判断。

在讨论目录、角色或流程之前，先锁一个最小“方向与边界锚点”。
至少要明确：

1. 首批真实使用场景
2. 首批交付物
3. 一到三个核心用户故事
4. 三到八个验收或测试用例，至少包含一个失败或越界边界
5. 明确不做的范围
6. 仅用于校准质量的参考对象
7. 由谁来判断这次算不算达标

处理规则：

- 把握度 `low`，或边界还在漂移时，先问一到三个短问题，不要提前给完整蓝图
- 先问使用场景、交付预期、成功标准和非目标，再问工具和目录
- governed pack / harness 话题里，默认把 `BOUNDARY.md` 当作 pack 级第一入口，再看 workflow 合同

边界还不稳时，优先读：

- [起步阶段：故事与测试对齐](references/起步阶段_故事与测试对齐.md)
- [说人话需求确认工具包](references/说人话需求确认工具包.md)

### 2. 只画四层与真源

默认先把文档系统按四层看清：

1. `truth_source`
2. `execution_object`
3. `status_projection`
4. `display_projection`

至少回答三件事：

1. 当前可信真源在哪里
2. 哪些文件在推进执行、承载实例或记录过程
3. 哪些文件只是摘要、恢复入口或展示出口

只有在它会改变责任边界、工具适配或机读合同设计时，
再补可选 `source_kind` 标签：

- `policy_or_rules`
- `object`
- `workflow`
- `skill`
- `agent`

硬约束：

- `status_projection` 与 `display_projection` 只做派生、摘要或展示，不生成新的 `allowed_next_steps`、放行结论或权限语义
- runtime、程序和工具入口是适配面，不是真源；仓库内被多个 runtime 共同读取、且实际定义执行边界或读写约束的项目级规则文件，才属于真源
- 优先以仓库文件为准，不以对话记忆为准；仓库证据不完整时，要显式区分证据和推断

### 3. 判断当前主要失真

只点出真正驱动建议的几个压力，不要把所有框架都过一遍。
常见信号包括：

- 边界或验收标准漂移
- 重复真源或版本锚点不清
- `status_projection` / `display_projection` 越权
- 读取顺序不清，接手恢复成本高
- workflow 仍停留在 prose-first，harness / validator 难以稳定消费
- discussion 长期停在聊天层，晋升路径不清
- “继续开发 / 开始审计 / 推进 / 讲解一下” 这类短口令反复滑路
- 多工具过程已经不透明，handoff 只能靠聊天补叙

必要时再问自己：

1. 这次问题主要卡在边界、真源、控制还是恢复
2. 哪个上游文件一旦看错，会把错误往下游传播
3. 现在最该先止血的漂移面是什么

### 4. 给出最小动作

正式回答时，默认只给有先后顺序的最小动作，不默认展开全套治理编制。

常见顺序：

- `existing_repo`
  - 先找真源与摘要页
  - 再标出越权投影和写权边界
  - 先止漂移，再修命名和目录
- `greenfield`
  - 先锁方向与边界
  - 再定最小真源和一条恢复入口
  - 只在需要时补 governed pack / harness / discussion 分支
- `recovery_or_realignment`
  - 先止血
  - 选定当前可信事实
  - 降级旧摘要页和旧展示页
  - 恢复责任边界与交接链

## 条件升级包

### A. AI-Native 同构团队与跨层共享

只有在多人、多代理或多工具会碰同一组事实时，再升级成共享设计。
优先判断：

1. 共享仓库根路径
2. 项目级规则文件集合及优先级
3. 哪些路径允许直接写
4. 哪些路径只能生成、复核或展示
5. 冲突时按什么规则处理

全员通过 AI 工具工作、并在 Git 上目录级全量共享时，先读：

- [AI-Native 同构团队协作](references/AI-Native同构团队协作.md)
- [跨层共享约定](references/跨层共享约定.md)

### B. governed pack / harness / 受控 workflow

出现以下话题时启用：

- `BOUNDARY.md`
- `workflow.contract.json`
- `objects/*.json`
- `workflow.state.json`
- `workflow.events.jsonl`
- `status.projection.json`
- validator、CI、hook、check、harness

最小受控链默认是：

1. `BOUNDARY.md`
2. `workflow.contract.json`
3. `objects/*.json`
4. `rules.contract.json` + `agent.contract.json`
5. `workflow.state.json` / `workflow.events.jsonl`
6. 可选 `status.projection.json`

这里要记住：

- `WORKFLOW.md` 是解释层，`workflow.contract.json` 才是受控模式下的机读控制真源
- workflow 顶层 `checks` 只按 `route / evidence / write / stop` 注册检查入口，不授予放行权
- validator 与 CI 是确定性执行面，不是所有 skill 调用时都要预加载的默认心智路径

需要时读：

- [QUICKSTART.md](QUICKSTART.md)
- [MIGRATION.md](MIGRATION.md)
- [schemas/README.md](schemas/README.md)
- [examples/smoke-governed-review/README.md](examples/smoke-governed-review/README.md)

### C. discussion 收口与晋升

当议题还没到 `task / decision`，或争议已经影响关键决策时启用。
默认主路径是：

`discussion -> decision_package -> task_or_decision`

只在以下情况再升级：

- 争议已经影响关键决策，且需要制度化反方视角：升级到 adversarial inquiry
- 多工具各自保留 trace，但人和下游 agent 需要统一接手面：补 `process_projection`

需要时读：

- [讨论收口与晋升](references/讨论收口与晋升.md)
- [examples/discussion-decision-task/README.md](examples/discussion-decision-task/README.md)
- [examples/adversarial-convergence/README.md](examples/adversarial-convergence/README.md)
- [examples/multi-tool-process-projection/README.md](examples/multi-tool-process-projection/README.md)

### D. 关口硬化

只有在这类故障反复出现时，才补完整关口包：

1. 该停没停
2. 该问没问
3. `partial / blocked` 已经判出，却仍继续下游动作
4. 短口令会在 `audit / explain / design / modify / publish` 之间滑动

最小硬化对象仍按：

1. `route_gate`
2. `evidence_gate`
3. `write_gate`
4. `stop_gate`

偶发失误、低风险、单人一次性任务，先补轻量澄清和最小读取顺序，不必立刻上完整硬化包。

需要时读：

- [关口硬化与稳定放行](references/关口硬化与稳定放行.md)

### E. 短口令与理解型输入

如果对话里反复出现“讲解一下”“再检查一下”“我还是担心”这类解释型摩擦，
或者项目已经决定用“继续开发”“开始审计”“推进”这类短口令做稳定入口，
再启用这一包。

先区分：

1. `understanding`
2. `constraint`
3. `evidence`
4. `decision`

只有项目真的要把短口令做成稳定入口时，再做显式约定，而不是聊天默契。

需要时读：

- [理解型输入与低带宽压缩包](references/理解型输入与低带宽压缩包.md)
- [意图触发约定](references/意图触发约定.md)

### F. 官方读取顺序与恢复

只有在以下情况再下钻读取顺序和恢复件：

- 真源入口不清
- 版本锚点不清
- 新接手者无法在短时间恢复现场
- 项目已经漂移到需要先止血、再重整

原则是：

- 先读能完成当前判断的最短入口
- 不要默认全仓库通读
- 不要把摘要页当真源

需要时读：

- [官方读取顺序](references/官方读取顺序.md)
- [场景手册](references/场景手册.md)
- [文档生命周期与压缩](references/文档生命周期与压缩.md)

## 默认回答骨架

正式回答时，默认用最小骨架组织：

1. 边界与假设
2. 四层与真源
3. 当前主要失真
4. 下一步一到三条动作

规则：

- 把握度 `medium`，明确写出关键假设
- 把握度 `low`，先问问题，再给最小建议
- 只有命中条件升级包时，才附加 governed pack / harness、discussion、共享、gate 或读取顺序区块

更细的回答组织规则，读：

- [输出约定](references/输出约定.md)

## 按问题读哪个参考件

- 边界还不稳：读 [起步阶段：故事与测试对齐](references/起步阶段_故事与测试对齐.md)、[说人话需求确认工具包](references/说人话需求确认工具包.md)
- 需要判断是先提问、先假设还是先给最小建议：读 [理解把握度与澄清规则](references/理解把握度与澄清规则.md)
- 需要固定正式回答形状：读 [输出约定](references/输出约定.md)
- 需要判断共享存储、跨层写权和多工具协作：读 [AI-Native 同构团队协作](references/AI-Native同构团队协作.md)、[跨层共享约定](references/跨层共享约定.md)
- governed pack / harness / workflow 合同化：读 [QUICKSTART.md](QUICKSTART.md)、[MIGRATION.md](MIGRATION.md)、[schemas/README.md](schemas/README.md)
- 议题还没到 `task / decision`，或要判断是否升级到质询 / process projection：读 [讨论收口与晋升](references/讨论收口与晋升.md) 和相关 examples
- 已出现越级动作、提前改写、`partial / blocked` 无法约束下游时：读 [关口硬化与稳定放行](references/关口硬化与稳定放行.md)
- 真源入口不清、恢复困难或历史页堆积：读 [官方读取顺序](references/官方读取顺序.md)、[场景手册](references/场景手册.md)、[文档生命周期与压缩](references/文档生命周期与压缩.md)

## 边界约束

- 先诊断，再开药方
- 边界先于设计，`BOUNDARY.md` 先于 governed pack workflow 合同
- 真源清晰度优先于目录外观
- `status_projection` 必须保持轻、保持可追溯
- 不要让投影层反向改写真源
- 不要让 `discussion` 长期兼任任务桶
- 不要让 `Agent`、`Skill`、`Workflow`、`Object` 互相改义
- 不要让工具品牌变成项目角色
- 没到必要程度，不要默认上重变更控制
- 不要把看似解释型追问自动归成低价值理解同步

## 示例请求

- “分析这个多代理仓库的现有文档体系，判断哪些文件是真源，哪些只是状态摘要，并给出收口方案。”
- “我要做一个 AI Agent 驱动的 OpenClaw 项目，请给我一套早期够用、后续还能扩展的文档治理结构。”
- “这个项目的 README、状态页、任务和流程说明已经互相漂移，请判断主要问题和修复顺序。”
- “这个项目很多机制争议都讲不清，请判断哪些话题需要进入反方质询、最小决策包或验证链，哪些保持轻量处理。”
- “我们要把 workflow 从 prose-first 说明推进成 harness 可消费的最小合同链，请判断 `BOUNDARY.md`、`workflow.contract.json`、`workflow.state.json`、`workflow.events.jsonl` 和 validator 应该怎么配。”
- “这个议题还没到 task 或 decision，请判断是继续 discussion、升级到质询，还是压成 decision package。”
- “多个工具各自保留 trace，但我需要统一 handoff 面，请判断是否该补 `process_projection` 或 `topology_supplement`。”
- “团队总把 Codex / Claude Code / AntiGravity 的品牌差异当成治理问题，请按共享存储视角重画真源、读取顺序和写权边界。”
