from app import db

# get result from database from query rerutn fetchall

def fetch_data_from_query(query: str, db):
    result = db.session.execute(query).fetchall()
    return result
