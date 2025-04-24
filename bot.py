import os
import requests
import time
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print("✅ BTC OI Bot 已启动")

def get_oi():
    url = "https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT"
    try:
        print("📡 正在请求 Binance API...")
        response = requests.get(url, timeout=10)
        print("🔁 返回内容：", response.text)
        return float(response.json()["openInterest"])
    except Exception as e:
        print("❌ API 请求失败：", e)
        return None

while True:
    oi = get_oi()
    if oi is not None:
        print(f"📊 BTCUSDT 当前 OI: {oi}")
        bot.send_message(chat_id=chat_id, text=f"📊 BTCUSDT 当前 OI: {oi}")
    else:
        print("⚠️ 没拿到 OI，跳过推送")
    time.sleep(60)