import os
import requests

SERPER_API_KEY = os.environ["SERPER_API_KEY"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://google.serper.dev/search"

payload = {
    "q": '(SpOG OR Obgyn OR "dokter kandungan" OR "obstetri ginekologi") (lowongan OR vacancy OR hiring OR recruitment)',
    "gl": "id",
    "hl": "id",
    "tbs": "qdr:w",
    "num": 20
}

headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

message = "🩺 LOWONGAN DOKTER KANDUNGAN / SpOG\n\n"

results = []

print(data)

for item in data.get("organic", []):

    title = item.get("title", "Tanpa Judul")
    link = item.get("link", "")
    snippet = item.get("snippet", "")

    results.append(
        f"• {title}\n{link}\n{snippet}\n"
    )

if results:
    message += "\n".join(results[:10])
else:
    message += "Tidak ditemukan lowongan baru."

print(message)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
