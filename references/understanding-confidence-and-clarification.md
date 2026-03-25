# Understanding Confidence And Clarification

Use this reference when the project basics are still partially unclear and the skill needs to decide whether to ask the user targeted questions before locking a governance diagnosis.

The goal is not to ask more questions by habit.
The goal is to ask fewer, higher-leverage questions when ambiguity would materially distort the recommendation.

## What counts as project basics

Judge understanding confidence against these basics:

1. project boundary and current objective
2. main actors, agents, and role surfaces
3. main tool entrypoints and whether they are canonical or adapter-only
4. current canonical sources and current-version anchors
5. the primary usage scenario and first deliverable
6. the current acceptance boundary, non-goals, and desired governance strength

## Confidence levels

### `high`

Use `high` when:

- the project boundary is clear
- the first deliverable and usage scenario are pinned
- the main structural families can be located
- tool entrypoints are not masquerading as canonical sources
- the user's goal is specific enough to choose a governance bundle confidently

### `medium`

Use `medium` when:

- one or two important assumptions remain open
- the recommendation would still be directionally correct, but family boundaries, adapter design, control loops, or acceptance boundaries might shift
- the missing facts are narrow enough to resolve with one to three focused questions

### `low`

Use `low` when:

- you cannot tell whether the project is `existing_repo`, `greenfield`, or `recovery_or_realignment`
- you cannot tell what the first deliverable actually is
- the canonical source or current-version anchor is unclear for key families
- a tool entrypoint such as `OpenClaw`, `Claude Code`, or `Codex` may be hiding the real role or workflow contract
- the user's target output is too vague to select a governance mode safely

## When to ask questions

Ask targeted questions when:

1. the answer may change the selected start state
2. the answer may change which family is canonical
3. the answer may change whether a tool surface is an adapter or a truth source
4. the answer may change the recommended control loop or gate intensity
5. the answer may change the default flow set
6. the answer may change the primary user story, first deliverable, or acceptance boundary

Do not ask questions that can be answered by reading the repo's canonical sources.

## Question design rules

When you need clarification:

1. ask only the smallest number of questions that will materially reduce ambiguity
2. keep each question on one topic
3. tie the question to a governance consequence
4. prefer questions that help separate canonical source from adapter surface
5. prefer questions that clarify current practice over aspirational language
6. when the project is early or scope is drifting, ask a compact startup question set about usage scenario and delivery expectation before architecture questions
7. phrase the question in everyday language the user can answer directly, not in internal architecture shorthand

## Good question shapes

Prefer:

- "第一批真实使用者是谁？他们在什么场景里使用这次交付物？这会决定我先锚定哪个用户故事。"
- "这次第一交付物到底是什么？请给我两个成功例子和一个不属于这次交付的例子。"
- "在这个项目里，`OpenClaw` 是主要执行入口，还是只是一层 adapter/launcher？这会影响我是否把它降级为 tool surface。"
- "你希望我优先诊断现有漂移，还是先给终态治理蓝图？这会改变我选择 `existing_repo` 还是 `recovery_or_realignment`。"
- "当前 `agent` 的真源是在独立角色契约里，还是散落在各工具入口文件中？这会直接影响检索与同步设计。"

Avoid:

- asking the user to restate the whole repo
- asking broad preference questions with no design consequence
- asking for history when current canonical source is already enough
- asking architecture or folder questions before the first deliverable and acceptance boundary are pinned

## Output behavior

If confidence is `high`:

- proceed directly

If confidence is `medium`:

- ask one to three focused questions when the ambiguity is material
- otherwise proceed and mark the assumptions explicitly

If the project is early and the first deliverable is still moving:

- use the startup alignment packet
- ask a compact set of short questions around usage scenario and delivery expectation before freezing the blueprint

If confidence is `low`:

- pause the blueprint
- ask the user targeted clarification questions first
- resume only after the missing basics are resolved or bounded
