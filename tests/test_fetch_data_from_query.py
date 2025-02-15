import pytest
from sqlalchemy import text

from app.services.utils import fetch_data_from_query
from app import db

class TestUtils:
    def test_get_stat_player1(self):
        query = text("""
            SELECT
                 ut."name" 				AS unit_type_name
                ,avg(g.player1_place) 	AS avg_p1_place
                ,count(*)
            FROM maindata.games g 
            JOIN maindata.unit_types ut
                ON g.player1_unit_type_id = ut.id
            GROUP BY 1
            ORDER BY 2;
        """)

        result = fetch_data_from_query(query, db)
        assert len(result) > 0