# Telegram 订阅信息查询机器人 / Telegram Subscription Info Bot

[English](#english) | [中文](#中文)

---

## 中文

### 📖 简介

这是一个基于 Python 的 Telegram 机器人，用于查询和显示机场订阅信息。支持多种订阅格式（Clash/Surge/V2Ray/SS），能够解析流量使用情况、到期时间、节点数量等详细信息。

### ✨ 功能特性

- 🔍 **多格式支持**: 自动识别 Clash YAML、V2Ray/SS Base64 等订阅格式
- 📊 **流量统计**: 显示总流量、已用流量、剩余流量及使用百分比
- 📈 **可视化进度条**: 直观展示流量使用情况
- ⏰ **到期提醒**: 显示订阅到期时间
- 🌐 **节点信息**: 统计节点数量和类型
- 📄 **导出功能**: 支持将查询结果导出为 TXT 文件
- 🔄 **批量查询**: 一次可查询多个订阅链接
- 🏷️ **机场识别**: 通过远程映射文件自动识别机场名称

### 📋 系统要求

- Python 3.7+
- Telegram Bot Token

### 🚀 快速开始

#### 1. 安装依赖

```bash
pip install python-telegram-bot httpx pyyaml beautifulsoup4 python-dateutil
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

#### 2. 配置机器人

编辑 `subinfo.py` 文件，替换以下内容：

```python
TOKEN = "你的_TELEGRAM_BOT_TOKEN"  # 替换为你的 Bot Token
```

**获取 Bot Token:**
1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人
3. 按照提示完成创建，获取 Token

#### 3. 运行机器人

```bash
python subinfo.py
```

### 📱 使用方法

#### 基本命令

- `/subinfo [订阅链接]` - 查询订阅信息
- `/subinfo txt [订阅链接]` - 查询并导出为 TXT 文件
- `/cha [订阅链接]` - 兼容旧版命令

#### 使用示例

**方式 1: 直接发送链接**
```
/subinfo https://example.com/sub?token=xxx
```

**方式 2: 回复包含链接的消息**
```
[回复一条包含订阅链接的消息]
/subinfo
```

**方式 3: 导出为文件**
```
/subinfo txt https://example.com/sub?token=xxx
```

**方式 4: 批量查询**
```
/subinfo https://sub1.com/xxx https://sub2.com/xxx
```

### 📊 输出示例

```
📄 机场名称: `示例机场`
🏷️ 订阅链接: `https://example.com/sub?token=xxx`
📊 流量信息:
预览: `[████████░░░░░░░░░░░░] 40.5%`
总流量: `100.00 GB`
已使用: `40.50 GB` (↑5.20 GB ↓35.30 GB)
剩余量: `59.50 GB`
⏰ 到期时间: `2025-01-31`
🌐 节点信息: `50个节点 (Clash/Surge)`
```

### ⚙️ 自定义配置

#### 修改机场名称映射

编辑远程映射文件 URL：
```python
REMOTE_MAPPINGS_URL = "https://your-url.com/mappings.txt"
```

映射文件格式：
```
example.com=示例机场
another-sub.com=另一个机场
```

#### 添加更多地区规则

在 `REGION_RULES` 中添加：
```python
REGION_RULES = [
    ('香港', ['香港', 'hong kong', 'hk']),
    ('新地区', ['关键词1', '关键词2']),
    # ...
]
```

### 🔧 依赖项

```txt
python-telegram-bot>=20.0
httpx>=0.24.0
pyyaml>=6.0
beautifulsoup4>=4.12.0
python-dateutil>=2.8.0
```

### 📝 注意事项

- 机器人需要持续运行才能响应命令
- 建议使用进程管理工具（如 systemd, supervisor）保持运行
- 订阅链接必须包含 `subscription-userinfo` Header
- 部分机场可能有访问频率限制

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 📄 许可证

MIT License

---

## English

### 📖 Introduction

A Python-based Telegram bot for querying and displaying airport subscription information. Supports multiple subscription formats (Clash/Surge/V2Ray/SS) and can parse detailed information including traffic usage, expiration time, and node count.

### ✨ Features

- 🔍 **Multi-format Support**: Automatically recognizes Clash YAML, V2Ray/SS Base64, and other subscription formats
- 📊 **Traffic Statistics**: Displays total traffic, used traffic, remaining traffic, and usage percentage
- 📈 **Visual Progress Bar**: Intuitive display of traffic usage
- ⏰ **Expiration Reminder**: Shows subscription expiration date
- 🌐 **Node Information**: Counts nodes and identifies types
- 📄 **Export Function**: Export query results as TXT files
- 🔄 **Batch Query**: Query multiple subscription links at once
- 🏷️ **Airport Recognition**: Automatically identifies airport names via remote mapping file

### 📋 Requirements

- Python 3.7+
- Telegram Bot Token

### 🚀 Quick Start

#### 1. Install Dependencies

```bash
pip install python-telegram-bot httpx pyyaml beautifulsoup4 python-dateutil
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

#### 2. Configure Bot

Edit `subinfo.py` and replace:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Replace with your Bot Token
```

**Getting Bot Token:**
1. Find [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` to create a new bot
3. Follow the prompts to complete creation and get your Token

#### 3. Run Bot

```bash
python subinfo.py
```

### 📱 Usage

#### Basic Commands

- `/subinfo [subscription_link]` - Query subscription info
- `/subinfo txt [subscription_link]` - Query and export as TXT file
- `/cha [subscription_link]` - Legacy command compatibility

#### Usage Examples

**Method 1: Direct Link**
```
/subinfo https://example.com/sub?token=xxx
```

**Method 2: Reply to Message**
```
[Reply to a message containing subscription link]
/subinfo
```

**Method 3: Export as File**
```
/subinfo txt https://example.com/sub?token=xxx
```

**Method 4: Batch Query**
```
/subinfo https://sub1.com/xxx https://sub2.com/xxx
```

### 📊 Output Example

```
📄 Airport Name: `Example Airport`
🏷️ Subscription Link: `https://example.com/sub?token=xxx`
📊 Traffic Information:
Preview: `[████████░░░░░░░░░░░░] 40.5%`
Total Traffic: `100.00 GB`
Used: `40.50 GB` (↑5.20 GB ↓35.30 GB)
Remaining: `59.50 GB`
⏰ Expiration Date: `2025-01-31`
🌐 Node Information: `50 nodes (Clash/Surge)`
```

### ⚙️ Custom Configuration

#### Modify Airport Name Mapping

Edit remote mapping file URL:
```python
REMOTE_MAPPINGS_URL = "https://your-url.com/mappings.txt"
```

Mapping file format:
```
example.com=Exampl