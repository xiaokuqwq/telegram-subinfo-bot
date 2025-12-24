import asyncio
import base64
import re
import time
import html
import logging
from datetime import datetime
from io import BytesIO

import httpx
import yaml
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- 日志配置 ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 静态配置 ---
TOKEN = "你的_TELEGRAM_BOT_TOKEN"
REMOTE_MAPPINGS_URL = "https://raw.githubusercontent.com/Hyy800/Quantumult-X/refs/heads/Nana/ymys.txt"
REMOTE_CONFIG_MAPPINGS = {}

# 【高性能核心】全局并发限制：允许全系统同时进行 30 个网络请求（可根据 CPU 调整）
# 即使 100 人同时发链接，系统也会有序、高速地消化这 30 个窗口
GLOBAL_SEMAPHORE = asyncio.Semaphore(30)

# 全局共享的 HTTP 客户端池，极大提升连接复用率
shared_client = httpx.AsyncClient(
    timeout=httpx.Timeout(15.0, connect=5.0),
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=50),
    follow_redirects=True,
    headers={'User-Agent': 'Clash-Verge/1.0.0 (Windows NT 10.0; Win64; x64) Meta/1.18.0'}
)

# --- 工具函数 ---

def format_size(size: float) -> str:
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    level = 0
    while size >= 1024 and level < len(units) - 1:
        size /= 1024
        level += 1
    return f"{size:.2f} {units[level]}"

def parse_user_info(header: str):
    info = {}
    for part in header.split(';'):
        if '=' in part:
            k, v = part.split('=', 1)
            info[k.strip().lower()] = v.strip()
    return info

async def get_node_info(url: str):
    """异步获取节点数，复用全局连接"""
    try:
        resp = await shared_client.get(url)
        data = resp.text
        if 'proxies' in data: # YAML 简单判定
            config = yaml.safe_load(data)
            return {"count": len(config.get('proxies', [])), "detail": "Clash"}
        # 尝试 Base64
        try:
            missing_padding = len(data) % 4
            if missing_padding: data += '=' * (4 - missing_padding)
            decoded = base64.b64decode(data).decode('utf-8')
            lines = [l for l in decoded.splitlines() if '://' in l]
            if lines: return {"count": len(lines), "detail": "V2Ray/SS"}
        except: pass
    except: pass
    return None

async def process_sub(url: str):
    """处理单个链接的协程任务"""
    async with GLOBAL_SEMAPHORE: # 只有拿到“通行证”的请求才能执行
        try:
            resp = await shared_client.get(url)
            if resp.status_code != 200:
                return {"success": False, "url": url, "error": f"HTTP {resp.status_code}"}
            
            user_info_raw = resp.headers.get('subscription-userinfo')
            if not user_info_raw:
                return {"success": False, "url": url, "error": "无 Header 统计"}
            
            info = parse_user_info(user_info_raw)
            u, d, t, e = int(info.get('upload', 0)), int(info.get('download', 0)), int(info.get('total', 0)), int(info.get('expire', 0))
            
            used = u + d
            percent = round((used / t) * 100, 2) if t > 0 else 0
            name = next((v for k, v in REMOTE_CONFIG_MAPPINGS.items() if k in url), "未知机场")
            node = await get_node_info(url)
            
            return {
                "success": True, "url": url, "name": name, "total": t, "used": used,
                "remain": max(0, t - used), "percent": percent, "expire_ts": e,
                "node": node, "up": u, "down": d
            }
        except Exception as e:
            return {"success": False, "url": url, "error": "连接超时"}

# --- 消息处理器 ---

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg: return

    # 1. 提取链接
    content = msg.text or msg.caption or ""
    urls = re.findall(r'https?://[^\s]+', content)

    # 2. 处理附件
    if msg.document and (msg.document.file_name.endswith('.txt') or msg.document.mime_type == 'text/plain'):
        file = await msg.document.get_file()
        byte_content = await file.download_as_bytearray()
        urls.extend(re.findall(r'https?://[^\s]+', byte_content.decode('utf-8', errors='ignore')))

    urls = list(dict.fromkeys(urls)) # 去重
    if not urls: return

    # 提示开始
    status_msg = await msg.reply_text("🚀 系统正在并发处理您的请求...")

    # 3. 并发派发任务（这里的任务是并行的，不会卡住其他用户）
    tasks = [process_sub(url) for url in urls]
    responses = await asyncio.gather(*tasks)

    # 4. 结果拼装
    results = []
    for res in responses:
        safe_url = html.escape(res['url'])
        if not res["success"]:
            results.append(f"❌ <code>{safe_url}</code> | <b>{res['error']}</b>")
            continue
        
        filled = min(10, int(res['percent'] / 10))
        bar = "█" * filled + "░" * (10 - filled)
        expire = datetime.fromtimestamp(res['expire_ts']).strftime('%Y-%m-%d') if res['expire_ts'] > 0 else "无限"
        
        item = (
            f"📄 <b>{html.escape(res['name'])}</b>\n"
            f"📊 <code>{bar} {res['percent']}%</code>\n"
            f"余: <code>{format_size(res['remain'])}</code> | 到期: <code>{expire}</code>\n"
            f"🔗 <code>{safe_url}</code>"
        )
        results.append(item)

    # 5. 高性能发送逻辑：针对多用户和大结果进行分包
    final_output = "\n\n".join(results)
    
    if len(final_output) > 4000:
        bio = BytesIO(final_output.replace("<b>", "").replace("<code>", "").encode())
        bio.name = "result.txt"
        await msg.reply_document(document=bio, caption="✅ 结果已汇总至文件")
        await status_msg.delete()
    else:
        await status_msg.edit_text(final_output, parse_mode=constants.ParseMode.HTML, disable_web_page_preview=True)

# --- 入口 ---

async def init_data():
    await load_remote_mappings()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_data())
    
    # 调优参数：concurrent_updates 允许多少个用户消息同时被处理
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()
    
    app.add_handler(MessageHandler(filters.TEXT | filters.Document.Category("text/plain"), handle_request))
    
    print(">>> 工业级高性能 Bot 已启动，支持上百人并发...")
    app.run_polling()
