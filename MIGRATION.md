# MIGRATION

这份文档说明如何把旧约定迁到当前 governed pack 约定。
它只讨论 governed pack / contract 的 `tranche v1`，不重定义能力模型 `v1 -> v2 -> v2.1`。
能力模型基线仍以 [docs/项目治理能力模型.md](docs/项目治理能力模型.md) 为准。

## 1. 这次迁移改了什么

当前 governed pack / contract `tranche v1` 有 7 个实质变化：

1. pack 根目录现在要求补一份 `BOUNDARY.md`，把场景、交付物、故事、测试、非目标、质量参考对象和验收责任人显式落盘
2. project-level object 合同目录从 `schemas/*.json` 迁到 `objects/*.json`
3. `rules.contract.json` 的 rule 形态从自由 `statement` 收口到带 `effect` 的结构化规则
4. workflow 不再在 node / transition 层重复登记 checks，只保留顶层 `checks.route/evidence/write/stop`
5. `status.projection.json` 使用扁平来源锚点 `source_last_event_id / generated_at`，不再使用 `derived_from`
6. `workflow.agent_refs` 固定指向 `agent.contract.json` 的顶层 `agent_id`
7. `workflow.events.jsonl` 的 `subject_ref` 在 `tranche v1` 固定指向 `node_id / transition_id`

## 2. 迁移顺序

建议按下面顺序做，不要跳步：

1. 先补 `BOUNDARY.md`
   - 至少补齐 `scenarios / deliverable / user_stories / test_cases / non_goals / quality_references / acceptance_owner`
   - 用户故事保持 1 到 3 条
   - 测试用例保持 3 到 8 条，且至少一条明确写 `失败/越界边界`
2. 迁目录
   - 把 pack 里的 `schemas/*.json` 移到 `objects/*.json`
3. 迁 workflow
   - 删除 `node.check_refs`
   - 删除 `transition.required_check_refs`
   - 只保留 workflow 顶层 `checks`
4. 迁 rules
   - 每条 rule 至少补 `rule_id` 和 `effect`
   - 根据需要补 `condition_ref / target_refs / required_refs`
5. 迁 status projection
   - 去掉 `derived_from`
   - 改成 `source_last_event_id / generated_at`
   - 不再携带 `allowed_next_step_refs`
6. 迁 agent / event 语义
   - `agent_refs` 不再写 role id，改写顶层 `agent_id`
   - `approver_ref` 继续写 `roles[].role_id`
   - `workflow.events.jsonl.subject_ref` 只保留 `node_id / transition_id`
7. 安装依赖并运行 validator

## 3. 旧字段到新字段

### 3.1 boundary anchor

新：

```text
pack/
└── BOUNDARY.md
```

最小 section tag：

- `[scenarios]`
- `[deliverable]`
- `[user_stories]`
- `[test_cases]`
- `[non_goals]`
- `[quality_references]`
- `[acceptance_owner]`

### 3.2 object 目录

旧：

```text
pack/
└── schemas/*.json
```

新：

```text
pack/
└── objects/*.json
```

### 3.3 rules contract

旧：

```json
{
  "rule_id": "rule.example",
  "statement": "Do not release when evidence is missing."
}
```

新：

```json
{
  "rule_id": "rule.example",
  "effect": "require_evidence",
  "required_refs": ["evidence.example"]
}
```

### 3.4 checks

旧：

- `workflow.checks`
- `node.check_refs`
- `transition.required_check_refs`

新：

- 只保留 `workflow.checks.route/evidence/write/stop`

### 3.5 status projection

旧：

- `derived_from`
- `allowed_next_step_refs`

新：

- `source_last_event_id`
- `generated_at`
- 只保留派生摘要字段

### 3.6 agent refs

旧：

- `agent_refs` 里混写 agent id / role id

新：

- `agent_refs` 只写 `agent.contract.json.agent_id`
- `approver_ref` 只写 `roles[].role_id`

### 3.7 event subject_ref

旧：

- `subject_ref` 可能混写节点、转移、证据或其他对象 ref

新：

- `subject_ref` 在 `tranche v1` 只写 `node_id / transition_id`

## 4. validator 的兼容策略

当前 validator 已经不再保留 pack 内 `schemas/*.json` 的通过路径：

1. 只要 pack 里还保留 `schemas/*.json`，就会直接报迁移错误
2. 缺少 `BOUNDARY.md` 或边界锚点不完整，会直接报错
3. `rules.contract.json` 的旧 `statement` 形态不会再被视为合规
4. `status.projection.json` 的旧 `derived_from` 形态也不会再通过
5. `workflow.state.json` 不再允许携带 `allowed_next_step_refs`
6. `agent_refs` 如果继续写 role id，会报错
7. `subject_ref` 如果继续写 object ref，会报错

也就是说：

- `BOUNDARY.md` 现在是“必须补齐”
- `objects/*.json` 才是 canonical pass path；pack 内不再允许残留 `schemas/`
- `statement -> effect` 与 `derived_from -> source_last_event_id/generated_at` 已经是“必须迁”

## 5. 迁完后的最低验证

至少跑一次：

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_governance_assets.py /abs/path/to/pack
```

建议直接对照 smoke pack：
[examples/smoke-governed-review](examples/smoke-governed-review)
