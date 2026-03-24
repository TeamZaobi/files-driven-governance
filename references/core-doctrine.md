# Core Doctrine

Use three lenses in sequence: system, information, and control.
Do not turn these lenses into abstract philosophy. Use them to make practical governance choices.

## System Lens

Ask these questions first:

1. What is the project boundary?
2. Which layers are stable, and which layers change quickly?
3. Which roles, agents, tools, or workflows interact with the same facts?
4. Which artifacts define the system, and which artifacts merely describe it?
5. Where is the coupling high enough that a documentation mistake will propagate?

Before discussing folders, map these project structure families when they exist:

1. `policy_or_rules`
2. `object`
3. `workflow`
4. `skill`
5. `agent`
6. `execution_object`
7. `status_projection`
8. `display_projection`

System-level design choices:

- Keep slow variables in stable truth sources.
- Keep fast work in execution objects.
- Keep recovery and navigation separate from canonical definitions.
- Resist making one file serve every role.
- Separate structural families before refining directory layout.
- Make it clear which family defines facts and which family only consumes or projects them.
- Define `agent` as role contract and control-surface carrier.
- Define `skill` as task capability and reusable procedure package.
- Treat “role” and “task skill” as different kinds of structure unless there is strong evidence they must be merged.
- Give `policy_or_rules`、`object`、`workflow`、`skill`、`agent` stable locators and retrieval anchors before trusting tool bootstraps.

## Information Lens

Ask these questions next:

1. Where does each important fact originate?
2. Which files copy, summarize, or project those facts?
3. Where are duplication, lag, and drift already visible?
4. What is the minimum recovery path for a fresh agent or teammate?
5. Which pages are noisy but feel authoritative?

Information-level design choices:

- Prefer one explicit truth source over many implied ones.
- Prefer references over copy-paste.
- Prefer a stable current-version locator over “read everything.”
- Prefer a short recovery chain over full-history replay.
- Make source family relationships legible: which rule points to which workflow, which workflow depends on which objects, which skills consume which references, which status files summarize which upstream facts.
- If confidence about project basics is still low, ask targeted clarification questions before freezing the diagnosis.

## Control Lens

Ask these questions after mapping facts:

1. How does the project observe current state?
2. Who can decide, who can execute, and who can review?
3. What events should trigger promotion, versioning, rollback, or reclassification?
4. How does the project detect a broken state?
5. How does it recover from drift without freezing all work?

Map at least one explicit control loop:

1. `observe`
2. `decide`
3. `act`
4. `review`
5. `rollback_or_improve`

Control-level design choices:

- Use lightweight gates by default.
- Increase formal review only when autonomy, risk, or rollback cost rises.
- Make status projections derivable from upstream objects whenever practical.
- Record ownership and update order when multiple actors can touch the same facts.
- Define documentary responsibility for each role: who owns rules, who owns workflows, who owns execution objects, who owns projections, and who can authorize rollback or reclassification.

## Practical Mapping

Map the three lenses to project structure governance like this:

- System lens chooses boundaries, source families, ownership surfaces, and artifact layering.
- Information lens chooses truth-source rules, references, sync order, version locators, and recovery entrypoints.
- Control lens chooses role loops, promotion rules, review cadence, rollback paths, and exception handling.

If the repo is immature:

- keep the model small
- define one clear entrypoint
- define one current truth-source path per major topic

If the repo is drifting:

- stop creating new structural layers
- identify current canonical facts
- downgrade stale pages to projection or history
- restore role ownership before redesigning taxonomy

If the repo is scaling:

- split artifacts by function
- add ownership and sync discipline
- keep projections light
- make family boundaries explicit so roles and tools do not redefine each other

## Red Flags

Treat these as signals that governance is failing:

- status pages speak more authoritatively than specs or decisions
- README files silently replace canonical source documents
- the same rule is copied into multiple folders
- active work only survives inside chat history
- every new problem is answered by adding another top-level directory
- no one can tell what to read first
- rules, agents, workflows, and skills redefine each other without a stable ownership model
