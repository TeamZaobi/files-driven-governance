# files 引擎脚手架工程

这份文档只回答一件事：
当 `files-driven` 不再只解释世界观，而要作为一个 `meta-skill` 帮下游项目把 `files engine` 装起来时，
最小必须交付哪些脚手架工程。

它不是底层能力模型真源。
能力模型基线仍只认 [项目治理能力模型](项目治理能力模型.md)。
这份文档只负责把“修正后的需求、缺口、质询和执行收敛”写清。

## 1. 修正后的核心需求

这轮修正后的主问题，不是“理念够不够完整”，而是：

**这套方法能不能把下游项目从空目录带到一个可注册、可解析、可验证、可继续编辑的最小 `files engine` 起点。**

最小通过线收成 3 条：

1. 第一次采用的人或 AI 代理，应能在 `10-15` 分钟内起出一个最小可验证起点
2. 新文件出生时，就要稳定声明 identity core；需要时再补 annotations，而不是事后补解释
3. starter、registry、route、validator 和下一步编辑点，必须形成一条闭环，而不是靠人从 example 倒推

## 2. 四层边界

### 2.1 `repo.files-driven`

这是本仓库自己作为被维护对象的资产层。
它同时扮演 `reference implementation + regression fixture`。
它负责：

- 维护公开入口
- 维护统一真源
- 维护项目故事和测试
- 维护 schema 草案、starter、脚本与回归

### 2.2 `skill.files-driven`

这是当前技能包本身。
它负责：

- 给代理执行导览
- 先判动作、边界和一级关口
- 给出应读什么、应写什么、何时升级

### 2.3 `meta-skill capability`

这是当前最缺、也最该补齐的一层。
它负责：

- 为下游项目提供官方 starter
- 为文件注册表提供机读 schema
- 为路由入口提供 route contract
- 为冷启动提供 bootstrap 脚本
- 为 `register / repair / audit` 提供统一 `manage` CLI
- 为 starter 专属形状约束提供单独的 starter profile
- 为 starter 完整性提供 scaffold validator
- 为 repo-local hooks 提供项目级 policy 真源与工具适配模板

### 2.4 `downstream project instance`

这是被 `files-driven` 驱动的具体项目实例。
它负责承载：

- 项目边界入口
- 项目 `Skill`
- 项目规则
- 项目实体
- governed pack / workflow 合同和运行实例

一句话区分：

**仓库维护资产，技能负责判路，元技能负责装引擎，下游实例负责承载项目事实。**

### 2.5 能力模型下的 `AI-Native E2E` / replay-harness 承接层

当问题已经从“给下游项目装 files engine”升级到“证明这套治理能力在 `self-hosting` 下仍可回放、可恢复、可复核”时，这里不再只讲 starter 安装，而要承接能力模型真源已经定义好的 `AI-Native E2E` 执行骨架。

- `AI-Native E2E` 已并入统一能力模型主真源，不单独发明第二套世界观
- 下游会有独立的 `replay/harness starter`，但它只承接 `conversation/replay E2E` 的执行骨架，不定义新的断言世界观
- 这条验证线仍然消费本节定义的四层边界、`manifest / registry / routes / validator` 分工，不反过来重写它们

## 3. 从多个角色看缺口

### 3.1 产品 / 架构负责人

缺的是 repo 级架构蓝图：

- 哪些资产属于仓库自身
- 哪些资产属于技能包
- 哪些资产属于下游 starter
- 哪些资产属于项目实例

没有这张蓝图时，README 和 QUICKSTART 容易把 pack、starter 和仓库入口混讲。

### 3.2 下游项目采用者

缺的是官方 starter 闭环：

- 从零生成一个最小项目起点
- 生成后知道先改哪里
- 不需要先读完整 example 再自己拼路径

### 3.3 validator / runtime 工程师

缺的是 repo 级引擎执行面：

- `scaffold manifest`
- `hooks policy`
- `file registration schema`
- `files registry`
- `intent routes`
- hooks template / script scaffold
- bootstrap / resolve / validate 脚本
- 能把 unregistered file、route 漏绑、角色漂移打回的测试

### 3.4 培训 / onboarding 负责人

缺的是一条稳定的教学路径：

- 先起 starter
- 再看文件注册表
- 再看 route 怎么消费这些文件
- 最后看 validator 怎样把 drift 打回来

没有这条路径时，培训很容易回到“概念说明 + 目录漫游”。

## 4. 质询与答辩

| 质询 | 通过线 | 当前决议 |
| --- | --- | --- |
| 只保留真源、starter、schema 和 validator，新项目还能不能从零长出来？ | 必须能给出冷启动闭环，而不是要求继续读长文 | 增加官方 starter 与 bootstrap 脚本 |
| 新文件出生时，最小必须变量是什么？ | 必须落成 machine-readable 注册项 | 增加 `file.registration.schema.json` |
| `files-driven` 的核心资产到底是文档、registry 还是 generator？ | 三者都要有，但不能互相替代 | README 只做入口；registry 和 generator 必须机读 |
| starter 拓扑、文件岗位、证据类型、路由绑定发生变化时，谁先改？ | 先分清是拓扑变更、身份变更还是路由变更，再按单向级联改 | 拓扑先改 manifest；身份先改 registry；route 只在消费面改 |
| 如何防止把 self-hosting 仓库入口误当成下游 starter？ | 必须显式区分 repo / skill / meta-skill / downstream | 本文与 starter README 都写死四层边界 |
| starter 专属形状约束应该放哪里？ | 不能继续塞进 manifest | 单独 starter profile 持有，manifest 只保留拓扑 |
| workflow 能不能继续只靠 prose 推断？ | 不能；控制面要消费注册与 route 合同 | starter 加 `intent.routes.json`，validator 校 route 绑定 |

## 5. 收敛后的执行面

当前决定先补一条最小而完整的执行链：

1. [starters/minimal-files-engine/](../starters/minimal-files-engine/): 官方最小 starter
2. `governance/hooks.policy.md`: 项目级 hooks 真源
3. `tooling/hooks/`: repo-local hooks 模板与脚本
4. [schemas/scaffold.manifest.schema.json](../schemas/scaffold.manifest.schema.json): starter 拓扑合同
5. starter profile: starter 专属形状约束合同
6. [schemas/file.registration.schema.json](../schemas/file.registration.schema.json): 单个文件注册项
7. [schemas/files.registry.schema.json](../schemas/files.registry.schema.json): 仓库级文件注册表
8. [schemas/intent.routes.schema.json](../schemas/intent.routes.schema.json): workflow / tool 可消费的路由合同
9. [scripts/bootstrap_files_engine_starter.py](../scripts/bootstrap_files_engine_starter.py): 冷启动脚本
10. 统一 `manage` CLI: `register / repair / audit`
11. [scripts/validate_files_engine_scaffold.py](../scripts/validate_files_engine_scaffold.py): scaffold 校验脚本

这条链的目标不是一次性做成全功能引擎，而是先让这件事从“隐含知识”变成“官方可执行资产”。

## 6. 脚手架耦合与级联原则

这一轮先冻结 3 条原则：

1. `scaffold.manifest.json` 只定义 starter 拓扑
   - 它回答 validator 应跟踪哪些路径和 glob，不承担文件身份或 route 语义
2. `files.registry.json` 只定义文件身份核心 + annotations
   - 它冻结 `file_id / path / family / layer / work_post` 作为 identity core
   - `evidence_type / truth_status / write_roles / workflow_binding / stale_policy` 只是 annotations
   - 它不反向持有 `route_id`
3. `intent.routes.json` 只做入口编排
   - 它单向消费 registry 里的 `file_id`
   - route 重命名、入口动作改写、读写目标调整，不应要求回写 registry
4. starter 专属形状约束属于单独 starter profile，不属于 manifest
5. `bootstrap` 只播种 starter，`manage` CLI 负责 `register / repair / audit`

这意味着默认改动顺序也必须分开：

1. 只改某个工具的 hook 接法：先改 `tooling/hooks/`，不要先改项目真源
2. 要改“哪些动作可拦、哪些只记录”：先改 `governance/hooks.policy.md`
3. 只改 route 行为：只改 `intent.routes.json`
4. 新增或移动 tracked 文件：先改 `scaffold.manifest.json`，再改 `files.registry.json`，最后按需改 route
5. 文件岗位或证据类型变化：先改 `files.registry.json`，再检查 route 消费面是否需要刷新
6. starter 专属形状变化：先改 starter profile，再看 validator 是否需要同步

`bootstrap` 只负责播种 starter。
starter 起出来以后，hook 真源由 `governance/hooks.policy.md` 管，拓扑由 manifest 管，身份由 registry 管，动作编排由 routes 管。

## 7. 新文件注册表的最小变量

当前先冻结 identity core：

1. `file_id`
2. `path`
3. `family`
4. `layer`
5. `work_post`

其余字段按 annotations 处理：

6. `evidence_type`
7. `truth_status`
8. `write_roles`
9. `workflow_binding`
10. `stale_policy`
11. `upstream_refs`

这里的关键不是把标签越做越多，
而是把“这个文件是谁、它在干什么、它能证明什么、谁能写、被哪个 route 消费”分开存。

## 8. 当前不做

- 不把这一轮扩成全量 `files engine` 产品
- 不在这一轮引入完整 stale graph 或自动刷新拓扑
- 不要求所有 reference 立即转成 route contract
- 不把 self-hosting 仓库资产直接拿去冒充下游 starter
