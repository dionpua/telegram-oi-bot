import requests
import asyncio
from telegram import Bot
from datetime import datetime

# ✅ Telegram 配置
TELEGRAM_BOT_TOKEN = '7945839049:AAHQSBpLs_hK6KojiYhq9sow08L-s7KGpMM'
TELEGRAM_CHAT_ID = '720632182'

# ✅ 有效币种（45个）
SYMBOLS = [
    'ACHUSDT', 'BELUSDT', 'DUSKUSDT', 'EDUUSDT', 'TUSDT', 'AERGOUSDT', 'ALPHAUSDT',
    'ARPAUSDT', 'ATAUSDT', 'GHSTUSDT', 'HIGHUSDT', 'LOKAUSDT', 'MOVRUSDT', 'OGNUSDT',
    'PERPUSDT', 'RDNTUSDT', 'RIFUSDT', 'SFPUSDT', 'STORJUSDT', 'TRUUSDT', 'XVSUSDT',
    'YGGUSDT', 'ZENUSDT', 'CHRUSDT', 'DENTUSDT', 'FUNUSDT', 'PHBUSDT', 'ZILUSDT',
    'HBARUSDT', 'KAVAUSDT', 'LRCUSDT', 'MANAUSDT', 'NKNUSDT', 'ONTUSDT', 'RLCUSDT',
    'STXUSDT', 'SYSUSDT', 'TRBUSDT', 'VETUSDT', 'WAXPUSDT', 'XLMUSDT', 'XVGUSDT',
    'ZECUSDT', 'ZRXUSDT', 'DIAUSDT', 'CTSIUSDT'
]

INTERVAL = 60  # 每轮查询间隔（秒）
SLEEP_BETWEEN_SYMBOLS = 0.2
THRESHOLD = 10  # OI 变动百分比，超过才推送

bot = Bot(token=TELEGRAM_BOT_TOKEN)
last_oi = {}

def get_open_interest(symbol):
    url = f'https://fapi.binance.com/fapi/v1/openInterest?symbol={symbol}'
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()
    if 'openInterest' not in data:
        raise ValueError(f"{symbol} 无合约数据")
    return float(data['openInterest'])

async def send_telegram(text):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

# ✅ 主监控函数
async def main():
    global last_oi
    while True:
        for symbol in SYMBOLS:
            try:
                current_oi = get_open_interest(symbol)
                print(f'{symbol} 当前 OI: {current_oi}')
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if symbol in last_oi:
                    change = ((current_oi - last_oi[symbol]) / last_oi[symbol]) * 100
                    if abs(change) >= THRESHOLD:
                        msg = f'⚠️ [{now}] {symbol}\n持仓量: {current_oi:.2f}\n变动: {change:.2f}%'
                        await send_telegram(msg)
                else:
                    # 初次记录（默认不发通知，想要发就取消注释下面两行）
                    # msg = f'📊 [{now}] {symbol}\n首次记录 OI: {current_oi:.2f}'
                    # await send_telegram(msg)
                    pass

                last_oi[symbol] = current_oi
                await asyncio.sleep(SLEEP_BETWEEN_SYMBOLS)

            except Exception as e:
                print(f"跳过 {symbol}：{e}")
                continue

        await asyncio.sleep(INTERVAL)

# ✅ 启动主程序
if __name__ == "__main__":
    asyncio.run(main())