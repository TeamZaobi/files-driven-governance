# reports

这里存放 replay / harness 的执行产物。

## 期望内容

- 断言报告。
- diff。
- 运行元数据。
- 失败摘要和回放结果摘要。

## 当前合同锚点

- `schemas/ai-native-e2e.assertion-report.schema.json`
- 断言分类应至少覆盖 `route / read / write / boundary / projection / recovery / trajectory`

## 命名建议

- `runs/`：单次执行输出。
- `diffs/`：对比结果。
- `summaries/`：失败和回归摘要。

## 不放什么

- 不放 case 定义。
- 不放 fixture 原始材料。
- 不把 report 目录反过来当作 source of truth。
