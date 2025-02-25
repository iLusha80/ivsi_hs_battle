from dataclasses import dataclass
from typing import List

from app.services.utils import get_data_from_query


@dataclass
class UnitStat:
    unit_type_name: str
    count_games: int
    avg_place: float
    count_1place: int
    percent_1place: float
    count_top4: int
    percent_top4: float

    def __post_init__(self):
        self.percent_1place = round(self.percent_1place * 100)
        self.percent_top4 = round(self.percent_top4 * 100)

@dataclass
class PlayerStats:
    player1: List[UnitStat]
    player2: List[UnitStat]

def get_player_unit_stats(p: int = 1) -> UnitStat:
    """

    Получает статистику по юнитам игрока.

    :param p: Игрок 1 или 2
    :type p: int
    :return:
    :rtype: PlayerStats

    """
    sql = f"""
    WITH cte AS (
        SELECT
            ut."name"																				AS unit_type_name
            ,count(*)																				AS count_games
            ,ROUND(avg(g.player{p}_place), 2)														AS avg_place
            ,sum(CASE WHEN g.player{p}_place = 1  THEN 1 ELSE 0 END) 								AS count_1place
            ,(sum(CASE WHEN g.player{p}_place = 1 THEN 1 ELSE 0 END)::float)/(count(*)::float)		AS percent_1place
            ,sum(CASE WHEN g.player{p}_place <=4  THEN 1 ELSE 0 END) 								AS count_top4
            ,(sum(CASE WHEN g.player{p}_place <=4 THEN 1 ELSE 0 END)::float)/(count(*)::float)		AS percent_top4
        FROM maindata.games g
        LEFT JOIN maindata.unit_types ut 
            ON g.player{p}_unit_type_id = ut.id
        GROUP BY 1
    )
    SELECT
        unit_type_name
        ,count_games
        ,avg_place
        ,count_1place
        ,ROUND(percent_1place::numeric, 2)	AS percent_1place
        ,count_top4
        ,ROUND(percent_top4::numeric, 2)	AS percent_top4
    FROM cte
    ORDER BY 3;
    """

    sql_result = get_data_from_query(sql=sql)

    result = [UnitStat(*row) for row in sql_result]
    return result

def get_players_all_unit_stats():
    player1 = get_player_unit_stats(p=1)
    player2 = get_player_unit_stats(p=2)

    return PlayerStats(player1, player2)
