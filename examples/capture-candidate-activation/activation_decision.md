# 激活决策

这一页对应 `activation_or_rollback`，但它本身不是正式激活真源。

## 这一页只做什么

- 记录最终是激活，还是回退。
- 把试验结果和回退路径写清楚。
- 作为展示页，让读者看懂结论，但不替代合同、状态和事件。

## 关键字段

- `decision_kind`
- `activation_ref`
- `rollback_ref`
- `decision_rationale`

## 这页不能做什么

- 不能冒充正式激活。
- 不能覆盖 `workflow.contract.json` 的控制语义。
- 不能把 display landing 写成真源。
