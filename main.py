import os
import requests

SERPER_API_KEY = os.environ["SERPER_API_KEY"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://google.serper.dev/search"

# QUERY PALING STABIL UNTUK INSTAGRAM + SpOG
payload = {
    "q": '(SpOG OR Obgyn OR "dokter kandungan" OR "obstetri ginekologi") site:instagram.com',
    "gl": "id",
    "hl": "id",
    "tbs": "qdr:w",
    "num": 30
}

headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

# DEBUG (aktifkan kalau perlu troubleshooting)
print("=== SERPER RAW RESPONSE ===")
print(data)
print("===========================")

message = "🩺 LOWONGAN DOKTER SpOG / OBGYN (INSTAGRAM TERBARU)\n\n"

results = []

for item in data.get("organic", []):

    title = item.get("title", "")
    link = item.get("link", "")
    snippet = item.get("snippet", "")

    text = f"{title} {snippet}".lower()

    # FILTER RINGAN (jangan terlalu ketat)
    if any(k in text for k in [
        "spog",
        "obgyn",
        "obstetri",
        "ginekologi",
        "kandungan",
        "hiring",
        "we are hiring",
        "join",
        "vacancy",
        "lowongan"
    ]):

        results.append(f"• {title}\n{link}\n")

# fallback: kalau kosong, tetap tampilkan hasil mentah (biar tidak "kosong total")
if results:
    message += "\n".join(results[:10])
else:
    message += "Tidak ditemukan hasil spesifik lowongan, berikut hasil umum:\n\n"

    for item in data.get("organic", [])[:5]:
        message += f"• {item.get('title')}\n{item.get('link')}\n\n"

print(message)

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
