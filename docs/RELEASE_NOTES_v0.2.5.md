# Files-Driven Governance `v0.2.5`

发布日期：`2026-03-25`

## 本次补丁做了什么

`v0.2.5` 把项目起始阶段的“方向与边界确认”从隐含经验提升成显式前置步骤。

这次补丁解决的问题是：

- 用户故事、使用场景或交付预期只要有一点漂移，后续治理设计和开发范围就会一起外溢
- 对话太快进入工具、架构或目录讨论，但首批交付物还没有钉住
- 用户故事和测试用例写得过粗，导致后续实现时很难判断什么算通过、什么算越界

## 主要变化

1. 更新 [`SKILL.md`](../SKILL.md)
   - 新增 `方向与边界锚点` 前置阶段
   - 要求先用说人话的问题确认使用场景、首批交付物、用户故事、测试用例和非目标
   - 要求用户故事和测试用例写到足够细，能区分通过、失败和越界

2. 新增 [`references/startup-alignment-through-stories-and-tests.md`](../references/startup-alignment-through-stories-and-tests.md)
   - 定义起始对齐包
   - 定义问题设计、细粒度故事/测试规则、漂移信号和纠偏动作

3. 更新 [`references/output-contract.md`](../references/output-contract.md)
   - 新增核心必答区块：
     `方向与边界锚点`
   - 要求该区块先用人话写清楚边界，再进入治理蓝图

4. 更新 [`references/understanding-confidence-and-clarification.md`](../references/understanding-confidence-and-clarification.md) 与 [`references/scenario-playbooks.md`](../references/scenario-playbooks.md)
   - 把首批交付物漂移纳入理解置信度与场景剧本

5. 更新 [`README.md`](../README.md)、[`docs/MANUAL.md`](./MANUAL.md)、[`docs/REPO_METADATA.md`](./REPO_METADATA.md)、[`agents/openai.yaml`](../agents/openai.yaml) 和 [`CHANGELOG.md`](../CHANGELOG.md)
   - 同步新版本定位与默认 prompt

## 为什么这次补丁重要

如果起始阶段只确认“想做什么方向”，却没有把“谁在什么场景下用、第一阶段到底交付什么、什么算通过”写清楚，后续再精细的治理设计也会建立在漂移边界上。

这次补丁的核心是：

1. 先用人话锁边界，再谈结构
2. 先写细用户故事和测试用例，再谈方法组合
3. 一旦发现漂移，先回到边界锚点，而不是继续叠加治理设计

## 推荐发布标题

`v0.2.5 - Startup alignment through stories and tests`
