# Classic Governance Flows

Use this reference when the project needs more than a static structure recommendation.
The goal is to select a reusable flow set, not to force every project to carry every governance ritual.

## How to use this file

For each candidate flow, decide whether it should be:

1. a default project habit
2. a conditional escalation path
3. explicitly deferred

Prefer the minimum set that solves the diagnosed problem.

## Default Flows Worth Preserving

These are the flows most consistently reused across AIJournal and HQMDClaw, and they usually deserve a first-pass recommendation.

### 1. Low-token recovery chain

Core shape:

`status entry -> active object -> canonical source -> history on demand`

Use when:

- the project has recurring handoff
- multiple agents or teammates may enter midstream
- status pages currently over-explain or under-direct

Minimum expectations:

- one reliable recovery entrypoint
- one active-work locator
- one canonical-source locator
- an explicit rule for when history should be read

### 2. Discussion to decision package to task or decision

Core shape:

`discussion -> minimal decision package -> task_or_decision`

Use when:

- a topic is still open
- the team needs structured comparison before execution
- the project wants to prevent chat from acting like a hidden decision system

Minimum expectations:

- typed discussion object
- synthesis of agreement, disagreement, and open issues
- promotion criteria for `task`, `decision`, or continued discussion

### 3. Fixed sync order across layers

Core shape:

`truth_source -> execution_object -> status_projection -> display_projection`

Use when:

- the same facts are consumed across multiple layers
- drift is already visible
- the repo is edited by multiple people, agents, or tools

Minimum expectations:

- one direct writer per object per round
- explicit `sync_pending` or equivalent marker when a round is incomplete
- status and display layers prohibited from inventing facts

### 4. Mechanism review to repair or split

Core shape:

`execution or review -> mechanism_review -> direct_fix_or_split_followup`

Use when:

- tasks touch `rules`, `agents`, `skills`, or `workflows`
- a failure reveals a governance defect rather than only a local bug
- the team wants retro to change the system, not just narrate the problem

Minimum expectations:

- a typed review of agent, skill, and workflow boundaries
- a clear owner for follow-up
- an explicit choice between direct fix, split card, or defer

## Conditional Escalation Flows

These flows are important, but should not be turned on by default for every project or every topic.

### 5. Adversarial inquiry to defense to convergence

Core shape:

`claim -> hostile_questions -> defense -> convergence_or_reopen`

Use when:

- disagreement is material
- user-value challenge is needed
- the output may directly promote into `task` or `decision`
- the team repeatedly reaches shallow consensus too quickly

Read [adversarial-convergence-loop](./adversarial-convergence-loop.md) for the detailed contract.

### 6. Isolated multi-role deliberation

Core shape:

`isolated_role_start -> clean_context -> structured_issue_ledger -> auditable_promotion`

Use when:

- one model or one person is simulating multiple formal roles
- the resulting discussion may be used as a promotion basis
- the project needs evidence that roles were not mixed by convenience

Minimum expectations:

- `context_manifest`
- `context_receipt`
- structured `issue_ledger`
- rule for `delta_pack` and pseudo-isolation detection

### 7. Proposal to validation to rollout to activation or rollback

Core shape:

`proposal -> validation -> shadow/canary -> activation_or_rollback`

Use when:

- the change affects governance, policy, workflow, public claims, or runtime behavior
- the project needs bounded adoption instead of instant defaulting
- rollback cost is non-trivial

Minimum expectations:

- a typed proposal object
- an explicit validation object
- rollout stage boundaries
- closeout or rollback target named at stage entry

### 8. Skill seed to package contract to active package

Core shape:

`seed_topic -> package_contract -> validation -> active_package`

Use when:

- the team wants reusable procedure packages
- a skill may become a stable part of the project's way of working
- the repo uses multiple tools and needs a portable procedure layer

Minimum expectations:

- explicit package root
- `SKILL.md` plus consumed references
- clear distinction between `planned` and `active`
- boundary against silently redefining workflows or policies

### 9. Contract gap split and closure

Core shape:

`downstream_design_hits_gap -> split_closure_topic -> repair_contract -> resume_downstream`

Use when:

- a skill, agent, or workflow draft is compensating for a missing upstream contract
- the team is about to smuggle schema or gate logic into the wrong layer
- repeated design arguments point to the same upstream hole

Minimum expectations:

- the gap becomes its own typed topic
- the upstream family to repair is named explicitly
- downstream work is blocked, narrowed, or rerouted until the gap is closed

### 10. Growth signal to lifecycle review to compact or archive

Core shape:

`growth_signal -> lifecycle_review -> compact_or_archive -> trusted_reentry`

Use when:

- active docs are getting longer without adding decision quality
- status or README pages start accumulating historical narrative
- multiple stale pages still look current
- recovery cost is rising because people must reread too much history

Minimum expectations:

- explicit lifecycle states such as `active`, `stable`, `projection`, `history`
- a named rule for when an artifact must be split, compacted, or archived
- a trusted reentry path after compaction
- an explicit rule against deleting canonical facts while compacting derivative surfaces

## Practical Selection Guide

### Small or early project

Usually start with:

- low-token recovery chain
- discussion to decision package to task or decision
- fixed sync order

Usually defer:

- rollout ladders
- adversarial loops on every topic
- isolated multi-role deliberation unless direct promotion risk exists
- lifecycle compaction policy until active docs actually begin to sprawl

### Existing repo with drift

Usually start with:

- low-token recovery chain
- fixed sync order
- mechanism review
- discussion to decision package to task or decision

Add conditionally:

- adversarial convergence on disputed or high-risk topics
- proposal/validation/activation on governance changes
- lifecycle review and compaction when active docs or status pages start bloating

### Governance-heavy or multi-agent project

Usually include:

- all default flows
- adversarial convergence for key disputes
- isolated multi-role deliberation for direct promotion topics
- proposal/validation/activation for governance or runtime changes
- skill package promotion where reusable procedures are becoming durable assets

## What not to inherit literally

Do not hardcode:

1. project-specific role names
2. project-specific object prefixes
3. project-specific rollout vocabulary
4. project-specific memo intensity
5. tool-specific workarounds as if they were universal governance law
6. arbitrary length limits without a lifecycle rationale

The transferable asset is the flow shape and trigger logic, not the local naming shell.
