# governed review workflow

这个文件是 workflow 的解释层。
控制真源仍然是 `workflow.contract.json`；
文件注册事实在 `governance/files.registry.json`，
route 绑定在 `governance/intent.routes.json`。

最小控制链：

1. `BOUNDARY.md` 锁边界
2. `workflow.contract.json` 持有机读控制语义
3. `objects/*.json` 定义状态、动作、证据、批准与输出对象
4. `workflow.state.json` / `workflow.events.jsonl` 记录运行态
5. `status.projection.json` 只做派生摘要

这里的 `WORKFLOW.md` 只解释，不放行。
