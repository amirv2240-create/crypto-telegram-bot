import requests

def get_usd_price():
    try:
        res = requests.get("https://api.exir.io/v1/usd/toman/latest")
        res.raise_for_status()
        data = res.json()
        return data.get("lastPrice", None)
    except Exception:
        return None
