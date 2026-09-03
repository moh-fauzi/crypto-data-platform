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
    "ripple",
    "solana",
    "dogecoin",
    "cardano",
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
# COINGECKO API
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


# =========================
# REQUEST DATA
# =========================

try:

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

except Exception as e:

    print("ERROR mengambil data CoinGecko:")
    print(e)

    raise


# =========================
# VALIDASI DATA
# =========================

print(f"Jumlah coin diterima: {len(data)}")

if len(data) != len(COINS):

    print("WARNING: jumlah coin tidak lengkap!")

    received = {coin["id"] for coin in data}

    missing = set(COINS) - received

    print("Coin yang tidak diterima:")

    for coin in missing:
        print("-", coin)

    raise Exception(
        f"Data tidak lengkap. "
        f"Diterima {len(data)}/{len(COINS)} coin."
    )


# =========================
# TIMESTAMP
# =========================

timestamp = datetime.now(timezone.utc).isoformat()


# =========================
# SIMPAN KE GOOGLE SHEETS
# =========================

rows = []

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

    rows.append(row)

    print(
        f"{coin['name']} | "
        f"${coin['current_price']} | "
        f"{coin['symbol']}"
    )


# =========================
# KIRIM SEMUA BARIS
# =========================

sheet.append_rows(rows)

print()
print("===================================")
print("DATA BERHASIL DIKIRIM")
print("===================================")
print(f"Timestamp : {timestamp}")
print(f"Jumlah    : {len(rows)} coin")
print("===================================")
