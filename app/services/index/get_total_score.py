from dataclasses import dataclass
from sqlalchemy import func

from app import db
from app.models import Game


@dataclass
class TotalScore:
    total_score: int
    txt_score: str
    score_color: str



def get_total_score():
    total_score = db.session.query(
        func.sum(Game.player1_place - Game.player2_place)
    ).scalar() or 0

    if total_score > 0:
        txt_score = f'-{total_score}'
        score_color = 'color:red'
    elif total_score < 0:
        txt_score = f'+{-total_score}'
        score_color = 'color:green'
    else:
        txt_score = '0'
        score_color = 'color:yellow'

    return TotalScore(total_score=total_score, txt_score=txt_score, score_color=score_color)