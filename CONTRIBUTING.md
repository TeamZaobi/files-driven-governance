# Contributing

欢迎改进 `files-driven`。

本仓库的核心原则是：**把技能真源、参考资料、仓库包装文档分开维护**。

## 1. 修改前先判断改动类型

### 改 `SKILL.md`

只有在以下情况才应修改：

- 技能定位改变
- 触发条件改变
- 核心工作流改变
- 输出契约入口改变

### 改 `references/`

以下情况优先改这里：

- 新增稳定方法论
- 新增协作规则
- 新增跨层共享约定
- 新增跨工具实践
- 补充判断矩阵和 playbook

### 改 GitHub 包装文档

包括：

- `README.md`
- `docs/`
- `.github/`
- `SECURITY.md`
- `LICENSE`

这些文件用于仓库读者，不应反向成为 skill 真源。

## 2. 贡献原则

1. 优先保持多工具可移植性。
2. 不要把工具品牌写成 canonical role。
3. 不要把工具专属 UI 动作写成项目治理原则。
4. 优先扩展 `references/`，避免把 `SKILL.md` 变成超长百科。
5. 保持“项目结构治理优先，目录外观其次”。

## 3. 提交前检查

建议在提交前执行：

```bash
python3 /Users/jixiaokang/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

并人工检查：

- `SKILL.md` 与 `references/` 链接是否正确
- `agents/openai.yaml` 是否仍与对外定位一致
- GitHub 文档是否没有反向定义 skill 真源

## 4. Pull Request 建议

PR 说明建议回答：

1. 这次改的是 skill 真源、参考资料，还是仓库包装？
2. 为什么需要这次改动？
3. 是否影响触发条件、输出契约或多工具兼容性？
4. 是否需要同步更新 `README.md` 或 `openai.yaml`？
