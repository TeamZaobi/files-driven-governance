# task_or_decision

- `owner`: `project-maintainer`
- `current_object`: `discussion 主路径模板与 example`
- `source_discussion`: [discussion.md](/Users/jixiaokang/.agents/skills/files-driven/examples/discussion-decision-task/discussion.md)
- `source_decision_package`: [decision_package.md](/Users/jixiaokang/.agents/skills/files-driven/examples/discussion-decision-task/decision_package.md)
- `stop_condition`: `主路径资产已落仓，入口已可读，测试已通过`
- `next_response_role`: `reviewer`

## 落点

这一页是最终落点，不再继续扩写前面的讨论。

## 如果落到 task

- 任务名：把已确认方案执行完
- owner：明确的人
- 完成标准：能检查、能验收、能关闭
- 依赖：来自 `decision_package` 的裁定

## 如果落到 decision

- 选中的选项：已经定下
- 为什么选它：在 `decision_package` 里已经说明
- 还接受了什么风险：在这里保持简短、可恢复

## 如果应该 archive

- 当前事实已经稳定
- 后续动作已经由 `task` 或 `decision` 接住
- 这里只保留一句话总结和去向

## Owner Handoff

如果执行对象已经打开，但 discussion 仍保留为边界线程，接手时默认：

1. 先看当前落点
2. 再回看 `decision_package`
3. 最后只在需要时回看 `discussion`

## 这一层的边界

- 不再回写争议细节
- 不再继续扩写证据链
- 不再把收口页改写成新讨论
