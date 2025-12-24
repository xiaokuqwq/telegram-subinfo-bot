# Telegram Subscription Info Bot

[English](#english) | [中文](#中文)

---

## English

### 📋 Overview

A Telegram bot that queries subscription information from V2Ray/Clash/Surge subscription links, including traffic usage, expiration dates, and node counts. Supports batch processing with concurrent requests.

### ✨ Features

- 🔍 **Multiple Input Methods**: Direct links, text files, or reply to messages
- ⚡ **Concurrent Processing**: Handles multiple subscriptions simultaneously
- 📊 **Detailed Statistics**: Traffic usage, remaining quota, upload/download breakdown
- 🌐 **Node Detection**: Automatically detects node count and type (Clash/V2Ray/SS)
- 📁 **Export Options**: View results in chat or export as TXT file
- 🏷️ **Custom Naming**: Supports custom airport name mappings via remote config

### 🚀 Quick Start

#### Prerequisites

- Python 3.8+
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))

#### Installation

1. Clone the repository:
```bash
git clone https://github.com/xiaokuqwq/telegram-subinfo-bot.git
cd telegram-subinfo-bot
```

2. Install dependencies:
```bash
pip install python-telegram-bot httpx pyyaml
```

3. Configure the bot:
   - Open `subinfo.py`
   - Replace `TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"` with your actual bot token

4. Run the bot:
```bash
python subinfo.py
```

### 📖 Usage

#### Commands

- `/subinfo` or `/cha` - Query subscription information

#### Usage Examples

1. **Direct link query**:
   ```
   /subinfo https://example.com/sub?token=xxx
   ```

2. **Multiple links**:
   ```
   /subinfo 
   https://sub1.com/link1
   https://sub2.com/link2
   ```

3. **Upload text file**:
   - Send a `.txt` file containing subscription links
   - Caption it with `/subinfo`

4. **Reply to message**:
   - Reply to any message containing links with `/subinfo`

5. **Export as file**:
   ```
   /subinfo txt https://example.com/sub
   ```

### 📊 Output Format

```
📄 机场: Airport Name
🏷️ 订阅: https://example.com/sub
📊 流量: [████████████░░░░░░░░] 60.5%
总计: 100.00 GB | 剩余: 39.50 GB
已用: 60.50 GB (↑5.2 GB ↓55.3 GB)
⏰ 到期: 2025-12-31
🌐 节点: 50个 (Clash/Surge)
```

### ⚙️ Configuration

#### Remote Mappings

The bot loads airport name mappings from:
```python
REMOTE_MAPPINGS_URL = "https://raw.githubusercontent.com/Hyy800/Quantumult-X/refs/heads/Nana/ymys.txt"
```

Format:
```
keyword1=Airport Name 1
keyword2=Airport Name 2
```

#### Concurrency Settings

Adjust concurrent request limit:
```python
MAX_CONCURRENT_REQUESTS = 5  # Default: 5
```

### 🛠️ Technical Details

- **Supported Formats**: Clash YAML, V2Ray/Shadowsocks Base64
- **Timeout**: 15 seconds per request
- **User-Agent**: `FlClash/v0.8.76 clash-verge`
- **Message Limit**: 4000 characters (auto-truncates)

### 📝 License

MIT License

### 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 中文

### 📋 项目简介

一个 Telegram 机器人,用于查询 V2Ray/Clash/Surge 订阅链接的流量使用情况、到期时间和节点数量。支持批量并发查询。

### ✨ 功能特点

- 🔍 **多种输入方式**: 直接发送链接、上传文本文件或回复消息
- ⚡ **并发处理**: 同时处理多个订阅链接
- 📊 **详细统计**: 流量使用、剩余额度、上传/下载分解
- 🌐 **节点检测**: 自动检测节点数量和类型 (Clash/V2Ray/SS)
- 📁 **导出选项**: 在聊天中查看或导出为 TXT 文件
- 🏷️ **自定义命名**: 支持通过远程配置自定义机场名称映射

### 🚀 快速开始

#### 环境要求

- Python 3.8+
- Telegram Bot Token (从 [@BotFather](https://t.me/botfather) 获取)

#### 安装步骤

1. 克隆仓库:
```bash
git clone https://github.com/xiaokuqwq/telegram-subinfo-bot.git
cd telegram-subinfo-bot
```

2. 安装依赖:
```bash
pip install python-telegram-bot httpx pyyaml
```

3. 配置机器人:
   - 打开 `subinfo.py`
   - 将 `TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"` 替换为你的实际 Bot Token

4. 运行机器人:
```bash
python subinfo.py
```

### 📖 使用说明

#### 命令

- `/subinfo` 或 `/cha` - 查询订阅信息

#### 使用示例

1. **直接查询链接**:
   ```
   /subinfo https://example.com/sub?token=xxx
   ```

2. **批量查询**:
   ```
   /subinfo 
   https://sub1.com/link1
   https://sub2.com/link2
   ```

3. **上传文本文件**:
   - 发送包含订阅链接的 `.txt` 文件
   - 在标题中输入 `/subinfo`

4. **回复消息查询**:
   - 用 `/subinfo` 回复任何包含链接的消息

5. **导出为文件**:
   ```
   /subinfo txt https://example.com/sub
   ```

### 📊 输出格式

```
📄 机场: 机场名称
🏷️ 订阅: https://example.com/sub
📊 流量: [████████████░░░░░░░░] 60.5%
总计: 100.00 GB | 剩余: 39.50 GB
已用: 60.50 GB (↑5.2 GB ↓55.3 GB)
⏰ 到期: 2025-12-31
🌐 节点: 50个 (Clash/Surge)
```

### ⚙️ 配置说明

#### 远程映射

机器人从以下地址加载机场名称映射:
```python
REMOTE_MAPPINGS_URL = "https://raw.githubusercontent.com/Hyy800/Quantumult-X/refs/heads/Nana/ymys.txt"
```

格式:
```
关键词1=机场名称1
关键词2=机场名称2
```

#### 并发设置

调整并发请求数量限制:
```python
MAX_CONCURRENT_REQUESTS = 5  # 默认: 5
```

### 🛠️ 技术细节

- **支持格式**: Clash YAML、V2Ray/Shadowsocks Base64
- **超时时间**: 每个请求 15 秒
- **User-Agent**: `FlClash/v0.8.76 clash-verge`
- **消息限制**: 4000 字符 (自动截断)

### 📝 开源协议

MIT License

### 🤝 贡献

欢迎提交 Pull Request! 如有重大更改,请先开启 Issue 讨论。

---

### 📞 Support

If you encounter any issues, please open an issue on GitHub.

如遇到任何问题,请在 GitHub 上提交 Issue。