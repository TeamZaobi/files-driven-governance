# hooks policy

这个文件是当前 starter 的项目级 hooks 真源。
它回答的是：

1. hooks 在这个项目里负责什么
2. hooks 不负责什么
3. 各工具配置模板应如何消费这些规则

它不是工具配置文件本身。
`.claude/settings.json`、`.codex/hooks.json`、`.github/hooks/*.json` 只属于适配层，
应消费这里和其他 governance 真源，而不是反过来改写这里。

## 1. 作用范围

当前 starter 只推荐把 hooks 用在三类动作：

1. `SessionStart`
2. `PreToolUse`
3. `UserPromptSubmit` 或同类审计入口

如果工具支持更丰富的事件，
`PostToolUse` 和 `Stop` 也可以启用；
但默认先不把它们做成 starter 强制动作。

## 2. 不负责什么

hooks 不负责：

1. 生成 approval
2. 推进 workflow state
3. 改写 `workflow.contract.json`
4. 改写 `rules.contract.json`
5. 代替 `BOUNDARY.md`
6. 给出 release 结论

一句话说：

**hook 可以观测、提醒、阻断，但不持有项目控制权。**

## 3. 默认读序

如果 hook 需要给 agent 注入最小上下文，
默认只提醒这四个入口：

1. `BOUNDARY.md`
2. `governance/hooks.policy.md`
3. `governance/files.registry.json`
4. `governance/intent.routes.json`

## 4. 默认 deny 面

当前 starter 默认只建议 deny 这些高风险 shell 模式：

1. `sudo` / `su` / `runas`
2. `rm -rf /`
3. `mkfs`
4. `dd`
5. `format`
6. `curl ... | bash`
7. `wget ... | sh`

这些 deny 规则默认只当最小 guardrail，
不是完整权限系统。

## 5. rollout 顺序

推荐 rollout：

1. 先启 session-start 提示
2. 再启 prompt / tool metadata logging
3. 最后只对极小 deny list 启用阻断

## 6. 工具适配规则

默认把工具模板放在：

- `tooling/hooks/templates/`

默认把可执行脚本放在：

- `tooling/hooks/scripts/`

当前 starter 的 adapter 规则：

1. 模板文件只负责把工具接到项目规则
2. 脚本只做可测试的最小动作
3. 本地日志默认写到 `tooling/hooks/logs/`
4. 日志目录默认不进 git

## 7. 当前已知边界

截至 `2026-04-14` 的当前已知边界：

1. Claude Code hooks 最完整，适合作为复杂项目的主 hooks 面
2. GitHub Copilot CLI 适合 repo-scoped policy rollout
3. Codex hooks 仍是 experimental，且 `PreToolUse / PostToolUse` 目前只对 `Bash` 有意义

因此：

- 这个 starter 提供跨工具最小脚手架
- 不假装不同工具已经有同一成熟度
- 如果项目要做强控制面，仍应优先靠 workflow / rules / approval 真源
