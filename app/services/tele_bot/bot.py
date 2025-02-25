import telebot

from config import load_config

from app.models import Game

config = load_config()
chat_id = -4759747181

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)

def send_result_to_telegram(game: Game):
    message = (f"🏆 *Результат матча #{game.id}* 🏆\n"
               f"🕒 _{game.timestamp.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
               f"{game.player1_hero.name} | {game.player1_unit_type.name}\n"
               f"{game.player1_place} 🆚 {game.player2_place}\n"
               f"{game.player2_hero.name} | {game.player2_unit_type.name}" )


    try:
        # Отправка сообщения
        bot.send_message(chat_id, message, parse_mode='Markdown')
        print("Сообщение успешно отправлено")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")

