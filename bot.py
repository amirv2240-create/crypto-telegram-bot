import telebot
from config import BOT_TOKEN, COIN_MAP
from api import nobitex, forex, gold, chart
from utils import detect_coin, parser, chart_generator

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text or ""
    command = parser.parse_message(text)

    if command == "price_usd":
        price = forex.get_usd_price()
        if price:
            bot.reply_to(message, f"قیمت دلار: {price} تومان")
        else:
            bot.reply_to(message, "نمی‌توانم قیمت دلار را دریافت کنم.")

    elif command == "price_gold":
        price = gold.get_gold_price()
        if price:
            bot.reply_to(message, f"قیمت طلا: {price} تومان")
        else:
            bot.reply_to(message, "نمی‌توانم قیمت طلا را دریافت کنم.")

    elif command == "price_coin":
        coin = detect_coin.detect_coin_name(text)
        if coin:
            price = nobitex.get_price(coin)
            if price:
                bot.reply_to(message, f"قیمت {coin.upper()}: {price} تومان")
            else:
                bot.reply_to(message, "نمی‌توانم قیمت ارز را دریافت کنم.")
        else:
            bot.reply_to(message, "نام ارز را درست وارد کنید.")

    elif command == "chart":
        coin = detect_coin.detect_coin_name(text)
        if coin:
            prices = chart.get_coin_chart_data(coin, days=1)
            chart_path = chart_generator.save_price_chart(prices, coin)
            if chart_path:
                with open(chart_path, "rb") as photo:
                    bot.send_photo(message.chat.id, photo)
            else:
                bot.reply_to(message, "نمی‌توانم نمودار قیمت را بسازم.")
        else:
            bot.reply_to(message, "نام ارز را درست وارد کنید.")

    elif command == "convert":
        bot.reply_to(message, "قابلیت تبدیل ارز در نسخه بعدی اضافه می‌شود.")
        
    else:
        bot.reply_to(message, "دستور یا پیام شما را متوجه نشدم.")

if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
