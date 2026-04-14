# minimal files engine starter

这是一份官方最小 starter。
它的目标不是替代完整业务模板，而是把 `files-driven` 装进一个下游项目，让你能从空目录起出一个可注册、可解析、可验证的最小起点。
它本身也是下游项目的参考实现样本，不是通用模板本体。

这里要先记住：

- 这是 `downstream project instance`，不是 `repo.files-driven`
- 它包含最小 governed pack，也包含 starter 层的 `scaffold manifest`、`files registry` 与 `intent routes`
- 冷启动后先跑 scaffold validator，再跑 pack validator

默认依赖顺序：

- `governance/scaffold.manifest.json` 负责 starter 拓扑和 validator 跟踪范围
- `governance/hooks.policy.md` 负责项目级 hooks 真源，不让工具配置文件自己发明规则
- `governance/files.registry.json` 负责文件身份核心与 annotations
- `governance/intent.routes.json` 单向消费注册过的 `file_id`，决定入口、必读和写入目标
- starter 专属形状约束由单独的 starter profile 持有，不写进 manifest
- `bootstrap` 只负责 install；`register / repair / audit` 通过统一 `manage` CLI 处理
- `tooling/hooks/` 提供 repo-local hooks 模板和脚本，但这些模板属于适配层，不是 control truth

因此：

- 只改 route 名称或入口动作时，只改 `governance/intent.routes.json`
- 只改某个工具的 hooks 接法时，先看 `tooling/hooks/README.md`，不要先改项目真源
- 要改“这个项目到底哪些动作该拦、哪些只记录”时，先改 `governance/hooks.policy.md`
- 新增或移动 tracked 文件时，先改 `governance/scaffold.manifest.json`，再改 `governance/files.registry.json`
- starter 专属形状变化时，先改 starter profile，再检查 validator 是否需要跟进

推荐顺序：

1. 先改 `BOUNDARY.md`
2. 再改 `governance/hooks.policy.md`
3. 如果 starter 拓扑要变化，先改 `governance/scaffold.manifest.json`
4. 再改 `governance/files.registry.json`
5. 再改 `governance/intent.routes.json`
6. 再改 `tooling/hooks/README.md` 与模板
7. 再改 `skills/review-skill/SKILL.md`
8. 最后改 `workflow.contract.json`、`objects/*.json` 和运行实例
