from flask import Blueprint, render_template
from app.services.for_test.get_players_unit_stats import get_players_all_unit_stats

for_test_bp = Blueprint('for_test', __name__)


@for_test_bp.route('/tests')
def tests():
    players_unit_stat = get_players_all_unit_stats()
    return render_template('tests.html',
                           players_unit_stat=players_unit_stat
                           )