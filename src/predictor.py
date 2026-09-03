import pandas as pd


def load_data():
    df = pd.read_csv("data/crypto_data.csv")

    print("Data berhasil dibaca!")
    print(df.head())

    return df


if __name__ == "__main__":
    load_data()
