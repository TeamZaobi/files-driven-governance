# 本项目的用户故事与测试用例

这份文档只回答一件事：
`files-driven` 这个仓库作为一个正在开发的项目，本轮到底在为谁做什么，以及怎么判断没有做偏。

它不是某个下游 governed pack 的边界说明，
而是这个仓库自己当前迭代的具体用户故事和具体测试用例。

这份文档不是 pack 级 `BOUNDARY.md`。
它不复用 pack 的固定 section contract，只服务于本仓库自己的开发和维护。

能力模型基线只认 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)。
这份文档只记录仓库当前迭代的用户故事、测试锚点和非目标；如果与基线冲突，以基线为准。

这里显式区分两条版本轴：

1. 能力模型：`v1 -> v2 -> v2.1`
2. governed pack / contract：`tranche v1`

像 `checks.route / evidence / write / stop`、`subject_ref` 这类冻结语义，默认都属于后者。

## 当前使用场景

- 仓库维护者准备把能力模型 `v1 -> v2 -> v2.1` 收口到同一份底层真源上，并继续推进它的公开入口、专项 reference 和验证面，避免边改边漂移。
- 新接手的 AI coding 代理需要在一次会话内判断：这个仓库当前是在完善方法论说明、推进可执行合同层，还是已经转向做一个更重的产品框架。
- 外部贡献者希望判断自己提的文档、schema、validator 或示例改动，是否仍然落在当前项目目标之内。
- AI-Native 团队负责人希望把“全员通过 AI 工具工作 + 项目级规则文件跟仓共享 + Git 目录级全量共享”这一协作前提讲清，避免团队继续按工具品牌而不是按共享存储理解协作。
- governed pack 的作者或维护者希望用 `BOUNDARY.md + workflow.contract.json + validator` 搭出一个真正对准场景、故事和测试锚点的最小资产包，而不是只补一堆看似完整的合同文件。
- 团队培训者希望快速把“files-driven 到底在解决什么问题、为什么常见做法不够、团队应该怎么工作”讲清楚，而不是再产出一份只讲概念和目录的说明文档。
- 公开项目维护者希望把这套 skill 给几乎没有软件工程基础的读者或使用者时，先给他们一条只说工作语言的起步路径，而不是要求他们先读懂完整说明书。
- 负责 harness、agent runtime 或治理执行链的人，希望把 `workflow` 从 prose-first 说明重构为最小可执行控制载体，减少运行时歧义、提高检查、恢复和自动化执行效能。
- 团队负责人或新接手的协作者希望看到官方 `discussion` 模板、晋升路径和分支 example，不必再从其他项目逆向理解“讨论如何收口、何时升级到质询、何时进入执行”。
- 下游项目的采用者或 AI coding 代理，希望拿到一条官方 starter 闭环，能把 `files-driven` 作为 `meta-skill` 安装进新项目，而不是继续从 example 和说明文里反推起步路径。

## 当前交付物

- 一套可以公开理解、可以本地验证、也可以持续演进的 `files-driven` 项目基线：
  - 中文主叙事入口
  - 问题导向的团队使用手册
  - 项目治理能力模型统一真源
  - `v1` 历史阶段兼容入口
  - AI-Native 同构团队协作 reference
  - discussion 收口与晋升 reference
  - 最小 schema 草案
  - 非工程背景读者起步页
  - files engine 脚手架工程说明
  - 官方 starter
  - 文件注册表与路由合同 schema
  - starter bootstrap 与 scaffold validator
  - 统一 `manage` CLI 的动作面
  - starter profile 与 manifest 分层约定
  - `workflow` 作为控制载体的最小合同化实现
  - pack 级 `BOUNDARY.md` 入口
  - smoke governed pack
  - discussion / adversarial / process projection examples
  - validator 与最小回归测试
  - 清晰的项目边界、迁移说明和下一阶段执行计划

## 项目用户故事

### 用户故事 US-1

- 谁在用：第一次接手这个仓库的维护者或 AI coding 代理。
- 在什么场景下：需要先判断这个仓库当前阶段到底在做什么，再决定该优先改 README、SKILL、validator、示例 pack 或 schema 草案说明。
- 他/她现在想完成什么：在不翻遍历史讨论的前提下，快速理解项目目标、能力模型基线、当前 governed pack / contract tranche、通过线和非目标。
- 为什么这件事对当前阶段重要：如果项目本身的边界不清楚，后续文档、schema、示例和脚本会各自演化，重新制造这个仓库试图解决的“真源漂移”。
- 这次完成后，用户应该看到什么变化：新接手的人可以直接解释这个仓库现在是“以 [docs/项目治理能力模型.md](docs/项目治理能力模型.md) 为唯一底层真源、以 `v1 -> v2 -> v2.1` 为能力模型演进轴、并附带 governed pack / contract `tranche v1` 最小合同链”的项目治理模型，而不是泛化成任何文档治理都要全包的大全集。
- 这次明确不包含什么：不要求一上来就覆盖生产级安全、完整平台化产品或所有外部工具生态。

### 用户故事 US-2

- 谁在用：持续为本仓库补文档、schema、validator、示例和测试的人。
- 在什么场景下：准备新增或调整仓库资产，但担心改动只是在局部变多，却没有帮助项目主线更清楚、更可验证。
- 他/她现在想完成什么：判断一个改动是否真的加强了项目入口、边界、最小合同层或回归能力。
- 为什么这件事对当前阶段重要：当前项目仍在从“方法说明”推进到“最小可执行能力”，最容易出现的风险就是新增很多资产，却没有共同服务同一条交付线。
- 这次完成后，用户应该看到什么变化：改动能明确归类到入口说明、能力模型、合同草案、示例 pack、validator 或回归测试中的某一环，而不是漂成游离材料。
- 这次明确不包含什么：不要求每次改动都扩版本范围，也不要求所有参考件一次性合同化。

### 用户故事 US-3

- 谁在用：负责合并、审查或监督本仓库变更的人。
- 在什么场景下：需要判断当前仓库是否仍然适合长期交给 AI coding 协作维护。
- 他/她现在想完成什么：看到项目级故事、测试锚点和验收责任人已经显式存在，并有最小回归保护。
- 为什么这件事对当前阶段重要：如果项目自己没有清楚的故事和测试锚点，AI coding 在后续会话中就只能从零猜范围，维护成本会持续上升。
- 这次完成后，用户应该看到什么变化：仓库里存在一份项目级故事与测试文档，测试会在它退化成口号或缺失关键部分时及时失败。
- 这次明确不包含什么：不要求把项目所有路线图都转成硬性自动校验，只要求守住最小项目故事与测试入口。

### 用户故事 US-4

- 谁在用：正在推动团队落地 `files-driven` 的 AI-Native 团队负责人或培训者。
- 在什么场景下：需要向团队解释为什么这个项目现在首先解决的是“共享存储上的事实漂移和写权失控”，而不是“选哪个 AI 工具最好用”。
- 他/她现在想完成什么：让团队成员能明确区分 runtime / 工具入口 与仓库中的项目级规则文件，并接受“协作先按共享存储理解”的前提。
- 为什么这件事对当前阶段重要：如果协作前提没讲清，团队后续仍会把 `Codex / Claude Code / AntiGravity` 的品牌差异误当成治理主问题，继续忽略真源、路径和写权。
- 这次完成后，用户应该看到什么变化：团队成员能直接说明为什么 `AGENT.md / CLAUDE.md / CODEX.md / SKILL.md / RULES.md` 可以作为协作入口或执行包装，但不能越过能力模型和项目规则真源，并知道什么时候该读 AI-Native 协作 reference、什么时候才需要升级到复杂共享约定。
- 这次明确不包含什么：不要求把所有工具行为完全统一，也不要求团队只使用一种 AI 工具。

### 用户故事 US-5

- 谁在用：准备搭建或维护 governed pack 的作者、维护者或 AI coding 代理。
- 在什么场景下：希望把 pack 做成一个真正服务具体场景和验收边界的最小可执行资产，而不是只堆 `workflow.contract.json`、`objects/*.json` 和状态文件。
- 他/她现在想完成什么：先通过 `BOUNDARY.md` 锁定场景、故事、测试和失败边界，再用 validator 验证 pack 是否至少具备最小边界入口和最小合同链。
- 为什么这件事对当前阶段重要：如果 pack 只有 schema、workflow 和 state，却没有显式边界入口，它会重新退化成“形式上看起来完整，实际上不知道在服务谁”的空壳。
- 这次完成后，用户应该看到什么变化：pack 作者能够解释为什么 `BOUNDARY.md` 先于 workflow 合同，并能用 smoke pack 与 validator 验证最小边界和失败边界是否存在。
- 这次明确不包含什么：不要求这个阶段就覆盖所有生产级流程、全部对象家族或复杂审批拓扑。

### 用户故事 US-6

- 谁在用：需要给团队做培训、推广或让几乎没有软件工程基础的新成员先上手的负责人。
- 在什么场景下：需要快速讲清 `files-driven` 解决什么问题、常见做法为什么不够、团队应该怎么把用户故事、测试锚点和正向反馈迭代接进日常工作，且不希望非工程背景读者一上来就被术语和长手册压垮。
- 他/她现在想完成什么：拿到一份不再被元叙事和目录细节淹没、而是能直接围绕真问题和解决路径展开的团队手册，以及一条先讲工作语言的公开起步路径。
- 为什么这件事对当前阶段重要：如果培训材料只剩方法名词和目录结构，团队会把这套能力理解成“文档规范”而不是“问题驱动的协作与治理方式”，后续采用会越来越弱。
- 这次完成后，用户应该看到什么变化：培训者可以先用 [docs/非工程背景起步.md](docs/非工程背景起步.md) 让读者只掌握“哪份文件算数 / 今天先做什么 / 哪些先别改”，再用手册讲问题、成因、解决路径以及与用户故事和反馈迭代的关系。
- 这次明确不包含什么：不要求培训材料在第一次就覆盖所有 reference、schema 字段或底层理论细节。

### 用户故事 US-7

- 谁在用：负责 harness、agent runtime、validator 或受控执行链设计的人。
- 在什么场景下：需要把 `workflow` 从“主要靠 Markdown 解释的流程说明”推进成“最小可执行的控制载体”，让运行时、检查器和恢复链都能稳定消费同一套控制语义。
- 他/她现在想完成什么：通过 `workflow.contract.json`、`workflow.state.json`、`workflow.events.jsonl`、顶层 `checks.route/evidence/write/stop` 和最小 validator，把高风险路径从 prose-first 解释推进成最小可执行合同链。
- 为什么这件事对当前阶段重要：如果 workflow 仍然主要停留在说明文档层，harness 侧就只能从 prose 猜状态、猜关口、猜缺证据和猜下一步，运行时歧义、恢复成本和自动化失真都会持续偏高。
- 这次完成后，用户应该看到什么变化：维护者能够明确说明为什么 `workflow` 是控制载体、为什么 `workflow.contract.json` 是机读控制真源、为什么实例与检查执行面必须与合同分层对齐，以及这会如何提升 harness 的可执行性、可验证性和可恢复性。
- 这次明确不包含什么：不要求这一阶段就把全部 workflow 都推进到生产级重治理，也不要求一次性补齐 hostile-environment 安全、细粒度权限或完整沙箱。

### 用户故事 US-8

- 谁在用：需要把 discussion 管理、质询收敛和执行晋升讲清的新接手者、维护者或培训者。
- 在什么场景下：需要回答“什么时候开正式 discussion、什么时候升级到质询、什么时候压成 decision package、什么时候进 task / decision”，但当前仓库又不想把源项目案例整包搬进来。
- 他/她现在想完成什么：直接看到一条首轮可用的官方主路径，以及两个条件分支 example，而不是只在 reference 里看到流程名。
- 为什么这件事对当前阶段重要：如果 discussion 相关模式继续只活在 reference 层，用户仍然要去别的项目逆向学习，这会让 `files-driven` 看起来像理论集而不是可直接用的方法项目。
- 这次完成后，用户应该看到什么变化：第一次读仓库的人可以直接沿着 `discussion -> decision_package -> task_or_decision` 主路径理解收口方式，并知道什么时候再看 adversarial 和 process projection 分支。
- 这次明确不包含什么：不要求这一阶段就把 `decision_package` 或 `process_projection` 合同化，也不要求把源项目角色名、领域对象和编号体系上升为通用模板。

### 用户故事 US-9

- 谁在用：第一次把 `files-driven` 装进新项目的维护者、AI coding 代理或团队负责人。
- 在什么场景下：手头还没有现成 pack，但希望在短时间内起出一个最小可验证的 `files engine` 起点。
- 他/她现在想完成什么：不用先读完整 example 和长文，就能生成一个带 `BOUNDARY.md`、项目 `Skill`、文件注册表、route 合同和最小 governed pack 的官方 starter。
- 为什么这件事对当前阶段重要：如果 starter 闭环不存在，`files-driven` 就仍然只是解释型 skill，而不是能帮下游项目冷启动的 `meta-skill`。
- 这次完成后，用户应该看到什么变化：从零目录出发，也能用官方 starter 在 `10-15` 分钟内起出一个最小项目起点，并知道先改哪里。
- 这次明确不包含什么：不要求这一阶段就覆盖完整平台化产品、复杂生成 UI 或所有行业模板。

### 用户故事 US-10

- 谁在用：负责 workflow、validator、tool entry 或项目规则的人。
- 在什么场景下：需要让新文件在创建时就稳定拥有工作职位、证据类型、写权和 route 绑定，而不是靠事后解释。
- 他/她现在想完成什么：把 `file_id / path / family / layer / work_post` 这类 identity core，以及按需携带的 annotations，落成机读合同，并让 validator 能直接消费。
- 为什么这件事对当前阶段重要：如果文件出生后没有注册事实，workflow、validator 和工具入口就会重新退化成从 prose 猜归属、猜用途、猜下一步。
- 这次完成后，用户应该看到什么变化：新增、迁移或角色变化的文件会先改注册表，再刷新派生物，而不是靠 README 或状态页补口头说明。
- 这次明确不包含什么：不要求这一阶段就完成全量 stale graph、自动推理拓扑或完整图数据库。

### 用户故事 US-11

- 谁在用：要把本仓库、当前 skill 和下游项目实例分清的人。
- 在什么场景下：同时讨论 self-hosting、skill 执行导览和下游 starter，最容易把 `repo / skill / meta-skill / downstream` 混成一层。
- 他/她现在想完成什么：看到一条稳定边界，知道哪些资产属于本仓库、哪些属于技能包、哪些属于引擎安装层、哪些属于下游项目实例。
- 为什么这件事对当前阶段重要：如果这四层边界继续混写，后续即使加了 starter 和 registry，也会再次把 self-hosting 入口误当成下游模板。
- 这次完成后，用户应该看到什么变化：维护者和采用者都能清楚区分仓库资产、技能资产、元技能安装资产和下游项目资产，并据此判断文件该落在哪里。
- 这次明确不包含什么：不要求所有 scope 都进入 starter 合同；这里只要求把四层边界和资产职责讲清。

### 用户故事 US-12

- 谁在用：负责把 `files-driven` 作为可执行元 skill 交付的人。
- 在什么场景下：不想再从长文里猜动作，而是要直接进入 install / register / repair / audit。
- 他/她现在想完成什么：先知道 `install` 由 bootstrap 完成，`register / repair / audit` 由统一 `manage` CLI 完成；同时知道 registry 的 identity core / annotations 分层，以及 starter profile 与 manifest 的边界。
- 为什么这件事对当前阶段重要：如果动作目录还藏在解释文档后面，`files-driven` 仍然只是说明书，不是元 skill。
- 这次完成后，用户应该看到什么变化：维护者能直接把问题归到对应动作，并知道 starter 专属形状约束不应该回写 manifest。
- 这次明确不包含什么：不要求这一阶段就做平台级 CLI、自动修复器或全量生成器。

## 项目测试用例

### 测试用例 TC-1

- 对应故事：US-1
- 前提：新接手的人或代理刚进入仓库，只知道这是 `files-driven` skill 项目。
- 当：从 `README.md` 的“继续开发本仓库”入口进入，先读 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)，再读 `PROJECT_STORIES_AND_TESTS.md` 和相关入口文档。
- 那么：应能说明这个项目当前的服务对象、能力模型基线、当前 governed pack / contract tranche 的交付物、最重要的通过线和明确非目标。
- 通过条件：无需依赖历史聊天，也能解释“为什么这个仓库现在要同时维护文档、schema、smoke pack、validator 和测试”。
- 这次明确不要求：不要求在首次阅读时就理解所有 reference 的细节。
- 失败/越界边界：如果新接手的人仍然把项目理解成“只是在写一个 README 技巧集合”或“已经要做完整平台产品”，说明项目故事与测试入口不合格。

### 测试用例 TC-2

- 对应故事：US-2
- 前提：有人准备新增一份文档、schema 或脚本。
- 当：用 `PROJECT_STORIES_AND_TESTS.md` 对照该改动是否服务当前基线投影与当前 governed pack / contract tranche 交付物。
- 那么：应能判断这项改动是在加强入口、合同层、示例链路还是回归面；若都对不上，应视为边界外或至少需要先澄清。
- 通过条件：项目级故事与测试文档能帮助贡献者拒绝“看起来相关、实际上会扩范围”的改动。
- 这次明确不要求：不要求这里替代详细设计评审。
- 失败/越界边界：如果一个改动既对不上当前交付物，也不补入口或回归，却仍被当成当然的下一步，说明项目主线仍然模糊。

### 测试用例 TC-3

- 对应故事：US-3
- 前提：仓库持续被人和 AI coding 共同修改。
- 当：运行最小单元测试。
- 那么：测试应确认项目级故事与测试文档仍然存在，并保有用户故事、测试用例、非目标和验收责任人这几项最小内容。
- 通过条件：一旦 `PROJECT_STORIES_AND_TESTS.md` 退化成没有故事、没有测试或没有验收责任人的摘要，回归会失败。
- 这次明确不要求：不要求自动测试判断每条自然语言陈述的业务优劣。
- 失败/越界边界：如果项目级故事与测试文档缺失或严重缩水，而测试仍然通过，说明本仓库自己还没有把“可维护性”落实到回归面。

### 测试用例 TC-4

- 对应故事：US-4
- 前提：AI-Native 团队准备采用 `files-driven`，并且团队成员主要通过 AI 工具协作。
- 当：从 `README.md` 的培训入口进入，再读 `docs/使用手册.md` 与 `references/AI-Native同构团队协作.md`。
- 那么：团队成员应能解释为什么这里默认先按“多个执行上下文共享同一份 Git 存储”理解协作，并能区分 runtime / 工具入口 与仓库级规则真源。
- 通过条件：无需额外聊天补充，也能说清“为什么项目主问题是共享存储上的真源、路径和写权，而不是工具品牌对比”。
- 这次明确不要求：不要求团队在首次培训后就掌握所有共享矩阵、流程合同或 schema 细节。
- 失败/越界边界：如果读完入口材料后，团队仍然把协作问题主要理解成“选哪个 AI 工具更好用”或仍把仓库规则文件视为工具包装文案，说明这条能力还没真正落到用户问题上。

### 测试用例 TC-5

- 对应故事：US-5
- 前提：有人准备基于本仓库当前约定搭一个 governed pack。
- 当：按 `QUICKSTART.md`、smoke pack 和 validator 的入口顺序搭建或检查一个 pack。
- 那么：应能说明为什么 `BOUNDARY.md` 必须先于 workflow 合同出现，并能指出这个 pack 服务哪些场景、故事和测试锚点。
- 通过条件：pack 作者能用 `BOUNDARY.md + workflow.contract.json + validator` 解释最小边界入口、最小合同链和至少一个失败/越界边界之间的关系。
- 这次明确不要求：不要求这里一次性验证完整生产环境、所有审批模式或所有对象家族。
- 失败/越界边界：如果一个 pack 只有合同和状态文件，没有显式边界入口或失败边界，但仍被视为“已经足够可用”，说明当前能力还没有真正解决 pack 作者的真实问题。

### 测试用例 TC-6

- 对应故事：US-6
- 前提：团队负责人准备向新成员或团队做一次 30 到 45 分钟培训。
- 当：以 [docs/非工程背景起步.md](docs/非工程背景起步.md) + `docs/使用手册.md` 组织培训材料。
- 那么：应能先把“哪份文件算数 / 今天先做什么 / 哪些先别改”讲成可执行工作语言，再围绕“真实问题 -> 成因 -> 常见方式为什么不够 -> `files-driven` 怎么解 -> 用户故事与正向反馈迭代 -> 团队今天怎么执行”讲清楚这套方法。
- 通过条件：培训材料能先让非工程背景读者安全开工，再服务团队落地，而不是退化成概念列表、目录漫游或元叙事说明。
- 这次明确不要求：不要求在一次培训里完整覆盖所有 references、schema 字段或内部演进历史。
- 失败/越界边界：如果培训最后仍然主要在讲“这个仓库有哪些文档”“这个理论从哪里来”，或者非工程背景读者听完仍然不知道哪份文件算数、今天先做什么，说明培训入口还没有对准目标。

### 测试用例 TC-7

- 对应故事：US-7
- 前提：有人需要判断这套仓库最近关于 `workflow`、schema、validator 和 smoke pack 的更新，是否真的在提升 harness 侧的可执行性与恢复能力。
- 当：从 `README.md`、`docs/项目治理能力模型.md`、`QUICKSTART.md`、`examples/smoke-governed-review/BOUNDARY.md` 和 `examples/smoke-governed-review/WORKFLOW.md` 的入口顺序阅读当前资产。
- 那么：应能说明这轮 workflow 重构不是单纯“多了几个 JSON 文件”，而是把控制语义从 prose-first 解释推进到最小可执行合同链，并解释 `workflow.contract.json`、`workflow.state.json`、`workflow.events.jsonl`、顶层 `checks` 与 validator 分别承担什么职责。
- 通过条件：读者能够用“减少运行时歧义、提高检查稳定性、降低恢复成本、提升 harness 可消费性”来解释这轮能力提升，而不是只把它理解成 schema 扩展或目录调整。
- 这次明确不要求：不要求这里已经证明所有 runtime 或 harness 都与当前合同层完全适配，也不要求此时就覆盖全部高风险生产场景。
- 失败/越界边界：如果读者读完这些入口后，仍然把 workflow 重构理解成“只是把说明文档拆成更多文件”或说不清它为什么会提升 harness 效能，说明当前项目故事还没有把这条真实问题面表达清楚。

### 测试用例 TC-8

- 对应故事：US-8
- 前提：有人第一次需要把 discussion 管理和执行晋升讲清，但不想再去 HQMDClaw 或 AIJournal 里逆向找案例。
- 当：从 `README.md` 和 `docs/使用手册.md` 进入，再读 `references/讨论收口与晋升.md`、`examples/discussion-decision-task/BOUNDARY.md`、`examples/discussion-decision-task/WORKFLOW.md`、`examples/adversarial-convergence/README.md` 与 `examples/multi-tool-process-projection/process-projection.md`。
- 那么：应能说明什么时候开正式 discussion、什么时候升级到质询、什么时候压成 decision package、什么时候进入 task / decision，以及什么时候才需要补 process projection。
- 通过条件：无需额外依赖外部项目，也能沿着仓库内的主路径和条件分支看懂 discussion 收口与晋升。
- 这次明确不要求：不要求这一阶段就掌握所有 schema、validator 或源项目里的具体角色编排。
- 失败/越界边界：如果读者看完仓库内材料后，仍然只能说出流程名，不能判断 discussion 何时晋升、何时质询、何时只补 process projection，说明这轮新增资产还没有形成真正可用的主路径。

### 测试用例 TC-9

- 对应故事：US-2
- 前提：有人准备改造 `SKILL.md`、`references/输出约定.md` 或相关 metadata，希望默认执行路径更轻，但又不能伤到 skill 的召回面。
- 当：对照 `SKILL.md`、`agents/openai.yaml`、`README.md`、`QUICKSTART.md`、examples、validator 和测试基线检查这轮改动。
- 那么：应能确认本轮改造同时满足三件事：触发面不缩水、默认执行路径更轻、文档入口与 validator/examples/tests 仍保持一致。
- 通过条件：现有 governed-pack 与 discussion 回归继续通过，并新增 skill 级回归冻结触发家族和轻量化指标，不再只靠人工记忆守住这些边界。
- 这次明确不要求：不要求这一轮同时合并 schema、重写 validator 或清理所有历史背景资产。
- 失败/越界边界：如果默认路径变短了，但老请求不再自然命中 skill，或入口文档与 validator/examples 口径重新漂移，说明这轮精简只是把风险藏起来，没有真正提升可维护性。

### 测试用例 TC-10

- 对应故事：US-9
- 前提：有人从空目录开始，希望把 `files-driven` 安装进一个新项目。
- 当：运行官方 starter bootstrap，再通过统一 `manage` CLI 执行 `register / repair / audit`，最后依次执行 scaffold validator 和 pack validator。
- 那么：应能得到一个同时包含 `BOUNDARY.md`、最小 governed pack、`governance/files.registry.json`、`governance/intent.routes.json`、starter profile 线索和项目 `Skill` 骨架的 starter，并且两类 validator 都能通过。
- 通过条件：冷启动不再要求先自己拼 example、schema 和目录；官方 starter 本身就是一个可跑的最小起点。
- 这次明确不要求：不要求 starter 一次性生成生产级业务对象或复杂多 skill 拓扑。
- 失败/越界边界：如果 starter 只能生成目录壳子，或者只能通过文档阅读手工补齐关键资产，说明它还不是有效脚手架。

### 测试用例 TC-11

- 对应故事：US-10
- 前提：项目里新增、迁移或改义了一个核心文件。
- 当：文件存在，但没有被注册到文件注册表，或者 identity core 与实际角色不一致，或者 annotations 与实际角色不一致。
- 那么：scaffold validator 应直接报错，并指出缺失的是注册事实还是角色漂移。
- 通过条件：文件出生和角色变更不再只靠人工约定，而有稳定的机读守卫。
- 这次明确不要求：不要求这一阶段就做自动修复；只要求先把 drift 打回去。
- 失败/越界边界：如果新增文件、路由漏绑或角色漂移仍然能通过回归，说明 `files engine` 还没有真正站起来。

### 测试用例 TC-12

- 对应故事：US-11
- 前提：同一轮讨论里同时涉及本仓库入口、当前 skill 的执行导览和下游 starter。
- 当：从 README、统一真源、脚手架工程说明和 starter README 进入。
- 那么：应能说明哪些是 `repo.files-driven` 资产，哪些是 `skill.files-driven` 资产，哪些是 `meta-skill capability`，哪些属于 `downstream project instance`。
- 通过条件：不依赖额外聊天补充，也能判断某个文档、schema、脚本或 starter 文件该落在哪一层。
- 这次明确不要求：不要求把四层边界直接编码成所有 starter 字段。
- 失败/越界边界：如果读完入口材料后，维护者仍会把 self-hosting 仓库入口误当成下游模板，或把下游 starter 误写回本仓库入口，说明这轮收口仍然不稳。

### 测试用例 TC-13

- 对应故事：US-12
- 前提：有人只看仓库入口、执行导览、脚手架工程说明和 starter README，不额外依赖对话记忆。
- 当：读取 `README.md`、`SKILL.md`、`docs/files引擎脚手架工程.md`、`schemas/README.md` 和 `starters/minimal-files-engine/README.md`。
- 那么：应能明确说出 `install` 由 bootstrap 完成，`register / repair / audit` 由统一 `manage` CLI 完成，registry 只保留 identity core + annotations，starter 专属形状约束不放进 manifest。
- 通过条件：不需要再翻 examples 或 tests，也能把动作面、注册面和 starter profile 边界说清。
- 这次明确不要求：不要求这里已经扩成平台级 CLI；只要求最小命令面和动作路径可用。
- 失败/越界边界：如果读者仍然只能把这些内容理解成“又多了一套解释文档”，说明元 skill 的动作面还没有真正上首屏。

## 当前非目标

- 不把 `files-driven` 在当前阶段扩成全功能平台产品。
- 不承诺这一版就覆盖 hostile-environment 安全、细粒度权限或完整部署级防护。
- 不要求每一份 reference 都立即转成 JSON 合同。
- 不把 smoke pack 误当成完整项目模板或默认最佳实践大全。

## 质量判断参考

- 参考标准是“一个对新接手的人和 AI coding 都足够清楚、最小可执行、可持续回归的开源方法项目”。
- 质量重点是边界清楚、入口稳定、合同层最小闭环可跑、starter 与校验链相互印证，并且 workflow 重构能真实提升 harness 的可执行性、可验证性和可恢复性，而不是材料数量越多越好。
- 能力模型阶段判断只认 [docs/项目治理能力模型.md](docs/项目治理能力模型.md)；`docs/项目治理能力模型_v1.md` 与 `docs/治理能力模型_v1_下一阶段执行计划.md` 只保留为历史兼容与迁移背景，不再作为并行阶段基线。
- governed pack / contract 侧的最小通过线则单独按 `tranche v1` 理解，不与能力模型 `v1 -> v2 -> v2.1` 混写。

## 验收责任人

- `files-driven` 仓库维护者，以及任何负责审查是否继续按“统一底层真源 + 最小可执行基线”推进的人。
