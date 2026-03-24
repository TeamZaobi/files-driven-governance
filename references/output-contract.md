# Output Contract

Use this section order in the final answer unless the user asks for a different format.
Do not jump straight to folders or templates before completing the diagnosis.

## Required Sections

### 1. 项目画像

Summarize:

- project type
- current stage
- main objective
- main actors or agents
- autonomy level
- current collaboration shape

### 2. 项目结构家族图

Map the current or proposed structure across:

1. `policy_or_rules`
2. `object`
3. `workflow`
4. `skill`
5. `agent`
6. `execution_object`
7. `status_projection`
8. `display_projection`

For each family, state:

- current or proposed canonical source
- main projection or adapter surfaces
- ownership expectations
- whether stronger gates are needed

### 3. 跨层共享矩阵

For each important family, specify:

- producer
- main consumers
- writable surface
- projection surface
- visibility scope
- sync trigger
- conflict rule

If multiple tools are involved, explain how the same contract survives across them.

### 4. 当前主要失真或治理压力

Identify the dominant pressures, such as:

- duplicated truth sources
- projection overreach
- version ambiguity
- weak handoff
- overloaded notes
- status drift
- recovery cost

### 5. 推荐治理模式

State the chosen governance mode or combination.
Explain why it fits the current diagnosis.

### 6. 推荐项目结构分层

Map the proposed documentation system into:

1. `truth_source`
2. `execution_object`
3. `status_projection`
4. `display_projection`

Also explain how the source families sit across those layers.

### 7. 推荐角色控制回路

Describe the main control loops in this project.
At minimum, cover:

1. who observes
2. who decides
3. who acts
4. who reviews
5. who rolls back or improves

When the project uses agents, specify which documentary responsibility belongs to each agent family rather than only naming roles.

### 8. 推荐入口/恢复链

Specify:

1. what to read first
2. where active work lives
3. how to locate current canonical facts
4. when to read history

### 9. 推荐版本与同步纪律

Specify:

- current-version anchors
- update order
- ownership expectations
- whether `sync_pending` or equivalent markers are needed
- when promotion or review should happen
- where family boundaries require stricter no-overwrite rules

### 10. 工具可移植性约束

When the team uses more than one tool or may migrate tools later, specify:

- which artifacts are tool-agnostic canonical sources
- which files are tool-specific adapters or entrypoints
- which practices depend on a tool capability and which are general rules
- how to avoid duplicating role definitions across tools

### 11. 推荐下一步实施顺序

Provide a short ordered sequence.
Keep it practical.
Prioritize stabilization before refinement when drift is present.

### 12. 明确不建议的做法

Call out the high-probability mistakes for this specific project.
Examples:

- over-engineering too early
- letting status pages define facts
- adding directories before clarifying object roles
- turning discussion notes into permanent task buckets
- letting rules, workflows, skills, and agents silently redefine each other

## Scenario-Specific Additions

### Existing Repository

Also answer:

- which files currently act like duplicate truth sources
- which projections are overreaching
- where version location is ambiguous
- which execution object types are missing or overloaded
- which source families are conflated or missing
- which ownership or gate assumptions are implicit instead of documented
- where cross-layer sharing is currently underspecified
- where tool-specific entrypoints are acting like canonical sources

### Greenfield

Also answer:

- what the minimum viable governance package is
- which artifacts can be deferred
- what not to formalize yet
- which source families should exist from day one and which can remain implicit temporarily
- what the first role loop should be
- what the first cross-layer sharing contract should be

### Recovery or Realignment

Also answer:

- how to stop the bleeding
- what should be frozen or demoted first
- what the migration order is
- what the target steady-state looks like after stabilization
- which family boundaries must be re-established before any cosmetic cleanup
- which tool-specific conventions should be demoted to adapters during recovery

## Reasoning Discipline

Make evidence and inference separable.
Mark assumptions when the repo is incomplete.
Prefer the minimum mechanism that solves the diagnosed problem.
Recommend combinations of methods, not dogmatic single-method answers.
Treat project structure governance as the primary problem and file layout as a downstream consequence.
