from flask import Blueprint, render_template
from app.services.for_test.get_players_places import get_player_place_stats

for_test_bp = Blueprint('for_test', __name__)





@for_test_bp.route('/tests')
def tests():
    player1 = get_player_place_stats(p=1)  # Получаем статистику игрока 1
    player2 = get_player_place_stats(p=2)
    return render_template('tests.html', data_stat=[player1, player2])