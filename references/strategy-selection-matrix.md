# Strategy Selection Matrix

Start from `balanced governance`.
Move lighter or stricter only when the project signals justify it.

## Diagnostic Axes

Use these seven axes together:

1. Stage
2. Risk
3. Collaboration density
4. Agent autonomy
5. Recovery pressure
6. Collaboration topology
7. Tool heterogeneity

## Governance Modes

| Mode | When to Choose | Main Methods | Minimum Rules |
| --- | --- | --- | --- |
| `lean-bootstrap` | early stage, low risk, low collaboration density, low autonomy | light Spec-Driven plus simple Kanban | one truth-source path per topic, one task lane, one recovery entrypoint |
| `balanced-governance` | default choice for most AI agent projects | combine Spec-Driven, Kanban, and milestone reviews | typed execution objects, current-version anchors, light sync discipline |
| `controlled-delivery` | high risk, strong coupling, compliance pressure, expensive rollback | stronger Spec-Driven plus review and decision gates | explicit truth-source ownership, versioning, review criteria, controlled promotion |
| `flow-heavy-operations` | many parallel streams, ongoing operational work, continuous visibility needs | Kanban-centered with bounded specs | WIP clarity, status projections, lightweight current-state recovery |
| `recovery-realignment` | facts drift, recovery is broken, projections overreach, repo trust is low | triage first, then balanced or controlled mode | freeze drift, pick canonical facts, repair entry chain, demote stale projections |

## Structural Design Emphasis by Mode

| Mode | Rules | Agents | Workflows | Skills | Execution Objects |
| --- | --- | --- | --- | --- | --- |
| `lean-bootstrap` | keep minimal | keep few and broad | keep simple | only package repeated methods | keep a small active set |
| `balanced-governance` | make explicit | separate role contracts from methods | define key paths and gates | package reusable procedures | type active work clearly |
| `controlled-delivery` | version and review | tighten authority and review surfaces | formalize promotion and rollback | tightly bind to approved contracts | use explicit gates and acceptance |
| `flow-heavy-operations` | keep bounded | optimize handoff roles | favor visible flow transitions | support frequent operational work | emphasize queue clarity and review checks |
| `recovery-realignment` | restate canonical rules | re-clarify authority | repair broken control paths | demote stale packages if needed | stabilize current work first |

## Method Selection Rules

### Prefer Spec-Driven when

- facts are slow variables
- acceptance criteria are important
- multiple downstream artifacts depend on the same boundary
- changes are expensive to undo

### Prefer Kanban when

- work arrives continuously
- multiple contributors or agents move in parallel
- visibility of current state matters more than long narrative documents
- the project needs bounded queues and explicit handoff

### Prefer Agile or Sprint-like cadence when

- the team benefits from time-boxed convergence
- milestone review is more useful than continuous micro-decisions
- integration timing matters across several workstreams

### Add stronger review or decision gates when

- autonomy is high
- review cost is lower than failure cost
- rollback is difficult
- compliance or public trust pressure is real

### Increase role-loop explicitness when

- multiple agents or teams touch the same facts
- tools are mistaken for roles
- workflows are being inferred from habit instead of documents
- no one can state who can approve reclassification or rollback

### Increase sharing-contract explicitness when

- several roles consume the same facts from different layers
- multiple tools expose different entrypoints to the same project
- public or stakeholder pages summarize active work
- review, release, and rollback happen in different systems

## Simplified Decision Guide

Use this quick guide when time is short:

1. If risk is low and the project is early, choose `lean-bootstrap`.
2. If risk is medium and more than one active actor exists, choose `balanced-governance`.
3. If risk or compliance is high, choose `controlled-delivery`.
4. If operational flow is dense, layer `flow-heavy-operations` onto the chosen base mode.
5. If the repo is already drifting, enter `recovery-realignment` before redesigning the long-term structure.

## Recommended Artifact Emphasis by Mode

| Mode | Truth Source | Execution Objects | Status Projection | Display Projection |
| --- | --- | --- | --- | --- |
| `lean-bootstrap` | minimal and stable | simple task or discussion flow | one start-here style entry | optional |
| `balanced-governance` | versioned by topic | discussion, task, review, decision as needed | current state plus recent updates | derived only |
| `controlled-delivery` | explicit, versioned, reviewed | typed and promoted with gates | tightly synced | strictly secondary |
| `flow-heavy-operations` | bounded to slow variables | flow-oriented tasks and review checks | central for visibility | low authority |
| `recovery-realignment` | reselected and clarified first | triage, recovery, decision, handoff | used to re-establish trust | demoted until stable |

## Anti-Patterns

Do not choose a method because it sounds mature.
Do not use Spec-Driven as an excuse to bury active work.
Do not use Kanban as an excuse to avoid stable truth sources.
Do not use sprint rituals if the project lacks a stable integration rhythm.
Do not escalate to heavy gates before restoring basic clarity.
