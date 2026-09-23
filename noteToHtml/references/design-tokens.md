# Design Tokens — 笔记转 HTML 设计系统

## 颜色系统

| Token | Value | Usage |
| --- | --- | --- |
| `--accent` | `#2496ED` | 主色调（Docker 蓝），用于链接、强调、边框 |
| `--accent-soft` | `rgba(36,150,237,0.08)` | 轻量强调背景 |
| `--accent-hover` | `#1a7bc4` | 悬停态主色 |
| `--bg` | `#f5f7fa` | 页面背景（暖白） |
| `--surface` | `#ffffff` | 卡片/容器表面 |
| `--fg` | `#1a1d23` | 主要文字色 |
| `--muted` | `#6b7280` | 次要文字/说明文字 |
| `--border` | `#e2e5ea` | 边框/分割线 |
| `--code-bg` | `#0d1117` | 代码块背景（深色） |
| `--code-fg` | `#c9d1d9` | 代码文字颜色 |
| `--code-hl` | `#58a6ff` | 代码高亮/内联代码 |
| `--success` | `#10b981` | 成功/解决方案提示 |
| `--warning` | `#f59e0b` | 警告/问题提示 |
| `--danger` | `#ef4444` | 错误/危险提示 |

## 字体

| Role | Font Family | Fallback | Size |
| --- | --- | --- | --- |
| Display (标题) | Space Grotesk | Noto Sans SC, system-ui, sans-serif | clamp(32px, 4.5vw, 52px) for h1 |
| Body (正文) | Noto Sans SC | Space Grotesk, system-ui, sans-serif | 16px base |
| Code (代码) | JetBrains Mono Variable | SFMono-Regular, Consolas, monospace | 13.5px in blocks, 0.88em inline |
| Meta (元信息) | inherit | — | 13px |

### 字号层级
- `--fs-h1`: `clamp(32px, 4.5vw, 52px)`
- `--fs-h2`: `clamp(24px, 3vw, 34px)`
- `--fs-h3`: `20px`
- `--fs-body`: `16px`
- `--fs-small`: `14px`
- `--fs-meta`: `13px`

## 布局

| Property | Value | Notes |
| --- | --- | --- |
| Container max-width | `1100px` | 主内容区域最大宽度 |
| Gutter | `24px` | 左右内边距 |
| TOC width | `240px` | 左侧导航栏宽度 |
| Grid gap | `40px` | TOC 与主内容间距 |
| Section margin-bottom | `48px` | 章节间距 |
| Border radius | `10px` | 默认圆角 |
| Border radius-lg | `16px` | 大卡片圆角 |

### 响应式断点
- **Desktop**: > 900px — 显示左侧 TOC + 主内容双栏布局
- **Mobile**: ≤ 900px — 隐藏 TOC，单栏布局，减小间距

## 组件样式规范

### Hero 区域
- 标签：圆角药丸形 (`border-radius: 20px`)，小字号 + 等宽字体
- H1：大标题，字重 700，负字距 (-0.02em)
- Lead：副标题，次要文字色，最大 60ch 宽度

### 数据表格
- 头部：浅灰背景 (#f0f4f8)，全大写字母，细字重
- 行悬停：轻量强调背景
- 无外框线，仅行间分割

### 代码块
- 深色终端风格背景 (#161b22 header + #0d1117 body)
- 三点指示器（红黄绿）模拟终端窗口
- 语言标签在右上角，等宽字体小写
- 内联代码：深色背景 + 蓝色文字

### 提示框 (Callout)
- 四种类型：info(蓝)、success(绿)、warning(橙)、danger(红)
- 左侧 3px 彩色边条
- 图标 + 内容双栏布局

### 问题卡片
- 白底卡片，大圆角
- 标题带徽章标签
- 解决方案用绿色前缀标识

### 特性网格
- 自适应列数 (minmax(220px, 1fr))
- 悬停上浮效果 (+2px translateY)
- 图标圆形背景容器
