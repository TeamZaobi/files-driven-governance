# schemas

这个目录承载 `files-driven` 当前重构中的结构化合同草案。

它不是要替代 `README.md`、`SKILL.md`、`references/` 或 `docs/`，
而是为高风险控制语义提供机读入口。

当前放在这里的内容主要是：

1. `workflow.contract.schema.json`
2. `object.contract.schema.json`
3. `policy.contract.schema.json`
4. `agent.contract.schema.json`

术语冻结：

1. `policy_or_rules` 家族在项目里的 canonical 资产名叫 `rules contract`
   - 建议文件名：`rules.contract.json`
   - 本目录里的 schema 文件名：`policy.contract.schema.json`
2. `object` 家族在项目里的 canonical 资产名叫 `object schema`
   - 建议文件落点：`schemas/*.json`
   - 本目录里的 schema 文件名：`object.contract.schema.json`
3. `workflow` 家族在项目里的 canonical 资产名叫 `workflow contract`
   - 建议文件名：`workflow.contract.json`
   - 本目录里的 schema 文件名：`workflow.contract.schema.json`
4. `agent` 家族在项目里的 canonical 资产名叫 `agent contract`
   - 建议文件名：`agent.contract.json`
   - 本目录里的 schema 文件名：`agent.contract.schema.json`

这里的 schema 文件名描述的是“本仓库里的 schema 草案”，
不是要求项目实例必须逐字照搬同名文件。

这些文件描述的是“合同的结构”，
不是某个具体项目的实例数据。

当前默认的分工是：

1. `workflow.contract.schema.json` 负责控制路径、节点、转移和检查点声明
2. `object.contract.schema.json` 负责状态、动作、证据、输出、批准对象的语义
3. `policy.contract.schema.json` 负责跨 workflow 的规则、风险和限制
4. `agent.contract.schema.json` 负责执行、复核、批准与回退权限矩阵

重要边界：

1. `workflow` 合同只引用对象、规则和角色，不应自己发明它们的语义
2. `workflow.state.json` 与 `workflow.events.jsonl` 属于 `execution_object`，不是 workflow 家族真源
3. `checks/` 属于 `skill` 或工具适配执行面，不等于 workflow 自己持有放行权
4. `WORKFLOW.md` 是解释层，`workflow.contract.json` 才是受控模式下的机读控制真源

使用原则：

1. `Markdown` 继续负责解释、边界和人工复核
2. `JSON` 负责合同和状态
3. `JSONL` 负责事件流和运行轨迹
4. 脚本、hook、validator 负责执行这些合同

当前状态：

- 它们还是 v1 草案
- 主要目标是冻结最小字段和引用关系
- 还没有取代现有 reference 的解释职责
