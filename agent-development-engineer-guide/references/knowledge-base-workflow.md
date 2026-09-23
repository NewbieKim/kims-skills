# kims-llm-wiki 学习沉淀工作流

遵守 `D:\kimsweb\kims-llm-wiki\AGENTS.md`；若本文件与其冲突，以仓库内 AGENTS.md 为准。

章节学习仍在 wiki 记录阶段、错题、代码证据与日志；用户在章节完成后明确要求总结时，另按 [章节深化与总结流程](chapter-deep-dive.md) 在 Skill 的 `daydayup/` 生成 `MMDD知识点名称.md`。两者职责不同，不要提前写“完成”总结或用 daydayup 替代 wiki。

## 会话开始

1. 读 `AGENTS.md`。
2. 读 `wiki/index.md` 定位页面。
3. 读 `wiki/log.md` 最近 5 条记录。
4. 读本次主题的 concept/project/analysis 页面；不要从零重复推导已有知识。

## 写入边界

- `raw/` 永远只读。
- 仅在 `wiki/` 创建或更新结构化页面。
- 每页使用规范 frontmatter：title/type/created/updated/sources/tags/status。
- 文件名 kebab-case，内部链接用 `[[name]]`。
- 每次更新补反向链接、`wiki/index.md` 和 `wiki/log.md`；大图景变化时更新 `overview.md`，新术语更新 `glossary.md`。

## 学习记录分层

| 内容 | 页面位置 | 写什么 |
|---|---|---|
| 稳定机制 | `wiki/concepts/` | 定义、机制、失败模式、项目连接、面试问法 |
| 框架/协议 | `wiki/tools/` | 能力、边界、选型、替代与版本注意 |
| 阶段学习 | `wiki/courses/` | 目标、完成节点、测验、未解问题 |
| 真实代码 | `wiki/projects/` | 代码地图、数据流、架构决策、验证与指标 |
| 错题/评测/复盘 | `wiki/analyses/` | 原回答、错误原因、正确模型、证据、复测日期 |

## 每次实战结束模板

```markdown
## YYYY-MM-DD｜主题

- 目标：
- 修改范围：
- 关键机制：
- 验证命令与结果：
- 基线/改进指标：
- 失败样例与原因：
- 架构取舍：
- 90 秒面试表达：
- 下一次复测：D+1 / D+3 / D+7 / D+14
```

没有实测指标时写“未测/待测”，不得编造。

## 代码地图维护

六个项目分别维护 project 页面。以下变化必须更新：

- 新入口、包、路由或协议边界。
- 状态真相源或持久化方式改变。
- 新增 Agent/RAG/MCP/Eval/Safety 主链。
- 已知限制被修复或出现新的生产风险。
- 验证命令、性能数据或部署方式变化。

代码地图保留“基线日期”和“已实现/计划中”区分。更新前先读实际文件，不从 Skill 参考直接复制过期内容。

## 面试错题工作流

在 `wiki/analyses/agent-interview-errors.md` 维护：题目、首次回答摘要、评分、核心错误、项目证据、重答、复测日期。通过一次不删除；至少在 D+3、D+7 各复测一次。

## 日志格式

按 AGENTS.md 追加，不改历史：

```markdown
## [YYYY-MM-DD] query | Agent 强化：<主题>
Pages consulted: ...
Pages created: ...
Pages updated: ...
Evidence: ...
Next review: ...
```
