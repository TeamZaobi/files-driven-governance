# GitHub 上传清单

本清单用于把 `files-driven` 作为独立 GitHub 仓库发布。

## 1. 仓库内文件检查

上传前确认以下文件存在：

- `README.md`
- `LICENSE`
- `.gitignore`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `docs/MANUAL.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`

## 2. GitHub 仓库设置

建议补齐：

1. 仓库名称
2. About 描述
3. Topics
4. 默认分支
5. License 识别
6. Social preview
7. Issue 开关
8. Discussions 开关
9. Wiki 开关（通常可关闭）

详细建议见 [`REPO_METADATA.md`](./REPO_METADATA.md)。

## 3. 发布前检查

### 内容检查

- `README` 是否足够让陌生用户理解这个 skill 是什么
- `MANUAL` 是否覆盖设计目标、结构模型、使用方式、维护方式
- `SKILL.md` 是否仍是技能真源，而不是被 README 反向定义
- `references/` 是否与 `SKILL.md` 的链接一致

### 包装检查

- `LICENSE` 是否符合预期
- `.gitignore` 是否排除了系统和编辑器噪音
- GitHub 模板是否存在
- `openai.yaml` 是否与当前对外定位一致

### 结构检查

- 是否没有把工具专属命令写成 canonical rule
- 是否没有把 GitHub 仓库说明写回 skill 真源
- 是否保留多工具可移植性

## 4. 建议的首个发布动作

1. 初始化 Git 仓库并提交
2. 推送到 GitHub
3. 设置 About 与 Topics
4. 检查 License 是否被 GitHub 正确识别
5. 检查 Markdown 渲染
6. 打一个初始 tag，例如 `v0.1.0`

## 5. 建议的首个发布说明

建议首发说明包含：

- 这是一个项目结构治理 skill
- 面向 AI Agent / OpenClaw / AI 驱动 workflow 项目
- 支持现有仓库诊断、绿地搭建、漂移收口
- 默认兼容 Claude Code / Codex / AntiGravity 多工具环境
- 核心能力包括 source family 分析、跨层共享矩阵、角色控制回路与工具可移植性约束

## 6. 不建议上传前做的事

- 为了“看起来完整”而添加大量空模板
- 把工具专属操作说明写进 skill 真源
- 把 GitHub 仓库说明写成比 `SKILL.md` 更权威
- 在没有想清楚 license 的情况下随意更换许可协议
