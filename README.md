# kims-skills

一套前端开发辅助 Skills 合集，适用于 Cursor、Codex 等支持 `SKILL.md` 的编程助手。每个 Skill 都是独立目录，包含一个 `SKILL.md` 说明文件，可按需复制使用。

## Skill 列表

| Skill 目录 | 用途 | 使用场景 |
| --- | --- | --- |
| `brainstorming` | 前端方案发散、可行性比较、产品技术协同分析 | 需求不清晰、方案不唯一、需要多方案对比或拆解复杂业务时 |
| `code-review` | 前端代码审查 | 评审 PR / Merge Request、走查 diff、检查「这样写有没有问题」时 |
| `debug-analysis-and-fix` | 系统分析并修复前端问题 | 页面报错、白屏、接口异常、交互不生效、构建失败或需要定位回归问题时 |
| `frontend-design` | 设计前端技术方案和页面实现方案 | 新增页面、重构模块、接入复杂接口、设计组件拆分或输出前端设计文档时 |
| `optimization-analysis-and-design` | 分析性能、体验、稳定性和可维护性问题并设计优化方案 | 页面慢、列表卡顿、重复请求、导出慢、包体积大或需要重构复杂组件时 |
| `requirement-analysis-and-decomposition` | 分析前端需求并拆解开发任务 | 提供 PRD、原型、Story、接口文档、截图或口头需求，需要梳理场景、接口、权限和验收标准时 |

## 安装

### Cursor

1. 克隆本仓库：

   ```bash
   git clone https://github.com/NewbieKim/kims-skills.git
   ```

2. 把需要的 Skill 目录复制到项目的 `.cursor/skills` 下：

   ```bash
   # 以 brainstorming 为例
   cp -r kims-skills/brainstorming <你的项目>/.cursor/skills/
   ```

3. 重启或重新加载 Cursor，Skill 即可生效。

### Codex

1. 克隆本仓库：

   ```bash
   git clone https://github.com/NewbieKim/kims-skills.git
   ```

2. 把需要的 Skill 目录复制到 Codex 的 skills 目录：

   - Windows：`C:\Users\<你的用户名>\.codex\skills\`
   - macOS / Linux：`~/.codex/skills/`

   例如：

   ```bash
   cp -r kims-skills/debug-analysis-and-fix ~/.codex/skills/
   ```

3. 在新的对话中使用，或者按对应 Skill 里的「何时使用」描述自然触发。

## 说明

- 每个 Skill 的触发方式、工作流程和输出模板都在对应 `SKILL.md` 中。
- `vue2-dialog`、`vue2-table-page` 等与具体 Vue2 项目强绑定的 Skill 不在本仓库中。

## License

Apache License 2.0
