import time
import os
import requests
from tradingview_ta import TA_Handler, Interval

TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

SYMBOL = "EURUSD"
EXCHANGE = "FX_IDC"
INTERVAL = Interval.INTERVAL_1_MINUTE

def send(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)

def get_signal():
    try:
        h = TA_Handler(
            symbol=SYMBOL,
            exchange=EXCHANGE,
            screener="forex",
            interval=INTERVAL
        )
        a = h.get_analysis()
        rsi = a.indicators.get("RSI")
        ema10 = a.indicators.get("EMA10")
        ema20 = a.indicators.get("EMA20")

        if rsi is None or ema10 is None or ema20 is None:
            return None

        if rsi > 55 and ema10 > ema20:
            return "📈 BUY (EURUSD 1m)"
        if rsi < 45 and ema10 < ema20:
            return "📉 SELL (EURUSD 1m)"
        return None
    except Exception:
        return None

send("🤖 Bot connected successfully")

last = None
last_ping = time.time()

while True:
    sig = get_signal()

    if sig and sig != last:
        send(sig)
        last = sig

    # heartbeat (every 5 minutes)
    if time.time() - last_ping > 300:
        send("✅ Bot running (waiting for signal)")
        last_ping = time.time()

    time.sleep(30)
