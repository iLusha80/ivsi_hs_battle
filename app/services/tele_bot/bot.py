import telebot

from app import app
from app.services.index.get_total_score import TotalScore, get_total_score
from config import load_config

from app.models import Game
from app.services.utils import get_data_from_query

config = load_config()
# chat_id = -4759747181
# chat_test_id = -4722900052

place_emojis = {
    1: "🥇",  # 1-е место: бриллиант (особый)
    2: "🥈",  # 2-е место: большой оранжевый ромб
    3: "🥉",  # 3-е место: оранжевый ромб
    4: "🏅",  # 4-е место: синий ромб
    5: "😭",  # 5-е место: красный квадрат (ромба нет, но близкий по форме)
    6: "🙈",  # 6-е место: коричневый квадрат
    7: "🐢",  # 7-е место: белый квадрат
    8: "💩"   # 8-е место: чёрный квадрат
}

bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)


def get_count_serial_games(str_start_date: str = '2025-02-25'):
    sql = f'''SELECT COUNT(*) FROM maindata.games g WHERE g."timestamp">='{str_start_date}'::date;'''
    count_games = get_data_from_query(sql=sql)

    return count_games[0][0]



def send_result_to_telegram(game: Game, str_start_date: str = '2025-02-25', chat_id: int = -4759747181):

    count_games = get_count_serial_games(str_start_date=str_start_date)
    total_score: TotalScore = get_total_score()

    # если game None, то выбираем игру с максимальным id
    if game is None:
        game = Game.query.order_by(Game.id.desc()).first()

    message = (
        f"🏆 <b>Результат матча #{game.id}</b> 🏆\n"
        f"🕒 <i>{game.timestamp.strftime('%d.%m.%Y %H:%M')}</i>\n\n"
        f"<i>{game.player1_hero.name} | {game.player1_unit_type.name}</i>\n"
        f"{place_emojis[game.player1_place]} <b>{game.player1_place}</b>      🆚      {place_emojis[game.player2_place]} <b>{game.player2_place}</b>\n"
        f"<i>{game.player2_hero.name} | {game.player2_unit_type.name}</i>\n\n"
        f"📊 Текущая серия: {count_games}/50 ({count_games * 2}%)\n"
        f'📊 Общий счет:      <u>{total_score.txt_score}</u>'
    )

    try:
        # Отправка сообщения с HTML-разметкой
        bot.send_message(chat_id, message, parse_mode='HTML')
        print("Сообщение успешно отправлено")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")


with app.app_context():
    send_result_to_telegram(None, chat_id=-4722900052)