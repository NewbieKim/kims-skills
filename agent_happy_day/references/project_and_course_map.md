# Course -> project mapping

This file is the detailed reference for translating the agent-study Python course into the kimsweb-front TypeScript project. Read when adapting a chapter to TS or when planning a stage.

## Table of contents

1. Project asset inventory
2. Chapter -> project mapping (all 36)
3. Python -> TS dependency map
4. Splitting rules (server vs browser vs transport)

## 1. Project asset inventory

Already-built agent assets in kimsweb-front (use as teaching artifacts, not as something to rebuild):

- ltbot/src/mcp/index.ts: hand-rolled toolRegistry (definitions + handlers map), registerTool(), getToolDefinitions(), executeToolCall(name, args). Defines tools add_todo, query_todos, update_todo_status, query_project_info. This is a ReAct-ready tool layer missing only the LLM decision loop.
- ltbot/src/remote/webMcp.ts: startRemoteMcp() builds a WebMcpServer over a MessageChannel transport, registers ltbot.page.getCurrent and ltbot.todo.list as browser-side remote tools with permission/riskLevel fields. Good anchor for Ch18 security and Ch10 MCP.
- ltbot-server/routes/remote.ts: Remote session store (createSessionId, TTL, heartbeat, tool snapshot sync) and POST /chat calling runRemoteControlWorkflow from @ain-framework/ain-agent-sdk. This is the server-side agent runner.
- ltbot-server/routes/chat.ts: Redis-backed chat session service (getChatService): createSession, getSessionDetail, saveMessages, updateSession, deleteSession, batchDelete. This is the memory/persistence layer.
- ltbot-server/routes/agency.ts: todo CRUD over redis-om (agencyRepository). Backs the todo tools.
- ltbot-server/db/chatService.ts + redis.ts: Redis OM repositories and chat persistence.
- doc-mcp/src/server.ts: FeishuMcpServer class wrapping @modelcontextprotocol/sdk McpServer with Stdio + SSE transports, registerTools() pattern, logging via server.sendLoggingMessage. The canonical MCP teaching artifact.

## 2. Chapter -> project mapping

| Ch | Topic (Python) | kimsweb-front TS counterpart |
|----|----------------|------------------------------|
| 0 | Course overview / env | pnpm workspace setup; API keys already in env vars |
| 1 | First agent / ReAct | ltbot/src/mcp/index.ts toolRegistry + executeToolCall; build the missing LLM loop in ltbot-server |
| 2 | Components (planner/memory/tools) | ChatBot component + chatService (memory) + toolRegistry (tools) |
| 3 | Agent types (ReAct/Plan-Execute/Reflexion) | hand-roll in ltbot-server over the same tool layer |
| 4 | Frameworks (LangChain/LangGraph) | @ain-framework/ain-agent-sdk runRemoteControlWorkflow; state machine optional via hand-roll or XState |
| 5 | Multi-agent | crewAI-style orchestration on top of ain-agent-sdk |
| 6 | Evaluation | add a test harness in ltbot-server; LLM-as-judge route |
| 7 | Interview prep | stage-end design questions in this skill |
| 8 | Claude Code architecture | reverse-engineer patterns; no direct project asset |
| 9 | RAG deepdive | Redis VSS (redis-om supports vector) + embedding route in ltbot-server |
| 10 | MCP protocol | doc-mcp/src/server.ts (server) + webMcp.ts (browser) |
| 11 | Tool calling internals | extend toolRegistry with strict zod schemas; OpenAI vs Anthropic shapes |
| 12 | Production infra | apply to ltbot-server harness |
| 13 | Service (FastAPI/SSE/WebSocket) | ltbot-server Express + SSE in remote.ts |
| 14 | Persistence (SQLite 5-table) | Redis + redis-om schema in chatService/agency |
| 15 | A2A protocol | multi-agent on ltbot-server |
| 16 | MemGPT/Letta memory | extend chatService into Core Memory blocks |
| 17 | Computer use | out of scope unless user wants; screenshot-action loop |
| 18 | Security/guardrails | toolRegistry permission/riskLevel already present in webMcp.ts; extend |
| 19 | Workflow patterns (7) | hand-roll Reflection/Routing/Orchestrator-Worker |
| 20 | Context engineering | prompt + context budget in ltbot-server runner |
| 21 | Streaming architecture | SSE + backpressure in remote.ts |
| 22 | DSPy | no TS equivalent; treat conceptually or script via Python helper |
| 23 | Code agent architecture | conceptual + optional practice |
| 24 | Observability | add tracing span tree; LangFuse self-host |
| 25 | Vector DB selection | Redis VSS; compare with Chroma/Qdrant conceptually |
| 26 | Model routing | add a router in ltbot-server |
| 27 | Prompt engineering | system prompt template for the todo agent |
| 28 | Cache/token optimization | semantic cache in Redis |
| 29 | Multimodal | extend chat to image inputs |
| 30 | Reliability | circuit breaker/backoff/idempotency around tool calls |
| 31 | Benchmarks | conceptual; tau-bench style local eval |
| 32 | Self-improving | bad-case collection -> prompt rewrite loop |
| 33 | Prompt caching | Anthropic cache control on system prompt |
| 34 | Fine-tune for function calling | conceptual; data prep only |
| 35 | Data flywheel | log interactions -> bad cases -> auto-improve |
| 36 | Defense in depth | canary tokens, layered isolation, behavior sandbox |

## 3. Python -> TS dependency map

| Python | TypeScript (use this) |
|--------|------------------------|
| openai SDK / anthropic SDK | @ain-framework/ain-agent-sdk (runRemoteControlWorkflow) or direct fetch to model API |
| pydantic | zod |
| FastAPI | express 5 |
| SQLite | Redis + redis-om |
| mcp python sdk | @modelcontextprotocol/sdk |
| LangChain/LangGraph | not used; map concepts onto ain-agent-sdk + hand-rolled loops |
| Chroma/Pinecone | Redis VSS |
| SSE (sse-starlette) | @modelcontextprotocol/sdk SSEServerTransport + express |
| logging/structlog | console + server.sendLoggingMessage (see doc-mcp) |

## 4. Splitting rules (server vs browser vs transport)

When a Python single-file example must be translated, place each piece:

- LLM decision loop, tool execution, persistence, RAG, tracing, security enforcement: SERVER (ltbot-server).
- Tool definitions that act on the page/DOM, Web MCP server, ChatBot UI rendering: BROWSER (ltbot).
- Cross-boundary: SSE (streaming tokens/tool events), MCP (tool discovery + invocation), HTTP REST (sessions, CRUD).
- Tool schema definitions can live in ltbot/src/mcp/index.ts (browser-side tools) AND/OR be registered on the server; keep the toolRegistry/getToolDefinitions/executeToolCall shape consistent with the existing pattern.
- Memory/session: reuse chatService (Redis). Do not introduce SQLite.

## 5. Chapter TS teaching-file location (authoritative)

All chapter-adapted TS teaching/demo files go to `packages/ltbot/src/hooks/mockAgent/` (the folder that already holds firstAgent.ts for Ch1 and ch02_components.ts for Ch2). This overrides the server/browser splitting rules for TEACHING/DEMO code: even when the Python original is a server-side loop, the teaching TS file is a self-contained, importable module in mockAgent that matches firstAgent.ts conventions (export-style, getConfig() via import.meta.env + VITE_DEEPSEEK_*, main() entry). Production code adapted for the real app still follows the splitting rules in section 4. Do not output teaching files to ltbot-server/agent-learn.
