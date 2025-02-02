from flask import Blueprint, render_template
from sqlalchemy import func, text, desc

from .. import db
from ..models import Game, Hero, UnitType

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # games = Game.query.all()
    games = db.session.query(Game).order_by(desc(Game.timestamp)).limit(10).all()
    hero_list = Hero.query.all()
    unit_types = UnitType.query.all()

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
            GROUP BY date(timestamp)
            ORDER BY timestamp DESC
            LIMIT 5
    '''

    with db.engine.connect() as conn:
        scores_5day = conn.execute(text(scores_5day_sql)).fetchall()

    return render_template('index.html',
                           games=games,
                           score=txt_score,
                           score_color=score_color,
                           hero_list=hero_list,
                           scores_5day=scores_5day,
                           unit_types=unit_types
                           )