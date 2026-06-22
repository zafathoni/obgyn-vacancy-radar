import os
import requests

SERPER_API_KEY = os.environ["SERPER_API_KEY"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://google.serper.dev/search"

payload = {
    "q": 'site:instagram.com/p/ (SpOG OR Obgyn OR "dokter kandungan")',
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

message = "🩺 HASIL PENCARIAN SpOG / OBGYN INSTAGRAM\n\n"

results = []

for item in data.get("organic", []):

    title = item.get("title", "Tanpa Judul")
    link = item.get("link", "")

    # Hanya ambil post Instagram
    if "instagram.com/p/" in link:
        results.append(
            f"• {title}\n{link}\n"
        )

if results:
    message += "\n".join(results[:10])
else:
    message += "Tidak ditemukan post Instagram yang relevan."

print(data)
print("--- DEBUG ---")
print(message)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
