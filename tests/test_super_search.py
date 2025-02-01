import pytest

import sqlite3

from app.services.search import super_search


# : sqlite3.Connection, str
class TestSuperSearch:
    db = sqlite3.connect('/home/i80/PycharmProjects/ivsi_hs_battle/games.db')
    @pytest.mark.parametrize(
        "search_input, db, expected",
        [
            ('Ноздорму', db, {'Ноздорму'}),
            ('Мали', db, {'Малигос'}),
            ('Бра', db, {'Укротитель ящеров Бранн'}),
            ('Рак', db, {'Раканишу', 'Лорд Джараксус'}),
            ('Лор', db, {'Лорд Баров', 'Лорд Джараксус', 'Скаббс Маслорез'}),
            ('Фаэлин', db, {'Посол Фаэлин'})

    ]
    )
    def test_search_heroes(self, search_input, db, expected):
        result = super_search(search_input, self.db)
        assert result == expected
