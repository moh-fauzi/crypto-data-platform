import pandas as pd
from sklearn.ensemble import RandomForestRegressor


# =========================
# LOAD DATA
# =========================

def load_data():
    df = pd.read_csv("data/crypto_data.csv")

    print("Data berhasil dibaca!")
    print(f"Jumlah data: {len(df)}")

    return df


# =========================
# PREPARE DATA
# =========================

def prepare_data(df, coin_symbol):

    # Ambil data crypto tertentu
    coin_data = df[df["symbol"] == coin_symbol].copy()

    # Urutkan berdasarkan waktu
    coin_data["timestamp"] = pd.to_datetime(
        coin_data["timestamp"]
    )

    coin_data = coin_data.sort_values("timestamp")

    # Buat target:
    # harga pada data berikutnya
    coin_data["target_price"] = coin_data["price_usd"].shift(-1)

    # Hapus baris terakhir karena tidak punya target
    coin_data = coin_data.dropna()

    return coin_data


# =========================
# TRAIN MODEL
# =========================

def train_model(coin_data):

    features = [
        "price_usd",
        "market_cap_usd",
        "volume_24h_usd",
        "change_24h_pct"
    ]

    X = coin_data[features]
    y = coin_data["target_price"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


# =========================
# PREDICT
# =========================

def predict_price(model, coin_data):

    features = [
        "price_usd",
        "market_cap_usd",
        "volume_24h_usd",
        "change_24h_pct"
    ]

    latest_data = coin_data[features].iloc[[-1]]

    prediction = model.predict(latest_data)

    return prediction[0]


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    df = load_data()

    coin = "btc"

    coin_data = prepare_data(
        df,
        coin
    )

    print()
    print(f"Data {coin.upper()}: {len(coin_data)} baris")

    if len(coin_data) < 2:

        print("Data belum cukup untuk membuat model.")

    else:

        model = train_model(
            coin_data
        )

        predicted_price = predict_price(
            model,
            coin_data
        )

        print()
        print("==============================")
        print("HASIL PREDIKSI")
        print("==============================")
        print(f"Coin              : {coin.upper()}")
        print(f"Prediksi harga    : ${predicted_price:.4f}")
        print("==============================")
