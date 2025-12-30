import time
from telegram import Bot

TOKEN = "7676286154:AAEJ32BhL7TInN5h1HnsToVctiEVYIljvQQ"
CHAT_ID = 6339346924

bot = Bot(token=TOKEN)

print("Bot starting...")
bot.send_message(chat_id=CHAT_ID, text="✅ Bot started on Railway VPS")

while True:
    try:
        bot.send_message(
            chat_id=CHAT_ID,
            text="⏳ Bot alive (waiting for EURUSD 1m signal)"
        )
        time.sleep(300)

    except Exception as e:
        print("Error:", e)
        time.sleep(15)
