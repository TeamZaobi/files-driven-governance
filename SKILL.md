---
name: files-driven
description: 项目结构治理与文档化项目管理设计。用于 AI Agent 项目、AI 驱动 workflow 项目和 OpenClaw 类项目：诊断或设计以文档为载体的治理系统，明确 `policy_or_rules`、`object`、`workflow`、`skill`、`agent`、`execution_object`、`status_projection` 与 `display_projection` 的真源、投影、owner、sync order 与 gate，并设计多人/多 Agent 在不同层级文档间的共享协议与经典流程库。适用于现有仓库诊断、绿地项目搭建、或 rules、agents、workflows、skills、status、README 漂移后的治理收口。基于系统论做结构设计、信息论做信息流、共享链与恢复链设计、控制论做角色回路与变更控制设计。默认先用简单明确的使用场景、用户故事、测试用例和非目标锚定方向与边界，再输出诊断、项目结构治理蓝图和推荐流程库；不默认套用固定目录模板或重审批流；默认支持 Claude Code、Codex、AntiGravity、OpenClaw 等多工具环境，不把任何工具名当成角色真源。
---

# Files Driven

## Overview

Treat documentation as the governance substrate for project structure rather than as passive notes.
Use this skill to design how rules, roles, workflows, skills, objects, and operational records are defined, synchronized, and evolved.

## Core Workflow

### 1. Classify the project start state

Choose one start state before recommending any structure:

- `existing_repo`: the project already has files, conventions, or collaboration artifacts that must be diagnosed.
- `greenfield`: the project is early and needs a minimum viable documentation system.
- `recovery_or_realignment`: the project has drift, duplicated truth sources, broken handoff, or mismatched status signals and needs stabilization first.

If the situation is mixed, pick the state that matches the user's immediate problem.

### 1.5 Lock direction and boundary anchors before governance expansion

Before turning an early conversation into governance design, create a minimum `方向与边界锚点` packet in plain language.
Do this for `greenfield` by default, and also do it for `existing_repo` or `recovery_or_realignment` when the requested product surface, usage scenario, or delivery expectation is still moving.
Write this packet in everyday language that the user can approve quickly.
Do not hide scope inside architecture shorthand, tool jargon, or folder language.

Anchor at least:

1. primary usage scenario and first real users
2. expected first deliverable
3. one to three core user stories
4. three to seven acceptance or test cases, including at least one fail boundary or non-example
5. explicit non-goals or delayed capabilities
6. any reference artifact that calibrates quality without silently redefining scope

Each user story and each test case must be specific enough that another person or agent can tell:

1. what is in scope now
2. what counts as success
3. what is explicitly not required yet

Questioning rule:

- do not stop at one vague clarification question
- for early-stage or drifting projects, ask a compact startup question set, usually four to six short questions, to confirm usage scenario and delivery expectation
- ask those questions in plain language the user can answer without translating product or architecture jargon
- prefer user-story, acceptance, and non-goal questions before tool, folder, or architecture questions

If the user cannot provide the packet directly, draft it and ask for correction.
Do not recommend folder layout, governance family splits, or tool adapters until this packet is stable enough to survive the next clarification round.

Read [startup-alignment-through-stories-and-tests](references/startup-alignment-through-stories-and-tests.md) when:

1. the project is early and the requested outcome is broad
2. several reasonable first deliverables could all sound correct
3. small user-story drift would cascade into large downstream structure changes
4. a recent thread already expanded from one delivery surface into several adjacent ones

### 2. Build a seven-dimensional diagnosis

Diagnose the project across these dimensions:

1. Project stage
2. Change risk
3. Collaboration density
4. Agent or automation autonomy
5. Recovery pressure from drift, ambiguity, or weak handoff
6. Collaboration topology across humans, agents, and systems
7. Tool heterogeneity and portability needs
8. Documentation sprawl and retrieval cost

Read [core-doctrine](references/core-doctrine.md) first when the project is ambiguous or the governance choice feels under-specified.
Read [strategy-selection-matrix](references/strategy-selection-matrix.md) after the diagnosis to choose the governance bundle.

### 2.5 Assess understanding confidence before locking the diagnosis

Before turning partial repo evidence into a governance blueprint, judge how well you understand the project's basics.

Assess confidence on:

1. project boundary and objective
2. main actors, agents, and tool entrypoints
3. current canonical sources and current-version anchors
4. current collaboration shape and risk profile
5. the user's requested usage scenario and first deliverable
6. the user's requested outcome, acceptance boundary, and governance intensity

Use these levels:

- `high`: the main governance choice and first-delivery boundary would likely survive without further clarification
- `medium`: one or two material assumptions remain and may change family mapping, tool adaptation, control loops, or acceptance boundary
- `low`: project boundary, first deliverable, canonical source, major tool entrypoint, or desired outcome is still too unclear

When confidence is `low`, ask targeted user questions before finalizing the blueprint.
When confidence is `medium`, ask one to three focused questions if the answer may materially change the recommendation; otherwise proceed with explicit assumptions.
When the startup boundary is still moving, use the compact alignment question set instead of forcing a premature blueprint.
Do not ask the user to restate facts already discoverable from canonical sources.

Read [understanding-confidence-and-clarification](references/understanding-confidence-and-clarification.md) when the repo is sparse, tool entrypoints may be mistaken for canonical sources, the first deliverable is not pinned, or the requested governance target is underspecified.

### 3. Map project structure families before discussing folders

Classify the project into these governance families:

1. `policy_or_rules`: normative boundaries, rules, policies, or shared constraints
2. `object`: schemas, records, state models, or domain object definitions
3. `workflow`: path, transition, gate, lifecycle, or orchestration logic
4. `skill`: repeatable methods, packaged procedures, helper guidance
5. `agent`: role contracts, authority boundaries, responsibility surfaces
6. `execution_object`: active discussions, tasks, reviews, decisions, handoffs, change artifacts
7. `status_projection`: low-token recovery, navigation, current-state summary
8. `display_projection`: reports, websites, dashboards, public or stakeholder-facing projections

For each family, determine:

1. current canonical source
2. projection or adapter surfaces
3. current owner or direct writer
4. sync order with adjacent artifacts
5. promotion, review, or rollback gate

Only after this map is clear should you recommend any folder layout or file naming changes.

For the five core structural families:

- `policy_or_rules`
- `object`
- `workflow`
- `skill`
- `agent`

also determine:

6. current-version locator
7. official retrieval order
8. tool-specific adapter surfaces

Read [family-locator-contract](references/family-locator-contract.md) and [official-retrieval-orders](references/official-retrieval-orders.md) when the repo has multiple entrypoints, registries, tool bootstraps, or ambiguous “current version” signals.

### 4. Design the cross-layer sharing contract

Read [cross-layer-sharing-contract](references/cross-layer-sharing-contract.md) whenever the project involves multiple people, multiple agents, or multiple tools.
For each important family, define:

1. producers
2. consumers
3. writable surface
4. projection surface
5. visibility scope
6. sync trigger
7. conflict rule
8. handoff packet

If the project uses several tools, treat tool entrypoints as adapters or projections unless there is explicit evidence that they are canonical sources.
Do not let `Claude Code`、`Codex`、`AntiGravity`、`OpenClaw` or any other tool name stand in for a durable project role.
Read [tool-adapter-matrix](references/tool-adapter-matrix.md) when you need to explain how the same family should be surfaced across different tools without duplicating canonical definitions.

### 5. Map four documentation layers across those families

Map the documentation system into four layers:

1. `truth_source`: files that define canonical facts, boundaries, versions, or contracts
2. `execution_object`: files that carry active work, analysis, decisions, reviews, or handoff
3. `status_projection`: files that help low-token recovery and navigation
4. `display_projection`: pages or artifacts meant for presentation, reporting, or external browsing

When relevant, distinguish these process objects inside `execution_object`:

- `discussion`
- `task`
- `review`
- `decision`
- `handoff`

Keep these structural boundaries explicit:

- `Agent` defines role contract
- `Skill` defines repeatable procedure
- `Workflow` defines path, gate, or transition logic
- `Object` defines schema, record type, or state semantics

Apply these naming and design rules:

- define `Agent` by role, authority, and boundary, not by one-off task or tool brand
- define `Skill` by task capability, procedure, or reusable method, not by persona identity
- do not let one `Agent` absorb many unrelated task skills
- do not let one `Skill` pretend to be a durable organizational role

Do not let one of these assets silently redefine another.

### 6. Use the three doctrine lenses on different design problems

Use the three lenses for different outputs instead of blending them into one generic recommendation:

1. System lens: design structure, boundaries, family splits, ownership surfaces, and coupling points
2. Information lens: design truth-source rules, references, version locators, sync order, and recovery chain
3. Control lens: design role loops, promotion logic, review cadence, rollback paths, and change-control intensity

For control design, map at least this loop:

1. `observe`
2. `decide`
3. `act`
4. `review`
5. `rollback_or_improve`

For each important loop, specify which role, agent, or artifact carries each function.

### 7. Choose a governance bundle, not a slogan

Start from `balanced governance` unless the evidence clearly points to a lighter or stricter mode.

Use `Spec-Driven` when the project has high-consequence facts, slow variables, strong coupling, or acceptance criteria that must stay stable.
Use `Kanban` when the project has continuous flow, multiple parallel streams, operational visibility needs, or frequent small transitions.
Use `Agile/Sprint-like` when the project benefits from milestone-based integration, time-boxed convergence, or phase-level review.
Add `decision`, `review`, or `change-control` gates only when risk, compliance, autonomy, or rollback cost justifies them.

Combine methods when needed. Do not force a single methodology to govern every artifact.
Read [tool-portable-team-practices](references/tool-portable-team-practices.md) when the user asks about collaboration setup, planning habits, notes discipline, reusable skills, evidence collection, subagents, or multi-tool team workflows.

### 8. Select the classic governance flow set

Read [classic-governance-flows](references/classic-governance-flows.md) before finalizing the recommendation.
Always decide which flows should become:

1. default project habits
2. conditional escalation paths
3. explicit non-default patterns

Default candidates:

- `low_token_recovery_chain`
- `discussion -> decision_package -> task_or_decision`
- `truth_source -> execution_object -> status_projection -> display_projection`
- `mechanism_review -> repair_or_split`

Conditional candidates:

- `adversarial_inquiry -> defense -> convergence`
- `isolated_multi_role_deliberation`
- `proposal -> validation -> shadow/canary -> activation_or_rollback`
- `skill_seed -> package_contract -> active_package`
- `contract_gap -> closure_topic -> downstream_resume`
- `growth_signal -> lifecycle_review -> compact_or_archive`

Read [adversarial-convergence-loop](references/adversarial-convergence-loop.md) when:

1. disagreement is material
2. a topic may directly promote into `task` or `decision`
3. the project needs institutional opposition or user-value challenge
4. a team is mistaking polite agreement for true convergence

Do not make every project carry every flow.
Recommend only the smallest flow set that matches the diagnosed risk and maturity.

### 9. Produce the governance blueprint

Before answering, read [output-contract](references/output-contract.md) and follow its section order.
Always include the core sections:

- `方向与边界锚点`
- `项目画像`
- `当前主要失真或治理压力`
- `推荐治理模式`
- `推荐经典流程库`
- `项目结构家族图`
- `推荐入口/恢复链`
- `推荐下一步实施顺序`
- `明确不建议的做法`

Add conditional sections only when the diagnosis says they are material:

- `跨层共享矩阵`
- `推荐项目结构分层`
- `推荐角色控制回路`
- `推荐版本与同步纪律`
- `对象家族检索与适配策略`
- `工具可移植性约束`
- `文档生命周期与压缩策略`

Do not emit empty sections just to satisfy a template.
Prefer the smallest response shape that still solves the diagnosed problem.

Explain why the chosen governance strength fits the diagnosis.
Explain why the chosen flow set fits the diagnosis.
Recommend the minimum structure that can stabilize the project and leave room for growth.
Make `policy_or_rules`、`object`、`workflow`、`skill`、`agent`、`execution_object`、`status_projection`、`display_projection` visible in the answer whenever they matter.
When the environment is multi-tool, explain how the same governance model survives across tools without duplicating canonical source definitions.
If understanding confidence remained `medium`, state the material assumptions explicitly.

Use these activation heuristics:

- add `跨层共享矩阵` when more than one human, more than one agent, or more than one tool entrypoint touches the same facts
- add `推荐项目结构分层` when layering confusion is itself a diagnosed problem
- add `推荐角色控制回路` when autonomy, role ambiguity, or review responsibility is material
- add `推荐版本与同步纪律` when there is version ambiguity, drift, multi-writer risk, or promotion complexity
- add `对象家族检索与适配策略` when the five core families are hard to retrieve or tools may overshadow canonical sources
- add `工具可移植性约束` when multiple tools are active or migration risk is non-trivial
- add `文档生命周期与压缩策略` when active docs are bloating, retrieval cost is rising, stale pages are accumulating, or history is pretending to be current truth

### 10. End with sequencing instead of abstract advice

Do not stop at principles. Close with an ordered implementation sequence.

For `existing_repo`, prefer:

1. map current truth sources and projections
2. map current source families and ownership
3. stop active drift
4. consolidate canonical sources
5. refine naming or directory layout last
6. institutionalize only the flows that proved necessary

For `greenfield`, prefer:

1. define slow variables
2. define the minimum source-family set
3. define one status entrypoint
4. define role loops and version or sync rules
5. defer heavier governance until growth or risk justifies it
6. start with a minimum default flow set, not the full escalation library

For `recovery_or_realignment`, prefer:

1. stop the bleeding
2. choose current canonical facts
3. mark obsolete or duplicated projections
4. restore handoff, ownership, and status clarity
5. redesign the long-term structure after stabilization
6. reintroduce escalated flows only after current truth is trusted

## Scenario Routing

### Existing Repository

Inspect the current entry documents, active status files, READMEs, boards, working artifacts, and any registry-like files.
Use [scenario-playbooks](references/scenario-playbooks.md) to diagnose duplicated truth sources, projection overreach, version ambiguity, broken handoff, family-boundary confusion, or process objects that are doing too many jobs.

### Greenfield

Design the smallest viable governance package that can support growth.
Avoid full-scale bureaucracy at the start.
Use [scenario-playbooks](references/scenario-playbooks.md) to define the minimum source-family set, minimum execution objects, one reliable recovery chain, and one workable control loop.

### Recovery or Realignment

Treat the project as a control failure before treating it as an information architecture problem.
Stabilize truth, recovery, and ownership before renaming directories or expanding the process.
Use [scenario-playbooks](references/scenario-playbooks.md) to sequence triage, stabilization, and redesign.

## Guardrails

- Diagnose before prescribing.
- Govern project structure first, folder shape second.
- Prefer source-of-truth clarity over folder proliferation.
- Keep `status_projection` light and derived.
- Make `policy_or_rules`、`object`、`workflow`、`skill`、`agent` boundaries explicit when they are currently blurred.
- Design document sharing explicitly when multiple humans, agents, or tools collaborate on the same facts.
- Do not copy AIJournal or HQMDClaw role names, directory names, or governance rituals verbatim.
- Do not default to heavy change-control when medium governance is enough.
- Do not default to adversarial loops, validation ladders, or rollout stages when the project does not need them.
- Do not default to the full output contract when a smaller, more precise blueprint will solve the user's current problem.
- Do not let `discussion` become a long-lived task bucket.
- Do not let every historical signal remain active forever; demote, compact, or archive when retrieval cost rises.
- Do not let README pages, dashboards, or websites silently redefine canonical facts.
- Do not let `Agent` definitions absorb `Workflow` or `Skill` responsibilities.
- Do not let tool brands become canonical role identities.
- Do not let `OpenClaw` bootstraps, launch surfaces, or runtime entry docs silently become the only readable source for rules, workflows, skills, or agents.
- Do not let skill packages, helper scripts, or workflow drafts patch contract gaps silently.
- Explicitly separate evidence from inference when the repo is incomplete.
- State assumptions when key facts cannot be verified.

## References

- Read [core-doctrine](references/core-doctrine.md) when choosing evaluation lenses or explaining the rationale behind a strategy.
- Read [shared-patterns-from-aijournal-and-hqmdclaw](references/shared-patterns-from-aijournal-and-hqmdclaw.md) when you need reusable patterns without inheriting project-specific structure.
- Read [strategy-selection-matrix](references/strategy-selection-matrix.md) when choosing governance strength or method combinations.
- Read [classic-governance-flows](references/classic-governance-flows.md) when selecting which reusable governance flows should be default, conditional, or explicitly deferred.
- Read [adversarial-convergence-loop](references/adversarial-convergence-loop.md) when the project needs hostile inquiry, structured defense, or question-level convergence semantics.
- Read [family-locator-contract](references/family-locator-contract.md) when the user needs family-specific source locators, current-version anchors, or fallback retrieval rules.
- Read [official-retrieval-orders](references/official-retrieval-orders.md) when the user needs a stable read order for `policy_or_rules`、`object`、`workflow`、`skill`、`agent`.
- Read [tool-adapter-matrix](references/tool-adapter-matrix.md) when the user needs adapter guidance across Claude Code, Codex, AntiGravity, OpenClaw, MCP, CLI wrappers, or other tool entrypoints.
- Read [cross-layer-sharing-contract](references/cross-layer-sharing-contract.md) when the user needs multi-role, multi-agent, or multi-tool collaboration rules.
- Read [understanding-confidence-and-clarification](references/understanding-confidence-and-clarification.md) when the project basics are still ambiguous and you need a confidence-gated clarification strategy.
- Read [document-lifecycle-and-compaction](references/document-lifecycle-and-compaction.md) when active docs are sprawling, stale pages are accumulating, or the user needs a policy for compaction, archiving, or history demotion.
- Read [tool-portable-team-practices](references/tool-portable-team-practices.md) when the user needs portable operational habits, writing rules, or team workflow adjustments across tools.
- Read [output-contract](references/output-contract.md) immediately before drafting the final answer.
- Read [scenario-playbooks](references/scenario-playbooks.md) after classifying the start state.

## Example Requests

- “分析这个多 Agent 仓库的现有文档体系，判断哪些文件是事实源、哪些只是状态页，并给出重构方案。”
- “我要做一个 AI Agent 驱动的 OpenClaw 项目，请为它设计一套适合早期阶段的文档管理策略，要求不过重，但要能支撑后续扩展。”
- “这个项目现在 discussion、任务、状态页和 README 已经互相漂移，请诊断主要问题，并给出收口和迁移顺序。”
- “这个项目的重要机制争议很多，请判断哪些主题必须进入敌意质询、最小决策包或 proposal-validation-activation 链，哪些保持轻量处理。”
