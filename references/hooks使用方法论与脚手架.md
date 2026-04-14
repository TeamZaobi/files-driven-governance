# Hooks 使用方法论与脚手架

当用户问“hooks 该不该上、挂在哪、怎么和 CLI / governed pack 对齐”时，使用这个 reference。
它不替代项目真源、workflow 合同或项目规则，只负责回答：

1. hooks 适合承接哪类动作
2. hooks 不该承接哪类控制权
3. 项目里最小可复用的 hooks 脚手架应长什么样

这里的判断基于截至 `2026-04-14` 可查到的官方文档和社区实践。

## 1. 先看官方成熟度

### 1.1 Claude Code

- 官方 hooks 能力最完整。
- 支持 `command / http / prompt / agent` 四类 hook handler。
- 事件面覆盖 `SessionStart / UserPromptSubmit / PreToolUse / PostToolUse / Stop / SubagentStop / Notification / FileChanged / MCP` 等。
- 支持在 settings、plugin、skill、subagent frontmatter 中定义 hooks。
- 多个 hook 并行运行；做决策时取“更严格”的结果。

适合：

- 细粒度工具前置拦截
- MCP 写入约束
- repo-local 质量检查
- stop 前复核
- 条件复杂时的 prompt / agent verifier

来源：

- [Anthropic: Hooks reference](https://code.claude.com/docs/en/hooks)
- [Anthropic: Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide)

### 1.2 GitHub Copilot CLI / cloud agent

- 官方支持 repo-scoped `.github/hooks/*.json`。
- `preToolUse` 可显式 allow / deny，`postToolUse` 可做结果处理与审计。
- 官方教程明确建议先定义组织策略、先做 logging-first rollout，再逐步引入 deny。
- 官方文档明确提示：没有内建 secret redaction，日志需自己脱敏。

适合：

- 团队共享的 repo policy
- prompt / tool 审计
- 高风险 shell deny
- 组织级渐进 rollout

来源：

- [GitHub: Hooks configuration](https://docs.github.com/en/copilot/reference/hooks-configuration)
- [GitHub: Using hooks with Copilot CLI for predictable, policy-compliant execution](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/copilot-cli-hooks)

### 1.3 Codex

- 官方 hooks 仍属 experimental。
- 需要 `features.codex_hooks = true`。
- 当前 `PreToolUse / PostToolUse` 只覆盖 `Bash`，不覆盖 `Write / MCP / WebSearch` 等非 shell 调用。
- 多个匹配 hook 会并发启动；部分字段目前 `fail open`。
- 官方文档明确提醒：把它当 guardrail，不要当完整 enforcement boundary。

适合：

- Bash 命令前置 deny
- session start 注入读序
- stop 时继续一轮自检

不适合：

- 依赖全工具覆盖的硬阻断
- 把 release / approval 控制权交给 hook

来源：

- [OpenAI: Codex Hooks](https://developers.openai.com/codex/hooks)
- [OpenAI: Codex Config Reference](https://developers.openai.com/codex/config-reference)

## 2. 从官方结论反推方法论

### 2.1 hook 是执行点，不是真源

默认把 hook 放在：

1. `adapter_surface`
2. `deterministic check`
3. `audit trail`

不要把 hook 放成：

1. 项目控制真源
2. workflow 合同替身
3. approval authority

在 `files-driven` 里，项目级 hook 真源应落在仓库文件里，例如：

- `governance/hooks.policy.md`
- `workflow.contract.json`
- `rules.contract.json`

工具配置文件只消费这些真源：

- `.claude/settings.json`
- `.codex/hooks.json`
- `.github/hooks/*.json`

### 2.2 先按四类 gate 落 hook

hooks 最稳的分工，不是按品牌名，而是按 gate：

1. `route`
   - `SessionStart`
   - `UserPromptSubmit`
   - 用来注入读序、提示当前规则、记录 prompt 元数据
2. `evidence`
   - `PostToolUse`
   - 用来记录证据、脱敏、补摘要、留审计
3. `write`
   - `PreToolUse`
   - 用来拦高风险写入、危险 shell、下载即执行、越权写面
4. `stop`
   - `Stop` / `agentStop` / `SubagentStop`
   - 用来做结束前复核、自检提醒、遗漏项回推

### 2.3 默认优先级

默认优先级建议是：

1. `command hook`
2. `local script`
3. `short timeout`
4. `single-purpose`

只有在以下情况，才升级成 LLM / agent hook：

1. 问题确实需要语义判断，不是正则或固定脚本能解决
2. 错放行成本高
3. latency 和额外 token 成本可接受
4. 已有确定性 hook 守住最基本边界

### 2.4 rollout 顺序

官方和社区的共同结论是：

**先记录，再提醒，再阻断。**

最小 rollout 顺序：

1. `logging-first`
2. `narrow deny`
3. `stop review`
4. `semantic review`

### 2.5 fail-open / fail-closed 规则

要显式区分：

1. 你想要“提醒”
2. 你想要“记录”
3. 你想要“阻断”

推论：

- 如果一个决定必须 fail-closed，优先本地 command hook，不优先远端 HTTP hook。
- 如果一个工具当前只覆盖部分 tool surface，不要把它说成“完整权限边界”。

这里第二条对 Codex 尤其重要。
这是根据其官方文档对 `Bash` 覆盖范围、`fail open` 字段和 shell 拦截不完整性的描述做出的明确推论。

## 3. 社区经验里最值得保留的东西

### 3.1 机械约束通常比长指令稳

社区反复出现的共识是：

- 同一类错如果已经重复出现，继续加长 instruction 往往不如补一个机械 hook
- hook 不和上下文竞争注意力
- 它更像“每次都执行的外置装置”，而不是“希望模型记住的提醒”

参考：

- [merlinmann gist: Claude Code seems to benefit from mechanical hooks](https://gist.github.com/merlinmann/34708a72be7ed2e3aad013a2bbeb7f83)

### 3.2 不要把所有质量动作都放到每次写入后

社区最常见的反模式之一，是把 formatter、lint、build、test 都挂在每次 `Write / Edit` 后面。

更稳的经验是：

- 高风险命令放 `PreToolUse`
- 审计和脱敏放 `PostToolUse`
- 真正的“任务完成了吗”更多放 `Stop`

参考：

- [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips)
- [rosmur/claudecode-best-practices](https://rosmur.github.io/claudecode-best-practices/)

### 3.3 hook 要小、专、可测

社区里最好维护的 hooks，通常都满足：

1. 一个 hook 只做一类事
2. 脚本可以脱离工具单独喂 JSON 测
3. stdout / stderr / exit code 行为固定
4. 先有日志，再有 deny

### 3.4 优先做 repo-local、可审计的 hook

社区成熟方案大多把 hook 资产放进仓库：

- 方便 code review
- 方便团队共识
- 方便回归
- 方便分 repo rollout

参考：

- [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)
- [GitHub tutorial rollout section](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/copilot-cli-hooks)

## 4. files-driven 里的最小落法

推荐最小落法：

1. `governance/hooks.policy.md`
2. `tooling/hooks/README.md`
3. `tooling/hooks/templates/`
4. `tooling/hooks/scripts/`
5. `tooling/hooks/logs/`

角色分工：

- `governance/hooks.policy.md`：说“什么该拦、什么只记录、什么不能交给 hook”
- `tooling/hooks/templates/*`：说“某个工具怎么接上这些规则”
- `tooling/hooks/scripts/*`：说“实际执行逻辑是什么”

## 5. starter 该自带什么

starter 里默认只建议自带三类能力：

1. `SessionStart` 读序提示
2. `PreToolUse` 高风险 shell deny
3. 可选 prompt / tool logging

默认不自带：

1. 每次写文件就自动 format
2. 每次结束都强行跑全量测试
3. 自动改 workflow state
4. 自动生成 approval

## 6. 反模式

避免以下做法：

1. 把 hook 当成 workflow 真源
2. 用工具配置文件偷偷改写项目规则
3. 没做脱敏就记录 prompt / command 全量文本
4. deny 规则很宽，却没有日志和例外处理
5. 在 Codex 当前能力面上假设 hook 已覆盖全部工具
6. 把 hook 做成“全都检查”的巨型脚本
7. 不给 hook 单独测试输入，只靠真人在会话里试

## 7. 一句话结论

在 `files-driven` 里，hooks 最好的位置是：

**把重复、确定、可审计的执行点机械化，但把控制真源、合法转移和审批边界继续留在仓库合同里。**
