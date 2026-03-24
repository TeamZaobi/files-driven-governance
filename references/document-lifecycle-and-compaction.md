# Document Lifecycle And Compaction

Use this reference when a project's docs are growing faster than their governance value.
The goal is not to delete history aggressively.
The goal is to keep active surfaces short, trustworthy, and recoverable while preserving durable facts and useful history.

## Core principle

Treat document growth as a lifecycle problem, not just a naming problem.
When retrieval cost rises, the project should reclassify documents rather than keep every artifact active forever.

## Recommended lifecycle states

Use a small lifecycle vocabulary:

1. `active`
   - currently drives work, decisions, or handoff
2. `stable_reference`
   - still canonical, but no longer the center of active change
3. `projection`
   - derived summary, dashboard, README section, or start-here helper
4. `history`
   - preserved for audit, archaeology, or narrative memory
5. `archive`
   - retained but explicitly outside active recovery paths

Do not let `history` or `archive` pretend to be `active`.

## Growth signals

Trigger lifecycle review when one or more of these appear:

1. a status page keeps absorbing historical narrative
2. a README mixes entrypoint, design history, and active execution notes
3. one discussion object is carrying analysis, tasking, decisions, and retrospective notes together
4. people must reread too much old content to recover current state
5. the same fact is copied into many pages because the original is hard to find
6. stale pages still look current enough to mislead a fresh reader

## Compaction actions

Use these actions deliberately:

1. `split`
   - separate one overloaded artifact into distinct active objects or layers
2. `compact`
   - replace long repeated narrative with a shorter summary plus canonical refs
3. `demote`
   - move a page from active truth into projection or history
4. `archive`
   - keep the artifact but remove it from normal recovery paths
5. `index_only`
   - preserve a locator entry while pushing full details into history

Do not compact canonical facts into vague summaries.
Compact derivative or overloaded surfaces first.

## Active-surface rules

Recommended rules:

1. `status_projection` should stay short, directional, and derivable
2. `display_projection` should never become the only place where durable facts live
3. active `discussion` should stop growing once it has enough material to promote, split, or defer
4. current entrypoints should point to canonical sources rather than re-explain them

If a page cannot stay short without losing meaning, it is probably carrying the wrong lifecycle state.

## History rules

Preserve history, but demote it explicitly.

Recommended rules:

1. keep history discoverable through indexes or links
2. do not force history through the normal recovery path
3. mark historical pages so they cannot be mistaken for current truth
4. prefer references into history over copying history into active pages

## Safe compaction sequence

When a repo is already bloated, prefer this order:

1. identify the current canonical source for each overloaded topic
2. identify which active pages are really projections or history
3. compact status and README surfaces first
4. split overloaded execution objects next
5. archive or demote stale pages after reentry paths are stable
6. update entrypoints so fresh readers land on compact current paths

## What not to do

Avoid these mistakes:

1. deleting upstream facts while trying to simplify the repo
2. archiving before creating a stable reentry path
3. preserving every historical signal as active because it feels safer
4. inventing arbitrary page-length rules with no governance trigger
5. compacting a page without clarifying whether it is truth, execution, projection, or history

## Recommendation pattern for this skill

When the user asks about document bloat, answer these questions explicitly:

1. which artifacts are bloated right now
2. which lifecycle state each bloated artifact should move to
3. which compaction actions should happen first
4. what the trusted reentry path will be after compaction
5. which pages must remain canonical and must not be compacted into summaries
