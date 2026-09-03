import gspread
import pandas as pd

from google.oauth2.service_account import Credentials


# ==========================================
# KONFIGURASI
# ==========================================

SERVICE_ACCOUNT_FILE = "service-account.json"

SPREADSHEET_NAME = "Crypto Data Platform"

OUTPUT_FILE = "data/crypto_dataset.csv"


# ==========================================
# GOOGLE SHEETS
# ==========================================

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


# ==========================================
# AMBIL DATA
# ==========================================

print("Mengambil data dari Google Sheets...")

records = sheet.get_all_records()

print(f"Jumlah baris: {len(records)}")


# ==========================================
# DATAFRAME
# ==========================================

df = pd.DataFrame(records)


# ==========================================
# CEK DATA
# ==========================================

print("\nKolom yang ditemukan:")

for column in df.columns:
    print("-", column)


# ==========================================
# KONVERSI TIPE DATA
# ==========================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

numeric_columns = [
    "price_usd",
    "market_cap_usd",
    "volume_24h_usd",
    "change_24h_pct"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ==========================================
# HAPUS DATA INVALID
# ==========================================

before = len(df)

df = df.dropna(
    subset=[
        "timestamp",
        "symbol",
        "price_usd"
    ]
)

after = len(df)

print()
print(f"Data sebelum dibersihkan : {before}")
print(f"Data setelah dibersihkan : {after}")


# ==========================================
# URUTKAN DATA
# ==========================================

df = df.sort_values(
    by=["symbol", "timestamp"]
)

df = df.reset_index(drop=True)


# ==========================================
# HAPUS DUPLIKAT
# ==========================================

df = df.drop_duplicates(
    subset=[
        "timestamp",
        "symbol"
    ]
)

# ==========================================
# SIMPAN DATASET
# ==========================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# INFORMASI DATASET
# ==========================================

print()
print("======================================")
print("DATASET BERHASIL DIBUAT")
print("======================================")

print(f"File   : {OUTPUT_FILE}")
print(f"Baris  : {len(df)}")
print(f"Kolom  : {len(df.columns)}")

print()
print("Jumlah data per coin:")

print(
    df["symbol"]
    .value_counts()
    .sort_index()
)

print()
print("======================================")
