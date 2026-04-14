---
name: files-driven
description: 用于 skill 驱动 AI-Native 项目的治理与收口设计：当前治理模型默认口径为 v2 项目总监世界观与 v2.1 作用域绑定规则；作为元 skill，它把 install / register / repair / audit 放在首屏，其中 audit 当前默认是脚手架基础体检，并通过 bootstrap + [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 帮下游项目装起 files engine；self-hosting 时也可通过 `capability-improve` 把能力改善 workflow 路由到脚本调度 + Codex CLI 节点执行；先判当前 scope，再在工作对象层判断入口规则、能力规则、项目规则、项目实体，按需补四层分层、结构家族、协作关口与恢复链。
---

# files-driven

## 核心定位

`files-driven` 不再把自己写成“结构治理顾问”。
在 skill-driven AI-Native 项目里，它先做项目总监替身，并在本仓库上同时扮演 `reference implementation + regression fixture`：
先判谁持有能力、谁承载项目事实、哪些规则必须运行时直接生效、当前动作该走哪个关口，
然后才下钻四层、结构家族、共享关系和恢复链。

这项能力的第一性原理不是把所有流程都脚本化，
而是帮助用户识别问题，解决问题。
长期路线是强化控制能力；
控制面外移、`Workflow` 脚本化、`CLI` backend 化，都是当前阶段为解决“复杂流程靠 LLM 内部对话流转时控制不稳”而采用的实现策略，不是长期本体。

底层能力模型的唯一真源只有 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。
`SKILL.md` 只负责执行导览，不与真源平行定义本体。

版本轴必须分开记：

1. 能力模型 `v1 -> v2 -> v2.1`
2. governed pack / contract `tranche v1`

像 `checks.route / evidence / write / stop`、`workflow.events.jsonl.subject_ref` 这类冻结语义，默认都属于后者。

当前治理模型口径：

1. `v1`：先解决真源、投影、合同化和执行实例怎么分层落盘
2. `v2`：`files-driven = 项目总监`
3. `v2.1`：在 `v2` 之上补 `作用域绑定与防变形规则`

当前版本的默认执行优先级：

1. 先判断用户真正要解决什么问题，以及当前需要多强控制
2. 宿主原生 `workflow / subagents / approvals` 足够时优先复用
3. 只有当复杂流程需要编排、恢复、回放、审计，或宿主能力暂时兜不住时，才启用脚本 runner 和 `CLI` 节点执行

这里按三条判断轴直接讲方法：

1. 世界观轴：`v1 -> v2 -> v2.1`
   - 先看清谁持有能力、谁承载事实、谁在治理谁
2. 控制强度轴：`L0 -> L4`
   - 再判断当前问题到底需要多强控制
3. 执行面轴：主线程 / `subagent` / 宿主 workflow / `CLI` / runner
   - 最后再决定具体由谁执行、怎样执行

默认顺序：

1. 先用世界观轴看清对象和边界
2. 再用控制强度轴判断该上多强控制
3. 最后才用执行面轴分配宿主、`CLI`、runner 的职责

## 首屏动作

对下游项目，默认先回答四个动作：

1. `install`
2. `register`
3. `repair`
4. `audit`

其中 `install` 通过 bootstrap 完成；`register / repair / audit` 通过统一 `manage` CLI 完成。
当前 `audit` 默认先解释成脚手架“基础体检”：
它先检查 starter、registry、route 和 profile 这条最小资产链是否闭环，
不直接冒充对下游项目的全量系统体检。

对下游项目，上面四个动作仍是默认首屏入口。
但当治理对象正好是 `files-driven` 自己，且用户明确要求把当前 workflow 改成“脚本调度 + Codex CLI 节点执行”的受控 run 时，
不要继续停在 prompt-only 解释层；
应改走 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 的 `capability-improve` 子命令，
由 [scripts/run_project_director_capability_improvement.py](scripts/run_project_director_capability_improvement.py) 维护 `workflow.state.json`、`workflow.events.jsonl`、`status.projection.json`，
让 `Codex CLI` 只写当前节点产物。

如果使用者明显几乎没有软件工程基础，
不要先把 `scope`、`projection`、`tranche`、`harness` 这些词扔给他。
首屏先压成 3 句工作语言：

1. 现在哪份文件算数
2. 今天先做哪一步
3. 哪些文件先别改

默认工作对象是：

1. 项目里的作家 `Skill`、`Coder Skill` 和其他项目 `Skill`
2. 这些 `Skill` 正在生产和维护的小说、软件、任务实例、状态页和展示页

对“全员通过 AI 工具工作 + 项目级规则文件跟仓共享 + Git 目录级全量共享”的项目，
默认先把治理问题理解成：

1. 入口规则该放哪，怎样保证每轮都能看见
2. 哪些内容属于 `Skill` 这个能力主容器
3. 哪些内容属于当前项目自己的规则和实体
4. 哪个动作应该先判归属、再落盘、判不清就升级

一句话原则：

**具体能力归 Skill，项目内容归实体。**

适用场景：

- 现有仓库开始出现规则、流程、状态页和说明页互相漂移
- 新项目需要一套够用但不过重的治理结构
- 项目已经失真，需要先止血、再收口、再重整
- governed pack 或 harness 需要从 prose-first 说明推进到最小可执行合同链
- 议题还没到 `task / decision`，需要判断 discussion 何时收口、何时晋升

## 默认主路径

### 1. 先抓当前动作、当前作用域与一级关口

先不要急着讲目录、家族或总论。
先判断当前问题是被什么动作触发的、当前站在哪个作用域说话，以及它该先落在哪个一级关口：

- 新建文件
- 迁移文件
- 拆分文件
- 合并文件
- 修改规则
- 抽离方法
- 回写业务事实
- governed pack / harness 入口设计

如果情况复杂，再补当前起点：

- `existing_repo`
- `greenfield`
- `recovery_or_realignment`

默认优先回答：

1. 这次到底在处理什么动作
2. 当前在 `capability_scope`、`project_scope` 还是 `runtime_scope`
3. 先在哪个一级关口停手
4. 什么情况下升级到二级争议处理

三个默认作用域：

- `capability_scope`：`files-driven` 自己作为治理能力主容器，持有分类法、触发法、读取顺序、升级规则、schema、validator、template
- `project_scope`：被治理项目的作用域，持有项目 `Skill`、项目规则、项目实体、写权边界和漂移状态
- `runtime_scope`：当前会话、工具、代理的作用域，持有本轮路由判断、临时读取栈、派生图谱和恢复缓存

默认规则：

- 除非明确进入 `self-hosting`，下面的四分法默认描述 `project_scope`
- 当治理对象正好是 `files-driven` 自己时，要先显式声明 `self-hosting`，不要把能力仓资产和工作对象资产混成同一层

处理规则：

- 把握度 `low`，或边界还在漂移时，先问一到三个短问题，不要提前给完整蓝图
- 先问当前动作、交付预期、成功标准和非目标，再问工具和目录
- governed pack / harness 话题里，默认把 `BOUNDARY.md` 当作 pack 级第一入口，再看 workflow 合同

边界还不稳时，优先读：

- [起步阶段：故事与测试对齐](references/起步阶段_故事与测试对齐.md)
- [说人话需求确认工具包](references/说人话需求确认工具包.md)

### 2. 再判工作对象层的四个顶层归属

以后在 skill-driven 项目里，第一判断轴不是八大家族。
默认先判这四类归属。
这里默认描述的是 `project_scope`，也就是被治理对象层，而不是 `files-driven` 自己的能力仓资产：

1. `入口规则`
2. `能力规则`
3. `项目规则`
4. `项目实体`

判断要点：

- `入口规则`：每轮稳定携带、必须立即生效、长度必须克制
- `能力规则`：描述某个工作对象 `Skill` 怎么工作、怎么判断、怎么验证、怎么迁移；例如项目里的作家 `Skill`、`Coder Skill`
- `项目规则`：只对当前项目成立的业务法则、命名法、版本法或作品规程
- `项目实体`：项目现在是什么，包含事实、实例、候选稿、状态和展示

在 `project_scope` 里，项目 `Skill` 仍是工作对象，不是治理者本身。
它们作为能力对象，内部再承载：

- `agent`：执行角色面
- `workflow`：控制路径面
- `references`：能力资产面
- `scripts`：执行支持面
- `schemas` / checklist：规范与校验面

回答“这个东西放哪”时，默认先判它属于项目 `Skill` 还是属于项目实体，
再判断它究竟是规则、实例、状态还是展示。

### 3. 只在需要时补四层与二级结构标签

顶层归属判完后，再按四层看清当前材料的治理位置：

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

这里要明确：

- 八大家族保留，但降成二级观察标签，不再是首屏入口
- `execution_object / status_projection / display_projection` 在观察上仍成立，但治理落位上优先作为项目实体体系解释
- `status_projection` 与 `display_projection` 只做派生、摘要或展示，不生成新的 `allowed_next_steps`、放行结论或权限语义
- runtime、程序和工具入口是适配面，不是真源；仓库内被多个 runtime 共同读取、且实际定义执行边界或读写约束的项目级规则文件，才属于真源
- 同一文件跨作用域时，不要全局只贴一个身份；要按 `(scope, file_ref)` 判断
- 优先以仓库文件为准，不以对话记忆为准；仓库证据不完整时，要显式区分证据和推断

### 4. 给最小动作与升级口

正式回答时，默认只给有先后顺序的最小动作，不默认展开全套治理编制。
优先把建议写成：

`动作触发 -> 一级关口 -> 二级升级`

常见顺序：

- `existing_repo`
  - 先冻结当前动作的归属判断
  - 再标出真源、越权投影和写权边界
  - 先止漂移，再修命名和目录
- `greenfield`
  - 先锁方向与边界
  - 再定最小入口规则与 `Skill` 主容器
  - 最后补第一批项目规则和项目实体
- `recovery_or_realignment`
  - 先止血
  - 选定当前可信事实
  - 降级旧摘要页和旧展示页
  - 恢复责任边界与交接链

## 条件升级包

### A. Skill 主容器、共享存储与跨层共享

只有在多人、多代理或多工具会碰同一组能力资产或项目事实时，再升级成共享设计。
优先判断：

1. 共享仓库根路径
2. 哪些内容属于入口规则、能力规则、项目规则、项目实体
3. 项目级规则文件集合及优先级
4. 哪些路径允许直接写
5. 冲突时按什么规则处理

全员通过 AI 工具工作、并在 Git 上目录级全量共享时，先读：

- [AI-Native 同构团队协作](references/AI-Native同构团队协作.md)
- [跨层共享约定](references/跨层共享约定.md)

### A1. 多规则工具治理与精准修改

如果这次不是只做真源判断，而是要真正同步、升级、对齐或收口多工具 / 多层 rules，
再启用这一包。

先区分五类载体：

1. `runtime_global_rules`
2. `repo_project_rules`
3. `subtree_or_pack_rules`
4. `adapter_surface`
5. `projection_or_handoff`

执行要求：

1. 先盘点规则载体，不要找到一个入口就停止
2. 先判共同上游真源，再判这次改的是哪一层语义
3. 先改共享真源，再改局部例外、工具入口和投影
4. 交付前补一轮覆盖检查，确认没有遗留旧语义、旧优先级或漏改 sibling files

需要时读：

- [多规则工具治理与精准修改协议](references/多规则工具治理与精准修改协议.md)
- [AI-Native 同构团队协作](references/AI-Native同构团队协作.md)
- [工具适配对照表](references/工具适配对照表.md)
- [hooks使用方法论与脚手架](references/hooks使用方法论与脚手架.md)

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
- [examples/smoke-governed-review/BOUNDARY.md](examples/smoke-governed-review/BOUNDARY.md)
- [examples/smoke-governed-review/WORKFLOW.md](examples/smoke-governed-review/WORKFLOW.md)

### C. discussion 收口与晋升

当议题还没到 `task / decision`，或争议已经影响关键决策时启用。
默认主路径是：

`discussion -> decision_package -> task_or_decision`

只在以下情况再升级：

- 争议已经影响关键决策，且需要制度化反方视角：升级到 adversarial inquiry
- 多工具各自保留 trace，但人和下游 agent 需要统一接手面：补 `process_projection`

需要时读：

- [讨论收口与晋升](references/讨论收口与晋升.md)
- [examples/discussion-decision-task/BOUNDARY.md](examples/discussion-decision-task/BOUNDARY.md)
- [examples/discussion-decision-task/WORKFLOW.md](examples/discussion-decision-task/WORKFLOW.md)
- [examples/adversarial-convergence/README.md](examples/adversarial-convergence/README.md)
- [examples/multi-tool-process-projection/process-projection.md](examples/multi-tool-process-projection/process-projection.md)

### C1. 运行观察 / 候选保留 / 能力晋升

当运行中反复出现纠偏、失败样本、用户纠正或补救动作，且当前回合不能直接热改能力真源时启用。
默认主路径是：

`运行观察 -> 证据包 -> 历史召回 -> 拆分出口 -> 候选试验 -> 激活或回退`

这里要记住：

- 当前回合先保留 `runtime_scope` 里的观察，不直接热改 `capability_scope`
- 展示页可以说明“这轮准备怎么试”，但不能冒充正式激活真源
- 候选试验必须同时带 `failure_signals` 和 `rollback_path`
- 只有试验可判定、成功条件命中且回退路径已声明，才允许谈激活

需要时读：

- [运行观察与能力晋升](references/运行观察与能力晋升.md)
- [examples/capture-candidate-activation/README.md](examples/capture-candidate-activation/README.md)
- [examples/capture-candidate-activation/WORKFLOW.md](examples/capture-candidate-activation/WORKFLOW.md)
- [项目治理能力模型](docs/项目治理能力模型.md)
- [经典治理流程库](references/经典治理流程库.md)

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

如果对方明显缺少软件工程背景，
默认先不要把完整术语表当首屏解释。
先压成最小工作语言：

1. 现在哪份文件算数
2. 这次先做什么
3. 哪些文件先别改
4. 卡住时回看哪个入口

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
- [作用域绑定与防变形规则](references/作用域绑定与防变形规则.md)

### G. files engine starter / 元 skill 安装

当问题已经不再是“怎么维护现有仓库或现有 pack”，
而是“怎么把 `files-driven` 安装进一个下游项目”时启用这一包。

先区分 4 层：

1. `repo.files-driven`
2. `skill.files-driven`
3. `meta-skill capability`
4. `downstream project instance`

默认主路径是：

1. 先补边界、用户故事和失败边界
2. 再起官方 starter（bootstrap 只负责播种）
3. 再通过统一 `manage` CLI 执行 `register / repair / audit`
4. 先跑 scaffold validator，再跑 pack validator
5. starter 专属形状约束放在单独的 starter profile，不写进 manifest

需要时读：

- [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md)
- [starters/minimal-files-engine/README.md](starters/minimal-files-engine/README.md)
- [references/hooks使用方法论与脚手架.md](references/hooks使用方法论与脚手架.md)
- [scripts/bootstrap_files_engine_starter.py](scripts/bootstrap_files_engine_starter.py)
- [scripts/validate_files_engine_scaffold.py](scripts/validate_files_engine_scaffold.py)
- [schemas/README.md](schemas/README.md)

## 默认回答骨架

正式回答时，默认用最小骨架组织：

1. 当前动作与边界
2. 当前作用域与归属判断
3. 四层与越权投影
4. 下一步动作与升级口

规则：

- 把握度 `medium`，明确写出关键假设
- 把握度 `low`，先问问题，再给最小建议
- 先标当前在 `capability_scope`、`project_scope` 还是 `runtime_scope`
- 先回答当前动作应落哪一个一级关口，再谈四层、结构家族或目录
- 如果用户明确说“看不懂”或明显不是工程背景，先把术语翻译成“哪份文件算数 / 这次先做什么 / 哪些先别改”
- 只有命中条件升级包时，才附加 governed pack / harness、discussion、共享、gate 或读取顺序区块

更细的回答组织规则，读：

- [输出约定](references/输出约定.md)

## 按问题读哪个参考件

- 边界还不稳：读 [起步阶段：故事与测试对齐](references/起步阶段_故事与测试对齐.md)、[说人话需求确认工具包](references/说人话需求确认工具包.md)
- 需要先判断问题在哪里、该上多强控制：读 [问题诊断与控制强度分级](references/问题诊断与控制强度分级.md)
- 需要决定主线程 / `subagent` / `CLI` / runner 怎么分工：读 [执行面判定与CLI生产策略](references/执行面判定与CLI生产策略.md)
- 需要判断是先提问、先假设还是先给最小建议：读 [理解把握度与澄清规则](references/理解把握度与澄清规则.md)
- 需要固定正式回答形状：读 [输出约定](references/输出约定.md)
- 需要判断共享存储、跨层写权和多工具协作：读 [AI-Native 同构团队协作](references/AI-Native同构团队协作.md)、[跨层共享约定](references/跨层共享约定.md)
- 目标读者几乎没有软件工程基础、说明和手册看不懂：先读 [docs/非工程背景起步.md](docs/非工程背景起步.md)、[理解型输入与低带宽压缩包](references/理解型输入与低带宽压缩包.md)
- 需要判断 `files-driven` 自己和工作对象怎么区分、或同一文件为何会有双重身份：读 [作用域绑定与防变形规则](references/作用域绑定与防变形规则.md)
- 需要处理工具全局 rules、跟仓项目 rules、局部 pack rules 和适配入口的联动修改：读 [多规则工具治理与精准修改协议](references/多规则工具治理与精准修改协议.md)
- 需要把外部项目现有 workflow 改造成宿主优先、脚本补强：读 [docs/外部项目Workflow改造脚手架.md](docs/外部项目Workflow改造脚手架.md)
  这份文档先把方法和判断路径讲清；当前它还不是 `manage` CLI 的正式子命令
- governed pack / harness / workflow 合同化：读 [QUICKSTART.md](QUICKSTART.md)、[MIGRATION.md](MIGRATION.md)、[schemas/README.md](schemas/README.md)，并以 `BOUNDARY.md -> workflow.contract.json -> objects/*.json` 作为 canonical pack 主路径
- 议题还没到 `task / decision`，或要判断是否升级到质询 / process projection：读 [讨论收口与晋升](references/讨论收口与晋升.md) 和相关 examples
- 运行中反复出现纠偏、需要判断先停在记录、候选还是晋升：读 [运行观察与能力晋升](references/运行观察与能力晋升.md)、[examples/capture-candidate-activation/README.md](examples/capture-candidate-activation/README.md) 和 [项目治理能力模型](docs/项目治理能力模型.md)
- 已出现越级动作、提前改写、`partial / blocked` 无法约束下游时：读 [关口硬化与稳定放行](references/关口硬化与稳定放行.md)
- 真源入口不清、恢复困难或历史页堆积：读 [官方读取顺序](references/官方读取顺序.md)、[场景手册](references/场景手册.md)、[文档生命周期与压缩](references/文档生命周期与压缩.md)
- 需要判断本仓库当前 tranche 还差什么、接下来先补什么：读 [docs/当前阶段补完计划.md](docs/当前阶段补完计划.md) 和 [PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md)

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
- “我要统一多个工具的全局 / 项目 / pack 级 rules，请先列出应改文件集合，再做精准且完整的修改。”
- “把 `files-driven` 当前的能力改善 workflow 改成脚本调度、Codex CLI 节点执行，并生成一条可审计的 self-hosting run pack。”
