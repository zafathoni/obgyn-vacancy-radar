import os
import requests

API_KEY = os.environ["GOOGLE_API_KEY"]
CX = os.environ["GOOGLE_CX"]

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

query = "dokter spesialis obgyn"

url = "https://www.googleapis.com/customsearch/v1"

response = requests.get(
    url,
    params={
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": 5
    }
)

data = response.json()

message = "🩺 TEST HASIL PENCARIAN\n\n"

if "items" in data:
    for item in data["items"]:
        title = item.get("title", "")
        link = item.get("link", "")

        message += f"• {title}\n{link}\n\n"
else:
    message += str(data)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
