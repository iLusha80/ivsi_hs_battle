from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func

from app import db
from app.models import Game


@dataclass
class TotalScore:
    total_score: int
    txt_score: str
    score_color: str



def get_total_score(start_data: str = '2024-01-01') -> TotalScore:
    """

    :param start_data:
    :return:
    """
    start_date = datetime.strptime(start_data, '%Y-%m-%d')

    total_score = db.session.query(
        func.sum(Game.player1_place - Game.player2_place)
    ).filter(
        Game.timestamp >= start_date
    ).scalar() or 0

    if total_score > 0:
        txt_score = f'-{total_score}'
        score_color = 'red'
    elif total_score < 0:
        txt_score = f'+{-total_score}'
        score_color = 'green'
    else:
        txt_score = '0'
        score_color = 'yellow'

    return TotalScore(total_score=total_score, txt_score=txt_score, score_color=score_color)