# MIGRATION

这份文档说明如何把旧约定迁到当前 governed pack 约定。

## 1. 这次迁移改了什么

当前 tranche 有 4 个实质变化：

1. project-level object 合同目录从 `schemas/*.json` 迁到 `objects/*.json`
2. `rules.contract.json` 的 rule 形态从自由 `statement` 收口到带 `effect` 的结构化规则
3. workflow 不再在 node / transition 层重复登记 checks，只保留顶层 `checks.route/evidence/write/stop`
4. `status.projection.json` 使用扁平来源锚点 `source_last_event_id / generated_at`，不再使用 `derived_from`

## 2. 迁移顺序

建议按下面顺序做，不要跳步：

1. 迁目录
   - 把 pack 里的 `schemas/*.json` 移到 `objects/*.json`
2. 迁 workflow
   - 删除 `node.check_refs`
   - 删除 `transition.required_check_refs`
   - 只保留 workflow 顶层 `checks`
3. 迁 rules
   - 每条 rule 至少补 `rule_id` 和 `effect`
   - 根据需要补 `condition_ref / target_refs / required_refs`
4. 迁 status projection
   - 去掉 `derived_from`
   - 改成 `source_last_event_id / generated_at`
   - 不再携带 `allowed_next_step_refs`
5. 运行 validator

## 3. 旧字段到新字段

### 3.1 object 目录

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

### 3.2 rules contract

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

### 3.3 checks

旧：

- `workflow.checks`
- `node.check_refs`
- `transition.required_check_refs`

新：

- 只保留 `workflow.checks.route/evidence/write/stop`

### 3.4 status projection

旧：

- `derived_from`
- `allowed_next_step_refs`

新：

- `source_last_event_id`
- `generated_at`
- 只保留派生摘要字段

## 4. validator 的兼容策略

当前 validator 仍保留一层轻兼容：

1. 如果 pack 里还在用 `schemas/*.json`，会给 warning，并尽量继续读取
2. 但 `rules.contract.json` 的旧 `statement` 形态不会再被视为合规
3. `status.projection.json` 的旧 `derived_from` 形态也不会再通过

也就是说：

- `schemas/ -> objects/` 目前是“告警兼容”
- `statement -> effect` 与 `derived_from -> source_last_event_id/generated_at` 已经是“必须迁”

## 5. 迁完后的最低验证

至少跑一次：

```bash
python3 scripts/validate_governance_assets.py /abs/path/to/pack
```

建议直接对照 smoke pack：
[examples/smoke-governed-review](/Users/jixiaokang/.agents/skills/files-driven/examples/smoke-governed-review)
