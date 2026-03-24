# v0.2.0 Release Notes

发布日期：`2026-03-24`

## 这次版本升级了什么

`files-driven` 从“项目结构治理技能”升级为“项目结构治理 + 经典流程库设计技能”。

这一版不只回答：

- 规则、对象、工作流、技能、角色、状态页应该如何分层

也会回答：

- 哪些经典流程应该成为项目默认习惯
- 哪些流程只在高风险或高分歧议题上启用
- 哪些重型流程当前应该明确延后

## 新增内容

1. 新增 [`references/classic-governance-flows.md`](../references/classic-governance-flows.md)
   - 总结 `AIJournal` 与 `HQMDClaw` 中可迁移的经典流程
   - 区分默认流程与条件升级流程
2. 新增 [`references/adversarial-convergence-loop.md`](../references/adversarial-convergence-loop.md)
   - 将 `敌意质询 -> 答辩 -> 收敛` 升成显式高级机制
   - 固化 `question_id`、问题终态与 `closure_authority`
3. 新增 [`CHANGELOG.md`](../CHANGELOG.md)
   - 记录版本演进历史

## 主要升级

1. `SKILL.md`
   - 新增“选择经典流程库”步骤
   - 要求输出时明确区分默认流程、条件升级流程和延后流程
2. `references/output-contract.md`
   - 新增必答区块 `推荐经典流程库`
3. `references/scenario-playbooks.md`
   - 为 `existing_repo / greenfield / recovery_or_realignment` 分别补了推荐 flow set
4. `references/shared-patterns-from-aijournal-and-hqmdclaw.md`
   - 补入发展弧线与可迁移经典流程
5. `README.md`、`docs/MANUAL.md`、`docs/REPO_METADATA.md`
   - 全部同步到新定位与新版本信息

## 这版沉淀的关键流程

默认优先考虑：

1. `low_token_recovery_chain`
2. `discussion -> decision_package -> task_or_decision`
3. `truth_source -> execution_object -> status_projection -> display_projection`
4. `mechanism_review -> repair_or_split`

按条件启用：

1. `adversarial_inquiry -> defense -> convergence`
2. `isolated_multi_role_deliberation`
3. `proposal -> validation -> shadow/canary -> activation_or_rollback`
4. `skill_seed -> package_contract -> active_package`
5. `contract_gap -> closure_topic -> downstream_resume`

## 向后兼容性

这次升级不改变 skill 的基本使用方式，也不要求现有项目一夜之间启用所有流程。

兼容性原则：

1. 现有“结构诊断”场景继续可用
2. 新增流程库选择只会增强输出，不会破坏原有结构诊断能力
3. 多工具环境仍按 adapter 处理，不把工具品牌升级为 canonical role

## 推荐发布标题

`v0.2.0 - Flow library upgrade`

## 推荐一句话摘要

`files-driven` now recommends not only the right project structure, but also the right governance flow set for AI agent systems.
