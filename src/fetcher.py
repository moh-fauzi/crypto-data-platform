import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timezone

# =========================
# KONFIGURASI
# =========================

SERVICE_ACCOUNT_FILE = "service-account.json"

SPREADSHEET_NAME = "Crypto Data Platform"

COINS = [
    "bitcoin",
    "ethereum",
    "binancecoin",
    "solana",
    "cardano",
    "ripple",
    "dogecoin",
    "polkadot"
]

# =========================
# GOOGLE SHEETS
# =========================

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=scopes
)

client = gspread.authorize(credentials)

sheet = client.open(SPREADSHEET_NAME).sheet1

# =========================
# COINGECKO
# =========================

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "ids": ",".join(COINS),
    "order": "market_cap_desc",
    "per_page": 8,
    "page": 1,
    "sparkline": "false"
}

response = requests.get(url, params=params)

response.raise_for_status()

data = response.json()

# =========================
# SIMPAN DATA
# =========================

timestamp = datetime.now(timezone.utc).isoformat()

for coin in data:

    row = [
        timestamp,
        coin["name"],
        coin["symbol"],
        coin["current_price"],
        coin["market_cap"],
        coin["total_volume"],
        coin["price_change_percentage_24h"]
    ]

    sheet.append_row(row)

    print(
        coin["name"],
        "-",
        coin["current_price"],
        "USD"
    )

print("Data berhasil dikirim ke Google Sheets!")