# MyWay Sidecar Governance Integration

Use this reference when `MyWay` has mounted or is about to mount an external
workflow sidecar such as Superpowers, GSD, gstack, or Archon, and the result may
affect project truth, write ownership, process state, recovery, or audit.

These four sidecars should be understood as the current `Driven` execution
stack:

- Superpowers: execution discipline
- GSD: long-task drive and context isolation
- gstack: virtual-team challenge and blind-spot coverage
- Archon: workflow orchestration

`Files` carries source-of-truth order, write boundaries, state, recovery, and
audit. `Driven` carries the force that pushes agent work through discipline,
context, challenge, and workflow. `files-driven` governs the interface between
the two.

For Codex, this stack is passive by default. Native Codex execution should
handle ordinary coding, reading, answering, one-shot debugging, and small
verification. A `Driven` sidecar is an escalation path, not a default ceremony.

This is not a vendor import path. The sidecar remains an external capability.
`files-driven` owns only the governance attachment: how the sidecar's work is
classified, written, registered, checked, or rejected inside the governed
project.

## Authority Split

| Layer | Owns | Must not own |
| --- | --- | --- |
| `MyWay` | Prelude, intent compression, sidecar selection, low-noise Postlude | Project truth, write authority, governance acceptance |
| `skills-master` | Install, link, adapter, upstream pin, host discovery, packaging | Project process truth or acceptance gates |
| `files-driven` | Source-of-truth order, write boundary, control strength, pack/runtime/governance audit, recovery | Upstream sidecar implementation |
| Sidecar | Its own discipline, planning, review, or workflow runtime | Final project truth unless registered by the project |

If these layers conflict, prefer this sequence:

1. `skills-master` proves the sidecar is installed and discoverable.
2. `MyWay` decides whether the current turn should route to it.
3. `files-driven` decides whether its output can enter the project truth chain.
4. The project itself remains the owner of domain facts and final artifacts.

## Trigger Rule

Stay in `MyWay` only when the sidecar is a local execution aid.

Switch to `files-driven` as soon as the sidecar touches one of these:

- a project rule, registry, boundary file, workflow, status page, or release
  projection
- a decision that should become durable project fact
- a planning state that another session or teammate must resume
- a destructive, shared, or regulated action
- a workflow output that needs replay, audit, rollback, or acceptance gates

Do not switch merely because a sidecar exists or was installed. Installing a
sidecar is capability inventory; using it is a separate decision.

## Sidecar Intake

| Sidecar | Treat as | `files-driven` intake rule |
| --- | --- | --- |
| Superpowers | Execution discipline | Use its outputs as evidence of disciplined work, not as project truth. Tests, receipts, review notes, and finish-branch checks still need project-level acceptance. |
| GSD | Long-context planning and execution state | Treat `.planning` or equivalent state as runtime/planning state. Register or summarize it into the project truth chain only when it must be resumed or shared. |
| gstack | Role review and decision challenge | Treat role opinions as discussion or decision inputs. A role verdict does not become accepted project direction until it is written into the right decision package or truth source. |
| Archon | Workflow runtime | Treat `.archon/workflows` and CLI runs as executable workflow surfaces. For governed projects, map them to `BOUNDARY.md`, `workflow.contract.json`, state/events, or the project's own control plane before calling them authoritative. |

## Control Strength

Do not equate "sidecar used" with "stronger governance applied".

Also do not equate "governance concern" with "sidecar required".

- `L0-L1`: main thread or subagent execution can use Superpowers or gstack as a
  method aid only when explicitly useful; normal Codex execution remains enough
  for most tasks.
- `L2`: host-native workflow or approvals can call a sidecar, but the project
  still needs a clear acceptance surface.
- `L3`: CLI-backed sidecar execution needs command receipts and artifact refs if
  it changes shared project state.
- `L4`: runner-level orchestration needs explicit state, events, recovery, and
  rollback paths; Archon can be a runtime, but it does not replace the governed
  pack unless the project adopts it as the control truth.

## Minimum Governance Attachment

When a sidecar output needs to enter a project, first write down five things:

1. `scope`: `runtime_scope`, `project_scope`, or `capability_scope`
2. `action`: `install`, `register`, `repair`, `audit`, or a project-specific
   task
3. `truth_source`: the file or object that will own the accepted fact
4. `write_allowlist`: which paths this sidecar-assisted action may change
5. `evidence`: test output, workflow receipt, review artifact, state event, or
   rollback note

If those five cannot be named, keep the sidecar result as a runtime note or
discussion input instead of promoting it.

## Non-Goals

- Do not copy upstream sidecar methodology into `files-driven`.
- Do not make all sidecars activate by default.
- Do not use the four-sidecar model as a mandatory Codex operating ritual.
- Do not let Archon, GSD, or any workflow engine silently become the project
  truth source.
- Do not turn every sidecar run into a governed pack.
- Do not treat installer success or host discovery as project acceptance.

## Practical Closeout

For sidecar-assisted work, a good closeout separates:

- `installed/discovered`: proved by `skills-master`
- `routed`: decided by `MyWay`
- `executed`: proved by the sidecar or host runtime
- `accepted`: owned by `files-driven` and the project truth source
- `rediscovered`: proved by a fresh host session when discovery caching matters
