# hooks scaffold

这个目录放的是 repo-local hooks 脚手架。

这里先记住两件事：

1. 项目级 hook 真源在 [governance/hooks.policy.md](../../governance/hooks.policy.md)
2. 这里的模板和脚本只是适配层，不是 control truth

## 目录说明

```text
tooling/hooks/
├── README.md
├── scripts/
│   ├── session_start_context.sh
│   ├── pre_tool_guard.sh
│   └── log_prompt.sh
└── templates/
    ├── claude.settings.hooks.json
    ├── codex.hooks.json
    └── copilot-cli-policy.json
```

## 依赖

当前脚本默认按 Unix shell 准备：

- `bash`
- `jq`
- `git`

## 启用方式

### 1. Codex

```bash
mkdir -p .codex
cp tooling/hooks/templates/codex.hooks.json .codex/hooks.json
```

### 2. Claude Code

把模板里的 `hooks` 节点合并进 `.claude/settings.local.json` 或 `.claude/settings.json`。

建议顺序：

1. 先放 `.claude/settings.local.json`
2. 观察一段时间
3. 再决定是否升级成团队共享的 `.claude/settings.json`

### 3. GitHub Copilot CLI

```bash
mkdir -p .github/hooks
cp tooling/hooks/templates/copilot-cli-policy.json .github/hooks/copilot-cli-policy.json
```

GitHub Copilot CLI 会自动发现 `.github/hooks/*.json`。

## 日志

当前脚本默认把本地审计日志写到：

```text
tooling/hooks/logs/audit.jsonl
```

建议把它加入 `.gitignore`：

```bash
echo "tooling/hooks/logs/" >> .gitignore
```

## 测试脚本

### 测 `SessionStart`

```bash
tooling/hooks/scripts/session_start_context.sh
```

### 测 `PreToolUse`

Codex / Claude 风格输入：

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"sudo rm -rf /"}}' \
  | tooling/hooks/scripts/pre_tool_guard.sh
```

Copilot 风格输入：

```bash
echo '{"toolName":"bash","toolArgs":"{\"command\":\"sudo rm -rf /\"}"}' \
  | tooling/hooks/scripts/pre_tool_guard.sh
```

### 测 prompt logging

```bash
echo '{"timestamp":1704614500000,"cwd":"/repo","prompt":"List branches"}' \
  | tooling/hooks/scripts/log_prompt.sh
```

## 维护规则

1. 先改 `governance/hooks.policy.md`
2. 再改模板
3. 最后才改具体脚本
