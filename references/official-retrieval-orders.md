# Official Retrieval Orders

Use these retrieval orders when the user asks how a project should officially locate the current source for a family.
These are retrieval contracts, not folder-style preferences.

## Global Retrieval Rule

Unless the user asks for raw historical archaeology, use this global order first:

1. low-token entrypoint to identify the current topic
2. family locator to identify the relevant family
3. canonical source for the family
4. bound supporting files actually consumed by the canonical source
5. execution objects for current change context
6. status or display projections last

Do not reverse this order unless the project is in recovery and the canonical source is broken or missing.

## Family Retrieval Orders

### 1. `policy_or_rules`

Official order:

1. current policy anchor or rules index
2. canonical rule document
3. latest approved amendment or decision
4. active proposal only if the rule is known to be changing
5. status summaries
6. tool-specific instruction files last

### 2. `object`

Official order:

1. object registry or object index
2. canonical schema or model definition
3. latest approved object amendment
4. consuming workflow or skill
5. status or display surfaces last

### 3. `workflow`

Official order:

1. workflow registry or workflow index
2. canonical workflow definition
3. latest approved workflow change
4. current execution object affecting the workflow
5. status page or helper scripts last

### 4. `skill`

Official order:

1. skill registry or skill index
2. canonical package root
3. `SKILL.md`
4. consumed `references/`, `assets/`, scripts, or checklists
5. adapter command or tool launcher
6. external examples last

### 5. `agent`

Official order:

1. agent registry or role index
2. canonical role contract
3. role-specific bound contracts
4. runtime mapping
5. tool-specific entrypoint
6. projection summaries last

## Recovery Override

If the repo is drifting badly, use this override:

1. identify the most trustworthy current anchor
2. identify the intended family
3. identify which surfaces are stale or overreaching
4. demote projections and adapters
5. then restore the official retrieval order

## Tool Rule

Official retrieval order should survive tool changes.
That means:

1. a tool may help find the family
2. a tool may help load the source
3. a tool must not redefine the retrieval order itself

Examples:

- a CLI wrapper may open the skill package
- an MCP tool may fetch the registry
- a tool bootstrap may summarize the role contract

But in all cases, the canonical family source still wins.
