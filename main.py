import os
import requests

SERPER_API_KEY = os.environ["SERPER_API_KEY"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://google.serper.dev/search"

payload = {
    "q": '(SpOG OR "Sp.OG" OR Obgyn OR OBGYN OR "dokter kandungan" OR "dokter spesialis kandungan dan kebidanan") (lowongan OR vacancy OR hiring OR dibutuhkan)',
    "gl": "id",
    "hl": "id",
    "tbs": "qdr:d",  # 24 jam terakhir
    "num": 10
}

headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

message = "🩺 LOWONGAN DOKTER KANDUNGAN / SpOG (24 JAM TERAKHIR)\n\n"

results = []

for item in data.get("organic", []):
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    link = item.get("link", "")

    text = f"{title} {snippet}".lower()

    # Filter sederhana supaya lebih relevan
    if any(k in text for k in [
        "spog",
        "sp.og",
        "obgyn",
        "dokter kandungan",
        "kebidanan",
        "ginekologi"
    ]):
        results.append(
            f"• {title}\n{link}\n"
        )

if results:
    message += "\n".join(results[:10])
else:
    message += "Tidak ditemukan lowongan baru yang relevan."

print(message)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
