# Output Contract

Use this section order in the final answer unless the user asks for a different format.
Do not jump straight to folders or templates before completing the diagnosis.

## Core Required Sections

### 1. 方向与边界锚点

Summarize:

- primary usage scenario
- expected first deliverable
- one to three core user stories
- detailed acceptance or test anchors
- explicit non-goals
- reference artifacts that calibrate quality without silently expanding scope

Write this section in plain language first.
Do not lead with architecture terms, tool brands, or folder plans.
Each user story and each test anchor should be concrete enough to judge pass, fail, in-scope, or out-of-scope.

If this packet is still unstable, say so explicitly and limit downstream governance detail to what would survive that uncertainty.

### 2. 项目画像

Summarize:

- project type
- current stage
- main objective
- main actors or agents
- autonomy level
- current collaboration shape
- current understanding confidence and main unknowns, if any

### 3. 当前主要失真或治理压力

Identify the dominant pressures, such as:

- user-story drift or acceptance-boundary drift
- duplicated truth sources
- projection overreach
- version ambiguity
- weak handoff
- overloaded notes
- status drift
- recovery cost
- documentation sprawl
- retrieval cost from oversized or stale docs

Limit this to the few pressures that actually drive the recommendation.

### 4. 推荐治理模式

State the chosen governance mode or combination.
Explain why it fits the current diagnosis.

### 5. 推荐经典流程库

State which classic governance flows should become:

1. default project habits
2. conditional escalation paths
3. explicitly deferred patterns

At minimum, judge whether the project needs:

- `low_token_recovery_chain`
- `discussion -> decision_package -> task_or_decision`
- `truth_source -> execution_object -> status_projection -> display_projection`
- `mechanism_review`
- `adversarial_inquiry -> defense -> convergence`
- `proposal -> validation -> shadow/canary -> activation_or_rollback`
- `skill_seed -> package_contract -> active_package`
- `contract_gap -> closure_topic -> downstream_resume`
- `growth_signal -> lifecycle_review -> compact_or_archive`

Explain only the flows that materially affect the current project.

### 6. 项目结构家族图

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

### 7. 推荐入口/恢复链

Specify:

1. what to read first
2. where active work lives
3. how to locate current canonical facts
4. when to read history

Keep this sequence short enough to be operational.

### 8. 推荐下一步实施顺序

Provide a short ordered sequence.
Keep it practical.
Prioritize boundary stabilization before refinement when story or acceptance drift is present.

### 9. 明确不建议的做法

Call out the high-probability mistakes for this specific project.
Examples:

- over-engineering too early
- letting adjacent ideas expand the first deliverable before the boundary packet is stable
- letting status pages define facts
- adding directories before clarifying object roles
- turning discussion notes into permanent task buckets
- letting rules, workflows, skills, and agents silently redefine each other

## Conditional Sections

Add these only when they are material to the diagnosis.
Do not emit empty sections.

### A. 跨层共享矩阵

For each important family, specify:

- producer
- main consumers
- writable surface
- projection surface
- visibility scope
- sync trigger
- conflict rule

If multiple tools are involved, explain how the same contract survives across them.

Activation hint:

- add this when more than one human, more than one agent, or more than one tool entrypoint touches the same facts

### B. 推荐项目结构分层

Map the proposed documentation system into:

1. `truth_source`
2. `execution_object`
3. `status_projection`
4. `display_projection`

Also explain how the source families sit across those layers.

Activation hint:

- add this when layering confusion is part of the diagnosed problem

### C. 推荐角色控制回路

Describe the main control loops in this project.
At minimum, cover:

1. who observes
2. who decides
3. who acts
4. who reviews
5. who rolls back or improves

When the project uses agents, specify which documentary responsibility belongs to each agent family rather than only naming roles.

Activation hint:

- add this when autonomy, role ambiguity, or review responsibility is material

### D. 推荐版本与同步纪律

Specify:

- current-version anchors
- update order
- ownership expectations
- whether `sync_pending` or equivalent markers are needed
- when promotion or review should happen
- where family boundaries require stricter no-overwrite rules

Activation hint:

- add this when there is version ambiguity, drift, multi-writer risk, or promotion complexity

### E. 对象家族检索与适配策略

For `policy_or_rules`、`object`、`workflow`、`skill`、`agent`, specify:

- canonical source locator
- current-version anchor
- official retrieval order
- tool-specific adapter surfaces
- which adapter surfaces are allowed to summarize only
- where retrieval readiness is currently weak

Activation hint:

- add this when the five core families are hard to retrieve or tools may overshadow canonical sources

### F. 工具可移植性约束

When the team uses more than one tool or may migrate tools later, specify:

- which artifacts are tool-agnostic canonical sources
- which files are tool-specific adapters or entrypoints
- which practices depend on a tool capability and which are general rules
- how to avoid duplicating role definitions across tools
- how `OpenClaw` surfaces should stay adapter-level unless explicitly promoted

Activation hint:

- add this when multiple tools are active or migration risk is non-trivial

### G. 文档生命周期与压缩策略

Specify only the document-lifecycle rules that materially reduce sprawl:

- which artifacts count as `active`
- which artifacts should become `stable reference`
- which artifacts should be downgraded to `projection`
- which artifacts should be downgraded to `history` or `archive`
- what triggers `split`, `compact`, `archive`, or `index-only retention`
- which pages must stay short enough for low-token recovery

Activation hint:

- add this when active docs are bloating, retrieval cost is rising, stale pages are accumulating, or history is pretending to be current truth

## Scenario-Specific Additions

### Existing Repository

Also answer only the items that materially change the recommendation:

- which files currently act like duplicate truth sources
- which projections are overreaching
- where version location is ambiguous
- which execution object types are missing or overloaded
- which source families are conflated or missing
- which ownership or gate assumptions are implicit instead of documented
- where cross-layer sharing is currently underspecified
- where tool-specific entrypoints are acting like canonical sources
- which classic flows are currently happening only by habit rather than by explicit contract
- where hostile inquiry or validation ladders are missing, overused, or fake
- which families currently cannot be reliably retrieved without tool-specific bootstraps
- where active and historical documents are currently mixed together

### Greenfield

Also answer only the items that materially change the recommendation:

- what the minimum viable governance package is
- which artifacts can be deferred
- what not to formalize yet
- which source families should exist from day one and which can remain implicit temporarily
- what the first role loop should be
- what the first cross-layer sharing contract should be
- what the first default flow set should be
- which escalated flows should stay deferred
- what the first official retrieval order should be for the five core families
- what the first lifecycle and compaction rules should be

### Recovery or Realignment

Also answer only the items that materially change the recommendation:

- how to stop the bleeding
- what should be frozen or demoted first
- what the migration order is
- what the target steady-state looks like after stabilization
- which family boundaries must be re-established before any cosmetic cleanup
- which tool-specific conventions should be demoted to adapters during recovery
- which flows should be frozen during triage and which can be reintroduced later
- which family locators must be rebuilt before the repo is considered stable
- which active documents should be compacted, demoted, or archived first

## Reasoning Discipline

Make evidence and inference separable.
Mark assumptions when the repo is incomplete.
Prefer the minimum mechanism that solves the diagnosed problem.
Recommend combinations of methods, not dogmatic single-method answers.
Treat project structure governance as the primary problem and file layout as a downstream consequence.
If understanding confidence is low on project basics, ask targeted clarification questions before emitting the full blueprint.
Do not inflate a simple diagnosis into a full governance dossier unless the project actually needs it.
Do not keep bloated or stale artifacts active by default when compacted references or archive status would serve the project better.
