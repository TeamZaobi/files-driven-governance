# multi-tool-process-projection

This is a minimal official example for a derived `process_projection` that comes from an `execution_object`.
It shows the upstream process carriers, the derived process projection, an optional topology supplement, and the status projection that carries the handoff-facing summary.

## 上游过程载体

- `discussion`
- `review`
- `decision`
- `handoff`
- `trace`

These are the inputs that different tools may already keep in their own form.
The example assumes those traces exist upstream and are not replaced by the projection.

## 派生 `process_projection`

- 来源：`execution_object`
- 作用：把“这次实际跑了什么”压成统一语义，方便人和下游 agent 快速接手
- 允许动作：`summarize`、`display`
- 最小字段：`goal`、`actions`、`findings`、`decisions`、`artifacts`、`status`、`next_step`
- 约束：只压缩过程，不定义事实；不发明新的 `allowed_next_steps`；不冒充真源

## 可选 `topology_supplement`

- 节点
- 流转
- 关口
- 并行分支
- 交接点
- 收敛点

这个补充只解释拓扑，不替代过程摘要本身，也不替代控制权。

## 挂到 `status_projection`

- companion file: [`status.projection.json`](./status.projection.json)
- `status_projection` 只承接派生摘要和当前态势，不新增放行权
- 这里的 `summary` 以过程投影为来源，服务接手面，而不是回写上游过程载体

## Non-goals

- 不引入源项目专有命名
- 不把 process projection 升格为新结构家族
- 不把 topology supplement 写成新的决策层
