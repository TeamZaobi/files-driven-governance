# Scenario Playbooks

Use these playbooks after classifying the project start state.

## Existing Repository

### Minimum Inspection

Inspect:

1. primary README or equivalent entrypoint
2. current status or start-here artifacts
3. active task, discussion, or review artifacts
4. any version locator, registry, or canonical-spec path
5. any websites, dashboards, or docs that might overreach as truth sources

### Minimum Deliverable

Deliver:

- a current-state map
- a source-family map
- a four-layer object classification
- a cross-layer sharing map
- the main drift points
- a recommended governance mode
- a recommended flow set
- a role-loop sketch
- a short migration sequence

### Common Failure Modes

- multiple files claim to define the same boundary
- status pages carry facts that upstream sources do not
- README is current only by habit, not by rule
- discussion notes are doing task and decision work at the same time
- no reliable handoff chain exists

### Preferred First Move

Map the current truth sources and demote untrusted projections before changing directory shape.

### Preferred Flow Set

Usually start with:

- `low_token_recovery_chain`
- `discussion -> decision_package -> task_or_decision`
- `truth_source -> execution_object -> status_projection -> display_projection`
- `mechanism_review` when governance objects are touched

Add conditionally:

- `adversarial_inquiry -> defense -> convergence` for high-disagreement or promotion-bound topics
- `proposal -> validation -> shadow/canary -> activation_or_rollback` for governance or public-surface changes

## Greenfield

### Minimum Design

Define only:

1. a small set of truth sources for slow variables
2. a minimum source-family set
3. a small set of execution objects for active work
4. one recovery entrypoint
5. one versioning and sync rule for changes that affect multiple layers

### Minimum Deliverable

Deliver:

- the recommended governance mode
- the minimum viable artifact set
- the minimum viable source-family set
- the first cross-layer sharing contract
- the first entry and recovery chain
- the first role loop
- the first default flow set
- the first review or promotion rule, if any

### Common Failure Modes

- copying a mature project's folder tree without matching its scale
- defining too many object types before active work exists
- mixing strategy, tasks, and status into one document
- adding heavy approval loops before risk justifies them

### Preferred First Move

Define the smallest stable truth-source set and one clear work-and-recovery path.

### Preferred Flow Set

Usually start with:

- `low_token_recovery_chain`
- `discussion -> decision_package -> task_or_decision`
- `truth_source -> execution_object -> status_projection -> display_projection`

Usually defer:

- adversarial convergence on every topic
- rollout ladders for routine low-risk work
- isolated multi-role deliberation unless direct promotion evidence is required

## Recovery or Realignment

### Minimum Triage

Identify:

1. which artifacts still deserve trust
2. which artifacts must be downgraded to projection or history
3. which active work objects need a clean current owner
4. which entrypoints confuse handoff
5. which source families are currently blurred together

### Minimum Deliverable

Deliver:

- the immediate stabilization sequence
- the canonical source reset
- the short-term status recovery chain
- the minimum repaired sharing contract
- the minimum repaired flow set
- the long-term redesign direction

### Common Failure Modes

- continuing to add new files before choosing current canonical facts
- renaming directories before clarifying authority
- trying to preserve every historical signal as active truth
- rebuilding dashboards or websites before upstream sources are repaired

### Preferred First Move

Stop new structural churn, choose the current truth baseline, and restore a usable handoff path before redesign.

### Preferred Flow Set

Start with:

- `low_token_recovery_chain`
- `truth_source -> execution_object -> status_projection -> display_projection`
- `mechanism_review`

Reintroduce later, once truth is trusted:

- `adversarial_inquiry -> defense -> convergence`
- `proposal -> validation -> shadow/canary -> activation_or_rollback`
- `skill_seed -> package_contract -> active_package`
