# 每日学习计划详表（chat_sdk_happy_day）

每天 = 学习目标 + 知识点清单 + 要实现的产出 + 实操任务 + 面试问答要点。
按「每天实现节奏四步」推进：概念(配Mermaid)→实现(自测)→实操→检查点。
自适应：一天可推进多天，也可一天不推进，按用户精力，不按日历。

---

## Day 1 — 类型契约层 + Provider 骨架

**学习目标**：把「SDK 只渲染、不持真相」的合同用类型钉死，并建出可插拔 runtime 的骨架。

**知识点清单**：
- UIMessage 结构（对齐 AI SDK 的 UIMessage：id/role/parts[]），为什么用 parts 而非 content 字符串。
- Compound Component 模式：容器+子组件通过上下文协作，而非 props 逐层透传。
- provide/inject vs React Context：Vue3 的依赖注入，响应式 + 类型安全注入键。
- peerDependencies：vue 放 peer 而非 dependencies，避免业务系统装两份 vue。
- AG-UI 事件协议概览：~16 类事件（text-delta/tool-call-start/tool-call-result/reasoning-delta/done/error 等），传输层解耦。

**实现产出**：
- `src/types.ts`：UIMessage、ChatStatus、ChatStreamEvent（对齐 AG-UI）、ChatRuntime 接口（可插拔）。
- `src/components/ChatProvider.ts`：provide ChatRuntime，不持 messages。

**实操任务**：写 types + Provider，`pnpm --filter @business-template/ai-chat-sdk typecheck` 通过。

**面试问答要点**：
- Q: 何为受控组件 SDK？ A: 组件从 props 读数据、emit 事件、不持真相；数据真相在调用方。
- Q: 为什么用 provide/inject 不用 props 透传？ A: 避免 prop drilling，深层子组件直接取上下文；Compound 模式必备。

---

## Day 2 — 核心展示组件

**学习目标**：把消息数组渲染成对话界面，含 Markdown + 代码高亮。

**知识点清单**：
- 受控 vs 非受控组件，defineModel() 双向绑定。
- v-html 的 XSS 风险与 DOMPurify 防范（白名单标签/属性）。
- markdown-it 流式增量解析：部分 Markdown 也能渲染（未闭合代码块的处理）。
- 消息 part 模型：text part / reasoning part / tool-call part / source part 各自的渲染。

**实现产出**：MessageList / Message / MessageContent / Markdown 渲染组件。

**实操任务**：喂 mock messages 数组，渲染出用户/助手气泡 + Markdown + 代码块。

**面试问答要点**：
- Q: v-html 怎么防 XSS？ A: DOMPurify 清洗 + 禁用 raw html + 白名单。
- Q: 流式 Markdown 怎么不卡顿？ A: 增量解析 + requestAnimationFrame 节流 + 避免每次全量重渲染。

---

## Day 3 — 输入区 + 自动滚动

**学习目标**：做输入框与流式自动滚动（含中文输入法兼容、停止生成）。

**知识点清单**：
- IME 输入法兼容：compositionstart/end，Enter 在拼音候选时不提交。
- Enter 提交 / Shift+Enter 换行。
- AbortController：中断 fetch/流式，abort 后保留已输出内容。
- 智能滚动（useStickToBottom）：用户在底部时跟随，上滑看历史时暂停，回到底部恢复。

**实现产出**：PromptInput 组件、useStickToBottom composable。

**实操任务**：输入提交 + 停止按钮 + 长流式内容自动跟随滚动 + 上滑暂停。

**面试问答要点**：
- Q: AbortController 怎么中断流式？ A: 传 signal 给 fetch，abort 触发，catch AbortError 保留半截。
- Q: 智能滚动怎么判断在底部？ A: scrollTop + clientHeight ≈ scrollHeight（带阈值），或 IntersectionObserver 监听底部哨兵。

---

## Day 4 — 流式协议适配器

**学习目标**：把 AG-UI 事件流解析成渲染器能消费的更新，含打字机效果。

**知识点清单**：
- SSE 协议与帧解析（data: 行、event: 行、id:、重连）。
- ReadableStream / 异步迭代，背压概念。
- AG-UI data-part 事件路由：把 text-delta 累加到对应 message part。
- 打字机缓冲：用队列 + rAF 逐字 flush，平滑而非一次性 dump。

**实现产出**：SSE 解析器（纯函数）、打字机 composable、事件→messages 更新映射。

**实操任务**：用 mock SSE 流跑通「逐字渲染 + 工具调用事件 + done 收尾」。

**面试问答要点**：
- Q: SSE vs WebSocket 取舍？ A: SSE 单向服务器推、自动重连、HTTP 友好；WS 双向但更重。对话流式默认 SSE。
- Q: 流式渲染如何避免重渲染卡顿？ A: 增量更新单条 message、rAF 节流、keyed 列表。

---

## Day 5 — Agent 特性

**学习目标**：做 Agent 区别于聊天机器人的可视化：推理链、工具调用、确认、引用。

**知识点清单**：
- CoT/Reasoning 可视化：可折叠灰色面板，展示思考过程。
- 工具调用卡片（Tool Call Widget）：状态机（pending→running→completed/failed）。
- human-in-the-loop 确认面板：emit confirm/cancel，阻塞工具执行。
- 引用锚点 Sources：[1]/[文件名] 角标，点击定位。

**实现产出**：Reasoning / Tool / Confirmation / Sources 组件。

**实操任务**：渲染一轮完整 agent 回复「推理→工具调用→确认→引用→最终回答」。

**面试问答要点**：
- Q: Agent 与聊天机器人的前端分水岭？ A: 状态管理（记忆/上下文）、原子化操作（打断/重试）、可观测性（推理/工具可视化）。
- Q: human-in-the-loop 怎么设计？ A: 工具执行前 emit confirmation 事件，业务系统/用户 confirm 后才继续，SDK 只渲染状态。

---

## Day 6 — 上下文与记忆

**学习目标**：做上下文窗口感知、草稿、重试分支等数据/记忆相关特性。

**知识点清单**：
- 上下文窗口 Token 指示器：实时消耗 + 接近阈值预警。
- localStorage 草稿箱：自动保存输入，关闭恢复。
- 重试/重新生成：基于历史消息分支（对话树修剪，遗忘编辑点之后回复）。
- 断网重连/断点续传：流式中断后「点击继续」而非清空。

**实现产出**：Token 指示器、草稿 composable、重试/重新生成。

**实操任务**：草稿关闭恢复 + Token 预警 + 重新生成分支。

**面试问答要点**：
- Q: 前端如何做对话树分支？ A: 每条消息存 parentId，编辑/重试时复制前置上下文生成新分支，旧分支保留。
- Q: 断网重连的断点续传怎么设计？ A: 记录已接收 offset，重连带 Last-Event-ID 续传，保留已渲染内容。

---

## Day 7 — 会话管理（左侧列表 + CRUD + 历史）

**学习目标**：做出 DeepSeek 左侧的会话列表，支持新建、重命名、删除、切换，刷新后历史恢复。

**知识点清单**：
- 会话/消息两层数据模型：session 只存元信息（id/title/createdAt/updatedAt），消息数组仍由 ChatRuntime 持有，session 通过 id 关联。
- 会话 CRUD 状态机：create → active、rename（双击进入编辑态）、delete（含删除当前会话的自动切换）、switch（切换 activeSessionId）。
- 历史记录持久化：localStorage 存会话元信息，消息历史由业务系统按 sessionId 加载。
- 边界处理：删除正在流式的会话要先 stop；重命名空标题回退原名。

**实现产出**：
- `src/types.ts`：ChatSession 类型（id/title/createdAt/updatedAt）。
- `src/composables/useChatSessions.ts`：sessions ref + activeSessionId + create/rename/delete/switch，localStorage 持久化。
- `src/components/SessionList.ts`：左侧会话栏（新建按钮、会话项、hover 操作：重命名/删除）。

**实操任务**：demo 页左侧接入会话列表，新建/重命名/删除/切换，刷新后恢复；删除当前会话自动切到最近一条。

**面试问答要点**：
- Q: 会话层和消息层怎么解耦？ A: 会话只存元信息 + 消息引用；消息数组归 ChatRuntime 持有，切换会话时业务系统替换 runtime 的消息数组，SDK 不碰会话状态。
- Q: 删除正在流式的会话怎么处理？ A: 先调 runtime.stop() 中止流，再删除会话；删除当前会话时把 activeSessionId 切到相邻会话并加载其消息。

---

## Day 8 — 附件上传与渲染

**学习目标**：先支持 txt、图片、PDF 三类附件的上传与消息内渲染，参考 DeepSeek 的附件体验。

**知识点清单**：
- FileUIPart 渲染：AI SDK 类型已对齐，缺的是 FilePart 展示组件（文件名/类型/大小/进度/错误）。
- 上传状态机：uploading → uploaded → error，支持取消与重试。
- 文件读取：FileReader 读 txt 文本预览；URL.createObjectURL 生成图片/PDF 的 blob URL 预览；用后 revokeObjectURL 释放内存。
- 输入区附件管理：待发送附件列表（可移除），发送时并入 user 消息 parts。

**实现产出**：
- `src/components/AttachmentPicker.ts`：输入区附件按钮 + 拖拽/点击选择 + 待发送附件行。
- `src/components/FilePart.ts`：消息内渲染 txt（文本卡片）/ image（缩略图+点击放大）/ pdf（iframe/blob 预览）。
- `src/composables/useAttachment.ts`：文件 → FileUIPart 的转换 + 上传状态机。

**实操任务**：demo 上传 txt/图片/PDF，消息内正常渲染；模拟上传失败可重试；切换会话后附件不残留。

**面试问答要点**：
- Q: 附件在 UIMessage 里怎么表示？ A: FileUIPart（type: file + mimeType + filename + data）对齐 AI SDK；上传中/失败态由本地状态机补充，成功后并入 parts。
- Q: 前端预览 PDF/图片的内存问题？ A: URL.createObjectURL 生成 blob URL，组件卸载/替换时 revokeObjectURL，避免内存泄漏。
- Q: 大文件上传怎么做？ A: SDK 只做展示与本地预览；真实上传走业务系统（分片/断点/OSS 直传），SDK 保持不持真相。

---

## Day 9 — 代码块增强（高亮 + 复制 + 数学公式）

**学习目标**：让消息里的代码块和数学公式达到 DeepSeek 的观感：语言高亮、一键复制、LaTeX 公式渲染。

**知识点清单**：
- markdown-it highlight 钩子：renderer 里对 ```lang 代码块调用高亮库，输出带 class 的 HTML。
- 代码高亮：接入 highlight.js（项目已有 markdown-it，评估复用；注意流式未闭合代码块的增量渲染）。
- 复制到剪贴板：navigator.clipboard.writeText 主路径 + document.execCommand('copy') 降级 + 复制成功态反馈。
- 数学公式：KaTeX + markdown-it-katex，$...$ 行内、$$...$$ 块级；CSS 注入 KaTeX 字体。
- 流式渲染坑：代码块未闭合时高亮库可能报错，需 try/catch 兜底或延迟到 done 后再高亮。

**实现产出**：
- `src/components/CodeBlock.ts`：代码块容器（语言标签 + 复制按钮 + 高亮内容）。
- `src/utils/markdown.ts`：renderMarkdown 接入 highlight.js + KaTeX。
- 依赖：highlight.js、katex（引入前说明理由）。

**实操任务**：demo 渲染 TS 代码块 + 数学公式（如 E=mc²、$$\int_0^1 x^2 dx$$），复制按钮可用；流式过程中代码块不闪断。

**面试问答要点**：
- Q: 复制到剪贴板的兼容方案？ A: 优先 navigator.clipboard（需 HTTPS/安全上下文），失败降级 execCommand('copy')，再失败提示手动复制。
- Q: KaTeX 接入的安全考虑？ A: KaTeX 有严格白名单和自校验，比直接 v-html 安全；仍需 DOMPurify 清洗整个 markdown 输出。
- Q: 流式代码块为什么容易闪？ A: 未闭合 ``` 时 markdown-it 渲染和代码高亮行为不稳定，可等代码块闭合后再高亮，或对不完整块降级为纯文本。

---

## Day 10 — 消息操作区（复制/编辑/删除/点赞/点踩/分享）

**学习目标**：每条消息底部挂操作栏（参考 DeepSeek）：复制、编辑、删除、点赞/点踩、分享。

**知识点清单**：
- hover 操作栏：桌面 hover 显示，移动端常显（触控友好）。
- 复制：只复制 text part 的纯文本。
- 编辑：把 user 消息切到编辑态 → 提交后改文本并砍掉其之后的消息（对话树修剪）→ 重新生成。
- 删除：单条消息删除 + 边界（删到空列表回到空态）。
- 点赞/点踩：feedback 事件，SDK 只 emit 状态变化，不持真相；业务系统持久化。
- 分享：生成会话/消息锚点链接，业务系统侧实现（SDK 提供 emit）。

**实现产出**：
- `src/components/MessageActions.ts`：操作栏（复制/编辑/删除/赞/踩/分享），hover/常显两态。
- `ChatRuntime` 扩展：editMessage(messageId, text)、deleteMessage(messageId)、feedback(messageId, kind) 可选回调。
- Message.ts 接入操作栏 + 编辑态输入。

**实操任务**：demo 每条消息 hover 出操作栏；编辑 user 消息后重新生成；点赞/点踩有即时状态；删除消息列表正常。

**面试问答要点**：
- Q: 编辑消息和 Day6 的 regenerate 是什么关系？ A: regenerate 只重跑最后一条；编辑是「改内容 + 剪掉该消息之后的回复 + 重新生成」，是对话树修剪的完整版。
- Q: 点赞/点踩数据归谁？ A: 归业务系统。SDK 通过 runtime.feedback 回调上报，不自己存，保持「只渲染不持真相」。
- Q: 分享链接怎么设计？ A: 会话 id + 消息 id 作为锚点（如 /chat/:sessionId#msg-xxx），SDK 只负责触发分享事件，链接生成与权限在业务系统。

---

## Day 11 — 打包发布 + 集成验证

**学习目标**：把 SDK 打成可发布的产物，在示例 app 接入验证。

**知识点清单**：
- vite library mode：lib 入口、formats(es/umd)、externals(vue)。
- dts 类型产物：vue-tsc 或 vite-plugin-dts。
- tree-shaking：sideEffects:false、ESM、按需引入。
- CSS 隔离：前缀 BEM / CSS 变量主题。
- peerDependencies 意义：vue 由消费方提供，不重复安装。

**实现产出**：vite lib 构建配置 + dist(es+dts+css) + 在 apps/vue3-admin 接入。

**实操任务**：构建出产物，vue3-admin 装上依赖、塞一个 mock runtime、能渲染对话。

**面试问答要点**：
- Q: 如何设计可 tree-shake 的 SDK？ A: ESM + 纯函数拆分 + sideEffects:false + externals 重大依赖。
- Q: peerDependencies 的意义？ A: 声明宿主依赖（如 vue），由消费方提供，避免多实例冲突。

---

## 每日总结文档规格（重申）

- 路径：D:\kimsweb\business-template\agent-docs\ai-chat-sdk\
- 命名：DayN_主题_MMDD.html（如 Day1_类型契约与Provider_0807.html）。
- 内容：①今天实现了什么 ②3-5个知识点（配Mermaid） ③3-5条面试问答 ④代码示例（落在项目上）。
- 自包含 HTML：内联 CSS + Mermaid CDN，浏览器打开即可看。
- 总计划 00_学习总计划.html 跟随路线变化更新。