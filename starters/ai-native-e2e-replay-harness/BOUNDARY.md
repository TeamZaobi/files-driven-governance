# 方向与边界锚点

这个文件是 starter 的边界入口。
先读它，再读 `governance/scaffold.manifest.json`、`governance/files.registry.json` 和 `governance/intent.routes.json`。

## 首批真实使用场景

- 需要为 AI-Native 项目准备一套可回放、可断言、可留痕的 E2E harness 骨架。
- 需要把 replay 用例、输入 fixture 和执行报告拆成不同目录，避免继续混在业务 starter 的 runtime 结构里。

## 首批交付物

- 一个最小 replay / harness starter。
- 一组明确的 case、fixture、report 目录说明。
- 一份只约束 starter 自身的治理合同。
- 一条能落回 `route / read / write / boundary / projection / recovery / trajectory integrity` 的最小验证面。

## 用户故事

### 用户故事 US-1

- 谁在用：准备搭建 AI-Native E2E 回放框架的维护者或代理。
- 在什么场景下：拿到一个新仓库或新工作区，想先建立 harness 的目录约束。
- 他/她现在想完成什么：快速知道 case、fixture、report 应该分别放什么。
- 为什么这件事重要：如果这三类资产混在一起，回放和报告就会继续退化成手工约定。
- 这次完成后应该看到什么变化：目录职责清楚，后续可以在这些目录上逐步加 schema、validator 和 runner。

### 用户故事 US-2

- 谁在用：负责 replay 断言和报告治理的人。
- 在什么场景下：需要新增一类回放用例，但不想碰业务 starter 的 runtime 目录。
- 他/她现在想完成什么：把用例、fixture、report 分别写到自己的位置。
- 为什么这件事重要：如果 harness 骨架不独立，后续的 replay 资产会继续污染业务真源。
- 这次完成后应该看到什么变化：新资产只能落到 harness 约定的目录，不会反写回原 starter。

## 测试用例

### 测试用例 TC-1

- 前提：新接手的人从 starter 根目录开始。
- 当：先读 `BOUNDARY.md`，再读 `README.md` 和 `governance/*`。
- 那么：应能说清这份 starter 只负责 replay / harness 骨架，不负责业务 runtime。
- 通过条件：目录分工清晰，没有把 case、fixture、report 混成一个通道。

### 测试用例 TC-2

- 前提：准备新增一条 replay case。
- 当：只看 `cases/README.md`。
- 那么：应能知道 case 里放输入、初始状态、断言和回放约束。
- 通过条件：不需要先读完整仓库就能定位到 case 目录。

### 测试用例 TC-3

- 前提：准备产出回放结果。
- 当：只看 `reports/README.md`。
- 那么：应能知道 reports 是执行产物，不是手工维护的真源。
- 通过条件：不会把 report 目录当成新的业务事实源。

## 非目标

- 不把这份 starter 扩成业务模板。
- 不在这里定义完整 replay schema。
- 不在这里平行定义第二套 gate 或 family 体系。
- 不在这里加入执行脚本或自动修复逻辑。
