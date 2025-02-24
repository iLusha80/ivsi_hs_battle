from app import db
from sqlalchemy import text


def get_data_from_query(sql: str):
    with db.engine.connect() as conn:
        result = conn.execute(text(sql)).fetchall()
    return result
