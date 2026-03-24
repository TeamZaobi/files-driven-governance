# Adversarial Convergence Loop

Use this reference when a project needs a formal `敌意质询 -> 答辩 -> 收敛` mechanism.
This is a high-signal flow for disputed, risky, or promotion-bound topics.

## When to trigger this loop

Trigger it when one or more of these conditions hold:

1. the topic may directly promote into `task` or `decision`
2. disagreement is material rather than cosmetic
3. the project needs a user-value or institutional-opposition lens
4. prior discussions converged too quickly without real collision
5. the topic changes governance, public claims, runtime behavior, or expensive execution

Do not trigger it for every low-risk note or routine coordination topic.

## Minimum role pattern

The exact titles may vary, but the loop usually needs these functions:

1. `institutional_opposition`
   - asks the hardest value, viability, or legitimacy questions
2. `builder_or_implementer`
   - answers what must be built or changed to satisfy the challenge
3. `auditor_or_assurance`
   - attacks evidence gaps, failure modes, and unsafe assumptions
4. `integrator_or_pm`
   - integrates tradeoffs and judges staged feasibility
5. `closure_authority`
   - signs off convergence, accepted risk, or mandatory reopen

In some teams, `institutional_opposition` and `closure_authority` are different.
Keep that split explicit if it matters.

## Core loop shape

Preferred shape:

`claim -> hostile_questions -> explicit_responses -> status_update -> convergence_or_reopen`

Recommended round order:

1. opposition or end-user advocate sets the challenge bar
2. builder responds to each question and proposes the construction path
3. auditor attacks the response quality and evidence
4. integrator proposes staged closure or reopen
5. final acceptance position confirms whether the answer is actually good enough

Repeat only when unresolved questions remain material.

## Required artifacts

For a formal loop, keep at least:

1. `question_id`
2. `response_ref`
3. `status`
4. `summary`
5. `accepted_risk`
6. `closure_authority`

If the loop is also using isolated multi-role execution, keep:

1. `context_manifest`
2. `context_receipt`
3. structured `issue_ledger`
4. `delta_pack` rule

## Question-state semantics

Use explicit question states.
Recommended minimum set:

1. `resolved`
2. `accepted`
3. `downgraded`
4. `deferred`

Interpretation:

- `resolved`: the challenge was answered satisfactorily
- `accepted`: the tradeoff remains but is consciously accepted
- `downgraded`: the issue is not fully solved, but residual risk is signed off for this round
- `deferred`: the issue is not settled and must reopen or roll forward

`deferred` does not count as convergence.
`downgraded` only counts as current-round closure when a named `closure_authority` explicitly signs the residual risk.

## Convergence criteria

The loop may converge only when:

1. key `question_id` items have explicit states
2. every `deferred` item is routed into a reopen chain
3. every `downgraded` item has accepted-risk wording and a named `closure_authority`
4. the final acceptance position confirms the result is good enough for the current stage

Do not let PM-style summary alone count as convergence.

## Failure modes to detect

Treat these as warning signs or policy violations:

1. the later speaker ignores upstream questions and publishes a new summary
2. the loop has roles but no structured `question_id -> response_ref -> status` chain
3. `downgraded` becomes a vague euphemism for unresolved blockers
4. the final summary claims consensus without naming remaining accepted risks
5. the project says it ran hostile inquiry, but no institutional opposition actually challenged the core claim

## Lightweight mode

You may recommend a lighter version when:

1. the discussion is low risk
2. the output will not directly promote into `task` or `decision`
3. humans are clearly dominating the discussion
4. the goal is stress-testing ideas, not authorizing action

In lightweight mode:

- keep `question_id`
- keep explicit responses
- keep explicit unresolved items
- do not pretend the result is promotion-grade evidence unless the heavier gate is rerun

## Recommendation pattern for this skill

When using this loop in a diagnosis, answer these questions explicitly:

1. which topics require it
2. which roles carry the opposition, builder, auditor, integrator, and closure functions
3. which artifact will carry the question ledger
4. what counts as convergence
5. what should happen to deferred issues
