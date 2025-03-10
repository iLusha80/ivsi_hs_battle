from flask import Blueprint, render_template
from sqlalchemy import func, text, desc

from .. import db
from ..models import Game, Hero, UnitType

from app.services.index.get_data_and_stats import get_5days_scores
from app.services.index.get_total_score import get_total_score
from app.services.for_test.get_players_places import get_players_all_stats


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    games = db.session.query(Game).order_by(desc(Game.timestamp)).limit(76).all()
    hero_list = Hero.query.all()
    unit_types = UnitType.query.all()

    all_games = Game.query.all()
    count_games = len(all_games)

    total_score = get_total_score()
    scores_5day = get_5days_scores()
    players_stats = get_players_all_stats(count_games=count_games)

    return render_template('index.html',
                           games=games,
                           total_score=total_score,
                           hero_list=hero_list,
                           scores_5day=scores_5day,
                           unit_types=unit_types,
                           player1_stats=players_stats.player1,
                           player2_stats=players_stats.player2,
                           )
