# 方向与边界锚点

这个文件是 starter 的边界入口。
先读它，再读 `governance/files.registry.json`、`governance/intent.routes.json` 和 `workflow.contract.json`。

## 首批真实使用场景 [scenarios]

- 团队第一次要把 `files-driven` 装进一个新项目，需要一个最小可运行起点，而不是从 example 倒推目录和合同。
- AI coding 代理第一次接手这个项目实例，需要知道从哪些文件开始改，哪些文件属于注册事实，哪些文件只是解释或展示。

## 首批交付物 [deliverable]

- 一个带最小 governed pack、项目 `Skill`、文件注册表和 route 合同的 starter 项目实例。

## 用户故事 [user_stories]

### 用户故事 US-1

- 谁在用：第一次安装 `files-driven` 的维护者或 AI coding 代理。
- 在什么场景下：从空目录或新项目起步，希望先得到一个可跑、可改、可验证的最小起点。
- 他/她现在想完成什么：快速判断先改 `BOUNDARY.md`、注册表、route 还是 workflow 合同。
- 为什么这件事对当前阶段重要：如果 starter 只有目录壳子，后续仍然需要自己拼解释文档和 example，冷启动就没有真的被解决。
- 这次完成后，用户应该看到什么变化：不用先翻完整仓库，就能得到一个最小可运行的 files engine 起点。
- 这次明确不包含什么：不要求这一版覆盖完整业务对象或复杂多 skill 拓扑。

### 用户故事 US-2

- 谁在用：负责 workflow、route、validator 或项目规则的人。
- 在什么场景下：需要让关键文件一出生就稳定拥有岗位和证据类型，而不是靠 README 或状态页补口头解释。
- 他/她现在想完成什么：通过 `governance/files.registry.json` 和 `governance/intent.routes.json`，让 route 与写入目标都可被机读消费。
- 为什么这件事对当前阶段重要：如果文件注册表缺位，workflow 和工具入口会重新退化成从 prose 猜状态和猜下一步。
- 这次完成后，用户应该看到什么变化：新增文件和角色变更必须先改注册事实，再刷新运行态和投影。
- 这次明确不包含什么：不要求在 starter 阶段就做自动推理拓扑或全量 stale 图。

## 测试用例 [test_cases]

### 测试用例 TC-1

- 对应故事：US-1
- 前提：新接手的人从 starter 根目录开始。
- 当：先读 `BOUNDARY.md`，再读 `governance/files.registry.json` 和 `workflow.contract.json`。
- 那么：应能说清 starter 服务谁、交付什么、哪些文件是注册事实、哪些是运行态。
- 通过条件：不依赖额外聊天，也能找到第一批要改的文件。
- 这次明确不要求：不要求只靠 `BOUNDARY.md` 理解全部字段语义。
- 失败/越界边界：如果读者仍然分不清这是下游 starter 还是本仓库自身入口，说明脚手架边界不合格。

### 测试用例 TC-2

- 对应故事：US-2
- 前提：starter 已经存在一个最小文件注册表和 route 合同。
- 当：新增或迁移一个关键文件，但没有同步更新注册表或 route 绑定。
- 那么：scaffold validator 应直接失败。
- 通过条件：新增文件、路由漏绑和角色漂移都能被自动发现。
- 这次明确不要求：不要求 validator 自动修复 drift。
- 失败/越界边界：如果新文件没注册、route 没绑定仍然通过，说明这仍然不是一个真正的 files engine 起点。

### 测试用例 TC-3

- 对应故事：US-1
- 前提：starter 已经被 bootstrap 脚本生成到一个新目录。
- 当：先跑 scaffold validator，再跑 pack validator。
- 那么：两者都应通过。
- 通过条件：starter 不是“看起来像模板”，而是真正可跑的最小闭环。
- 这次明确不要求：不要求当前 starter 立刻覆盖复杂审批或多节点流程。
- 失败/越界边界：如果 bootstrap 产物还要靠人工继续补关键文件才能通过校验，说明冷启动闭环没有成立。

## 非目标 [non_goals]

- 不把这份 starter 扩成完整业务模板。
- 不在 starter 阶段引入复杂多 skill 拓扑或完整平台化目录。
- 不让 `README.md` 或 `WORKFLOW.md` 反过来替代注册表和 workflow 合同。

## 质量参考对象 [quality_references]

- 参考标准是“最小但可运行、可注册、可验证的官方 starter”，而不是“尽量多放文件”。

## 验收责任人 [acceptance_owner]

- 负责把 `files-driven` 装进下游项目、并判断这份 starter 是否仍然可用的人。
