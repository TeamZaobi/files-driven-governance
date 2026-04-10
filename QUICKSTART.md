# QUICKSTART

这份文档只回答一件事：如何用当前约定搭出一个最小可验证的 governed pack。

## 1. 先认 5 个入口

1. 仓库根的 [schemas/](/Users/jixiaokang/.agents/skills/files-driven/schemas) 是 schema draft，不是 project pack 里的对象合同目录。
2. project pack 的 object 合同放在 `objects/*.json`。
3. `BOUNDARY.md` 是 pack 的边界锚点入口，先锁场景、故事、测试、非目标和验收责任人，再看 workflow 合同。
4. workflow 顶层 `checks.route/evidence/write/stop` 是 v1 唯一 check 注册面。
5. validator 的参数是 `pack_root`，应指向一个具体 pack 目录。

运行本地校验前，先安装最小开发依赖：

```bash
python3 -m pip install -r requirements-dev.txt
```

## 2. 最小 pack 形状

最小可跑形状建议如下：

```text
your-pack/
├── BOUNDARY.md
├── WORKFLOW.md
├── workflow.contract.json
├── objects/
│   ├── state.example.json
│   ├── action.example.json
│   ├── evidence.example.json
│   └── approval.example.json
├── rules.contract.json
├── agent.contract.json
├── workflow.state.json
├── workflow.events.jsonl
└── status.projection.json   # 可选
```

参考现成示例：
[examples/smoke-governed-review](/Users/jixiaokang/.agents/skills/files-driven/examples/smoke-governed-review)

其中 `BOUNDARY.md` 建议至少包含这些二级标题，并保留方括号里的稳定 section tag，方便人读和自动校验同时成立：

```markdown
## 首批真实使用场景 [scenarios]
## 首批交付物 [deliverable]
## 用户故事 [user_stories]
## 测试用例 [test_cases]
## 非目标 [non_goals]
## 质量参考对象 [quality_references]
## 验收责任人 [acceptance_owner]
```

## 3. 最小设计顺序

1. 先写 `BOUNDARY.md`
   - 先锁首批场景、首批交付物、1 到 3 个用户故事、3 到 8 个测试用例、非目标、质量参考对象和验收责任人
   - 至少有一个测试用例明确写出 `失败/越界边界`
2. 再写 `workflow.contract.json`
   - 定义节点、转移、`policy_refs`、`object_refs`、`agent_refs`
   - `agent_refs` 指向 `agent.contract.json` 的顶层 `agent_id`
   - `approver_ref` 另行指向 `roles[].role_id`
   - 顶层 `checks` 只按 `route / evidence / write / stop` 分段
3. 再写 `objects/*.json`
   - 至少补齐 `state_ref / action_ref / evidence_refs / approval_ref` 要引用到的对象
4. 再写 `rules.contract.json` 和 `agent.contract.json`
   - 规则讲“约束是什么”
   - agent 讲“谁能执行 / 复核 / 批准”
5. 最后写运行实例
   - `workflow.state.json`
   - `workflow.events.jsonl`
   - 其中 event 的 `subject_ref` 在 v1 只指向 `node_id / transition_id`
   - 可选 `status.projection.json`

## 4. 运行 validator

从仓库根执行：

```bash
python3 scripts/validate_governance_assets.py examples/smoke-governed-review
```

如果你在别的目录运行，参数必须仍然指向 pack root，例如：

```bash
python3 /Users/jixiaokang/.agents/skills/files-driven/scripts/validate_governance_assets.py /abs/path/to/your-pack
```

不要把仓库根传给 validator，除非仓库根本身就是一个完整 pack。

仓库级最小回归也已经接好：

- 本地运行：`python3 -m unittest discover -s tests -p 'test_*.py'`
- CI 入口：`.github/workflows/governance-assets-ci.yml`

## 5. 当前最容易犯的错

1. 把 object 合同继续放进 `schemas/*.json`
2. 没有先写 `BOUNDARY.md`，就直接开始搭 workflow / objects / rules
3. 在 node 或 transition 层重复写 check refs
4. 让 `status.projection.json` 带上 `allowed_next_step_refs` 或新的放行结论
5. `rules.contract.json` 继续使用旧的 `statement` 形态而不写 `effect`

## 6. 下一步看什么

如果你已经有旧 pack，要迁移：
[MIGRATION.md](/Users/jixiaokang/.agents/skills/files-driven/MIGRATION.md)

如果你想看更完整的能力模型：
[docs/项目治理能力模型_v1.md](/Users/jixiaokang/.agents/skills/files-driven/docs/项目治理能力模型_v1.md)
