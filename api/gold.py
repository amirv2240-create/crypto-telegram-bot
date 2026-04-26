import requests

def get_gold_price():
    try:
        res = requests.get("https://api.tgju.org/v1/data/phone/data.json")
        res.raise_for_status()
        data = res.json()
        for item in data.get("data", []):
            if item.get("InstrumentId") == "Gold":
                return item.get("LastPrice")
        return None
    except Exception:
        return None
