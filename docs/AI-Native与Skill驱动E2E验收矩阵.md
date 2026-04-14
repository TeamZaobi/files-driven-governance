# AI-Native 与 Skill 驱动 E2E 验收矩阵

状态：`working matrix`

这份文档只回答一个问题：

**前面围绕 AI-Native / skill-driven 场景做的改动，今天到底该用哪些端到端路径来验收。**

对这类场景，真正的 E2E 验收优先以 `CLI / runner` 作为触发面；纯 prose 的 route contract 只能算前置校验，不算最终验收。

这里说的“模拟真实生产场景”，不是把外部服务原封不动搬进本地，而是要尽量沿用真实入口、真实工作目录、真实文件读写和真实 runner 产物，让验收路径和生产路径尽量同构。

它不是能力模型真源，也不是新的执行器。
它只是把当前已经存在的分散回归，收敛成一张可读、可路由、可复查的 E2E 验收矩阵。

## 1. 为什么需要这张矩阵

最近这轮修改主要围绕三类场景：

1. `AI-Native / AI-Driven` 项目的治理入口
2. `skill-driven` 的 Agent 入口与默认 prompt 路由
3. 下游 starter、宿主化知识工作场景和 self-hosting 受控执行

这些改动如果只看单点测试，很容易看不出“用户从入口到结果”是否真的闭环。
所以这里把验收分成几条 E2E lane：

- 从用户原话到 skill 路由
- 从下游 starter 到 governance 体检
- 从宿主名先行到治理问题分诊
- 从运行观察到候选保留与能力晋升
- 从 self-hosting 诊断到受控执行

## 2. 当前 E2E lane

| lane | 端到端问题 | 入口面 | 主要回归资产 | 通过线 |
| --- | --- | --- | --- | --- |
| `agent-facing skill route` | 用户原话能否稳定进入正确的 skill / README / output 骨架 | `README.md`、`SKILL.md`、`agents/openai.yaml`、`references/输出约定.md` | [tests/test_agent_facing_e2e.py](../tests/test_agent_facing_e2e.py) | 常见请求能命中正确资产，输出骨架先于扩段 |
| `downstream starter governance` | 下游 starter 能否从空目录起步，并在 governance audit 下保持真源、scope 和 authority 边界 | `starters/minimal-files-engine/`、`scripts/bootstrap_files_engine_starter.py`、`scripts/manage_files_engine.py` | [tests/test_files_engine_actions.py](../tests/test_files_engine_actions.py) | `bootstrap -> audit scaffold/pack/runtime/governance/adoption` 至少能把 boundary、registry、route、hooks 边界守住 |
| `host-name-first triage` | 宿主名先行时，能否先回治理判断，再回工具操作 | `docs/宿主化知识工作场景矩阵.md`、`examples/hosted-knowledge-governance/`、`SKILL.md`、`agents/openai.yaml` | [tests/test_end_to_end_governance_alignment.py](../tests/test_end_to_end_governance_alignment.py) | `Obsidian / Notion / Docs / Sheets / Slides` 能稳定分诊到真源、索引、状态、展示或工具操作 |
| `runtime promotion chain` | 运行观察能否进入候选、回退、激活的受控链，而不是热改真源 | `references/运行观察与能力晋升.md`、`examples/capture-candidate-activation/`、`scripts/manage_files_engine.py` | [tests/test_capture_promotion_assets.py](../tests/test_capture_promotion_assets.py) 与 runtime 体检用例 | `recall_note.md / split_decision.md / workflow.events.jsonl` 的链路锚点、`reason_refs / artifact_refs / recall chain` 的 traceability 要能同时被守住 |
| `self-hosting control capability` | 仓库级收口能否被受控 runner 编码并复跑 | `scripts/run_repo_treatment_rollout.py`、`scripts/run_project_director_capability_improvement.py`、`manage capability-improve` | [tests/test_files_engine_actions.py](../tests/test_files_engine_actions.py) | 受控 rollout 能留下可审计产物，且不把 control plane 外移成长期本体 |

## 3. 这张矩阵怎么判

一条 lane 只有同时满足下面三件事，才算真正被 E2E 覆盖：

1. 入口侧有真实用户原话、宿主名、starter、`CLI / runner` 或其他可复跑起点，且这些起点要尽量对齐真实生产工作流
2. 中间层能走到治理判断、合同边界、候选链或体检层级
3. 结果侧能落回可验证资产，而不是只停在 prose 解释

如果只验证了其中一段，就只能叫局部回归，不能叫 E2E 验收。

其中 `agent-facing skill route` 目前仍以 route contract 作为代理验证；如果要做严格的 AI-Native E2E，还要再套一层宿主 CLI 或 runner 触发。

## 4. 当前结论

现在这几条 lane 已经都有稳定回归，但成熟度不完全相同：

1. `agent-facing skill route` 已经是本仓最稳定的 E2E 入口之一
2. `downstream starter governance` 已经覆盖 `scaffold / pack / runtime / governance / adoption` 五层 draft 入口
3. `host-name-first triage` 已经有正式矩阵和 fixture
4. `runtime promotion chain` 已经有官方 example、运行观察 reference 和记忆链字段检查，并开始把 `reason_refs / artifact_refs / recall chain` 收进 E2E 验收
5. `self-hosting control capability` 已经能跑受控 rollout，但还要继续收口 benchmark 和 promotion criteria

## 5. 还没纳入这张矩阵的东西

1. 真实在线模型 + 多 agent + 外部工具的黑盒 runtime E2E
2. 外部 workflow benchmark 的晋升验证
3. 更广的跨宿主、跨品牌、跨项目类型实战样本

这些还在下一 tranche，不算当前验收门。

## 6. 和其他文档的关系

- [当前阶段补完计划](./当前阶段补完计划.md)：回答下一 tranche 该按什么顺序补
- [三层信息架构复盘](./三层信息架构复盘.md)：回答哪些文档属于入口层、说明层和真源层
- [能力雷达与版本演进盘点](./能力雷达与版本演进盘点.md)：回答能力今天长到哪一步
- [能力覆盖矩阵与历史差分](./能力覆盖矩阵与历史差分.md)：回答这些能力已经照进了哪些入口和执行面
