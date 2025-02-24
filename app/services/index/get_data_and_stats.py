from dataclasses import dataclass
from typing import List

from app.services.utils import get_data_from_query

@dataclass
class DayScore:
    day: str
    score: int
    score_color: str


def get_5days_scores() -> List[DayScore]:
    scores_5day_sql = '''
            SELECT
                date(timestamp)                             as day,
                -1*SUM(player1_place - player2_place)       as score,
                CASE
                    WHEN SUM(player1_place - player2_place) < 0 THEN 'color:green'
                    WHEN SUM(player1_place - player2_place) > 0 THEN 'color:red'
                    ELSE 'color:yellow'
                END score_color
            FROM games
            GROUP BY 1
            ORDER BY 1 DESC
            LIMIT 5
    '''
    scores_5day = get_data_from_query(sql=scores_5day_sql)

    return [DayScore(*row) for row in scores_5day]
