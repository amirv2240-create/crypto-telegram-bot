import requests

BASE_URL = "https://api.nobitex.ir/v2"

def get_price(coin_symbol):
    try:
        res = requests.get(f"{BASE_URL}/market/stats/{coin_symbol}toman")
        res.raise_for_status()
        data = res.json()
        price = data.get("stats", {}).get("lastPrice")
        if price:
            return price
        return None
    except Exception:
        return None
