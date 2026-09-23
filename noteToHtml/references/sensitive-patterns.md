# Sensitive Information Patterns — 敏感信息匹配模式

## 检测原则

在将笔记转换为 HTML 页面时，自动检测以下模式并将匹配的值替换为 `***`。

## 1. 关键字段名（字段名 + 值）

### 认证相关
| 模式 | 说明 | 示例 |
| --- | --- | --- |
| `password` | 密码字段 | `password: mySecret123` → `password: ***` |
| `passwd` | 密码变体 | 同上 |
| `pwd` | 简写密码 | 同上 |
| `pass` | 通用密码 | 同上 |
| `secret` | 密钥/密文 | `secret: abc123` → `secret: ***` |
| `api_secret` | API 密钥 | 同上 |
| `app_secret` | 应用密钥 | 同上 |

### Token / Key 相关
| 模式 | 说明 | 示例 |
| --- | --- | --- |
| `api_key` | API 密钥 | `api_key: sk-xxx` → `api_key: ***` |
| `apikey` | 无下划线变体 | 同上 |
| `access_key` | 访问密钥 | 同上 |
| `access_token` | 访问令牌 | `token: eyJ...` → `token: ***` |
| `auth_token` | 认证令牌 | 同上 |
| `refresh_token` | 刷新令牌 | 同上 |
| `bearer_token` | Bearer 令牌 | 同上 |
| `private_key` | 私钥内容 | 多行替换为 `***` |
| `privatekey` | 无下划线变体 | 同上 |

### 凭证相关
| 模式 | 说明 | 示例 |
| --- | --- | --- |
| `credential` | 凭证对象 | 整个值替换 |
| `credentials` | 复数形式 | 同上 |
| `cert` | 证书内容 | 同上 |
| `certificate` | 完整证书 | 同上 |

## 2. 连接字符串中的凭证

### 数据库 URL
```
postgresql://user:password@host:5432/db
mysql://user:password@host:3306/db
mongodb://user:password@host:27017/db
redis://:password@host:6379
```
→ 替换为：`<protocol://***:***@host:port/db>`

### 其他连接字符串
- AWS Access Key 格式：`AKIA[0-9A-Z]{16}` → `***`
- JWT Token：`eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+` → `***`
- SSH 私钥标记：`BEGIN.*PRIVATE KEY` 及后续行 → `***`
- API Key 前缀：
  - `sk-` 开头（OpenAI 风格）
  - `ghp_` 开头（GitHub PAT）
  - `xoxb-` 开头（Slack Bot）
  - `AIza` 开头（Google API）

## 3. 特殊格式检测

### IP 地址 + 端口组合（仅当与认证上下文关联时）
- 不单独脱敏 IP 地址（可能是示例服务器地址）
- 但如果出现在 `user:pass@ip:port` 格式中，脱敏用户名和密码部分

### 环境变量赋值
```bash
export DB_PASSWORD=superSecret
# → export DB_PASSWORD=***
```

### JSON/YAML 配置中的敏感字段
```json
{
  "database": {
    "password": "myPassword"
  }
}
# → password 字段值变为 ***
```

## 4. 脱敏规则汇总

1. **字段名匹配**：上述关键字段名后的 `:` 或 `=` 后面的值
2. **值格式匹配**：特定前缀或格式的字符串
3. **上下文感知**：仅在配置、代码、命令等上下文中检测；普通文本中的 "password" 一词不触发
4. **保留长度提示**（可选）：对于需要确认长度的场景，可显示 `*** (length: N)`
5. **多行值**：私钥、证书等多行内容整体替换为单个 `***`

## 误判防护

以下情况**不**应触发脱敏：
- 文档中解释"什么是密码"的教学文本
- 示例值如 `password: your_password_here` 或 `changeme`
- URL 中的查询参数（非认证参数）
- 公开的演示账号/测试数据
- Markdown/文档中的占位符说明文字
