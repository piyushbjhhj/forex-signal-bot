import time
import requests
from telegram import Bot

# ===== CONFIG =====
TOKEN = "7676286154:AAEJ32BhL7TInN5h1HnsToVctiEVYIljvQQ"
CHAT_ID = "6339346924"

bot = Bot(token=TOKEN)

print("🤖 Bot started successfully")

# Test message (VERY IMPORTANT)
bot.send_message(chat_id=CHAT_ID, text="🤖 Bot connected successfully")

while True:
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text="⏳ Bot running (waiting for signal)"
        )
        time.sleep(300)  # 5 minutes

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
