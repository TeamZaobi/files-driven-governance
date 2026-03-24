# Files-Driven Governance `v0.2.3`

发布日期：`2026-03-24`

## 本次补丁做了什么

`v0.2.3` 的目标不是减少能力，而是让 skill 更擅长“按项目实际情况给出精确方案”。

这次补丁把输出契约从“默认全展开”改成了“核心必答 + 条件展开”：

- 核心必答区块始终保留
- 高级治理区块只在诊断显示它们确实重要时才展开

## 主要变化

1. 更新 [`SKILL.md`](../SKILL.md)
   - 不再要求每次都输出完整治理蓝图
   - 增加高级区块的触发条件

2. 更新 [`references/output-contract.md`](../references/output-contract.md)
   - 将输出拆分为核心必答区块与条件展开区块
   - 为 `跨层共享矩阵`、`角色控制回路`、`版本与同步纪律`、`检索与适配策略`、`工具可移植性约束` 增加 activation hint

3. 更新说明文档与元数据
   - [`README.md`](../README.md)
   - [`docs/MANUAL.md`](./MANUAL.md)
   - [`docs/REPO_METADATA.md`](./REPO_METADATA.md)
   - [`agents/openai.yaml`](../agents/openai.yaml)

## 为什么这次补丁重要

在真实项目里，不同仓库的主要矛盾不同：

- 有的项目只需要最小恢复链和 family 收口
- 有的项目主要问题是 drift 和 version ambiguity
- 有的项目才需要更完整的共享矩阵、控制回路、检索与适配策略

如果每次都默认输出完整治理大图，skill 很容易看起来“懂很多”，但不够精准。
这次补丁让它更接近“按项目态裁剪的治理求解器”。

## 适用场景

这次补丁尤其适合：

- 早期项目，需要轻量但准确的治理建议
- 漂移项目，需要先抓主要矛盾而不是全量重构
- 多工具项目，需要只在确实必要时展开 adapter 和 portability 设计

## 推荐发布标题

`v0.2.3 - Precision-first output shaping`
