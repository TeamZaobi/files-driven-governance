# Scenario Playbooks

Use these playbooks after classifying the project start state.

## Existing Repository

### Minimum Inspection

Inspect:

1. the currently intended first deliverable and whether recent conversation already drifted it
2. primary README or equivalent entrypoint
3. current status or start-here artifacts
4. active task, discussion, or review artifacts
5. any version locator, registry, or canonical-spec path
6. any websites, dashboards, or docs that might overreach as truth sources

### Minimum Deliverable

Deliver:

- a current-state map
- a source-family map
- a four-layer object classification
- a cross-layer sharing map
- the main drift points
- the current direction-and-boundary anchor if scope is still moving
- a recommended governance mode
- a recommended flow set
- a role-loop sketch
- a short migration sequence
- a compaction order if active docs are bloated

### Common Failure Modes

- multiple files claim to define the same boundary
- status pages carry facts that upstream sources do not
- README is current only by habit, not by rule
- discussion notes are doing task and decision work at the same time
- no reliable handoff chain exists
- historical material still lives in active status or README pages
- recent clarification rounds quietly expanded the first deliverable

### Preferred First Move

If the requested surface is drifting, freeze a temporary story-and-test anchor first.
Then map the current truth sources and demote untrusted projections before changing directory shape.

### Preferred Flow Set

Usually start with:

- `low_token_recovery_chain`
- `discussion -> decision_package -> task_or_decision`
- `truth_source -> execution_object -> status_projection -> display_projection`
- `mechanism_review` when governance objects are touched

Add conditionally:

- `adversarial_inquiry -> defense -> convergence` for high-disagreement or promotion-bound topics
- `proposal -> validation -> shadow/canary -> activation_or_rollback` for governance or public-surface changes
- `growth_signal -> lifecycle_review -> compact_or_archive` when active docs are sprawling or stale pages still appear current

## Greenfield

### Minimum Design

Define only:

1. a direction-and-boundary anchor packet for the first deliverable
2. a small set of truth sources for slow variables
3. a minimum source-family set
4. a small set of execution objects for active work
5. one recovery entrypoint
6. one versioning and sync rule for changes that affect multiple layers

### Minimum Deliverable

Deliver:

- the direction-and-boundary anchor packet
- the recommended governance mode
- the minimum viable artifact set
- the minimum viable source-family set
- the first cross-layer sharing contract
- the first entry and recovery chain
- the first role loop
- the first default flow set
- the first review or promotion rule, if any
- the first lifecycle and archive rule, if current growth rate justifies it

### Common Failure Modes

- copying a mature project's folder tree without matching its scale
- letting clarification rounds expand the first deliverable without rewriting the boundary
- defining too many object types before active work exists
- mixing strategy, tasks, and status into one document
- adding heavy approval loops before risk justifies them

### Preferred First Move

Lock one to three user stories and a handful of acceptance examples first.
Then define the smallest stable truth-source set and one clear work-and-recovery path.

### Preferred Flow Set

Usually start with:

- `low_token_recovery_chain`
- `discussion -> decision_package -> task_or_decision`
- `truth_source -> execution_object -> status_projection -> display_projection`

Usually defer:

- adversarial convergence on every topic
- rollout ladders for routine low-risk work
- isolated multi-role deliberation unless direct promotion evidence is required
- archive or compaction policy beyond one simple lifecycle rule unless active docs are already growing too fast

## Recovery or Realignment

### Minimum Triage

Identify:

1. which artifacts still deserve trust
2. which artifacts must be downgraded to projection or history
3. which active work objects need a clean current owner
4. which entrypoints confuse handoff
5. which source families are currently blurred together
6. which older story, deliverable, or acceptance anchor was last trustworthy

### Minimum Deliverable

Deliver:

- the recovered direction-and-boundary anchor for the next phase
- the immediate stabilization sequence
- the canonical source reset
- the short-term status recovery chain
- the minimum repaired sharing contract
- the minimum repaired flow set
- the long-term redesign direction
- the first compaction and demotion wave

### Common Failure Modes

- continuing to add new files before choosing current canonical facts
- renaming directories before clarifying authority
- trying to preserve every historical signal as active truth
- rebuilding dashboards or websites before upstream sources are repaired
- preserving every historical page as active just because it might still be useful later
- keeping every adjacent capability in scope because it was mentioned once during clarification

### Preferred First Move

Stop new structural churn, choose the current truth baseline, re-anchor the next deliverable, and restore a usable handoff path before redesign.

### Preferred Flow Set

Start with:

- `low_token_recovery_chain`
- `truth_source -> execution_object -> status_projection -> display_projection`
- `mechanism_review`

Reintroduce later, once truth is trusted:

- `adversarial_inquiry -> defense -> convergence`
- `proposal -> validation -> shadow/canary -> activation_or_rollback`
- `skill_seed -> package_contract -> active_package`

Usually include during triage if bloat is visible:

- `growth_signal -> lifecycle_review -> compact_or_archive`
