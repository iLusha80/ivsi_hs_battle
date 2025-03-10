import telebot

from app import app
from app.services.for_test.wins_players_stat import get_players_1x2_stats, Players1x2Stats
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


def get_count_serial_games(str_start_date: str = '2025-03-10'):
    sql = f'''SELECT COUNT(*) FROM maindata.games g WHERE g."timestamp">='{str_start_date}'::date;'''
    count_games = get_data_from_query(sql=sql)

    return count_games[0][0]



def send_result_to_telegram(game: Game, str_start_date: str = '2025-03-10', chat_id: int = -4759747181):

    count_games = get_count_serial_games(str_start_date=str_start_date)
    total_score: TotalScore = get_total_score()
    current_score: TotalScore = get_total_score(start_data=str_start_date)

    total_st1x2: Players1x2Stats = get_players_1x2_stats()
    current_st1x2: Players1x2Stats = get_players_1x2_stats(start_date=str_start_date)

    # если game None, то выбираем игру с максимальным id
    if game is None:
        game = Game.query.order_by(Game.id.desc()).first()


    message = (
        f"🏆 <b>Результат матча #{game.id}</b> 🏆\n"
        f"🕒 <i>{game.timestamp.strftime('%d.%m.%Y %H:%M')}</i>\n\n"
        f"<i>{game.player1_hero.name} | {game.player1_unit_type.name}</i>\n"
        f"{place_emojis[game.player1_place]} <b>{game.player1_place}</b>      🆚      {place_emojis[game.player2_place]} <b>{game.player2_place}</b>\n"
        f"<i>{game.player2_hero.name} | {game.player2_unit_type.name}</i>\n\n"
        f"📊 Текущая серия: {count_games}/30 ({count_games * 3.33}%)\n"
        f'📊 Текущий счет:    <u>{current_score.txt_score}</u>\n'
        f'📈 Текущий 1x2:     {current_st1x2.player1_wins}-{current_st1x2.draw}-{current_st1x2.player2_wins} ({current_st1x2.diff_wins})\n\n'
        f'📈 Общий счет:      <u>{total_score.txt_score}</u>\n'
        f'📈 Общий 1x2:       {total_st1x2.player1_wins}-{total_st1x2.draw}-{total_st1x2.player2_wins} ({total_st1x2.diff_wins})'

    )

    try:
        # Отправка сообщения с HTML-разметкой
        bot.send_message(chat_id, message, parse_mode='HTML')
        print("Сообщение успешно отправлено")
    except Exception as e:
        print(f"Ошибка при отправке: {e}")


with app.app_context():
    send_result_to_telegram(None, chat_id=-4722900052)
