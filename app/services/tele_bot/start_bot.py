import telebot
from config import load_config

config = load_config()

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def get_chat_id(message):
    print(f"Chat ID: {message.chat.id}")

bot.polling()