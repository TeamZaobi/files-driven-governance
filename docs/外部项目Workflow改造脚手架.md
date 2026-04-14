# 外部项目 Workflow 改造脚手架

这份脚手架只用于一种场景：

用户已经有一个外部 `AI-Native` 项目，
并且明确想判断“是否要把现有 workflow 改造成宿主优先、脚本补强、必要时 `CLI` 节点执行”的形态。

它不是通用 workflow 引擎，
也不是要求你一上来就落完整 runner。
它只提供一个最小可执行 starter。

这里先把边界讲清：

- 这份文档先讲判断方法和最小改造路径
- 它还不是 `manage` CLI 的正式子命令
- 当前正式动作面仍以 `install / register / repair / audit` 为准

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

### 6. 先定 benchmark 和迁移口

改造前就先写清：

1. 用什么 benchmark 证明流程更稳
2. 用什么信号证明过度设计了
3. 未来是否要迁移到独立 agent/runtime

## 最小 benchmark 模板

```md
## Benchmark
- 正样本：
- 失败样本：
- 通过信号：
- 回退信号：
```

示例填法：

```md
## Benchmark
- 正样本：一条宿主原生 workflow 已经能稳定跑通的短链路
- 失败样本：一条过去反复跳步、越权或恢复困难的复杂链路
- 通过信号：节点顺序稳定、角色不越权、恢复不靠聊天回忆
- 回退信号：新增 runtime 资产明显多于真实收益，或宿主原生能力已经足够但脚手架仍显著增重
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
