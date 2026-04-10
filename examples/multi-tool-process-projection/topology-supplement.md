# topology_supplement

## 节点

1. `primary-executor`
2. `reviewer`
3. `maintainer`

## 流转

1. `primary-executor` 先产出首轮判断
2. `reviewer` 追加质询
3. `maintainer` 做最终收缩和裁定

## 关口

1. 未经过 review，不进入最终裁定
2. 未经过 maintainer 裁定，不刷新状态入口

## 说明

这份补充只解释拓扑，不替代 [process-projection.md](/Users/jixiaokang/.agents/skills/files-driven/examples/multi-tool-process-projection/process-projection.md) 本身。
