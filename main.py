
import os
import requests

# Pastikan SERPER_API_KEY sudah terdaftar di GitHub Secrets Anda
SERPER_API_KEY = os.environ["SERPER_API_KEY"] 
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Query yang disesuaikan
query = '"Hiring+SpOG" OR "Hiring+Obgyn" OR "Hiring+dokter+kandungan" OR "Hiring+obstetri" OR "Lowongan+Obgyn" OR "Lowongan+dokter+kandungan" OR "Vacancy+Obgyn" OR "Vacancy+dokter+kandungan"'
# query ="Hiring+Obgyn"

url = "https://google.serper.dev/search"

payload = {
    "q": query,
    "gl": "id",
    "hl": "id",
    "tbs": "qdr:w",
    "num": 1
}

headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}

# Menggunakan POST request sesuai dokumentasi Serper
response = requests.post(url, json=payload, headers=headers)
data = response.json()

message = "🩺 HASIL PENCARIAN LOWONGAN OBGYN\n\n"

# Serper menyimpan hasil di key 'organic'
if "organic" in data and len(data["organic"]) > 0:
    for item in data["organic"]:
        title = item.get("title", "Tanpa Judul")
        link = item.get("link", "#")
        message += f"• {title}\n{link}\n\n"
else:
    message += "Maaf, belum ada lowongan Obgyn yang ditemukan saat ini."

# Debugging log untuk GitHub Actions
print("--- DEBUG MESSAGE START ---")
print(message)
print("--- DEBUG MESSAGE END ---")

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)
