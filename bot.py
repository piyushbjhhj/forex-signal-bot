import time
import requests
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

# ===== TELEGRAM DETAILS =====
BOT_TOKEN = "7676286154:AAEJ32BhL7TInN5h1HnsToVctiEVYIljvQQ"
CHAT_ID = "6339346924"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

# ===== TRADINGVIEW SETUP =====
tv = TvDatafeed()
SYMBOL = "EURUSD"
EXCHANGE = "OANDA"   # OTC approximation
INTERVAL = Interval.in_1_minute

send_telegram("🤖 OTC FORCED BOT STARTED\nPAIR: EURUSD_OTC\nTF: 1M")

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

last_minute = None

while True:
    try:
        df = tv.get_hist(symbol=SYMBOL, exchange=EXCHANGE,
                         interval=INTERVAL, n_bars=60)

        if df is None or len(df) < 50:
            time.sleep(10)
            continue

        df["ema9"] = df["close"].ewm(span=9).mean()
        df["ema21"] = df["close"].ewm(span=21).mean()
        df["ema50"] = df["close"].ewm(span=50).mean()
        df["rsi"] = rsi(df["close"])

        last = df.iloc[-1]
        candle_time = last.name

        if candle_time == last_minute:
            time.sleep(5)
            continue

        last_minute = candle_time

        signal = None
        confidence = "LOW (TREND BIAS)"

        if last["rsi"] < 35 and last["ema9"] > last["ema21"]:
            signal = "CALL"
            confidence = "HIGH"
        elif last["rsi"] > 65 and last["ema9"] < last["ema21"]:
            signal = "PUT"
            confidence = "HIGH"
        else:
            if last["close"] > last["ema50"]:
                signal = "CALL"
            else:
                signal = "PUT"

        message = (
            f"📊 OTC SIGNAL\n"
            f"PAIR: EURUSD_OTC\n"
            f"TF: 1M\n"
            f"SIGNAL: {signal}\n"
            f"CONFIDENCE: {confidence}\n"
            f"EXPIRY: 1 MIN"
        )

        send_telegram(message)
        time.sleep(60)

    except Exception as e:
        send_telegram(f"⚠️ BOT ERROR: {e}")
        time.sleep(30)
