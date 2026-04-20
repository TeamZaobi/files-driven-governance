# Git 治理审查与建议

状态：`draft reference`

这份 reference 只回答一个问题：

**当项目已经把 Git 当共享底座时，`files-driven` 应该主动审查哪些 Git 管理问题，并给出什么级别的建议。**

它不是 Git 教程，也不替代 CI、保护分支、代码评审平台或权限系统。
它只补 `governance` 体检里，过去长期缺失的一层：
共享存储本身的 `branch / worktree / upstream` 卫生。

## 为什么这层要算治理，而不只是 Git 技巧

在 AI-Native 同构团队里，
多人协作默认先近似成：

`多个执行上下文共享同一 Git 存储`

这里的执行上下文可以是：

- 一个人在两个工作站上同时工作
- 两个人分别使用 `Codex / Claude Code / AntiGravity`
- 一个主 agent 带多个并行 agent

一旦 `branch / worktree / upstream` 管理失稳，
项目问题就会直接表现为：

1. 稳定基线和集成线混写
2. 写权边界不清
3. 审查结论基于过期基线
4. 恢复成本上升

所以这层不该只算“开发者个人习惯”。
它本质上是共享写权和恢复链的一部分。

## 当前 draft 审查面

当前 `manage audit --layer governance` 会开始给出有限的 Git 卫生建议。
重点不是把项目打成“通过 / 不通过”，
而是尽早暴露共享风险。

当前会看：

1. 当前目录是否处于 Git workspace
2. HEAD 是否处于 detached 状态
3. 当前分支是否已经设置 upstream tracking
4. 当前分支相对 upstream 是 `behind` 还是 `diverged`
5. 稳定分支上是否直接积累了未提交改动，并需要 `feature branch / worktree` 隔离

## 当前不会假装检查的东西

下面这些都重要，但当前还不属于这层 draft 审查面的自动覆盖范围：

1. commit message 质量
2. PR 模板、review SLA、保护分支策略
3. CI/CD 配置与发布门槛
4. 仓库权限模型
5. monorepo 子项目发布流程
6. 复杂 `merge / rebase / cherry-pick` 决策

也就是说，
现在的目标不是把 `governance audit` 夸成“完整 Git 平台”，
而是先把最容易让共享基线失真的几类问题提前指出来。

## 结果怎么理解

- `finding`
  - 当前入口、真源、作用域或 authority surface 已经失稳
  - 这属于治理错误，可能直接影响结论有效性
- `warning`
  - Git 共享底座出现趋势性风险
  - 当前先给建议，不直接判失败
- `not_applicable`
  - 当前目录连治理层最小锚点都不够
  - 先不要把 Git 审查假装成已经生效

## 当前典型 warning 长什么样

- `git_workspace`
  - 当前目录根本不在 Git workspace 里，或者本机没有可用的 `git`
  - 这时还不能谈 branch / worktree / upstream 审查
- `git_head`
  - 当前处于 detached HEAD
  - 先回到命名分支，再把这里当共享基线
- `git_tracking`
  - 当前分支没有 upstream，或者已经 `behind / diverged`
  - 先同步共享基线，再依赖项目级审查结论
- `git_branch_strategy`
  - 稳定分支上仍直接积累本地改动
  - 先切到独立 `feature branch` 或 `worktree`

## 最小行动建议

如果当前 warning 已经出现，默认先按这个顺序收口：

1. 先确认当前工作区确实在 Git 管理下
2. 再确认是不是站在命名分支上
3. 再确认当前分支是否已设置 upstream tracking
4. 如果当前是稳定分支，先把活跃改动切到独立 `feature branch / worktree`
5. 如果已经 `behind / diverged`，先同步共享基线，再继续多上下文推进

这份 reference 的目的不是增加 Git 仪式，
而是让项目管理在共享存储层面具备最小的主动审查与建议能力。
