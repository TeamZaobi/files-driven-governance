# Intent Trigger Contract

Use this reference when a project wants short natural-language commands such as `继续开发`, `开始审计`, `反思`, or `推进` to reliably trigger work across tools.

The goal is not to make chat feel magical.
The goal is to make trigger phrases portable, testable, and operationally stable.

## Core Rule

Expand usability at the trigger layer, not at the semantic layer.

Each accepted utterance should resolve to:

1. one canonical intent id
2. zero or more extracted modifiers or slots
3. one retrieval path
4. one workflow binding
5. one agent-selection rule
6. one output and status-sync contract

Do not multiply hidden workflows just because the same request can be phrased in several ways.
Do not let a tool bootstrap, launcher note, or entry prompt become the only place where trigger semantics are defined.

## Three-Layer Trigger Model

Design trigger handling in three explicit layers:

1. `canonical_intent`: the stable internal action contract
2. `alias_layer`: natural-language phrases that map to that contract
3. `modifier_layer`: optional scope, target, depth, or constraint slots

This keeps operator ergonomics flexible while preserving stable execution semantics.

Example shape:

- canonical intent: `resume_delivery`
- aliases: `继续开发`, `接着做`, `继续这个`
- modifiers: `当前任务`, `登录模块`, `先别改 schema`

## Direct-Action Intents and Route Intents

Separate these two intent types explicitly:

1. `direct_action_intent`: binds directly to a known workflow
2. `route_intent`: inspects state, then chooses the next workflow by policy

Use route intents sparingly.
Typical examples:

- `resume_delivery` is usually a direct-action intent
- `start_audit` is usually a direct-action intent
- `advance_mainline` is usually a route intent

If a phrase like `推进` sometimes means “继续开发” and sometimes means “先审计”, do not hide that ambiguity.
Promote it to a route intent and document its routing policy.

## Minimum Portable Intent Set

Most AI development-and-operations projects can start with this portable set:

1. `recover_context`: rebuild current state before further action
2. `resume_delivery`: continue the active delivery task
3. `start_audit`: review a target change, task, rule, or release candidate
4. `reflect_mechanism`: review why the current path failed, drifted, or stalled
5. `advance_mainline`: route toward the best next mainline action
6. `plan_next_slice`: choose or shape the next bounded work slice
7. `release_or_rollback`: promote a validated result or return to a safe state

Do not start with a very large intent vocabulary.
Prefer a small stable set plus modifiers over many narrowly named commands.

## Required Contract Fields Per Intent

For each supported intent, define at least:

1. `id`
2. `intent_type`
3. `purpose`
4. `aliases`
5. `accepted_patterns`
6. `slots_or_modifiers`
7. `default_values`
8. `required_reads`
9. `preconditions`
10. `workflow_binding`
11. `agent_selection_rule`
12. `expected_outputs`
13. `status_sync_duties`
14. `ambiguity_policy`
15. `stop_or_escalation_rule`
16. `fallback_behavior`

If any of these are missing, the project is likely depending on chat habit rather than on a real trigger contract.

## Recommended Modifier Families

Keep modifier families small and reusable.
These are usually enough:

1. `scope`
   - examples: `当前`, `最近改动`, `主线`, `全部`
2. `target`
   - examples: `这个模块`, `这个 PR`, `登录流程`
3. `depth`
   - examples: `快速`, `标准`, `严格`, `深入`
4. `constraint`
   - examples: `先别改代码`, `不要发版`, `只读`
5. `priority`
   - examples: `先`, `优先`, `先解阻塞`

Do not create a new modifier family for every project-specific nuance.
If a modifier keeps growing special cases, it may actually be an upstream workflow or policy gap.

## Alias Design Rules

1. One alias should resolve to one primary canonical intent.
2. Alias expansion should improve ergonomics, not invent new semantics.
3. Keep alias sets short, high-frequency, and testable.
4. If a phrase is naturally overloaded, either ban it or make it a route intent with explicit routing rules.
5. Tool adapters may expose discovery-friendly phrases, but they must point back to the same canonical intent registry.
6. Do not let different tools assign different hidden defaults to the same phrase.

## Recommended Utterance Pattern

Use a simple composable pattern:

`[priority] [depth] {alias} [scope_or_target] [constraint]`

Examples:

1. `继续开发当前任务`
2. `先快速审一下最近改动`
3. `推进主线，但先别发版`
4. `复盘这次失败，看看是不是 workflow 有问题`

The system should parse the phrase into a canonical intent plus slots, not into a free-form chain of guesses.

## Retrieval and Execution Order

When a trigger phrase is received, prefer this order:

1. parse the utterance against the intent registry
2. load `status_projection`
3. load the active execution object or explicit target
4. load the canonical workflow and relevant boundary or policy anchors
5. resolve the agent and skill bindings
6. execute the selected workflow
7. write outputs, evidence, and status sync

If the intent cannot safely proceed because the target, state, or policy anchor is missing, route to `recover_context` or ask one short clarification question.

## Ambiguity and Stop Rules

Define explicit ambiguity handling:

1. explicit target beats default scope
2. explicit constraint beats convenience defaults
3. direct-action intents must not silently turn into route intents
4. route intents may choose among workflows only when the routing policy is documented
5. if several candidate targets remain and no tie-breaker exists, ask one short clarification question
6. if the required state is missing, fall back to `recover_context`
7. if a requested action conflicts with canonical rules or workflow gates, stop and surface the conflict

Do not let the system “pick something reasonable” when the decision boundary is actually material.

## Minimum Deployment Artifact Package

If a project wants command-driven operation, it should expose at least:

1. `boundary_anchor`
2. `intent_registry`
3. `workflow_registry`
4. `agent_registry`
5. `skill_registry` when reusable procedures exist
6. `status_projection`
7. an active execution object locator
8. a handoff packet contract
9. a tool `adapter_map`

If two or more of these are missing, short trigger phrases will usually degrade into guesswork.

## Minimal Portable Schema Example

```yaml
id: start_audit
intent_type: direct_action
purpose: Review the selected change or work object before promotion.
aliases:
  - "开始审计"
  - "审一下"
  - "过一遍"
accepted_patterns:
  - "{priority?}{depth?}审一下{scope_or_target?}"
slots:
  scope:
    enum: ["当前", "最近改动", "主线", "全部"]
  depth:
    enum: ["快速", "标准", "严格", "深入"]
  target:
    type: string
defaults:
  scope: "最近改动"
  depth: "标准"
required_reads:
  - "status_projection"
  - "active_execution_object"
  - "workflow_registry"
workflow_binding: "audit_mainline"
agent_selection_rule: "quality_gate_owner or assigned auditor"
expected_outputs:
  - "findings_or_pass_result"
  - "evidence_links"
  - "status_sync"
ambiguity_policy: "clarify_if_multiple_targets"
fallback_behavior: "recover_context_if_target_missing"
```

## Readiness Tests

Do not call the trigger contract ready until the project can pass tests like these:

1. saying `继续开发` resumes the correct active task without replaying a long chat
2. saying `开始审计` identifies the audit target, criteria, and expected output
3. saying `反思` routes into mechanism review instead of blindly continuing delivery
4. saying `推进` follows a documented routing policy rather than an undocumented mood
5. the same trigger phrase resolves the same way across supported tools
6. after execution, the result writes back status and evidence in the expected place

## Common Failure Modes

Watch for these failure patterns:

1. one phrase means different things in different tools
2. aliases keep expanding because canonical intents are still underspecified
3. trigger semantics live only in launcher prompts or chat memory
4. the project has no reliable status entry, so every trigger starts with archaeology
5. route intents are used as a license for hidden behavior changes
6. modifiers are compensating for missing upstream workflow or policy definitions
