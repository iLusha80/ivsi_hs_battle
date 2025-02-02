from flask import Blueprint, render_template
from flask import request, session, redirect

from .. import config, db
from ..models import Game, Hero, UnitType

add_game_bp = Blueprint('add_game', __name__)

@add_game_bp.route('/add-game', methods=['POST'])
def add_game():
    if not session.get('logged_in'):
        return redirect('/')

    try:
        player1_place = int(request.form['p1_place'])
        player2_place = int(request.form['p2_place'])
        player1_unit_type_id = int(request.form['p1_unit_type'])
        player2_unit_type_id = int(request.form['p2_unit_type'])
        player1_hero_id = int(request.form['p1_hero'])
        player2_hero_id = int(request.form['p2_hero'])

        if not (1 <= player1_place <= 8 and 1 <= player2_place <= 8):
            raise ValueError("Invalid position value")

        game = Game(player1_hero_id=player1_hero_id, player2_hero_id=player2_hero_id,
                    player1_place=player1_place, player2_place=player2_place,
                    player1_unit_type_id=player1_unit_type_id, player2_unit_type_id=player2_unit_type_id)
        db.session.add(game)
        db.session.commit()
        print('-'*66)
        print("Game added successfully!")
        print(game)
        print('-'*66)
    except Exception as e:
        print(f"Error adding game: {str(e)}")

    return redirect('/')