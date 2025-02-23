from dataclasses import dataclass

from flask import Blueprint, render_template
from flask import request, session, redirect

from .. import config

for_test_bp = Blueprint('for_test', __name__)


@dataclass
class indxStaticPlaceTableRow:
    name_games: str # название строки (кол-во игр) за которые статистика
    pl1: int
    pl2: int
    pl3: int
    pl4: int
    pl5: int
    pl6: int
    pl7: int
    pl8: int
    avg_place: float


@for_test_bp.route('/tests')
def tests():
    data_stat = list()
    player1 = indxStaticPlaceTableRow(name_games='Все игры (120)',
                                       pl1=12, pl2=10, pl3=8, pl4=6, pl5=4, pl6=2, pl7=0, pl8=0,
                                       avg_place=6.0)

    return render_template('tests.html', data_stat=[player1])