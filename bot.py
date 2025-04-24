import os
import requests
import time
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SYMBOLS = [
    'ACHUSDT', 'BELUSDT', 'DUSKUSDT', 'EDUUSDT', 'TUSDT', 'AERGOUSDT',
    'ALPHAUSDT', 'ARPAUSDT', 'ATAUSDT', 'GHSTUSDT', 'HIGHUSDT',
    'LOKAUSDT', 'MOVRUSDT', 'OGNUSDT', 'PERPUSDT', 'RDNTUSDT', 'RIFUSDT',
    'SFPUSDT', 'STORJUSDT', 'TRUUSDT', 'XVSUSDT', 'YGGUSDT', 'ZENUSDT',
    'CHRUSDT', 'DENTUSDT', 'FUNUSDT', 'PHBUSDT', 'ZILUSDT', 'HBARUSDT',
    'KAVAUSDT', 'LRCUSDT', 'MANAUSDT', 'NKNUSDT', 'ONTUSDT', 'RLCUSDT',
    'STXUSDT', 'SYSUSDT', 'TRBUSDT', 'VETUSDT', 'WAXPUSDT', 'XLMUSDT',
    'XVGUSDT', 'ZECUSDT', 'ZRXUSDT', 'DIAUSDT', 'CTSIUSDT'
]

THRESHOLD = 20
INTERVAL = 60

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_oi = {}

def get_open_interest(symbol):
    try:
        url = f'https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}'
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['openInterest'])
    except Exception:
        print(f"跳过 {symbol}：{symbol} 无合约数据")
        return None

while True:
    try:
        for symbol in SYMBOLS:
            current_oi = get_open_interest(symbol)
            if current_oi is None:
                continue
            print(f"{symbol} 当前 OI: {current_oi}")
            if symbol in last_oi:
                change = ((current_oi - last_oi[symbol]) / last_oi[symbol]) * 100
                if abs(change) >= THRESHOLD:
                    msg = f'⚠️ {symbol} OI 变动 {change:.2f}%\n当前OI: {current_oi}'
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
            last_oi[symbol] = current_oi
        time.sleep(INTERVAL)
    except Exception as e:
        print("发生错误：", e)
        time.sleep(10)
