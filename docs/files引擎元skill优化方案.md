# files 引擎元 skill 优化方案

这份文档回答一件事：
当 `files-driven` 已经具备最小 starter 闭环之后，下一步怎样把它从“解释型治理 skill”继续推到更完整的 `meta-skill`。

它不是底层能力模型真源。
能力模型本体仍以 [项目治理能力模型](项目治理能力模型.md) 为准。
这份文档只负责记录本轮的系统分析、计划、方案、质询与执行收敛。

## 1. 修正后的问题定义

当前的主问题不再是“世界观够不够统一”，而是：

**`files-driven` 是否已经具备稳定帮助下游项目安装、登记、修复、审计一个 `files engine` 的元 skill 能力。**

按这个问题看，当前仓库已经有明显进步：

1. 有 starter
2. 有 manifest / registry / routes
3. 有 bootstrap 与 validator
4. 有基础回归

但还存在三个结构性缺口：

1. registry 仍把“身份事实”和“策略注释”揉成同一层
2. 元 skill 的首屏动作目录还不够清晰
3. validator 还残留一部分对官方 starter 形状的硬编码依赖

## 2. 系统分析结论

### 2.1 registry 结论

当前真正的 engine-critical identity 只需要：

1. `file_id`
2. `path`
3. `family`
4. `layer`
5. `work_post`

其余字段更适合降成 overlay 或 annotations，例如：

1. `evidence_type`
2. `truth_status`
3. `write_roles`
4. `workflow_binding`
5. `upstream_refs`
6. `stale_policy`

### 2.2 元 skill 动作面结论

当前元 skill 最该对外暴露的不是更多总论，而是 4 个稳定动作：

1. `install`
2. `register`
3. `repair`
4. `audit`

解释层不是删除，而是下沉成这些动作的支撑说明。

### 2.3 coupling / cascade 结论

当前正确的单向级联应继续固定为：

1. `manifest`
2. `registry`
3. `routes`
4. `validator`

已经不该再回到：

- route 反向写 registry
- runtime 回写 topology
- repo/self-hosting 入口天然扮演下游模板

### 2.4 repo / self-hosting 偏置结论

当前剩余偏置主要在叙事和测试样本层：

1. repo 仍然容易被读成“通用模板本人”
2. 一部分测试仍在守 repo 自述短语，而不是专门守元 skill 行为

因此接下来应把 repo 更明确降级成：

**reference implementation + regression fixture**

而把通用动作能力集中到 `meta-skill capability`。

## 3. 串行执行计划

### Node 1. 问题分析

- 并行审 registry、动作面、coupling/self-hosting 偏置
- 收敛共识

### Node 2. 方案冻结

- 把分析结果写入本方案
- 冻结目标、范围、非目标、执行 tranche

### Node 3. 质询与答辩

- 质询是否过度设计
- 质询是否削弱回归价值
- 质询是否把 repo 经验错误地上升为全局规律
- 质询是否给出了真实可执行动作，而不是新口号

### Node 4. 执行

- 收缩 registry 到“核心身份层 + overlay”
- 抬高元 skill 动作目录
- 补 `register / repair / audit` 的最小工具面
- 继续把 starter 特有形状约束从 validator 代码移向 profile 化声明

### Node 5. 验收

- 设计并运行 install / register / repair / audit 的刁钻端到端测试
- 跑专项回归和全量回归

## 4. 解决方案

### 4.1 registry 双层化

收口成两层：

1. `identity core`
   - `file_id / path / family / layer / work_post`
2. `annotations`
   - `evidence_type / truth_status / write_roles / consumed_as / upstream_refs / stale_policy`

原则：

- validator 默认只要求核心身份层
- annotations 只在需要表达策略、消费、刷新或写权时携带

### 4.2 元 skill 动作目录

入口层统一暴露：

1. `install files engine`
2. `register new file`
3. `repair scaffold drift`
4. `audit files engine`

说明层默认回答：

1. 当前该用哪个动作
2. 先读哪些资产
3. 先改哪一层
4. 什么时候升级到更重的治理面
5. `install` 通过 bootstrap 完成，`register / repair / audit` 通过统一 `manage` CLI 完成

### 4.3 工具面

当前 tranche 先补最小闭环：

1. 保留 bootstrap 作为 `install`
2. 收口 `register / repair / audit` 到统一 `manage` CLI
3. `manage` CLI 读取 registry core + annotations 与 starter profile
4. `repair` 输出 ordered repair plan
5. `audit` 输出 finding-style 报告，而不只是一条 fail-fast 报错

### 4.4 validator profile 化

把 starter 专属形状约束继续往数据层下沉：

1. starter profile 负责声明 starter 专属形状约束
2. manifest 只负责 starter 拓扑
3. starter profile 负责声明 required work posts
4. starter profile 负责声明 runtime / projection / workflow truth expectations
5. validator 读取 starter profile，不继续在代码里固化“官方 starter 就是全局真理”

## 5. 质询与答辩

| 质询 | 通过线 | 当前答辩 |
| --- | --- | --- |
| 继续加动作会不会把元 skill 做得太重？ | 必须只补最小闭环，不做平台化产品幻想 | 本 tranche 只补 `install / register / repair / audit` 的最小工具面 |
| registry 瘦身会不会损失语义？ | 不能丢掉关键信息，但可以分层 | 核心身份层保留；策略语义下沉到 annotations |
| 把 repo 降成 regression fixture 会不会削弱 self-hosting 价值？ | 不能削弱回归价值 | self-hosting 继续保留为回归样本，但不再冒充通用模板 |
| validator profile 化会不会增加复杂度？ | 复杂度必须换来更少硬编码耦合 | 只迁出 starter 专属约束到 starter profile，不扩成通用 DSL |
| repair / audit 脚本会不会和 validator 重叠？ | 职责必须分开 | validator 负责判错，manage CLI 里的 repair 负责给顺序，audit 负责给 finding-style 汇总 |

## 6. 当前 tranche 的执行范围

本 tranche 接受：

1. registry 双层化
2. 动作目录上提到 README / SKILL / starter 文档
3. 最小 `register / repair / audit` 工具面
4. profile 化地迁出一部分 starter 专属 validator 约束
5. 新增针对 install / register / repair / audit 的端到端测试

本 tranche 不接受：

1. 全量平台化 generator
2. 完整 stale graph
3. 图数据库或知识图谱执行层
4. 把所有 reference 一次性合同化
