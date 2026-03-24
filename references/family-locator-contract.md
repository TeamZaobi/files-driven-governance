# Family Locator Contract

Use this reference when the project needs stable retrieval rules for the five core structural families:

1. `policy_or_rules`
2. `object`
3. `workflow`
4. `skill`
5. `agent`

The goal is to make each family reloadable across tools and across handoffs.

## What to specify for each family

For each family, determine:

1. canonical source root
2. current-version anchor
3. registry, index, or locator surface
4. preferred retrieval path
5. fallback retrieval order
6. adapter or projection surfaces
7. direct-write authority
8. red flags

## Family-by-family contract

### 1. `policy_or_rules`

Canonical source usually looks like:

- constitution or policy docs
- shared-rules directory
- rules registry or rule index

Current-version anchor:

- canonical policy doc
- rules README
- latest approved decision or amendment when the policy is versioned by change objects

Preferred retrieval path:

1. rules index or current-policy anchor
2. canonical rule document
3. latest approved amendment if the rule is under active revision
4. execution objects or projections only for context

Fallback order:

- canonical rule
- rule index
- approved decision
- status summary
- tool bootstrap last

Adapter surfaces:

- top-level tool instruction files
- startup summaries
- helper docs

Red flags:

- tool bootstrap becomes the real rule source
- status page announces a rule not found upstream

### 2. `object`

Canonical source usually looks like:

- object registry
- schema file
- `OBJECTS.*`
- model definition docs

Current-version anchor:

- object registry entry
- canonical schema doc
- latest approved object change if versioned separately

Preferred retrieval path:

1. object registry or object index
2. canonical schema or model definition
3. latest approved change object
4. consuming workflow or skill docs only after the schema is clear

Fallback order:

- object registry
- canonical schema
- approved change object
- consuming workflow
- projections last

Adapter surfaces:

- generated types
- validation helpers
- rendered field references

Red flags:

- workflow defines fields that object docs do not
- skill invents private object schema to get work done

### 3. `workflow`

Canonical source usually looks like:

- workflow registry
- `WORKFLOW.*`
- path and gate docs

Current-version anchor:

- workflow registry entry
- canonical workflow doc
- latest approved workflow amendment

Preferred retrieval path:

1. workflow registry or lifecycle index
2. canonical workflow definition
3. latest approved change object affecting gates or transitions
4. boards, status pages, or scripts only as consumers

Fallback order:

- workflow registry
- canonical workflow
- approved decision or proposal
- board or status entry
- scripts last

Adapter surfaces:

- helper scripts
- automation definitions
- state pages
- task boards

Red flags:

- script becomes the only readable workflow definition
- status page defines a gate that workflow truth source never approved

### 4. `skill`

Canonical source usually looks like:

- skill registry
- `skills/src/<skill-name>/`
- `SKILL.md`
- consumed `references/`

Current-version anchor:

- skill registry entry
- package root
- `SKILL.md` plus actually consumed supporting files

Preferred retrieval path:

1. skill registry or skills index
2. canonical package root
3. `SKILL.md`
4. bound references, assets, checklists, or scripts consumed by the package
5. external examples only as comparison

Fallback order:

- skill registry
- package root
- `SKILL.md`
- consumed supporting files
- external reference last

Adapter surfaces:

- slash commands
- CLI wrappers
- prompt shims
- tool-specific launch surfaces

Red flags:

- external installer or maintainer assumptions become canonical local procedure
- orphan checklist is treated as part of the skill without being bound to the package

### 5. `agent`

Canonical source usually looks like:

- agent registry
- canonical `AGENT.md`
- runtime mapping or adapter map

Current-version anchor:

- agent registry entry
- canonical role contract
- runtime mapping only for tool/runtime binding

Preferred retrieval path:

1. agent registry or role index
2. canonical `AGENT.md`
3. role-specific contracts or boundaries
4. runtime mapping
5. tool-specific entrypoints last

Fallback order:

- agent registry
- canonical role contract
- runtime mapping
- tool entrypoint
- status summary last

Adapter surfaces:

- `AGENTS.md`
- `CLAUDE.md`
- Codex bootstrap files
- AntiGravity entry docs
- launch presets

Red flags:

- tool brand becomes the role identity
- task-specific behavior is written into the agent instead of a skill

## Cross-family rule

When a family is hard to retrieve, do not patch the problem only with a better README.
First ask whether the project is missing:

1. a real canonical source
2. a stable current-version anchor
3. a family index or registry
4. a rule that demotes tool entrypoints to adapters
