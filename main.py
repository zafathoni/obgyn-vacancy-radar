import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = """
🩺 OBGYN Vacancy Radar

Bot berhasil berjalan dari GitHub Actions.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": message
    }
)
