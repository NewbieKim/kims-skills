# AI Agent 开发工程师能力模型与证据标准

用于基线诊断、岗位匹配、路线调整和月末验收。结论基于 2026 年 AgentGuide 开发岗路线、Agent/RAG 面试题库及近期职位样本；做具体求职分析时仍需重新核对目标 JD。

## 市场结论

当前开发岗寻找的是“能把非确定模型能力做成可靠业务系统”的复合型工程师。核心不是会调用 API，而是能设计 Agent Harness，接入业务工具与数据，建立 RAG、评测、可观测、安全和上线闭环。

用户已有 Vue/TypeScript/Node/Redis 与业务交付经验，这是全栈 Agent 岗的优势。一个月内的主要短板优先级：

1. 生产级 RAG 全链路与可量化评测。
2. Agent 评测、Trace/Replay、bad case 数据闭环。
3. 工具权限、超时重试、幂等、HITL、提示词注入防护。
4. 状态与记忆的一致性、并发隔离和可恢复执行。
5. 把现有多个项目讲成一个端到端平台，而非零散功能。
6. Python 代码阅读与基础异步服务能力。主项目继续用 TypeScript，不为补语言而重写系统。

## 八维能力模型

| 维度 | 市场要求 | 本工作区证据 | 月末最低证据 |
|---|---|---|---|
| LLM 基础 | Transformer、Attention、Token、解码、KV Cache、结构化输出 | 模型适配器、SSE、structured output | 90 秒讲清 8 个高频主题；能解释参数对延迟/稳定性的影响 |
| Agent/Harness | Loop、规划、状态、工具、记忆、上下文、恢复 | `ain-agent-sdk` 工作流与图、`chatAgent` 路由 | 一个有界循环或图工作流；状态转换测试；失败恢复设计 |
| Tools/MCP | schema、发现/调用、传输、权限、确认、审计 | `web-mcp-sdk`、`kims-dailywork-mcp`、ltbot 工具注册 | 严格 schema、权限等级、超时/错误、危险操作确认及契约测试 |
| RAG | 解析、切块、Embedding、Hybrid、Rerank、引用、增量索引 | `kims-llm-wiki` 内容资产；Redis 基础 | 可运行检索链路；不少于 30 条评测；检索与生成指标分离 |
| Memory/Context | 短期/工作/长期记忆、压缩、隔离、预算 | Redis ChatService、LangGraph state/checkpointer | 会话隔离测试；上下文预算策略；至少一种恢复或衰减机制 |
| Eval/Observability | Task/Trial/Grader/Trace/Replay、线上反馈 | 现有单元测试与流式协议 | 评测数据集、确定性 grader + judge 接口、回归阈值、trace 字段 |
| Reliability/Safety | 并发、重试、幂等、降级、HITL、注入/越权 | 邮件确认、Remote 权限、SSE abort | 关键失败矩阵；至少 3 类故障注入；危险工具不可静默执行 |
| 工程与表达 | API/DB/cache/async/test/deploy、系统设计、项目讲述 | 六个生产项目 | 架构图、README/运行命令、实测指标、3 个 STAR+Tech 故事 |

## 证据等级

每个能力使用 0-4 级，不接受只凭“看过/学过”升级：

- **0 未接触**：无法定义或定位。
- **1 能复述**：能说定义，但不能解释机制和边界。
- **2 能实现**：在提示下完成最小实现并通过基础测试。
- **3 能生产化**：处理失败、并发、安全、观测，能用指标说明取舍。
- **4 能设计与指导**：能比较方案、设计实验、定位复杂故障并接受连续追问。

目标：所有维度至少 2；Agent/Harness、Tools/MCP、RAG、Eval、工程表达至少 3。

## 诊断方式

每次基线包含四类证据：

1. 闭卷口述：定义、机制、边界、取舍。
2. 真实读码：指出入口、状态拥有者、协议边界和失败路径。
3. 限时实操：45-90 分钟完成小改造与测试。
4. 项目答辩：90 秒主答，追问“为什么不用另一方案”“如何证明有效”“线上坏了怎么办”。

## 项目证据清单

每个主项目至少保留以下材料：

- 问题与约束说明。
- 修改前基线与修改后结果。
- 架构/调用链和关键数据结构。
- 自动化验证命令、评测数据与失败样例。
- 至少一个被否决的方案及理由。
- 可复现演示步骤。
- 简历一句话与 3 分钟项目讲述稿。

## 资料入口

- AgentGuide 总览：https://github.com/adongwanai/AgentGuide
- 开发岗路线：https://github.com/adongwanai/AgentGuide/blob/main/docs/05-roadmaps/learning-roadmap-development.md
- 2026 求职路线：https://github.com/adongwanai/AgentGuide/blob/main/docs/05-roadmaps/agent-job-ready-roadmap-2026.md
- Agent Harness：https://github.com/adongwanai/AgentGuide/blob/main/docs/02-tech-stack/27-agent-harness-engineering.md
- 理论题：https://github.com/adongwanai/AgentGuide/blob/main/docs/04-interview/01-theory-questions.md
- RAG 题：https://github.com/adongwanai/AgentGuide/blob/main/docs/04-interview/02-rag-questions.md
- Agent 题：https://github.com/adongwanai/AgentGuide/blob/main/docs/04-interview/03-agent-questions.md

