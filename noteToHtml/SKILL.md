---
name: noteToHtml
title: 笔记转 HTML 页面
version: 1
description: 将笔记/文档内容转换为高质量、带左侧导航栏的 HTML 页面，自动脱敏敏感信息（密码/密钥显示为***）
when_to_use: 当用户需要将笔记、技术文档、教程、学习笔记等内容转换为美观的 HTML 页面时使用。适用于知识库整理、技术文档发布、学习笔记分享等场景。
---

# 笔记转 HTML 页面

## When to use

使用此技能当：
- 用户需要将笔记内容转换为 HTML 页面
- 用户需要将技术文档、教程转换为可发布的网页
- 用户需要带左侧目录导航的响应式 HTML 文档
- 用户需要自动脱敏敏感信息（密码、密钥、token 等）

## Runtime requirements

- Browser login required: no
- Sandbox required: yes（用于生成 HTML 文件）
- MCP required: no
- Page script required: no
- User local folder required: optional

## Capability routing

1. **内容收集阶段**：使用浏览器工具读取用户提供的笔记内容（截图、文档、网页等）
2. **内容处理阶段**：使用 E2B sandbox 进行敏感信息检测和处理
3. **HTML 生成阶段**：使用 E2B sandbox 生成完整的 HTML 文件
4. **质量检查阶段**：运行 HTML 验证脚本确保输出质量
5. **交付阶段**：返回生成的 HTML 文件路径

## Workflow

### 1. 理解内容结构
- 读取用户提供的笔记源（截图、文档、文本等）
- 识别文档的章节结构、标题层级
- 提取代码块、表格、列表等特殊内容
- 标记可能需要脱敏的敏感信息区域

### 2. 敏感信息检测与脱敏
运行 `/mnt/work/.skills/<skill_id>/scripts/sanitize_secrets.py` 检测并脱敏：
- 密码字段（password, passwd, pwd 等）
- 密钥（secret, api_key, token, access_token 等）
- 数据库连接字符串中的凭证
- 私钥内容
- 其他敏感配置项

脱敏规则：将所有敏感值替换为 `***`

### 3. 生成 HTML 页面
使用模板 `/mnt/work/.skills/<skill_id>/templates/doc_template.html` 生成 HTML：
- 应用设计系统（颜色、字体、间距）
- 构建左侧 TOC 导航栏
- 插入处理后的内容
- 添加代码高亮样式
- 确保响应式布局

### 4. 质量检查
运行 `/mnt/work/.skills/<skill_id>/scripts/check_html.py` 验证：
- HTML 结构完整性
- 无临时服务器引用（localhost, 127.0.0.1 等）
- 无 file:// 或 blob: 引用
- 无模板标记残留
- 敏感信息已正确脱敏

### 5. 交付
- 保存最终 HTML 到 `/mnt/cos/artifacts/<filename>.html`
- 返回文件路径和下载链接
- 说明设计特点和使用方式

## Files in this skill

| File | Purpose |
| --- | --- |
| `SKILL.md` | 技能主定义文件 |
| `templates/doc_template.html` | HTML 页面模板（包含完整样式系统） |
| `scripts/sanitize_secrets.py` | 敏感信息检测与脱敏脚本 |
| `scripts/check_html.py` | HTML 质量检查脚本 |
| `references/design-tokens.md` | 设计系统规范（颜色、字体、间距等） |
| `references/sensitive-patterns.md` | 敏感信息匹配模式清单 |

## Output contract

必需输出：
- 完整的单文件 HTML（自包含 CSS，无需外部依赖）
- 文件名格式：`<日期>_<主题>.html` 或用户指定名称
- 左侧固定 TOC 导航栏（支持点击滚动）
- 响应式布局（移动端自动隐藏侧边栏）
- 敏感信息已全部脱敏（显示为 `***`）

可选输出：
- 代码块语法高亮
- 表格样式
- 引用/提示框样式
- 页脚信息

## Failure handling

### 登录失败
不适用（无需登录）

### 内容提取失败
- 如果用户提供的截图无法读取，请求用户重新提供或改用文本形式
- 如果文档结构不清晰，向用户确认章节划分

### 敏感信息误判
- 如果正常内容被错误脱敏，记录模式并向用户说明
- 允许用户在生成后手动调整

### HTML 生成失败
- 检查模板文件是否完整
- 检查 E2B sandbox 是否有足够权限写入
- 如持续失败，降级为简化版 HTML（无复杂样式）

### 质量检查失败
- 根据错误报告修复具体问题
- 如果是敏感信息漏检，更新检测模式后重新生成
- 最多重试 2 次，仍失败则向用户报告具体问题

## Design System

参考 `references/design-tokens.md`：

### 颜色
- 主色调：Docker 蓝 `#2496ED`
- 背景色：暖白 `#f5f7fa`
- 表面色：纯白 `#ffffff`
- 文字色：深灰 `#1a1d23`
- 次要文字：中灰 `#6b7280`
- 代码背景：深色 `#0d1117`
- 代码高亮：蓝色 `#58a6ff`

### 字体
- 标题：Space Grotesk + Noto Sans SC
- 正文：Noto Sans SC
- 代码：JetBrains Mono Variable

### 布局
- 左侧 TOC 宽度：240px
- 主内容最大宽度：1100px
- 响应式断点：900px（小于此值隐藏侧边栏）

## Sensitive Data Patterns

参考 `references/sensitive-patterns.md`，检测以下模式：

### 关键字段名
- password, passwd, pwd, pass
- secret, api_secret, app_secret
- key, api_key, apikey, access_key
- token, access_token, auth_token
- credential, credentials
- private_key, cert, certificate

### 连接字符串
- 数据库 URL（含用户名密码）
- Redis 连接字符串
- MongoDB 连接字符串

### 特殊模式
- AWS Access Key ID (AKIA 开头)
- JWT Token (ey 开头的 base64)
- SSH 私钥 (BEGIN RSA PRIVATE KEY)

所有匹配的值替换为 `***`
