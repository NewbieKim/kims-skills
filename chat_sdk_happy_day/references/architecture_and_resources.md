## 技术决策（2026-08-06 定）

- 数据层：引入 `@ai-sdk/vue`(4.0.55) + `ai` 核心包。类型契约对齐官方 UIMessage/data parts/ChatStatus。
- 渲染层：自建 Vue3 组件（不装 ai-elements 包，它是 React+shadcn registry 无 Vue 版；其源码作参考蓝图）。
- 样式：Tailwind CSS + CSS 变量主题。
- 响应式：支持 PC + 移动端（Tailwind 断点 + 移动端优先）。
- 引擎桥接：AG-UI 协议（LangGraph 原生）。

查证事实：ai-elements 是 Vercel 官方包（github.com/vercel/ai-elements，0.23万星，React+shadcn registry，npx 拷源码进项目，无 Vue 版）。@ai-sdk/vue 已发布(4.0.55)。
# 架构与学习资源（调研确认，2026-08-06）

## 三条确认结论

1. **事件协议 = AG-UI**（ag-ui-protocol/ag-ui，1.5 万星）：agent↔前端标准事件协议，~16 类事件，传输解耦（SSE/WS/webhook），原生支持 LangGraph。定位原话：「MCP gives agents tools · A2A allows agents to communicate · AG-UI brings agents into user-facing applications」。→ https://docs.ag-ui.com
2. **渲染解耦范本 = assistant-ui Runtime 模式**（assistant-ui/assistant-ui，1.1 万星）：AssistantRuntimeProvider(渲染) + 可插拔 runtime（useLangGraphRuntime/useDataStreamRuntime/自定义）。已支持 LangGraph/AG-UI/A2A。→ https://www.assistant-ui.com
3. **vercel/ai 原生支持 Vue**（2.6 万星，topics 含 vue）：UIMessage/ChatStatus/DefaultChatTransport/data-part 类型契约可直接复用。→ https://ai-sdk.dev

## 渲染/数据解耦铁律

SDK 组件从 props 读数据、emit 事件、不持真相。业务系统持 messages 数组 + 传输层，监听 @send/@stop/@regenerate 自己请求后端、更新自己的 messages，再把新数组传回 props。范本：ai-elements(渲染) ↔ useChat(数据)；assistant-ui Provider ↔ runtime。

## 浏览器 agent 范式（browser-use 确认）

Agent(task, llm).run() → history。四层：引擎(agent loop) / 浏览器控制(Playwright) / 观测(截图+a11y树) / 渲染(chat+步骤卡片，每步=截图缩略图+动作+结果)。Tabbit 一手资料未查到，不编。

## 学习资源（按优先级）

### P0 决定 SDK 架构（必读）
- ag-ui-protocol/ag-ui — 1.5 万星，AG-UI 协议。→ https://docs.ag-ui.com
- assistant-ui/assistant-ui — 1.1 万星，同型 React 库，逐行读。→ https://www.assistant-ui.com

### P1 渲染与流式范本
- vercel/ai — 2.6 万星，AI SDK，支持 Vue。→ https://ai-sdk.dev
- CopilotKit/CopilotKit — 3.65 万星，AG-UI 制定者。→ https://docs.copilotkit.ai

### P2 浏览器 agent
- browser-use/browser-use — 10.8 万星。→ https://docs.browser-use.com
- nanobrowser/nanobrowser — 1.35 万星，TS 写的扩展。
- steel-dev/steel-browser — 0.74 万星，浏览器 API 沙箱。

### P3 官方文档
- AG-UI 协议规范 → https://docs.ag-ui.com
- Vercel AI SDK 文档 → https://ai-sdk.dev/docs/ai-sdk-ui
- MCP 规范 → https://modelcontextprotocol.io
- LangGraph 文档 → https://langchain-ai.github.io/langgraph

### P4 补充
- mckaywrigley/chatbot-ui — 3.3 万星。
- modelcontextprotocol/ext-apps — MCP Apps 协议，嵌入业务系统的 chatbot。
- Fosowl/agenticSeek — 2.6 万星，全本地 Manus 复刻。

## 项目现状诊断（business-template）

- packages/ai-chat-sdk：在建主战场。骨架已建。
- packages/remote：反面教材（自持 messages、耦合 apiClient/web-mcp），不改它。
- packages/agent：LangGraph 引擎。缺口：remoteControl.ts 是字符串拼接非 agent loop，引擎未 emit 标准事件。
- packages/web-mcp：工具协议，设计良好。
- apps/agent-server：托管引擎、对外 SSE。
- apps/vue3-admin：示例业务系统。
