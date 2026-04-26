from config import COIN_MAP

def detect_coin_name(text):
    lowered = text.lower()
    for persian_name, symbol in COIN_MAP.items():
        if persian_name in lowered:
            return symbol
    return None
