def parse_message(text):
    text = text.lower()
    if "قیمت" in text and ("دلار" in text or "ریال" in text):
        return "price_usd"
    if "قیمت" in text and ("طلا" in text):
        return "price_gold"
    if "قیمت" in text:
        return "price_coin"
    if "نمودار" in text:
        return "chart"
    if "تبدیل" in text:
        return "convert"
    return "unknown"
