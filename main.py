```python
import os
import json
import requests

# =========================
# ENVIRONMENT VARIABLES
# =========================
SERPER_API_KEY = os.environ["SERPER_API_KEY"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SERPER_URL = "https://google.serper.dev/search"

# =========================
# KOTA/PROVINSI YANG DIIZINKAN
# =========================
ALLOWED_LOCATIONS = [
    "jakarta",
    "bogor",
    "depok",
    "tangerang",
    "bekasi",
    "bandung",
    "cirebon",
    "tasikmalaya",
    "garut",
    "sukabumi",
    "karawang",
    "purwakarta",
    "serang",
    "cilegon",
    "semarang",
    "solo",
    "surakarta",
    "yogyakarta",
    "sleman",
    "bantul",
    "kulon progo",
    "gunung kidul",
    "surabaya",
    "malang",
    "kediri",
    "madiun",
    "jember",
    "banyuwangi",
    "dki jakarta",
    "banten",
    "jawa barat",
    "jawa tengah",
    "jawa timur"
]

# =========================
# FILTER LUAR NEGERI
# =========================
FOREIGN_KEYWORDS = [
    "usa",
    "united states",
    "canada",
    "australia",
    "new zealand",
    "india",
    "pakistan",
    "singapore",
    "malaysia",
    "philippines",
    "uk",
    "england",
    "dubai",
    "qatar",
    "saudi",
    "arab emirates",
    "abu dhabi"
]

# =========================
# QUERY PER KOTA
# =========================
QUERIES = [
    'lowongan dokter SpOG Jakarta',
    'lowongan dokter SpOG Bogor',
    'lowongan dokter SpOG Depok',
    'lowongan dokter SpOG Tangerang',
    'lowongan dokter SpOG Bekasi',
    'lowongan dokter SpOG Bandung',
    'lowongan dokter SpOG Cirebon',
    'lowongan dokter SpOG Semarang',
    'lowongan dokter SpOG Solo',
    'lowongan dokter SpOG Yogyakarta',
    'lowongan dokter SpOG Surabaya',
    'lowongan dokter SpOG Malang',
    'lowongan dokter kandungan Jawa Barat',
    'lowongan dokter kandungan Jawa Tengah',
    'lowongan dokter kandungan Jawa Timur',
    'vacancy Obgyn Indonesia',
    'hiring Obgyn Indonesia'
]

HEADERS = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json"
}


# =========================
# LOAD HISTORY
# =========================
SEEN_FILE = "seen_jobs.json"

if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        seen_jobs = set(json.load(f))
else:
    seen_jobs = set()

new_jobs = []


# =========================
# SEARCH LOOP
# =========================
for query in QUERIES:

    payload = {
        "q": query,
        "gl": "id",
        "hl": "id",
        "location": "Indonesia",
        "tbs": "qdr:w",
        "num": 10
    }

    try:
        response = requests.post(
            SERPER_URL,
            json=payload,
            headers=HEADERS,
            timeout=30
        )

        data = response.json()

        if "organic" not in data:
            continue

        for item in data["organic"]:

            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")

            text = f"{title} {snippet} {link}".lower()

            # Skip luar negeri
            if any(x in text for x in FOREIGN_KEYWORDS):
                continue

            # Hanya Jawa/Jabodetabek
            if not any(x in text for x in ALLOWED_LOCATIONS):
                continue

            # Dedup
            if link in seen_jobs:
                continue

            seen_jobs.add(link)

            new_jobs.append({
                "title": title,
                "link": link
            })

    except Exception as e:
        print(f"Error query {query}: {e}")


# =========================
# SAVE HISTORY
# =========================
with open(SEEN_FILE, "w", encoding="utf-8") as f:
    json.dump(list(seen_jobs), f)


# =========================
# TELEGRAM MESSAGE
# =========================
message = "🩺 OBGYN VACANCY RADAR\n\n"

if len(new_jobs) == 0:
    message += "No new OBGYN vacancies in Java today."
else:
    for i, job in enumerate(new_jobs, start=1):
        message += (
            f"{i}. {job['title']}\n"
            f"{job['link']}\n\n"
        )


print(message)

telegram_url = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
)

requests.post(
    telegram_url,
    json={
        "chat_id": CHAT_ID,
        "text": message[:4000],
        "disable_web_page_preview": True
    }
)
```
