# Shared Patterns from AIJournal and HQMDClaw

Use these patterns as reusable governance primitives.
Do not copy project-specific names, folder trees, or rituals unless the target project truly needs them.

## Patterns to Inherit

### 1. Treat documents as formal operational objects

Do not treat documentation as passive explanation.
Assume that some files define facts, some files carry active work, some files support recovery, and some files only display information.

### 2. Separate source families before artifact layers

In mature AI agent projects, first distinguish structural families such as:

- `policy_or_rules`
- `object`
- `workflow`
- `skill`
- `agent`
- `execution_object`

Then distinguish projection families such as:

- `status_projection`
- `display_projection`

Only after this split is stable should you optimize directory shape.

### 3. Separate four artifact layers

Use these layers unless the project is so small that fewer are sufficient:

1. `truth_source`
2. `execution_object`
3. `status_projection`
4. `display_projection`

This separation reduces drift and makes handoff cheaper.

### 4. Keep a fixed entry and recovery chain

A new agent or teammate should know:

1. what to read first
2. how to find the current active work
3. where canonical facts live
4. when deeper history is actually needed

### 5. Type process artifacts instead of dumping everything into notes

Distinguish at least these functions:

- discussion
- task
- review
- decision
- handoff

Each artifact should solve one problem.
Do not let a single note become analysis, execution, review, and historical archive all at once.

### 6. Use current-version anchors

Stable documentation systems make it obvious which document is current.
Use README-like pointers, registry-like indices, or equivalent locators so agents do not reconstruct version truth from memory.

### 7. Prefer unique source plus thin projection

Edit the real source.
Treat mirrors, adapters, summary pages, and websites as projections unless they are explicitly promoted.

### 8. Fix update order and ownership

When multiple people, agents, or tools can touch the same system:

- define a preferred update order
- define who owns direct edits
- surface unsynced states explicitly

The same principle applies to rules, agents, workflows, skills, and objects.
They need stable ownership and an explicit projection model, not just good naming.

### 9. Design role control loops, not only role names

Good governance does not stop at naming roles.
Specify who observes, who decides, who acts, who reviews, and who authorizes rollback or redesign.

### 10. Solve drift before taxonomy beautification

Folder refinement is useful only after:

- current facts are identifiable
- active work has typed objects
- recovery entrypoints are trustworthy
- projections stop pretending to be canonical

## Classic Flows Worth Preserving

These flow shapes recur across both projects and are more transferable than any directory tree.

### 1. Low-token recovery before deep reading

Prefer:

`workflow-state or start-here -> active work object -> canonical source -> history on demand`

### 2. Discussion before promotion

Prefer:

`discussion -> minimal decision package -> task or decision`

This keeps open topics from being smuggled straight into execution.

### 3. Explicit sync order across layers

Prefer:

`truth_source -> execution_object -> status_projection -> display_projection`

This keeps status and display layers derivative.

### 4. Mechanism review after touching governance objects

When `rules`, `agents`, `skills`, or `workflows` are touched, route findings into a repair loop rather than leaving them as informal retro comments.

### 5. Adversarial inquiry for risky or disputed promotion topics

Use an institutional opposition role, explicit `question_id`, explicit responses, and explicit convergence states when polite agreement is likely to hide weak thinking.

### 6. Isolated multi-role deliberation when promotion evidence matters

If one model or one person is simulating multiple formal roles, promotion-grade outputs need isolation evidence such as `context_manifest`, `context_receipt`, and structured issue tracking.

### 7. Proposal, validation, rollout, activation, rollback

For governance or runtime-affecting changes, bounded adoption is usually safer than instant defaulting.

### 8. Skill seed package promotion

Treat reusable procedures as governed packages, not as loose prompts.
Keep `planned` distinct from `active`.

### 9. Split contract-gap closure out of downstream drafts

If a skill, agent, or workflow draft is compensating for an upstream contract gap, extract that gap into its own closure topic instead of silently hardcoding the workaround.

## Development Arc

The reusable evolution pattern is:

1. `HQMDClaw` develops operational primitives under real collaboration pressure
2. `AIJournal` generalizes those primitives into proposal, validation, rollout, and package-governance shells

This means the transferable asset is not the local naming shell, but the operational flow beneath it.

## Patterns to Avoid Copying Literally

Do not inherit these elements by default:

1. project-specific role names
2. project-specific directory names
3. project-specific activation, rollout, or release vocabulary
4. project-specific memo intensity or every-turn logging habits
5. exact symlink or adapter mechanisms
6. exact website, runtime, or environment distinctions

These may be good local solutions, but they are not universal requirements.

## Reusable Generalization

The transferable lesson is:

- govern by object function first
- govern by source family and information flow second
- govern directory shape last

If a target project does not need a complex change loop, keep the pattern but shrink the mechanism.
If a target project does need stronger governance, add formality around the same primitives rather than inventing a completely different model.
