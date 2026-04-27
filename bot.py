import os
import telebot
import threading
from flask import Flask

# ============ BOT TOKEN FROM RENDER ============
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ============ Telegram Bot ============
bot = telebot.TeleBot(BOT_TOKEN)

# ============ Flask Server (for Render) ============
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running on Render 🎉"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# اجرای Flask روی ترد جدا
threading.Thread(target=run_flask, daemon=True).start()


# ============ START COMMAND ============
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(
        message,
        "سلام 👋\n"
        "به ربات قیمت ارز، طلا، فارکس و چارت خوش‌اومدی.\n\n"
        "دستورات کاربردی:\n"
        "• btc , eth , bnb → قیمت ارز دیجیتال\n"
        "• usd , eur → قیمت فارکس\n"
        "• gold → قیمت طلا\n"
        "• chart btc → نمایش چارت\n"
        "• chart eth 1h → چارت تایم‌فریم دار\n\n"
        "یک دستور ارسال کن 👇"
    )


# ============ PRICE HANDLER ============
@bot.message_handler(func=lambda m: m.text.lower() in ["btc", "eth", "bnb"])
def crypto_price(message):
    from api.nobitex import get_crypto_price
    coin = message.text.lower()
    price = get_crypto_price(coin)
    bot.reply_to(message, f"قیمت {coin.upper()}:\n{price:,} تومان")


@bot.message_handler(func=lambda m: m.text.lower() in ["usd", "eur", "gbp"])
def forex_price(message):
    from api.forex import get_forex_price
    coin = message.text.lower()
    price = get_forex_price(coin)
    bot.reply_to(message, f"قیمت {coin.upper()}:\n{price:,} تومان")


@bot.message_handler(func=lambda m: m.text.lower() == "gold")
def gold_price(message):
    from api.gold import get_gold_price
    price = get_gold_price()
    bot.reply_to(message, f"قیمت طلا: {price:,} تومان")


# ============ CHART HANDLER ============
@bot.message_handler(func=lambda m: m.text.lower().startswith("chart"))
def chart_handler(message):
    from utils.chart_generator import create_chart
    parts = message.text.lower().split()

    if len(parts) == 1:
        return bot.reply_to(message, "مثال صحیح:\nchart btc\nchart eth 1h")

    coin = parts[1]
    timeframe = parts[2] if len(parts) >= 3 else "1h"

    image_path = create_chart(coin, timeframe)

    with open(image_path, "rb") as img:
        bot.send_photo(message.chat.id, img, caption=f"چارت {coin.upper()} - {timeframe}")


# ============ UNKNOWN MESSAGES ============
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.reply_to(message, "دستور را متوجه نشدم ❗️\nمثال:\nbtc\ngold\nchart btc")


# ============ START BOT ============
bot.polling(none_stop=True)
