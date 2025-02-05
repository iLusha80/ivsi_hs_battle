from flask import Blueprint, render_template, redirect, session
from sqlalchemy import desc

from ..models import Game
from .. import  db

games_bp = Blueprint('games', __name__)

@games_bp.route('/games')
def games():
    games = db.session.query(Game).order_by(desc(Game.timestamp)).all()
    return render_template('games.html',
                           games=games
                           )

@games_bp.route('/games/delete/<int:id>', methods=['POST'])
def delete_game(id):
    if not session.get('logged_in'):
        return redirect('/')
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect('/games')

@games_bp.route('/games/toggle_flag/<int:id>', methods=['POST'])
def toggle_flag(id):
    if not session.get('logged_in'):
        return redirect('/')
    game = Game.query.get_or_404(id)
    # Переключаем значение флага
    game.fl_calculated = not game.fl_calculated
    db.session.commit()
    return redirect('/games')
