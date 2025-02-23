from dataclasses import dataclass
from typing import List
from sqlalchemy import text

from app import db

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

    with db.engine.connect() as conn:
        scores_5day = conn.execute(text(scores_5day_sql)).fetchall()

    return [DayScore(*row) for row in scores_5day]
