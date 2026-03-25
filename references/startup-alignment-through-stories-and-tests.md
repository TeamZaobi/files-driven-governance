# Startup Alignment Through Stories And Tests

Use this reference when the project is early, the requested outcome is broad, or small requirement drift could create large downstream overflow.

The goal is not to write a full specification first.
The goal is to freeze a small, readable alignment packet before governance, architecture, or folder design expands the solution surface.

## When to activate

Activate this reference when:

1. the project is `greenfield`
2. the requested deliverable is still described in broad nouns or platform terms
3. the conversation keeps introducing adjacent capabilities
4. multiple reasonable first deliverables could all sound compatible
5. a small change in user story would materially change the future repo, workflow, or tooling design

## What to anchor first

Create a `方向与边界锚点` packet that includes:

1. the primary usage scenario
2. the expected first deliverable
3. one to three core user stories
4. three to seven acceptance or test cases, including at least one out-of-scope or fail case
5. explicit non-goals
6. any reference example or precedent artifact that influences quality expectations

Keep it short.
Write it in plain language a real user can validate quickly.
Do not let architecture jargon stand in for scope.
If the user does not provide it, draft it and ask for correction.

## Questioning strategy

Do not stop at one vague clarification question.
For startup alignment, ask a compact question set that covers usage scenario and delivery expectation, usually four to six short questions.

Preferred question topics:

1. who uses it and in what real scenario
2. what the first deliverable actually is
3. what counts as success and what related result does not count as this delivery
4. which inputs or materials must be supported first
5. which capabilities are explicitly delayed or out of scope
6. whether a reference example is only for quality calibration or is part of the scope itself

Keep questions concrete and outcome-bound.
Say things the user would naturally say back, not internal design shorthand.

## Good question shapes

Prefer questions like:

- "第一批真实使用者是谁？他们在什么场景里打开这个系统？"
- "这次你要的第一交付物是什么？是知识台、知识图谱、讲座蓝图，还是别的其中之一？"
- "请给我两个成功例子和一个虽然相关但这次不交付的例子。"
- "哪些输入格式是首批必须支持的？哪些可以延后？"
- "有没有需要学习的参考作品？它是质量基线，还是范围本身的一部分？"

## Acceptance anchor shapes

Prefer acceptance examples over abstract adjectives.
Each acceptance example should show:

- input or trigger
- expected output or behavior
- what is explicitly not required

Example pattern:

- "给 1 份 PPTX 和 1 份 PDF，系统生成讲座蓝图草稿，并保留可追溯来源；不要求自动生成最终讲稿。"

## Story and test detail rule

Each user story should make these parts explicit:

1. who the user is
2. in what situation they use the deliverable
3. what they are trying to get
4. why it matters for this phase
5. what adjacent expectation is not included yet

Each test case should make these parts explicit:

1. precondition or input
2. action or trigger
3. expected output or observable behavior
4. pass condition
5. fail boundary or not-required outcome

If a story or test case cannot distinguish success from adjacency, it is still too vague.

## Drift signals

Treat these as drift signals:

- the named deliverable changes mid-conversation
- new adjacent capabilities are added without replacing old ones
- reference artifacts start acting as new scope definitions
- questions are about tools or architecture before the first deliverable is pinned
- acceptance is described only as "更完整" or "更智能"

When drift appears:

1. restate the current anchor packet
2. mark the new idea as `in-scope now`, `later`, or `out-of-scope`
3. only then continue governance design

## Promotion rule

Do not promote the conversation into structure governance, workflow design, or multi-tool adaptation until the alignment packet is stable enough that the next clarification round is unlikely to rename the first deliverable.
