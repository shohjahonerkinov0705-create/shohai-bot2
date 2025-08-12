import telebot
from flask import Flask, request
import openai
import random
import os

# ==== SOZLAMALAR ====
API_TOKEN = "8151738321:AAERKT9v3z2FyaNvppYwnDoeRmQKufngn0o"
CHANNEL_ID = "@shokh_shaxsiy_blog"  # majburiy kanal
openai.api_key = "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"  # OpenAI API kalit

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ==== Ibratli so'zlar ====
quotes = [
    "Orzularingiz uchun kurashing. 💪",
    "Har bir kun – yangi imkoniyat. 🌟",
    "Xatolardan qo‘rqmang, ular sizni o‘stiradi.",
    "Mehnat — muvaffaqiyat kaliti.",
    "Bilim – eng yaxshi qurol."
]

# ==== Majburiy kanalga obuna tekshirish ====
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ==== START komandasi ====
@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, f"Botdan foydalanish uchun kanalimizga obuna bo‘ling:\n{CHANNEL_ID}")
        return
    bot.send_message(message.chat.id,
        "Assalomu alaykum! 👋\nMen ShohAI — sizning shaxsiy sun’iy intellekt yordamchingizman.\n"
        "💬 Savollaringizga javob beraman\n📚 Foydali maslahatlar beraman\n"
        "🎯 Kun tartibingizni eslataman\n🎮 Qiziqarli o‘yinlar taklif qilaman\n\n"
        "Boshlash uchun /help buyrug‘ini bosing."
    )

# ==== HELP komandasi ====
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id,
        "/start - Botni ishga tushirish\n"
        "/help - Yordam olish\n"
        "/info - Bot haqida ma’lumot\n"
        "/chat - AI bilan suhbat\n"
        "/quote - Ibratli so‘z olish\n"
        "/reminder - Eslatma qo‘yish"
    )

# ==== INFO komandasi ====
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
        "Bot nomi: ShohAI\nYaratuvchi: @shokh_afx_00\n"
        "Kanal: t.me/shokh_shaxsiy_blog\n"
        "Men sun’iy intellekt yordamchiman 🤖"
    )

# ==== QUOTE komandasi ====
@bot.message_handler(commands=['quote'])
def quote(message):
    bot.send_message(message.chat.id, random.choice(quotes))

# ==== REMINDER komandasi ====
@bot.message_handler(commands=['reminder'])
def reminder(message):
    bot.send_message(message.chat.id, "⌛ Eslatma funksiyasi hozircha sinovda.")

# ==== CHAT komandasi ====
@bot.message_handler(commands=['chat'])
def chat_mode(message):
    bot.send_message(message.chat.id, "Menga savolingizni yozing, men javob beraman.")

# ==== AI Javoblar (oddiy matnlar) ====
@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    if not check_subscription(message.from_user.id):
        bot.send_message(message.chat.id, f"Botdan foydalanish uchun kanalimizga obuna bo‘ling:\n{CHANNEL_ID}")
        return
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response.choices[0].message['content']
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠ Javob olishda xatolik yuz berdi.")

# ==== Flask server (Railway uchun) ====
@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route('/')
def index():
    return "Bot ishlayapti!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.polling(none_stop=True)
