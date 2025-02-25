from dataclasses import dataclass
from typing import Optional, List

from app.services.utils import get_data_from_query


@dataclass
class IndexStaticPlaceTableRow:
    num_games: str # название строки (кол-во игр) за которые статистика
    pl1: int
    pl2: int
    pl3: int
    pl4: int
    pl5: int
    pl6: int
    pl7: int
    pl8: int
    avg_place: float
    div_count: int

@dataclass
class PlayersStats:
    player1: List[IndexStaticPlaceTableRow]
    player2: List[IndexStaticPlaceTableRow]

def get_player_place_stats(num_games: Optional[int] = None, p: int = 1) -> IndexStaticPlaceTableRow:
    """
    
    Получает статистику по местам игрока за указанное число игр.
    Если num_games не указан, то получает статистику по ВСЕМ играм.
    
    :param num_games: Число игр
    :type num_games: Optional[int]
    :param p: Игрок 1 или 2
    :type p: int
    :return:
    :rtype: IndexStaticPlaceTableRow
    
    """
    # Получаем данные из БД
    if not num_games: num_games = 99_999
    sql_tmp = f"""
    WITH lim_game AS (
        SELECT
            *
         FROM maindata.games g
         ORDER BY g."timestamp" DESC
         LIMIT {num_games}
    )
    SELECT
          {num_games}										AS num_games
        , count(CASE WHEN g.player{p}_place = 1 THEN 1 END) AS pl1
        , count(CASE WHEN g.player{p}_place = 2 THEN 1 END) AS pl2
        , count(CASE WHEN g.player{p}_place = 3 THEN 1 END) AS pl3
        , count(CASE WHEN g.player{p}_place = 4 THEN 1 END) AS pl4
        , count(CASE WHEN g.player{p}_place = 5 THEN 1 END) AS pl5
        , count(CASE WHEN g.player{p}_place = 6 THEN 1 END) AS pl6
        , count(CASE WHEN g.player{p}_place = 7 THEN 1 END) AS pl7
        , count(CASE WHEN g.player{p}_place = 8 THEN 1 END) AS pl8
        , ROUND(avg(g.player{p}_place), 2)  				AS avg_place
        , sum(g.player2_place) - sum(g.player1_place)       AS div_count
    FROM lim_game g
    """

    result = get_data_from_query(sql=sql_tmp)

    return IndexStaticPlaceTableRow(*result[0])

def get_players_all_stats(count_games: int = 99_999):

    player1 = list()
    player2 = list()
    num_games_list = [10, 25, 50, 100, count_games]
    for num_games in num_games_list:
        if num_games <= count_games:
            player1.append(get_player_place_stats(num_games=num_games, p=1))
            player2.append(get_player_place_stats(num_games=num_games, p=2))

    return PlayersStats(player1=player1, player2=player2)
