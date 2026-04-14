# 外部项目 Workflow 改造脚手架

这份脚手架只用于一种场景：

用户已经有一个外部 `AI-Native` 项目，
并且明确想判断“是否要把现有 workflow 改造成宿主优先、脚本补强、必要时 `CLI` 节点执行”的形态。

它不是通用 workflow 引擎，
也不是要求你一上来就落完整 runner。
它只提供一个最小可执行 starter。
当前也只能把它视为一次外部项目“校本化改造”实践提炼出的个案 benchmark，
还不能直接当成已经跨项目验证完的通用产品面。

这里先把边界讲清：

- 这份文档先讲判断方法和最小改造路径
- 它还不是 `manage` CLI 的正式子命令
- 当前正式动作面仍以 `install / register / repair / audit` 为准
- 当前默认把它视为 `candidate benchmark`，不是已经晋升完的通用 starter

## 这个 benchmark 当前为什么只能先按个案看

当前先把这条线压成个案 benchmark，而不是直接抬成通用能力，原因有三条：

1. 它主要来自一次最新的外部 workflow 改造实践，样本量还不够。
2. 当前收益最明确的，是 `human authority / machine-readable control plane / hook policy` 这组分层思路，不是某个固定文件组合本身。
3. 一旦把个案里的文件名、宿主习惯或模型品牌直接抬成通用模板，最容易把局部最优误写成仓库级真源。

所以这份脚手架当前更适合回答：

- 遇到类似外部项目时，先用什么框架去诊断
- 什么时候需要 control-plane 合同化
- 哪些合同面值得优先试做

它当前还不适合直接回答：

- 任何项目都应该按这套文件结构落盘
- 任何 workflow 都应该先加 `runner + hooks + model-routing`
- 这就是 `files-driven` 已经正式产品化的统一外部 starter

## 先决条件

使用前，至少先确认：

1. 当前项目的主要真源文件在哪里
2. 当前 workflow 到底是显式合同、宿主约定，还是散落在对话里
3. 当前失控现象是真源漂移、流程跳步、角色越权，还是 runtime 恢复困难

如果这三件事还没说清，先回到：

- [references/问题诊断与控制强度分级.md](../references/问题诊断与控制强度分级.md)
- [references/执行面判定与CLI生产策略.md](../references/执行面判定与CLI生产策略.md)

## 什么时候优先考虑脚本化改造

下面几类外部项目，优先考虑把 workflow 升级成“宿主优先、脚本补强”的形态：

- 未来可能迁移到独立于宿主的 agent/runtime
- 流程偏航成本高
- 需要恢复、回放或审计
- 需要跨工具、跨会话稳定执行
- 宿主原生 workflow 还不够稳，无法单独兜住控制

## 最小改造步骤

### 1. 收当前 workflow 现状

至少收四样东西：

1. 当前 workflow 来源
2. 当前主要失控现象
3. 当前宿主能力现状
4. 当前希望达到的控制强度

### 2. 先做问题分型

把问题先分到下面几类之一：

- 真源不清
- 控制不足
- 角色边界不清
- runtime 恢复不足
- 工具适配冲突

如果问题主要不在控制层，就不要把改造目标误写成脚本化。

### 3. 选择控制强度

优先按 `L0 -> L4` 判断：

- `L0` 主线程
- `L1` `subagent`
- `L2` 宿主原生 workflow / approvals
- `L3` `CLI`
- `L4` 脚本 runner + `CLI`

只有当 `L0-L2` 兜不住时，再上 `L3-L4`。

### 4. 切分宿主 / CLI / runner 分工

用最小表先写清：

| 层 | 负责什么 | 先不要负责什么 |
| --- | --- | --- |
| 宿主 | 计划、审批、checkpoint、thread context | 外部脚本级 state 编排 |
| `CLI` | 节点执行、checker、actuator、可落文件产物 | 长链路自治流转 |
| runner | state / events / projection、恢复、回放、审计 | 改写真源或偷换 workflow 语义 |

### 5. 只补最小 runtime artifact

不是每个项目都要一上来补全套 governed pack。
只有进入 `L3/L4` 时，再按需补：

- `BOUNDARY.md`
- `workflow.contract.json`
- `task packet`
- `workflow.state.json`
- `workflow.events.jsonl`
- `status.projection.json`

### 5.1 prose-first workflow 已经扛不住时，补最小 control plane 合同

如果当前项目已经出现下面这些症状：

- 宿主 workflow 能跑，但控制面主要靠人脑路由
- `SKILL`、README、状态页和脚本入口一起在定义流程
- hook 已经出现，但没有项目级 hook 真源
- 不同模型/不同工具的分工开始写进阶段说明，而不是单独配置

那就不要再只补一份更长的 prose。
这时应显式分开三层：

1. `human authority layer`
   - 负责冲突裁决、人工 override、责任边界说明
2. `machine-readable control plane`
   - 负责阶段图、工件流、模型路由、hook 注册和运行时状态
3. `leaf skill / tool adapter layer`
   - 负责具体能力说明、工具接法、CLI 节点执行

一个稳妥的最小合同面通常是：

| 文件 | 角色 | 最小字段 |
| --- | --- | --- |
| `config/workflow-control-plane.json` | 阶段图和工件流真源 | `schema_version`、`domain`、`entrypoints`、`stages`、`artifacts`、`change_classes`、`stop_conditions` |
| `config/model-routing.json` | 逻辑角色到具体模型的映射 | `schema_version`、`roles`、`models`、`primary`、`fallback`、`capabilities`、`stage_bindings` |
| `config/hook-policy.json` | hook 注册表 | `schema_version`、`hooks`、`trigger_paths`、`change_classes`、`commands`、`blocking`、`report_format` |
| `local/state/workflow.state.json` | 当前运行时快照 | `current_stage`、`current_owner_role`、`artifact_refs`、`blocked_reason`、`updated_at` |
| `local/state/workflow.events.jsonl` | 运行时事件账本 | `ts`、`actor`、`event`、`from_stage`、`to_stage`、`artifact_ids`、`note` |

这里要特别守两条线：

1. 阶段图里优先写逻辑角色，不直接写品牌或供应商名
2. 具体模型选择留在 `model-routing`，不要反向写进 `workflow-control-plane`

例如阶段图里更稳的是：

- `art_direction`
- `logic_governance`
- `code_implementation`

而不是把 `Gemini / Codex / Claude` 直接硬编码进 stage graph。

### 5.2 human authority、机读控制面和 leaf skill 怎么分层

如果当前仓库里已经有：

- 一份 `ops-authority`、运行规约或人工裁决页
- 一批 `skills/*/SKILL.md`
- 若干 CLI 脚本、hook 模板或 workflow 配置

那推荐这样分：

| 层 | 主要职责 | 不要承担什么 |
| --- | --- | --- |
| `human authority layer` | 冲突裁决、人工 override、例外说明、发布口径 | 不要承载阶段图、模型路由和 hook registry |
| `machine-readable control plane` | stage registry、model registry、hook registry、runtime state/events | 不要写成长篇操作说明或品牌化教程 |
| `leaf skill / tool adapter layer` | 解释每个能力包怎么用、CLI 节点怎么跑、hooks 怎么接宿主 | 不要继续充当控制真源 |

一句话说：

**人类权威层负责“最后谁说了算”，机读控制面负责“机器怎么稳定跑”，leaf skill 负责“具体能力怎么被解释和调用”。**

### 6. 先定 benchmark 和迁移口

改造前就先写清：

1. 用什么 benchmark 证明流程更稳
2. 用什么信号证明过度设计了
3. 未来是否要迁移到独立 agent/runtime

### 6.1 benchmark 晋升原则

这类 benchmark 不要做得太重，也不要做得太薄。
先保留一条薄共同骨架，再给每个 benchmark 留变量槽位。

共同骨架只保留四件事：

1. 诊断：当前对象、当前问题、失控现象、控制强度。
2. 分工：human authority、machine-readable control plane、leaf skill / tool adapter、宿主 / CLI / runner。
3. 证据：正样本、失败样本、通过信号、回退信号。
4. 晋升：是否需要独立 agent/runtime，还是继续停在 benchmark。

其余内容按 case 变量保留，不强行统一成一套重模板。
workflow 是这次的实例；下次可能是 hooks 或 scaffolding。
LLM 的作用是判断该补到哪一层，不是把所有 benchmark 拉成同一形状。

### 6.2 从个案 benchmark 晋升为通用能力，至少过这几条线

如果未来想把这条线从“外部个案 benchmark”升级成“正式能力面”，至少要补下面这些通过条件：

1. 不少于 `2-3` 个外部项目样本，而不是只看一次成功改造。
2. 样本之间要有异质性：
   - 不能全是同一类内容项目
   - 不能全依赖同一宿主
   - 不能全绑定同一组模型品牌
3. 相同分层思路必须反复证明有效：
   - `human authority`
   - `machine-readable control plane`
   - `leaf skill / tool adapter`
4. 至少要证明“逻辑角色先于品牌路由”在跨项目里仍成立，而不是只对某一次模型搭配有效。
5. 必须能明确指出什么情况下不该上这套 control-plane 合同面。
6. 最终要么进入正式 starter / CLI / audit，
   要么继续停留在 benchmark，不模糊挂在两者之间。

## 最小 benchmark 模板

```md
## Benchmark
- 本次 benchmark 类型：workflow / hooks / scaffolding / 其他
- 正样本：
- 失败样本：
- 通过信号：
- 回退信号：
- 变量槽位：
  - 当前对象：
  - 当前宿主：
  - 当前工件：
  - 这次明确不泛化的点：
```

示例填法：

```md
## Benchmark
- 本次 benchmark 类型：workflow
- 正样本：一条宿主原生 workflow 已经能稳定跑通的短链路
- 失败样本：一条过去反复跳步、越权或恢复困难的复杂链路
- 通过信号：节点顺序稳定、角色不越权、恢复不靠聊天回忆
- 回退信号：新增 runtime 资产明显多于真实收益，或宿主原生能力已经足够但脚手架仍显著增重
- 变量槽位：
  - 当前对象：Workflow 改造
  - 当前宿主：现有 AI-Native 项目
  - 当前工件：workflow-control-plane / model-routing / hook-policy / state / events
  - 这次明确不泛化的点：不把 workflow 的文件组合直接抬成通用模板
```

## 最小 starter 模板

下面这份模板可以直接作为外部项目改造包的第一页：

```md
# 外部项目 Workflow 改造包

## 当前对象
- 项目名：
- 当前宿主：
- 当前 workflow 来源：

## 当前问题
- 主要失控现象：
- 偏航代价：
- 当前最痛的恢复问题：

## 控制强度判定
- 目标级别：`L0 / L1 / L2 / L3 / L4`
- 为什么不是更低：
- 为什么还不需要更高：

## 执行面分工
- 宿主负责：
- subagent 负责：
- CLI 负责：
- runner 负责：

## 最小新增资产
- 必须新增：
- 可选新增：
- 这轮明确不做：

## Benchmark
- 正样本：
- 失败样本：
- 通过信号：
- 回退信号：

## 迁移判断
- 是否需要迁移到独立 agent/runtime：
- 如果需要，当前先保留哪些可迁移执行面：
```

## 反过度设计约束

1. 不要把宿主已具备的 workflow 能力重做一遍
2. 不要为了“未来可能要迁移”就提前落完整平台
3. 不要把 `CLI` 使用本身当成目标
4. 不要把 runtime artifact 数量当成成熟度
5. 必须先用 benchmark 证明改造确实提升了控制稳定性

## 一句话收口

**外部项目 workflow 改造，先做诊断和分工，再补脚本和 CLI；先求刚好够用，不求一次到位。**
