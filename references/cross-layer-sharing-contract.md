# Cross-Layer Sharing Contract

Use this reference when the project involves more than one human, more than one agent, or more than one tool entrypoint.
The goal is to prevent ambiguity about who shares which facts, at what layer, and under what write authority.

## Core Rule

For every important project structure family, define a sharing contract before scaling collaboration:

1. producer
2. consumer
3. writable surface
4. projection surface
5. visibility scope
6. sync trigger
7. conflict rule
8. handoff packet

## Recommended Sharing Matrix

Apply this matrix to:

- `policy_or_rules`
- `object`
- `workflow`
- `skill`
- `agent`
- `execution_object`
- `status_projection`
- `display_projection`

For each family, answer:

- Who is allowed to define canonical facts?
- Who may propose changes without direct write authority?
- Which files are allowed to summarize or project those facts?
- Which surfaces are read-only projections?
- Which events require synchronization across layers?
- What happens when two roles or tools disagree?

## Minimum Permission Verbs

Use these verbs rather than vague ownership language:

- `read`
- `comment`
- `propose`
- `write`
- `approve`
- `project`
- `archive`

Not every role needs every verb.
In most cases, very few roles should have `write` or `approve` on the same family.

## Visibility Scopes

Make visibility explicit:

- `private`
- `team`
- `project`
- `public`

Visibility scope and write authority are not the same thing.
A page can be public and still be a projection.
A draft can be project-private and still be canonical for a narrow family.

## Sync Triggers

Define the events that require cross-layer updates.
Common triggers include:

- spec or rule change
- workflow transition
- promotion from discussion to task or decision
- review outcome
- release or rollback
- tool or adapter mapping change

If synchronization is deferred, require an explicit pending marker.

## Conflict Rules

Pick one of these patterns explicitly:

1. canonical source wins
2. higher-approval gate wins
3. designated owner wins pending review
4. freeze and escalate before further writes

Do not leave conflict resolution to chat memory or personal habit.

## Handoff Packet

When work crosses people, agents, or tools, require a minimum handoff packet:

1. current objective
2. canonical sources
3. active execution object
4. current status snapshot
5. evidence or logs
6. next decision or next action
7. known constraints or blocked edges

This packet should be small enough to reload quickly and strong enough to avoid full-history replay.

## Team Roles to Consider

When the project follows Spec + Kanban + multi-agent collaboration, these responsibility surfaces are often useful:

- `Spec Owner`: owns specification clarity and acceptance readiness
- `Agent Steward`: owns tool permissions, runtime boundaries, and automation safety
- `Quality Gate Owner`: owns review gates, CI evidence, and release or rollback criteria

These are role patterns, not mandatory titles.
Map them to your actual project roles instead of copying the names blindly.

## Multi-Tool Rule

Treat `Claude Code`、`Codex`、`AntiGravity` and similar tools as execution environments or adapters.
Do not let tool names become canonical role identities unless the project intentionally chooses that model.

Preferred pattern:

- role contract lives in the `agent` family
- method guidance lives in the `skill` family
- tool-specific entrypoints live in projection or adapter surfaces

## Red Flags

These usually mean sharing rules are underspecified:

- several roles edit the same canonical file directly
- a tool-specific entrypoint becomes the de facto source of truth
- public pages start carrying facts that upstream sources never approved
- status summaries contain undocumented decisions
- handoffs require replaying large chat histories to recover context
