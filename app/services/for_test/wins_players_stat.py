from dataclasses import dataclass

from app.services.utils import get_data_from_query


@dataclass
class Players1x2Stats:
    player1_wins: int
    draw: int
    player2_wins: int
    total_games: int

    def __post_init__(self):
        self.diff_wins = self.player1_wins - self.player2_wins


def get_players_1x2_stats(start_date: str = '2024-01-01', end_date: str = '2999-12-30') -> Players1x2Stats:
    """
    
    :param start_date:
    :param end_date:
    :return:
    """
    sql = f"""
    SELECT
        COALESCE(SUM(CASE WHEN player1_place < player2_place THEN 1 ELSE 0 END), 0) AS player1_wins,
        COALESCE(SUM(CASE WHEN player1_place = player2_place THEN 1 ELSE 0 END), 0) AS draw,
        COALESCE(SUM(CASE WHEN player1_place > player2_place THEN 1 ELSE 0 END), 0) AS player2_wins,
        COUNT(*) AS total_games
    FROM maindata.games g
    WHERE g."timestamp" BETWEEN '{start_date}'::date AND '{end_date}'::date;
    """

    result = get_data_from_query(sql=sql)

    return Players1x2Stats(*result[0])
