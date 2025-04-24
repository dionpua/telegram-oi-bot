import os
import requests
import time
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

def get_oi():
    url = "https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT"
    r = requests.get(url, timeout=10)
    return float(r.json()["openInterest"])

print("✅ BTC OI Bot 启动")

while True:
    try:
        oi = get_oi()
        print(f"BTCUSDT 当前 OI: {oi}")
        bot.send_message(chat_id=chat_id, text=f"BTCUSDT 当前 OI: {oi}")
        time.sleep(60)
    except Exception as e:
        print("❌ 错误：", e)
        time.sleep(10)
