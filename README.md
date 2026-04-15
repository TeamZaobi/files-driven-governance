# files-driven

当前公开版本：`v0.5.1`<br>
未发布中的整理与修正见 [CHANGELOG.md](CHANGELOG.md) 的 `Unreleased`。
当前版本说明见 [docs/v0.5.1_版本说明.md](docs/v0.5.1_版本说明.md)；若要看上一版收口，再读 [docs/v0.5.0_版本说明.md](docs/v0.5.0_版本说明.md)。

`files-driven` 面向 AI-Native / AI-Driven 项目，帮助团队在项目持续演进中稳住真源、明确下一步、控制改动边界，并让 AI 协作过程可检查、可恢复。它把项目中的规则、文档、状态、流程和工具入口视为同一套治理资产；当项目进入多人、多代理、多工具协作阶段时，再进一步把这些问题收口到共享存储上的事实、写权和恢复治理。

- 哪份文件算数
- 今天先做哪一步
- 哪些地方先别动
- 什么时候该补更强控制
  
> 这一类项目在持久化过程中，普遍会遇到漂移、偏离、过度设计、写权失控和恢复困难。本项目的目标就是通过治理规则、状态、流程和工具入口来**预防**和**控制**这些问题，保持项目持续、稳定、可恢复地演进。

对“全员通过 AI 工具工作 + 项目级规则文件跟仓共享 + Git 目录级全量共享”的项目，它默认先把协作理解成共享存储上的事实、写权和恢复问题，
再判断入口规则、能力规则、项目规则、项目实体该怎样分开。

## 目录

- [先看你是哪种场景](#先看你是哪种场景)
- [首屏动作](#首屏动作)
- [什么时候该用](#什么时候该用)
- [什么时候不该用](#什么时候不该用)
- [它在解决什么问题](#它在解决什么问题)
- [第一性原理与当前版本方向](#第一性原理与当前版本方向)
- [统一真源](#统一真源)
- [当前治理模型演进口径](#当前治理模型演进口径)
- [核心模型](#核心模型)
- [理论基点](#理论基点)
- [这不是模板，而是方法学](#这不是模板而是方法学)
- [这套方法从哪里来](#这套方法从哪里来)
- [与 Prompt / Context / Harness 演化线的关系](#与-prompt--context--harness-演化线的关系)
- [这套方法的原创重点在哪里](#这套方法的原创重点在哪里)
- [它在教什么判断](#它在教什么判断)
- [这个仓库里各文件负责什么](#这个仓库里各文件负责什么)
- [当前 files engine 脚手架资产](#当前-files-engine-脚手架资产)
- [当前受控资产包约定](#当前受控资产包约定)
- [第一次怎么开始](#第一次怎么开始)
- [常见开口方式](#常见开口方式)
- [阅读路线](#阅读路线)
- [仓库结构](#仓库结构)
- [版本与变更](#版本与变更)

## 先看你是哪种场景

### 非工程背景读者或团队培训

先读 [docs/非工程背景起步.md](docs/非工程背景起步.md) 和 [docs/使用手册.md](docs/使用手册.md)。
首屏目标不是先懂 `scope`、`projection`、`contract tranche`，
而是先会三件事：

1. 哪份文件算数
2. 今天先做什么
3. 哪些文件先别改

如果需要把方法学讲清楚，默认也先用新手能接住的颗粒度来讲：
先讲项目哪里在漂、哪份文件算数、今天先做什么，
再按需下钻 [docs/完整说明书.md](docs/完整说明书.md) 和 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。

### 为下游项目安装 `files engine`

先读 [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md)，
再走 `install / register / repair / audit`。
当前 `audit` 默认只表示“基础体检”，不冒充下游项目的全量系统体检。

### 继续开发本仓库

先读 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)，
再读 [PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md)、[docs/当前阶段补完计划.md](docs/当前阶段补完计划.md)、[SKILL.md](SKILL.md)。
这条入口的目标是先看清当前基线、当前 tranche、当前通过线和明确非目标，
不是先重写理论总论。

### 处理 `self-hosting` 的能力改善或仓库级收口

先明确当前对象到底是 `capability_scope`、`repo.files-driven` 还是某个下游项目实例。
如果已经完成诊断，准备把方案编码成受控执行，
再走后面的 `capability-improve` 或 repo treatment runner，而不是停在 prompt-only 解释层。

## 首屏动作

对下游项目，`files-driven` 作为 meta-skill 的首屏动作只保留四个：
`install / register / repair / audit`。

- `install`：通过 [scripts/bootstrap_files_engine_starter.py](scripts/bootstrap_files_engine_starter.py) 播种官方最小 starter
- `register`：通过统一的 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 登记文件身份、归属和路由基础
- `repair`：通过统一的 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 收口脚手架或治理资产的失配
- `audit`：先做基础体检，检查 scaffold、registry、route、manifest、starter profile 这条最小资产链是否闭环

如果你的读者几乎没有软件工程基础，
可以先把用户侧语言压成：
`体检 -> 诊断 -> 治疗 -> 复查 -> 随访`。
这只是采用体验的翻译层；底层 canonical 术语、合同键名和 validator 语义不改。

## 什么时候该用

- 仓库里已经有不少规则页、任务页、状态页和入口文档，但它们开始互相漂移
- 你要让多人、多代理、多工具协作时还能共享同一套事实
- 你准备做治理，但不想一上来就堆很重的流程
- 你希望“继续开发”“开始审计”“推进”这类短口令能稳定跨工具复用
- 你需要一套能交接、能恢复、能回退的文档结构
- 你的项目反复出现“还没审完就想修改”“明明 `blocked` 了还继续往下走”这类 gate 失效

## 什么时候不该用

- 你只是在做一次性的小脚本或单人短任务
- 你现在只是想补一个简单 README，而不是治理一套协作结构
- 你的项目几乎没有状态页、过程页和工具入口，也没有明显恢复压力

## 它在解决什么问题

很多项目不是死在代码上，而是死在这些地方：

- README 因为最常被打开，慢慢变成真源
- 任务单或讨论页顺手改了规则，但没人回写上游
- 状态页为了方便接手，写出了上游没确认的新事实
- 工具入口各自包了一层口径，越包越不一致
- 人换了、代理换了、上下文断了以后，项目只能靠猜恢复
- 明明已经说了 `partial / blocked`，但下一步还是提前滑进修改、发布或放行

`files-driven` 的作用，就是先把这张责任图重新画清，再决定该启用哪些治理动作。
如果问题重心已经是 gate 不严，
仓库里现在也提供了一条专门的稳定解入口：
[references/关口硬化与稳定放行.md](references/关口硬化与稳定放行.md)。

## 第一性原理与当前版本方向

这套方法的第一性原理，不是把所有流程都脚本化，也不是把某一种 runtime 包装写成长期本体，
而是：

**帮助用户识别问题，解决问题。**

在项目治理语境里，它至少要帮用户回答：

- 当前真正的问题是什么
- 失控点出在真源、流程、角色边界还是 runtime
- 当前场景到底需要多强的控制能力
- 应该优先复用宿主原生能力，还是启用脚本、CLI、审批和审计补强

因此，本项目的长期路线是 **强化控制能力**，不是把“控制面外移”“Workflow 脚本化”或“CLI backend 化”直接写成长期本体。
后者只是当前版本为解决“复杂流程靠 LLM 内部对话流转时控制不稳”而采用的实现策略族。

当前版本先收三条执行原则：

1. 先识别问题，再决定控制强度
2. 宿主原生 `workflow / subagents / approvals` 能稳住时优先复用
3. 只有当复杂流程需要编排、恢复、回放、审计或宿主无力兜住时，才把部分控制责任外移到脚本 runner 和 `CLI`

这里先按三条判断轴把方法讲清，但不要并列乱用：

1. 世界观轴：`v1 -> v2 -> v2.1`
   - 负责看清真源、治理主语、作用域和工作对象
2. 控制强度轴：`L0 -> L4`
   - 负责决定当前问题需要多强控制
3. 执行面轴：主线程 / `subagent` / 宿主 workflow / `CLI` / runner
   - 负责决定具体由谁执行、怎样执行

默认顺序是：

1. 先用世界观轴看清“谁在治理谁”
2. 再用控制强度轴判断“该上多强控制”
3. 最后才用执行面轴决定“主线程、宿主、CLI、runner 怎么分工”

不要跳过前两步，直接从“要不要脚本化”开始。

## 统一真源

当前底层能力模型的唯一真源是 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。
`README.md`、`SKILL.md`、`PROJECT_STORIES_AND_TESTS.md`、`MIGRATION.md` 与 [schemas/README.md](schemas/README.md) 都只做入口、执行导览、迭代边界或合同说明，不与这份真源平行定义本体。

这里还要分清两条版本轴：

1. `v1 -> v2 -> v2.1` 说的是能力模型世界观的演进
2. governed pack / contract 侧仍有一条独立的 `contract tranche v1`

像 `checks.route / evidence / write / stop`、`subject_ref` 这类约束，默认属于后者。

如果你今天主要想知道怎么处理，先读 [docs/使用手册.md](docs/使用手册.md)。
如果你想系统理解模型和方法，再读 [docs/完整说明书.md](docs/完整说明书.md)。
如果你要改本体，回 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。

## 当前治理模型演进口径

当前统一口径只记三段演进：

1. `v1`：先解决真源、投影、合同化和执行实例怎么分层落盘
2. `v2`：`files-driven = 项目总监`，明确谁是治理者、谁是工作对象
3. `v2.1`：在 `v2` 之上补 `作用域绑定与防变形规则`

三者是演进关系，不是互斥关系。完整定义见 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。
默认工作对象、三个 `scope` 和 `self-hosting` 的硬约束，不在 `README` 里重讲；
需要系统解释时，直接读 [docs/完整说明书.md](docs/完整说明书.md) 和 [作用域绑定与防变形规则](references/作用域绑定与防变形规则.md)。

## 核心模型

`README` 只保留够用摘要，不在这里重写完整模型。
默认顺序只记五步：

1. 先判当前动作是什么
2. 再判当前站在哪个 `scope`
3. 再判这轮先停在哪个一级关口
4. 只有需要时，再补四层：`truth_source / execution_object / status_projection / display_projection`
5. 还不够时，才继续下钻结构家族、共享关系和恢复链

一句话原则仍然不变：

**具体能力归 Skill，项目内容归实体。**

如果需要和稳定键名、schema、JSON 或 `source_kind` 逐项对齐，
直接读 [docs/完整说明书.md](docs/完整说明书.md)、[docs/项目治理能力模型.md](docs/项目治理能力模型.md) 和对应 `references/`，
不要把 `README` 当成压缩版本体。

## 理论基点

这套方法默认同时看三个基点：

1. 系统：边界怎么稳
2. 信息：事实怎么流、怎么失真
3. 控制：秩序怎么维持、怎么恢复

`README` 不再展开长版说明；系统解释见 [docs/完整说明书.md](docs/完整说明书.md) 第 `5` 节。

## 这不是模板，而是方法学

`files-driven` 不是推荐目录树，也不是固定流程宗派。
它更像一套判断语言：什么进入口规则，什么沉到 `Skill`，什么留在项目规则，什么属于项目实体，什么时候该升级控制。
如果你要看展开版，读 [docs/完整说明书.md](docs/完整说明书.md) 第 `4`、`6`、`7` 节。

## 这套方法从哪里来

它吸收了 `Spec-Driven`、`Kanban`、`Agile / Sprint-like`、系统论、信息论和控制论，
但不要求你先认同哪个门派。
这里不再展开谱系表；系统说明见 [docs/完整说明书.md](docs/完整说明书.md) 的相关章节。

## 与 Prompt / Context / Harness 演化线的关系

`files-driven` 与 `Prompt / Context / Harness` 这条演化线是相通的，
但这里更关心的是真源、读取顺序、恢复链和控制回路怎样真正落到仓库资产里。
如果你要看这条关系的展开版，直接读 [docs/完整说明书.md](docs/完整说明书.md) 的对应章节。

## 这套方法的原创重点在哪里

重点不在发明新名词，而在把真源、过程、摘要、展示、共享、恢复和控制回路，压成可以直接落到仓库与协作中的判断语言。
需要展开版时，直接读 [docs/完整说明书.md](docs/完整说明书.md)。

## 它在教什么判断

如果把这套方法再压缩一层，它主要在教五种判断：

1. 什么应该成为慢变量，进入稳定真源
2. 什么应该保持流动，留在过程载体
3. 什么只能总结，不能反写上游
4. 什么需要正式关口，什么保持轻量回路
5. 当项目开始漂移时，应该先止血哪里，再恢复哪里

这也是为什么它既能吸收规格驱动、看板流和敏捷节奏，
又不直接退化成其中任何一种固定模板。

## 这个仓库里各文件负责什么

先按三层来记，再看具体文件：

1. `入口层`：先回答现在怎么办
2. `说明层`：再解释为什么这样办
3. `真源层`：最后冻结本体定义

另外还有一组 `侧车资产`：stories、examples、schemas、starters、scripts，
它们很重要，但默认不属于第一次阅读主线。
完整复盘见 [docs/三层信息架构复盘.md](docs/三层信息架构复盘.md)。

| 文件 | 主要读者 | 主要职责 |
| --- | --- | --- |
| [README.md](README.md) | 第一次接触这个项目的人 | 解释这是什么、什么时候该用、怎么开始 |
| [docs/项目治理能力模型.md](docs/项目治理能力模型.md) | 维护底层模型的人或审计者 | 作为 `v1 / v2 / v2.1` 的统一底层真源 |
| [docs/能力雷达与版本演进盘点.md](docs/能力雷达与版本演进盘点.md) | 想做系统盘点、版本回看或补完排序的人 | 盘点当前能力簇、两条版本轴和各版本能力增量 |
| [docs/能力覆盖矩阵与历史差分.md](docs/能力覆盖矩阵与历史差分.md) | 想反向检查能力模型今天到底照进了哪些入口、脚本和回归的人 | 对照 `v1 / v2 / v2.1` 与 `v0.2.0 -> v0.5.0`，盘清能力覆盖和历史差分 |
| [docs/宿主化知识工作场景矩阵.md](docs/宿主化知识工作场景矩阵.md) | 宿主名先行、但真正要判断真源与写权的人 | 把 `Obsidian / Notion / Docs / Sheets / Slides` 翻译回治理判断 |
| [docs/体检分层矩阵.md](docs/体检分层矩阵.md) | 想弄清当前 `audit` 到底覆盖到哪一层的人 | 盘清 `scaffold / pack / runtime / governance / adoption` 五层体检边界 |
| [docs/AI-Native与Skill驱动E2E验收矩阵.md](docs/AI-Native与Skill驱动E2E验收矩阵.md) | 想把 AI-Native / skill-driven 场景改动收口成端到端验收的人 | 把 agent-facing、downstream starter、宿主名先行、runtime 晋升链和 self-hosting rollout 统一到一张 E2E 矩阵 |
| [docs/使用手册.md](docs/使用手册.md) | 已决定按这套方式工作的团队成员 | 从项目要解决的问题出发，说明问题为什么会出现、常见方式为什么不够，以及团队今天该怎么执行 |
| [docs/v0.4.1_版本说明.md](docs/v0.4.1_版本说明.md) | 想理解这一版为何强调控制能力的人 | 说明当前版本的设计目标、实现纠偏和宿主/脚本/CLI 的关系 |
| [docs/外部项目Workflow改造脚手架.md](docs/外部项目Workflow改造脚手架.md) | 需要改造外部项目现有 workflow 的人 | 提供“宿主优先、脚本补强”的 benchmark family 入口；当前 workflow 只是一个实例，并显式分开 `human authority`、机读控制面和 hook policy |
| [PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md) | 会继续开发这个仓库的人或代理 | 直接写清本项目当前的具体用户故事、测试用例、非目标和验收责任人 |
| [SKILL.md](SKILL.md) | 会执行这个技能的代理 | 给出主流程、判断规则、边界约束和参考件路由 |
| [agents/openai.yaml](agents/openai.yaml) | 通过 Agent 使用这个 skill 的人或代理 | 作为 agent-facing 入口表面，固定显示名、简短定位和默认 prompt 路由 |
| [QUICKSTART.md](QUICKSTART.md) | 第一次搭建受控资产包的人 | 给出最小资产包形状、校验脚本（validator）用法和起步顺序 |
| [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md) | 需要给下游项目安装 `files engine` 的人 | 说明修正后的需求、四层边界、脚手架缺口、质询与收敛决议 |
| [MIGRATION.md](MIGRATION.md) | 已有资产包的维护者 | 说明从旧约定迁到当前约定要改什么 |
| [references/](references/) | 需要深入某一专题的人或代理 | 承载输出约定、流程库、读取顺序、共享约定和专项判断 reference |
| [examples/](examples/) | 想先看一条完整样例的人或代理 | 承载 discussion 主路径、受控 workflow、运行观察晋升链和条件分支 example |
| [schemas/](schemas/) | 需要结构化合同草案的人或代理 | 承载控制语义的机读结构草案（schema） |
| [starters/minimal-files-engine/](starters/minimal-files-engine/) | 第一次从零安装 `files engine` 的人或代理 | 提供官方最小 starter、拓扑 manifest、注册表样例和项目 skill 骨架 |
| [scripts/bootstrap_files_engine_starter.py](scripts/bootstrap_files_engine_starter.py) / [scripts/validate_files_engine_scaffold.py](scripts/validate_files_engine_scaffold.py) | 需要冷启动或回归 starter 的人或代理 | 负责 starter 生成与 scaffold 校验 |
| [scripts/run_repo_treatment_rollout.py](scripts/run_repo_treatment_rollout.py) | 需要在 `self-hosting` 场景把仓库级收口方案编码成受控执行的人或代理 | 负责编排 repo treatment rollout、写 runtime artifact，并调度 `codex exec` 落地本轮推进 |
| [docs/](docs/) | 想看完整背景、版本说明和公开专题材料的人 | 承载说明书、版本说明、公开专题记录和当前阶段补完计划 |
| [CHANGELOG.md](CHANGELOG.md) | 关心仓库变更账本的人 | 记录仓库层面的新增、调整和删除 |

除 [docs/项目治理能力模型.md](docs/项目治理能力模型.md) 外，上面这些文件都不负责重定义底层能力模型本体。

一句话区分：

- `README` 是入口
- `SKILL` 是执行导览
- `agents/openai.yaml` 是 Agent 使用这个 skill 时的入口表面
- `QUICKSTART` 是最小上手
- `MIGRATION` 是迁移说明
- `references` 是按需下钻
- `examples` 是最短样例
- `schemas` 是结构化合同草案
- `starters` 是官方最小起点
- `bootstrap / scaffold validator` 是冷启动执行面
- `docs` 是背景与公开说明
- `CHANGELOG` 是账本

## 当前 files engine 脚手架资产

如果你要做的不是“继续维护本仓库”，而是“把 `files-driven` 装进一个下游项目”，
先不要把 `QUICKSTART` 当成总入口。

`files-driven` 作为 meta-skill 的首屏动作只保留四个：`install / register / repair / audit`。
其中 `install` 通过 [scripts/bootstrap_files_engine_starter.py](scripts/bootstrap_files_engine_starter.py) 完成，`register / repair / audit` 通过统一的 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 完成。
这里的 `audit` 当前默认只表示“基础体检”：
先检查 scaffold、registry、route 和 starter profile 这类脚手架资产是否闭环，
不直接冒充对下游项目的全量系统体检；如果你明确要查 pack / contract 资产，可显式运行 `manage audit --layer pack`；如果你在查官方的 observation -> candidate -> activation 链，可运行 `manage audit --layer runtime`；如果你在查入口冒充真源、scope 混写或 hidden authority surface，可运行 `manage audit --layer governance`；如果你在查本仓库的新手路径、低带宽解释和宿主名先行分诊是否站得住，可运行 `manage audit --layer adoption`。
如果你要系统区分 `scaffold / pack / runtime / governance / adoption` 五层体检，直接读 [docs/体检分层矩阵.md](docs/体检分层矩阵.md)。
如果你要把 AI-Native / skill-driven 场景改动收口成端到端验收，直接读 [docs/AI-Native与Skill驱动E2E验收矩阵.md](docs/AI-Native与Skill驱动E2E验收矩阵.md)。
本仓库本身是 `reference implementation + regression fixture`，不是通用模板本体。

最小主路径只记下面 5 步：

1. 先读 [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md)
2. 再用 bootstrap 起一个最小 starter
3. 检查 [starters/minimal-files-engine/](starters/minimal-files-engine/) 里的 `governance/scaffold.manifest.json`、`governance/files.registry.json`、`governance/intent.routes.json`、starter profile 和项目 `Skill` 骨架
4. 用统一的 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 完成 `register / repair / audit`
5. 先跑 [scripts/validate_files_engine_scaffold.py](scripts/validate_files_engine_scaffold.py)，再跑 [scripts/validate_governance_assets.py](scripts/validate_governance_assets.py)

这里仍要分清 4 层对象：

- `repo.files-driven`：本仓库自己的资产
- `skill.files-driven`：当前技能包本身
- `meta-skill capability`：帮下游项目安装 `files engine` 的能力
- `downstream project instance`：starter 生成出来的具体项目实例

这里先只记 3 个边界：

- `scaffold.manifest.json` 管 starter 拓扑和 tracked globs
- `files.registry.json` 管文件身份核心和 `annotations`
- `intent.routes.json` 管入口、必读和写入目标；starter 专属形状约束由单独的 starter profile 持有

如果只改 route 名称或入口动作，只改 `intent.routes.json`。
如果新增或移动 tracked 文件，先改 `scaffold.manifest.json`，再改 `files.registry.json`，最后按需改 route。
如果只是 starter 专属形状变化，先改 starter profile，再按需碰 validator，不要回写 manifest。

如果当前要处理的是 `files-driven` 自己这套仓库资产，而不是某个下游 starter，
并且你已经完成一轮诊断、准备把收口方案编码成一次受控执行，
就分两条路：

- 仓库级收口 rollout：用 [scripts/run_repo_treatment_rollout.py](scripts/run_repo_treatment_rollout.py)
- `capability_scope` 自改善：用 [scripts/manage_files_engine.py](scripts/manage_files_engine.py) 的 `capability-improve`

`capability-improve` 的底层 runner 是 [scripts/run_project_director_capability_improvement.py](scripts/run_project_director_capability_improvement.py)。
它用脚本维护 `workflow.state.json`、`workflow.events.jsonl`、`status.projection.json`，
让 `Codex CLI` 只负责当前节点产物，不负责控制文件和流转判断。
如果用户明确说“把当前 workflow 改造成脚本调度、Codex CLI 节点执行”，
并且当前对象是 `files-driven` 自己的能力改善，就先路由到这里，而不是继续停在 prompt-only 解释层。

## 当前受控资产包约定

如果你要落一个受控流程的项目资产包，入口层先只记住这几件事：

- `BOUNDARY.md` 先锁首批场景、故事、测试、非目标、质量参考对象和验收责任人
- `workflow.contract.json` 是控制合同
- `objects/*.json` 是项目级对象合同
- `workflow.state.json` 与 `workflow.events.jsonl` 是运行实例
- 可选 `status.projection.json` 只做派生摘要
- workflow 顶层 `checks.route/evidence/write/stop` 是 v1 唯一检查注册面
- `agent_refs` 指向 `agent.contract.json` 的顶层 `agent_id`
- `approver_ref` 指向 `roles[].role_id`
- `workflow.events.jsonl.subject_ref` 在 v1 只指向 `node_id / transition_id`

第一次接触时，先把上面理解成：

- `BOUNDARY.md` 先回答“这个 pack 到底服务谁、交付什么、怎么才算没跑偏”
- `workflow.contract.json` 管流程怎么走
- `objects/*.json` 管状态、证据、输出、批准对象这些定义
- `workflow.state.json` 和 `workflow.events.jsonl` 记录这次运行到了哪里
- `status.projection.json` 只是帮助恢复现场的摘要页，不能偷偷放行

更细的键名和字段解释，统一放在 [QUICKSTART.md](QUICKSTART.md) 与 [schemas/README.md](schemas/README.md)。
这里只再额外记一个硬边界：

- 仓库根 [schemas/](schemas/) 是结构草案目录
- 项目资产包里的对象合同走 `objects/*.json`
- 只要 pack 里还保留 `pack_root/schemas/*.json`，validator 就会直接报迁移错误

如果运行中反复出现同类纠偏，不要直接热改能力真源。
先读 [references/运行观察与能力晋升.md](references/运行观察与能力晋升.md)，
再按 [examples/capture-candidate-activation/README.md](examples/capture-candidate-activation/README.md) 的官方路径，把信号停在 `运行观察 -> 证据包 -> 历史召回 -> 拆分出口 -> 候选试验 -> 激活或回退`。

当前仓库还附带两层最小验证面：

- [tests/](tests/) 提供校验脚本的最小回归测试
- [.github/workflows/governance-assets-ci.yml](.github/workflows/governance-assets-ci.yml) 把 smoke 资产包、JSON 语法和单元测试接进 CI

这里提到的“v1 唯一检查注册面”“v1 subject_ref 语义”，
默认都指 governed pack / contract 的 `tranche v1`，不是在回退世界观层的版本口径。

## 第一次怎么开始

如果你还没按前面的“先看你是哪种场景”分过一次诊，先回去选入口。
这里不再重做首屏分诊，只保留继续下钻时最常用的路由。

如果你是继续开发本仓库，或需要先建立统一基线，再用这 3 份建立共同口径：

1. [docs/项目治理能力模型.md](docs/项目治理能力模型.md)
2. [README.md](README.md)
3. [docs/使用手册.md](docs/使用手册.md)

如果你是要把这套 skill 给非工程背景读者或零基础使用者看，
不要从上面这 3 份开始，也不要一上来就让他们读完整模型、完整说明书或全部 reference。
先让他们读 [docs/非工程背景起步.md](docs/非工程背景起步.md)，
先只学会：

1. 哪份文件算数
2. 今天先做什么
3. 哪些文件先别改

接下来只按问题进入：

- 非工程背景读者先上手：读 [docs/非工程背景起步.md](docs/非工程背景起步.md)、[docs/使用手册.md](docs/使用手册.md)
- 继续开发本仓库：读 [PROJECT_STORIES_AND_TESTS.md](PROJECT_STORIES_AND_TESTS.md)、[docs/当前阶段补完计划.md](docs/当前阶段补完计划.md)、[SKILL.md](SKILL.md)、[docs/完整说明书.md](docs/完整说明书.md)
- 为下游项目安装 `files engine`：读 [docs/files引擎脚手架工程.md](docs/files引擎脚手架工程.md)，再跑 [scripts/bootstrap_files_engine_starter.py](scripts/bootstrap_files_engine_starter.py)
- 统一底层模型与 JSON 合同方向：读 [schemas/README.md](schemas/README.md)、[QUICKSTART.md](QUICKSTART.md)、[MIGRATION.md](MIGRATION.md)
- 手上已经有旧资产包：读 [MIGRATION.md](MIGRATION.md)、[examples/smoke-governed-review/BOUNDARY.md](examples/smoke-governed-review/BOUNDARY.md)、[examples/smoke-governed-review/WORKFLOW.md](examples/smoke-governed-review/WORKFLOW.md)
- 需要先判断问题在哪里、该上多强控制：读 [references/问题诊断与控制强度分级.md](references/问题诊断与控制强度分级.md)
- 需要决定主线程 / `subagent` / `CLI` / runner 怎么分工：读 [references/执行面判定与CLI生产策略.md](references/执行面判定与CLI生产策略.md)
- 需要把外部项目现有 workflow 改造成宿主优先、脚本补强，或显式分开 `human authority`、机读控制面和 hook policy：读 [docs/外部项目Workflow改造脚手架.md](docs/外部项目Workflow改造脚手架.md)
- 议题还没到 `task / decision`：读 [examples/discussion-decision-task/BOUNDARY.md](examples/discussion-decision-task/BOUNDARY.md)、[examples/discussion-decision-task/WORKFLOW.md](examples/discussion-decision-task/WORKFLOW.md)
- 争议已经很大，需要逐点质询后再收敛：读 [examples/adversarial-convergence/README.md](examples/adversarial-convergence/README.md)
- hooks 已经成为工具适配面的一部分：读 [references/hooks使用方法论与脚手架.md](references/hooks使用方法论与脚手架.md)、[references/工具适配对照表.md](references/工具适配对照表.md)、[references/关口硬化与稳定放行.md](references/关口硬化与稳定放行.md)
- 运行中反复出现纠偏、又不能直接热改能力真源：读 [references/运行观察与能力晋升.md](references/运行观察与能力晋升.md)、[examples/capture-candidate-activation/README.md](examples/capture-candidate-activation/README.md)
- 多工具过程已经不透明，需要统一接手面：读 [references/跨层共享约定.md](references/跨层共享约定.md)、[examples/multi-tool-process-projection/process-projection.md](examples/multi-tool-process-projection/process-projection.md)
- 需要把对话里的可点击文件链接、Obsidian vault 内 `.md` 双向链接和库外 Markdown 链接分开：读 [docs/宿主化知识工作场景矩阵.md](docs/宿主化知识工作场景矩阵.md)、[references/工具适配对照表.md](references/工具适配对照表.md)、[references/输出约定.md](references/输出约定.md)
- 希望用短口令推进工作或正式输出治理方案：读 [references/意图触发约定.md](references/意图触发约定.md)、[references/输出约定.md](references/输出约定.md)

## 常见开口方式

第一次使用时，不必把整个仓库讲成论文。像下面这样开口就够了：

- “帮我判断这个仓库里哪些文件是真源，哪些只是状态摘要。”
- “这个项目已经开始漂移了，请先给我一个止血顺序。”
- “我要搭一个 AI Agent 驱动的新项目，先帮我锁方向与边界。”
- “这条议题还不适合进 task，请先帮我开 discussion，并判断什么时候该晋升。”
- “这条讨论争议已经很大，请按质询-答辩-收敛来帮我收口。”
- “运行里同类纠偏反复出现，但我不想直接热改能力真源，先帮我判断该停在记录、候选还是晋升。”
- “我们现在有多工具过程，但接手时看不清到底跑了什么，请补一个 process projection。”
- “我们要统一多个工具的全局 / 项目 / pack 级 rules，请先列出应改文件，再做完整修改。”
- “我们想用‘继续开发’和‘开始审计’这类短口令驱动工作，帮我做成稳定约定。”
- “我的项目在 Obsidian 里，仓库 Markdown 内链要进双向链接，但对话里仍要保留可点击文件链接，请先帮我定分流规则。”
- “我的目标读者几乎没有软件工程基础，先别讲理论，告诉我哪份文件算数、今天先做什么。”

## 阅读路线

这部分只留最短阅读路由：

- 代理要执行：读 [SKILL.md](SKILL.md) -> [references/输出约定.md](references/输出约定.md) -> 对应专题 reference
- 非工程背景先开工：读 [docs/非工程背景起步.md](docs/非工程背景起步.md) -> [docs/使用手册.md](docs/使用手册.md)
- 想看语言和写法标准：读 [docs/语言体系规范.md](docs/语言体系规范.md) -> [references/说人话需求确认工具包.md](references/说人话需求确认工具包.md)
- 其余问题直接回上面的 [第一次怎么开始](#第一次怎么开始)

## 仓库结构

```text
.
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── docs/
│   ├── 完整说明书.md
│   ├── 使用手册.md
│   ├── 语言体系规范.md
│   └── v*_版本说明.md
└── references/
    ├── 输出约定.md
    ├── 经典治理流程库.md
    ├── 场景手册.md
    ├── 基本原则.md
    ├── 治理模式选择对照表.md
    ├── 结构家族定位约定.md
    ├── 官方读取顺序.md
    ├── 工具适配对照表.md
    ├── 跨层共享约定.md
    ├── 起步阶段_故事与测试对齐.md
    ├── 说人话需求确认工具包.md
    ├── 文档生命周期与压缩.md
    └── 意图触发约定.md
```

## 版本与变更

- 当前公开版本是 `v0.5.1`
- 未发布中的整理与修正统一记在 [CHANGELOG.md](CHANGELOG.md) 的 `Unreleased`
- 每一版为什么重要、改变了什么理解或用法，读 [docs/](docs/) 里的 `v*_版本说明.md`
- 研究过程留痕、任务计划、进度账本和内部案例默认留在本地忽略区，不进入公开仓库

## 贡献与安全

- 贡献方式见 [CONTRIBUTING.md](CONTRIBUTING.md)
- 安全问题见 [SECURITY.md](SECURITY.md)

## 许可证

当前许可证见 [LICENSE](LICENSE)，为 `MIT`。
