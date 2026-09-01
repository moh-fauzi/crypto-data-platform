import requests

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,binancecoin,solana,cardano,ripple,dogecoin,polkadot"
}

response = requests.get(url, params=params)

print("Status:", response.status_code)

data = response.json()

for coin in data:
    print(
        coin["name"],
        "-",
        coin["current_price"],
        "USD"
    )