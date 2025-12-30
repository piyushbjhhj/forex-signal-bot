import time
import requests
from tradingview_ta import TA_Handler, Interval

# ===== TELEGRAM CONFIG =====
TOKEN = "7676286154:AAEJ32BhL7TInN5h1HnsToVctiEVYIljvQQ"
CHAT_ID = "6339346924"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# ===== TRADINGVIEW CONFIG =====
symbol = "EURUSD"
exchange = "FX_IDC"
interval = Interval.INTERVAL_1_MINUTE

send("🤖 Forex Signal Bot STARTED (EURUSD 1M)")

last_signal = None

while True:
    try:
        tv = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="forex",
            interval=interval
        )

        analysis = tv.get_analysis()
        rsi = analysis.indicators.get("RSI")
        ema9 = analysis.indicators.get("EMA9")
        ema21 = analysis.indicators.get("EMA21")

        if rsi is None or ema9 is None or ema21 is None:
            time.sleep(60)
            continue

        signal = None

        if rsi > 55 and ema9 > ema21:
            signal = "📈 BUY (1 Minute)"
        elif rsi < 45 and ema9 < ema21:
            signal = "📉 SELL (1 Minute)"

        if signal and signal != last_signal:
            send(f"🔥 EURUSD SIGNAL\n{signal}\nRSI: {round(rsi,2)}")
            last_signal = signal

        time.sleep(60)

    except Exception as e:
        send(f"⚠️ Error: {e}")
        time.sleep(60)
