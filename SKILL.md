---
name: files-driven
description: 用于 AI-Native / AI-Driven 项目的最小治理与收口：当交付被真源不清、写权失控、投影越权、证据冲突、跨仓 / live / release 风险或重复文书阻断时使用。默认先用奥卡姆剃刀判断能否直接交付、融合现有真源、归档历史、冻结活跃读取/调度权；删除只用于明显错误、未生效或无保留价值的对象。只有轻治理反复失败且需要恢复、回放或审计时，才升级到 workflow / runner / 合同化控制面。
---

# files-driven

## 核心定位

`files-driven` 面向 AI-Native / AI-Driven 项目，先帮助团队稳住真源、明确下一步、控制改动边界，并让 AI 协作过程可检查、可恢复。
在 skill-driven AI-Native 项目里，它默认先回答四件事：

1. 现在哪份文件算数
2. 今天先做哪一步
3. 哪些地方先别动
4. 这次到底需不需要更强控制

默认处理对象：交付阻断、真源、写权、证据、恢复口；规则、文档、状态、流程和工具入口只在它们正在阻断交付时才成为治理对象。
默认治理目标：用最少控制恢复交付，并让过程可检查、可恢复。
进入多人、多代理、多工具协作后，再把问题收口到共享存储上的事实、写权和恢复治理。

When not to use: if the task is ordinary implementation, product content design, skill lifecycle maintenance, visual generation, or a simple tool operation with no truth-source / write-right / evidence risk, handoff to the product, skill, visual, engineering, or direct tool owner.

第一性原理：帮助用户识别问题，解决问题。
长期路线：用最小充分控制保护交付；只有轻控制反复失败时才强化控制。
当前实现策略：优先复用宿主原生能力；控制面外移、`Workflow` 脚本化、`CLI` backend 化只作为高风险或反复失稳时的例外补强，不是默认路径。

奥卡姆剃刀优先级：直接交付 / 融合到现有真源 / 归档为历史证据 / 冻结活跃读取或调度权 / 删除明显错误或未生效对象，优先于新建文件、状态、gate、workflow、runner 或控制面。治理的成功标准是交付更快、更少误读、更少回滚，不是流程更完整。
这里的“瘦身”不是按字数删薄，也不是把边界说明赶出真源；要压缩的是活跃真源数量、重复读取链和越权调度信号。边界可以讲，只要它服务于守住写口、停止线或责任归属。处理一段材料时，先判它是否应保留在当前真源、融合回其他已有真源、归档为历史，或冻结活跃读取 / 调度权；删除只作为最后手段。

FilesStuck 防护：如果一轮治理只新增文档、verdict、packet、index、dashboard 或 prompt 文案，却没有改变交付状态、实现准入、测试证据或唯一阻断对象，默认判为无效治理；下一步只能是 `open_implementation`、`blocked_one_evidence`、`no_more_docs`、融合 / 归档 / 冻结 / 删除或暂停。

### 低熵因果治理承接口

当 `MyWay` 以“低熵因果治理”把项目治理交给 `files-driven` 时，`files-driven` 不重写产品、架构或计划因果链。
它只把上游因果判断落成真源、写权、读取链、证据和恢复口的治理动作。

默认治理链：

`真实阻断 -> 活跃真源 -> 写权 / 读取权 -> 最小治理动作 -> 证据 / 恢复口`

执行约束：

1. 如果真实痛点、需求覆盖或产品定义还没说清，先回指 `ProEng / product-engineer` 或上游真源，不用治理规则替代产品判断。
2. 如果问题只是 skill live source、投影同步、上游 pin 或多宿主发现，交给 `skills-master`，不把 skill 生命周期吞进项目治理。
3. 如果已有真源能承接，优先融合；如果旧材料只剩历史价值，归档；如果旧入口仍会误导读取或调度，冻结；删除只处理明显错误、未生效或无保留价值的对象。
4. 新增文件、状态、`gate`、workflow、runner 或控制面，必须说明它减少了哪类漂移、误交付、恢复风险或证据缺口。

## 能力真源与版本边界

本仓同时是 `reference implementation + regression fixture`。底层能力模型的唯一真源是 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)；`SKILL.md` 只做执行导览，不与真源平行定义本体。

够用记法：

- `v1`：真源、投影、合同化和执行实例分层。
- `v2`：`files-driven` 做项目总监式分诊，不默认接管交付。
- `v2.1`：作用域绑定与防变形。
- governed pack / contract 侧仍可冻结在 `tranche v1`；不要把合同冻结语义误读成世界观回退。

## 最小主路径

先按三路分诊：

1. `bypass`：普通开发、debug、测试、单文件编辑、工具操作或上下文足够清楚时，直接做。
2. `delivery_guard`：交付受真源、写权、证据或边界影响时，只给最小交付卡：能做什么、能改哪里、怎么验证、不能声称什么、何时升级。
3. `governance_repair`：真源漂移、重复文书、投影越权、跨仓 / live / release 风险或连续浅交付时，先融合、归档、冻结读取 / 调度权或修现有入口。

正式治理只问三件事：

1. 现在要交付什么？
2. 哪份真源、写权或证据影响它？
3. 最小下一步是直接做、融合 / 归档 / 冻结、修现有文件，还是必须升级？

动作顺序：

`直接交付 / 测试 / 唯一阻断对象 -> 保留必要边界 -> 融合 -> 归档 -> 冻结 -> 修改现有文件 -> 删除明显错误 -> 新建 / 迁移 / 拆分 / 合并 -> 修改规则 -> 抽离方法 -> governed pack`

作用域只在影响判断时标明：

- `capability_scope`：`files-driven` 自己的能力仓资产。
- `project_scope`：被治理项目的规则、实体、写权和漂移状态。
- `runtime_scope`：当前会话、工具、代理和临时恢复缓存。

## 归属与分层判断

规则类问题先判约束载体：

- `runtime_global_rules`：执行者本地默认值。
- `repo_project_rules`：项目共享规则。
- `subtree_or_pack_rules`：局部 pack 细化，不改写上层语义。
- `adapter_surface` / `projection_or_handoff`：适配或投影，不偷权。

再判规则强度：

- `薄入口提醒`：入口文件。
- `方法规则`：项目 `Skill`。
- `边界规则`：项目规则或 `BOUNDARY.md`。
- `合同规则`：`workflow.contract.json`、schema、validator 或 hook。

项目对象默认四类：

1. `入口规则`
2. `能力规则`
3. `项目规则`
4. `项目实体`

事实分层默认四类：

1. `truth_source`
2. `execution_object`
3. `status_projection`
4. `display_projection`

投影只能摘要、恢复或展示，不能生成新的放行结论、权限语义或 allowed next steps。完整说明见 [docs/完整说明书.md](docs/完整说明书.md) 与 [作用域绑定与防变形规则](references/作用域绑定与防变形规则.md)。

## 工具、sidecar 与知识宿主

工具引入先做 `tool intake`，不是直接安装：

`job -> known practice -> scope -> role -> truth/write -> posture -> validation/rollback`

如果只是正常调用已有 skill 且不改变项目真源、写权或流程合同，不升级成治理议题。需要安装、链接、上游 pin、薄适配或宿主发现验证时交给 `skills-master`；影响项目事实、写权、流程、恢复或审计时才由 `files-driven` 收口。详细见 [工具引入思考栈](references/工具引入思考栈.md)。

`MyWay` 可选择 `Superpowers / GSD / gstack / Archon` 等 sidecar，但 sidecar 输出进入项目事实、写权、流程合同或审计链时，主 owner 切到 `files-driven`。`files-driven` 治理的是接口，不吸收 sidecar 上游实现。详细见 [myway-sidecar-governance.md](references/myway-sidecar-governance.md)。

Obsidian、Notion、Docs、Sheets、Slides 先当宿主名处理；只有用户实际在问真源、写权、投影、漂移、恢复或读取顺序时，才按治理问题处理。具体编辑请求不误吞成治理请求。

## 条件升级包

只在命中条件时读取对应 reference，不把全套升级包带入每轮：

- 边界不稳、需要说人话确认：读 [起步阶段：故事与测试对齐](references/起步阶段_故事与测试对齐.md)、[说人话需求确认工具包](references/说人话需求确认工具包.md)。
- 判断问题在哪里、该上多强控制：读 [问题诊断与控制强度分级](references/问题诊断与控制强度分级.md)。
- 主线程 / `subagent` / `CLI` / runner 分工：读 [执行面判定与CLI生产策略](references/执行面判定与CLI生产策略.md)。
- 多人、多代理、多工具共享资产：读 [AI-Native同构团队协作.md](references/AI-Native同构团队协作.md)、[跨层共享约定](references/跨层共享约定.md)。
- 多规则、多工具入口精准修改：读 [多规则工具治理与精准修改协议](references/多规则工具治理与精准修改协议.md)。
- governed pack / harness / workflow 合同化：普通任务只需边界句、可执行检查和 rollback；只有机器恢复、多人并发、正式迁移或重复失败复盘时，才补 `BOUNDARY.md -> workflow.contract.json -> objects/*.json -> state/events`，详见 [QUICKSTART.md](QUICKSTART.md)、[MIGRATION.md](MIGRATION.md)、[schemas/README.md](schemas/README.md)。
- discussion 收口、反方质询或 process projection：读 [讨论收口与晋升](references/讨论收口与晋升.md)。
- 运行观察、候选保留和能力晋升：读 [运行观察与能力晋升](references/运行观察与能力晋升.md)。
- 关口硬化：只有 `partial/blocked` 仍被下游继续消费、该停没停或短口令漂移反复出现时，读 [关口硬化与稳定放行](references/关口硬化与稳定放行.md)。
- 短口令与低带宽解释：读 [理解型输入与低带宽压缩包](references/理解型输入与低带宽压缩包.md)、[意图触发约定](references/意图触发约定.md)。
- 真源入口、版本锚点、恢复困难：读 [官方读取顺序](references/官方读取顺序.md)、[场景手册](references/场景手册.md)、[文档生命周期与压缩](references/文档生命周期与压缩.md)。
- `files-driven` 安装进下游项目：读 [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md) 与 starter / validator。
- 反向检查能力模型是否照进入口、手册和 metadata：读 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)、[docs/三层信息架构复盘.md](docs/三层信息架构复盘.md)。
- AI-Native / skill-driven E2E 验收：读 [docs/AI-Native与Skill驱动E2E验收矩阵.md](docs/AI-Native与Skill驱动E2E验收矩阵.md)。
- 心跳、trigger、自动唤醒：先用 `heartbeat` skill 定义 Agent 角色和 trigger contract，再由本 skill 判断真源、写权、证据、恢复和审计边界。

## 默认回答骨架

正式回答默认用最小骨架：

1. 结论
2. 最小动作
3. 验证证据
4. 停止线

把握度 `low` 时先问 1 到 3 个短问题；把握度 `medium` 时写明关键假设。只有治理边界确实阻断动作时，才展开作用域、四层、目录或升级包。面向非工程读者时，先翻译成“哪份文件算数 / 这次先做什么 / 哪些先别改”。

## 边界约束

- 先诊断，再开药方。
- 边界先于设计，`BOUNDARY.md` 先于 governed pack workflow 合同。
- 真源清晰度优先于目录外观；投影不能反向改写真源。
- `Agent`、`Skill`、`Workflow`、`Object` 不互相改义。
- 不把工具品牌变成项目角色，不把“引入工具”直接等同于全局安装或写 adapter。
- 明明有官方手册、用户手册和成熟社区实践时，不在本地反复造未验证方案。
- 没到必要程度，不默认上重变更控制。
