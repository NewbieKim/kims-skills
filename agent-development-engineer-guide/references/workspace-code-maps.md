# 六项目工作区代码地图

基线日期：2026-09-21。代码会变化；实操前用 `rg --files`、目标包 `package.json` 和入口文件重新核对。

## 总体关系

```text
ltbot (Vue 业务前端)
  ├─ 使用 remote-chat-sdk 渲染会话与消费 SSE
  ├─ 使用 web-mcp-sdk 暴露浏览器页面工具
  └─ 调用 ltbot-server 的 Chat/Agent/Remote/知识库 API

ltbot-server (Express 业务后端)
  ├─ 调用 ain-agent-sdk 路由并执行工作流
  ├─ 用 Redis/Redis OM 保存会话与业务数据
  └─ 为前端提供 SSE、LLM proxy、Remote session 与知识库 API

ain-framework (三个可发布 SDK)
  ├─ ain-agent-sdk：模型、LangGraph、workflow registry/router
  ├─ remote-chat-sdk：Vue 对话 UI + SSE runtime
  └─ web-mcp-sdk：浏览器内 JSON-RPC/工具注册与传输

kims-dailywork-mcp：把工单与邮件封装为独立 MCP Server
kims-llm-wiki：学习知识与项目证据的持久 Wiki
kims-skills：辅导、开发和复盘工作流的 Skill 集合
```

## 1. ain-framework

路径：`D:\kimsweb\ain-framework`。pnpm workspace，Node >=20。

### ain-agent-sdk

- `src/index.ts`：公共导出面；模型、图、workflow registry/router、Remote workflow 都从这里暴露。
- `src/model/deepseek.ts` / `openai.ts`：模型适配与结构化输出入口。
- `src/workflow/registry.ts`：`chat`、`marketing_agent`、`email_agent`、`remote_control` 的 schema、元数据与执行函数。
- `src/workflow/router.ts`：LLM 结构化路由、允许列表、0.65 置信阈值与 chat 降级。
- `src/graph/marketingAgent.ts`：planning → simple/research → writer 的 LangGraph；MemorySaver 保存 thread state。
- `src/graph/emailAgent.ts`：读邮件、分类、检索/工单、写回复、人工审核、发送的条件图；含本地 hook 测试替身。
- `src/graph/research.ts`：Deep Agent 研究流程、搜索工具与文件型 memory。
- `src/graph/writer.ts`：初稿 → 反思 → 改进循环 → 定稿，带最大内容约束与 MemorySaver。
- `src/tools/remote/*`：Remote tool 类型与 prompt 格式适配。

### remote-chat-sdk

- `src/index.ts`：组件、composable、stream runtime 和类型的公共 API。
- `src/stream/createStreamingRuntime.ts`：发送消息、读取 SSE、取消、运行状态。
- `src/stream/sseParser.ts` → `protocol.ts` → `streamReducer.ts`：字节/行解析、事件规范化、消息状态归约的核心链。
- `src/components/*`：MessageList、PromptInput、Tool、Reasoning、Sources、SessionList 等无业务 UI。
- `src/composables/useChatSessions.ts` / `useAttachment.ts`：会话与附件状态能力。

### web-mcp-sdk

- `src/protocol/types.ts`：JSON-RPC 消息与错误。
- `src/transport/messageChannelTransport.ts`：浏览器内双端 MessageChannel 传输。
- `src/tools/types.ts` / `registry.ts`：工具定义、permission/riskLevel、注册与执行。
- `src/server/webMcpServer.ts`：处理 initialize、tools/list、tools/call。
- `src/client/webMcpClient.ts`：请求关联、超时和客户端调用。

### 关键数据流

`ltbot/RemoteChat → ltbot-server/chatAgent → routeUserMessage → workflowRegistry/LangGraph → SSE → remote-chat-sdk reducer → Vue UI`。

### 强化重点

- MemorySaver 仅内存，缺少生产持久化/恢复证据。
- 路由、图节点和 Remote workflow 需要统一 trace/eval。
- `runRemoteControlWorkflow` 当前主要消费既有结果并格式化回答，不等于完整自主工具循环。
- 三个 SDK 需要跨包契约测试、版本兼容和发布回归。

## 2. kims-dailywork-mcp

路径：`D:\kimsweb\kims-dailywork-mcp`。Express 5 + MCP SDK + zod + IMAP/SMTP。

- `src/index.ts`：加载配置并选择 Streamable HTTP 或 `--stdio`。
- `src/server.ts`：`DailyworkMcpServer`，注册工具、HTTP health/MCP 路由、会话 transport、访问令牌校验。
- `src/core/config.ts`：共享服务配置；`user-config.ts`：Base64/JSON 个人配置解析与合并。
- `src/core/context.ts`：AsyncLocalStorage 保存每个 MCP 会话的用户配置，防止串号。
- `src/domains/ticket/icase-client.ts` / `tools.ts`：工单客户端及 list/detail/category/route 工具；部分接口待文档确认。
- `src/domains/mail/imap-client.ts`、`smtp-client.ts`、`reply.ts`、`tools.ts`：未读、读取、回复；默认写草稿，`confirm=true` 才发送。
- `tests/*`：配置、用户隔离、iCase、回复与 smoke 测试。

强化重点：真实写操作的确认令牌/幂等/审计；接口超时和错误分类；多会话并发；工具级指标；未完成 iCase API 的契约测试。

## 3. kims-llm-wiki

路径：`D:\kimsweb\kims-llm-wiki`。Markdown/Obsidian Wiki，不是向量库本身。

- `AGENTS.md`：schema 与 ingest/query/lint 操作规则；`raw/` 永不修改。
- `wiki/index.md`：所有实体主索引；任何查询先读。
- `wiki/overview.md` / `glossary.md` / `log.md`：全局综述、术语规范、append-only 活动日志。
- `wiki/sources`、`concepts`、`tools`、`courses`、`projects`、`analyses`：结构化知识层。

强化重点：把六项目地图、面试错题、评测报告和项目指标持续写入；建立可增量检索的解析/版本/引用层；保持链接和术语一致。

## 4. kims-skills

路径：`D:\kimsweb\kims-skills`。每个 Skill 是独立目录，核心为 `SKILL.md`，复杂说明放 `references/`，UI 元数据放 `agents/openai.yaml`。

- `agent_happy_day`：第一轮 agent-study 课程辅导与 TS 映射。
- `chat_sdk_happy_day`：对话 SDK 专项辅导。
- `brainstorming`、`requirement-analysis-and-decomposition`、`frontend-design`、`code-review`、`debug-analysis-and-fix`、`optimization-analysis-and-design`：通用研发流程。
- `agent-development-engineer-guide`：第二轮强化、生产实战、面试与求职闭环。

强化重点：每次改 Skill 用 quick validator；入口保持短，细节渐进披露；代码地图和市场材料注明基线日期，避免陈旧规则绑死未来实现。

## 5. ltbot

路径：`D:\kimsweb\kimsweb-front\packages\ltbot`。Vue 3 + Vite + Pinia + TDesign。

- `src/main.ts`：安装 Pinia、Router、TDesign Chat 和 remote-chat-sdk 样式。
- `src/components/RemoteChat/index.vue`：基于 remote-chat-sdk 的生产方向聊天 UI；调用 `/api/chatAgent`，把 SDK message 与数据库 message 转换并增量持久化。
- `src/components/ChatBot/index.vue`：较早的完整聊天实现，含直接模型请求/工具处理逻辑，是迁移与去重对象。
- `src/mcp/index.ts`：手写 OpenAI tool registry；add/query/update todo 与项目查询。
- `src/remote/webMcp.ts`：启动 WebMcpServer/Client，注册当前页面和可选 todo 读取工具。
- `src/stores/modules/chat.ts` + `src/api/chat.ts`：会话列表、消息和 Redis API 交互。
- `src/views/skillKnowledgeBase/*` + `src/api/skillKnowledgeBase.ts`：知识库树、HTML 源码编辑和预览。

关键边界：RemoteChat 负责 UI/runtime，业务会话真相在服务端 Redis；浏览器页面能力通过 web-mcp-sdk 暴露；模型密钥只应在服务端。

强化重点：合并/明确两套聊天与两套工具注册的责任；工具 schema 单一真相源；Remote action 权限确认；组件与 SSE 集成测试；前端断连/重连和重复持久化验证。

## 6. ltbot-server

路径：`D:\kimsweb\kimsweb-front\packages\ltbot-server`。Express 5 + Redis/Redis OM + ain-agent-sdk。

- `index.ts`：服务入口与路由装配；`/api/chat` 同时挂会话 CRUD 和 SSE router，另有 `/api/chatAgent`、`/api/llm`、`/api/remote`、`/api/skillKnowledgeBase`。
- `routes/chatAgent.ts`：todo 正则捷径 → SDK LLM 路由 → marketingAgent 或普通模型流；输出 AI SDK 风格 SSE。
- `routes/chatStream.ts`：直连 DeepSeek SSE 并转换 text/reasoning 事件，支持客户端 abort。
- `routes/llmProxy.ts`：OpenAI 兼容代理，支持 JSON 与 SSE 透传，保护服务端密钥。
- `routes/remote.ts`：内存 Remote session、TTL/heartbeat、tool snapshot 同步和 Remote workflow。
- `routes/chat.ts` + `db/chatService.ts`：Redis ZSET/Hash/List 的会话与消息 CRUD。
- `db/redis.ts`：Redis 客户端、Redis OM schema/index 与服务初始化。
- `routes/skillKnowledgeBase.ts`：限定根目录的 HTML 树/读写/静态预览，生产禁写。

强化重点：`chatAgent` 的 todo 意图仍是正则捷径；Remote session 仅内存；Agent/stream/proxy 存在重复模型链路；缺少系统性测试、统一错误模型、鉴权/租户边界、trace/eval 与限流；需验证 Redis 不可用、SSE 断连、重复消息和并发写的一致性。

## 推荐作品集叙事

把六个项目讲成一条平台链路：

1. `ain-framework` 提供模型无关的 Agent、Chat Runtime 与 Web Tool SDK。
2. `kims-dailywork-mcp` 把真实企业流程封装成安全工具。
3. `ltbot-server` 负责业务编排、状态、模型网关和流式服务。
4. `ltbot` 提供对话、页面工具与知识界面。
5. `kims-llm-wiki` 保存领域知识、评测与复盘。
6. `kims-skills` 固化可复用开发与学习流程。

面试时明确哪些已实现、哪些是下一步设计，绝不把规划说成线上成果。
