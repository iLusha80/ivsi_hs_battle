import sqlite3
from flask import g

DATABASE = 'games.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                player1_hero TEXT NOT NULL,
                player1_place INTEGER NOT NULL,
                player2_hero TEXT NOT NULL,
                player2_place INTEGER NOT NULL,
                fl_calculated BOOLEAN DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        ''')
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS heroes (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        image_url TEXT DEFAULT NULL
                        )
                       ''')
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS unit_types (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL
                        )
                       ''')
        db.commit()
