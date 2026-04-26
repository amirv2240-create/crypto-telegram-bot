import requests

def get_coin_chart_data(coin_id, days=1):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        prices = data.get("prices", [])
        return prices
    except Exception:
        return []
