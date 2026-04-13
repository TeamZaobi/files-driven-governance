# 方向与边界锚点

这个文件是 project-director capability improvement run pack 的边界入口。
先读它，再读 `WORKFLOW.md`、`workflow.contract.json` 和阶段产物。

## 首批真实使用场景 [scenarios]

- 维护者需要把“项目总监能力图谱改善”从自由讨论改成受控 run，而不是继续依赖长对话里的隐式记忆。
- 需要一条脚本控制、`codex cli` 节点执行的官方路径，验证控制权重分配是否真的能提升复杂流程遵循度。
- 负责基线与回归的人，需要一个能直接复跑、回放和校验的 capability-scope 自改造包。

## 首批交付物 [deliverable]

- 一个可直接运行、可直接校验的 self-hosting governed pack，包含边界页、workflow 合同、运行实例、对象合同、阶段产物和 Codex 调用留痕。

## 用户故事 [user_stories]

### 用户故事 US-1

- 谁在用：维护 `files-driven` 能力模型的人。
- 在什么场景下：需要把前面的讨论收口成一条真正受控的能力改善链。
- 他/她现在想完成什么：先看清能力缺口，再由脚本控制整个改善过程，并让 Codex CLI 只做节点内操作。
- 为什么这件事对当前阶段重要：如果控制权还留在模型内部，复杂流程遵循度仍然会持续偏低。
- 这次完成后，用户应该看到什么变化：改善链能够一次跑完，并留下可审计的 runtime artifacts。
- 这次明确不包含什么：不要求这一轮就把所有下游项目一起升级。

### 用户故事 US-2

- 谁在用：负责 benchmark 与回归的人。
- 在什么场景下：需要验证脚本控制方法是否真的比 prompt-only 工作流更稳。
- 他/她现在想完成什么：把 benchmark anchor 放进同一个受控 run 里，形成可复盘的 pilot 结论。
- 为什么这件事对当前阶段重要：没有 benchmark，改善结论很容易退回感受层。
- 这次完成后，用户应该看到什么变化：pilot 结果能清楚指出哪些能力已改善、哪些还需回退或补试。
- 这次明确不包含什么：不要求这里直接修改对话平台或外部业务系统。

### 用户故事 US-3

- 谁在用：负责 capability promotion/rollback 的维护者。
- 在什么场景下：需要决定这轮改善能否进入能力真源，还是应继续试验。
- 他/她现在想完成什么：在受控终点明确 promotion decision、rollback 条件和下一步动作。
- 为什么这件事对当前阶段重要：如果终点没有裁定面，改善会重新滑回开放式讨论。
- 这次完成后，用户应该看到什么变化：终点页能清楚说明 promote / continue pilot / rollback 的结论。
- 这次明确不包含什么：不要求这一轮直接发明新的世界观层或新的结构家族。

## 测试用例 [test_cases]

### 测试用例 TC-1

- 对应故事：US-1
- 前提：使用者只拿到这个 run pack。
- 当：先读 `BOUNDARY.md`，再读 `WORKFLOW.md`、`workflow.contract.json` 和阶段产物。
- 那么：应能按固定顺序看清整条能力改善链。
- 通过条件：入口、合同、实例和阶段产物角色清楚，不互相冒充。
- 这次明确不要求：不要求这里覆盖所有下游项目场景。
- 失败/越界边界：如果阶段产物能反过来替代 `workflow.contract.json` 或 runtime 文件，说明控制权还没有真正外移。

### 测试用例 TC-2

- 对应故事：US-2
- 前提：benchmark anchor 已作为证据输入 run pack。
- 当：检查 `observe_gaps.md`、`pilot_on_benchmarks.md` 和 `promote_or_rollback.md`。
- 那么：应能看到 benchmark 被当成证据，而不是被当成控制真源。
- 通过条件：benchmark 只进入分析、pilot 和裁定，不直接改写 workflow 合同。
- 这次明确不要求：不要求 benchmark 本身在包内完整复现原始会话内容。
- 失败/越界边界：如果 benchmark anchor 被直接当成运行时放行依据，而不是分析证据，说明方法仍在滑形。

### 测试用例 TC-3

- 对应故事：US-1
- 前提：脚本已经调用完 Codex CLI。
- 当：检查 `workflow.state.json`、`workflow.events.jsonl`、`status.projection.json` 和 `codex_runs/`。
- 那么：应能确认 runtime 由 runner 维护，Codex CLI 只留下节点内产物和执行留痕。
- 通过条件：控制文件由脚本写，节点产物由 worker 写，分工稳定。
- 这次明确不要求：不要求节点 worker 具备审批权或状态推进权。
- 失败/越界边界：如果节点 worker 可以直接改 runtime control files，说明控制面还没有从模型手里拿出来。

## 非目标 [non_goals]

- 不让 Codex CLI 直接拥有 workflow state 的写权。
- 不在这一轮引入新的顶层结构家族。
- 不把 benchmark anchor 直接当成 control truth。

## 质量参考对象 [quality_references]

- [project_governance_model](context/project_governance_model.md)
- [tool_adapter_matrix](context/tool_adapter_matrix.md)
- [runtime_promotion](context/runtime_promotion.md)

## 验收责任人 [acceptance_owner]

- `files-driven` capability maintainer

## Benchmark Anchors

- `019d859b-41f3-7752-bc49-ca9282c784ca`
