# Tool Adapter Matrix

Use this reference when the project needs to map the same family across multiple tool environments.
Treat tools as adapters, launch surfaces, or runtime bindings unless the project intentionally makes them canonical.

## Matrix

| Family | Tool-agnostic canonical source | Common adapter surfaces | Tool layer may do | Tool layer must not do |
| --- | --- | --- | --- | --- |
| `policy_or_rules` | policy docs, rules index, approved amendments | startup docs, bootstrap notes, helper summaries | summarize startup rules, point to current anchors | redefine rules by convenience or omission |
| `object` | schema docs, object registry, canonical models | generated types, validators, rendered field docs | validate, render, or consume schema | invent private fields or shadow schemas |
| `workflow` | workflow docs, lifecycle definitions, workflow registry | helper scripts, boards, state pages, automation configs | execute or route approved paths | invent gates or transitions not present upstream |
| `skill` | skill package root, `SKILL.md`, consumed references | slash commands, CLI wrappers, tool launchers, shims | invoke packaged procedures | redefine role authority or workflow policy |
| `agent` | role contract, agent registry, runtime mapping | top-level entry docs, presets, launch configs | bind roles to tool/runtime environments | let tool brand become role identity |

## Tool categories to think in

Use tool categories rather than product names when designing adapters:

1. top-level instruction files
2. CLI wrappers
3. MCP connectors
4. IDE launch surfaces
5. runtime mapping files
6. dashboards or status projections

This keeps the model portable across `Claude Code`, `Codex`, `AntiGravity`, `OpenClaw`, and future tools.

## Named tool-entry examples

When the project explicitly uses named tools, treat these surfaces as adapters unless the project intentionally promotes them:

- `Claude Code` startup files or launcher notes
- `Codex` task entrypoints or runtime bootstraps
- `AntiGravity` agent manager views or launch configs
- `OpenClaw` workspace bootstraps, launcher docs, project-entry prompts, or runtime adapter maps

These may help discovery, but they must not become the only durable place where canonical rules, workflows, skills, or agents can be found.

## Adapter design rules

1. Every adapter should point back to a canonical family source.
2. Every adapter should declare whether it is:
   - bootstrap
   - launcher
   - projection
   - compatibility shim
3. If an adapter contains extra rules, those rules must either:
   - be copied from canonical source and clearly marked as derivative
   - or be promoted upstream into canonical source
4. No adapter should be the only place where a durable role, workflow, or policy can be discovered.
5. If `OpenClaw` is a primary operator entrypoint, define how each family is surfaced there without letting `OpenClaw`-specific files redefine the canonical family source.

## Readiness questions

When assessing whether tool adaptation is “prepared enough,” ask:

1. Can each family be found without reading a tool-specific entrypoint first?
2. Can the current version of each family be located reliably?
3. Can the project survive migrating from one tool to another without redefining roles, workflows, or skills?
4. Are official adapters clearly demoted below canonical family sources?
5. Is there a documented fallback when a tool-specific surface is stale or missing?
6. If `OpenClaw` is present, can the project still retrieve rules, workflows, skills, and agents without relying on `OpenClaw`-only bootstraps?

If the answer to two or more of these is no, the project's tool-adaptation layer is not mature enough.
