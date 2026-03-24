# Tool-Portable Team Practices

Use this reference when the user asks how a team should work across tools such as Claude Code, Codex, AntiGravity, or other agent-capable environments.
Do not copy one tool's exact commands or UI habits into the project governance model.
Instead, extract portable operating patterns.

## Portable Patterns from Tool Teams

### 1. Parallel work contexts

If the team regularly handles several independent tasks, use separate work contexts in parallel.
This can be worktrees, separate checkouts, isolated workspaces, or independent agent sessions.

Portable principle:

- isolate concurrent work
- reduce context contamination
- keep one analysis context if the team often reads logs or metrics

### 2. Start complex work in planning mode

For complex changes:

1. plan first
2. review the plan
3. implement after ambiguity is reduced
4. re-plan when the work goes sideways

Portable principle:

- planning is not optional overhead
- verification steps may also need planning

### 3. Invest in living docs

After every recurring mistake or correction, update the durable guidance instead of relying on memory.
This may be project docs, notes directories, rules, or skills.

Portable principle:

- corrective knowledge should be written once and reused many times
- measure success by reduced mistake rate, not by document count

### 4. Turn repeated work into reusable packages

If a workflow repeats, package it as:

- a skill
- a command
- a checklist
- a controlled script

Portable principle:

- repeated behavior should move from chat habit into reusable project assets
- package the method, not just the words

### 5. Let agents work from evidence

Bug fixing and troubleshooting should start from concrete evidence:

- CI failures
- logs
- issue threads
- metrics
- reproduction steps

Portable principle:

- reduce context switching
- anchor agents in observable facts

### 6. Use prompts for challenge and review, not only execution

Useful portable prompting patterns:

- ask the agent to challenge a change before merge
- ask it to prove the behavior difference between branches or versions
- ask it to replace a mediocre fix with a cleaner one after learning more

Portable principle:

- agents should review, challenge, and explain, not only implement

### 7. Improve the operating environment

The exact terminal or IDE does not matter.
What matters is making task switching and context visibility cheap.

Portable principle:

- show active branch or workspace
- keep task contexts visually distinguishable
- reduce friction for switching among tasks

### 8. Use secondary agents or delegated workers when supported

If the tool supports subagents or parallel workers, use them for bounded tasks.
If it does not, use separate sessions or work contexts.

Portable principle:

- keep the main reasoning context clean
- offload bounded side tasks
- do not assume every environment supports the same delegation primitive

### 9. Use controlled interfaces for data and analytics

If the team relies on metrics, logs, or analytics, prefer controlled access through:

- CLI tools
- MCP-style connectors
- APIs
- curated skills

Portable principle:

- make data access repeatable and auditable
- do not rely on ad hoc manual dumping

### 10. Use agents for explanation and learning

Agents can also:

- explain why a change was made
- produce learning artifacts
- draw diagrams
- help close understanding gaps

Portable principle:

- learning output is part of project resilience, not just a personal convenience

## Spec + Kanban + Multi-Agent Team Adjustments

When agents participate in a traditional team flow, adjust the system, not just the prompts.

### Recommended responsibility surfaces

- `Spec Owner`
- `Agent Steward`
- `Quality Gate Owner`

These are portable responsibility patterns.
Map them to existing roles rather than copying the labels by force.

### Recommended flow states

A portable minimal flow can look like:

1. `Backlog`
2. `Spec Ready`
3. `Agent Run`
4. `Evidence Pending`
5. `Human Review`
6. `Merge or Release`
7. `Observe or Feedback`

### WIP rule

Set the upper bound by review capacity, not by generation capacity.
If agents can produce faster than humans can validate, quality debt will accumulate.

### Evidence rule

Do not treat “code written” as done.
Prefer “evidence complete” as the gate to review.

### Tool-portability rule

Do not encode project governance around one tool's UI affordances.
A project should survive migration between tools without losing:

- role definitions
- canonical sources
- review gates
- evidence requirements
- handoff packets

## Writing Guidance for Agent Teams

For durable collaboration artifacts:

- reduce ambiguity before handoff
- write specs that can be tested or reviewed against evidence
- separate stable constraints from task-local notes
- prefer concise, operational writing over ornamental prose
- write for reloadability: another person or agent should recover the state quickly

## Anti-Patterns

Avoid these mistakes:

- confusing tool preference with governance principle
- turning one product's command vocabulary into the team's formal process
- keeping critical know-how only in chat habits
- allowing parallel generation without parallel review design
- treating every productivity tip as a universal rule
