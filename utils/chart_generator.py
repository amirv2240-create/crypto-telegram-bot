import matplotlib.pyplot as plt
import os

def save_price_chart(prices, coin_symbol):
    if not prices:
        return None

    times = [t[0] for t in prices]
    price_values = [p[1] for p in prices]

    plt.figure(figsize=(8,4))
    plt.plot(price_values, color="blue")
    plt.title(f"نمودار ۲۴ ساعته قیمت {coin_symbol.upper()}")
    plt.xlabel("زمان")
    plt.ylabel("قیمت (USD)")
    plt.grid(True)

    chart_path = f"{coin_symbol}_chart.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path
