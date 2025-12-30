import time
import os
import requests
import pandas as pd
from tradingview_ta import TA_Handler, Interval

# ====== CONFIG (ENV VARS USE KARO) ======
TELEGRAM_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

SYMBOL = "EURUSD"
EXCHANGE = "FX_IDC"
INTERVAL = Interval.INTERVAL_1_MINUTE  # 1 minute scalping

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

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
            return "📈 BUY (1m)"
        if rsi < 45 and ema10 < ema20:
            return "📉 SELL (1m)"
        return None
    except Exception:
        return None

last = None
send("🤖 Bot started (EURUSD 1m)")

while True:
    sig = get_signal()
    if sig and sig != last:
        send(f"{sig}\nPair: EURUSD\nTF: 1 Minute")
        last = sig
    time.sleep(30)
