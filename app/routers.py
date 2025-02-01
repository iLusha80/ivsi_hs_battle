from flask import Flask, render_template, request, redirect, session
from .database import get_db
from . import app


@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    games = cursor.execute('''
        SELECT 
            id,
            datetime(timestamp) as timestamp,
            player1_hero,
            player1_place,
            player2_hero,
            player2_place
        FROM games 
        ORDER BY timestamp DESC 
        LIMIT 10
    ''').fetchall()

    total_score = cursor.execute('''
        SELECT SUM(player1_place - player2_place)
        FROM games
    ''').fetchone()[0] or 0

    scores_5day = cursor.execute('''
    SELECT 
        date(timestamp)                         as day,
        -1*SUM(player1_place - player2_place)   as score,
        CASE
            WHEN SUM(player1_place - player2_place) < 0 THEN 'color:green'
            WHEN SUM(player1_place - player2_place) > 0 THEN 'color:red'
            ELSE 'color:yellow'
        END score_color
    FROM games 
    GROUP BY date(timestamp)
    ORDER BY timestamp DESC 
    LIMIT 5
    ''').fetchall()

    if total_score > 0:
        txt_score = f'-{total_score}'
        score_color = 'color:red'
    elif total_score < 0:
        txt_score = f'+{-total_score}'
        score_color = 'color:green'
    else:
        txt_score = '0'
        score_color = 'color:yellow'

    with open('app/static/data/heroes.txt', 'r') as f:
        hero_list = f.read().splitlines()

    return render_template('index.html',
                           games=games,
                           score=txt_score,
                           score_color=score_color,
                           hero_list=hero_list,
                           scores_5day=scores_5day)


@app.route('/add-game', methods=['POST'])
def add_game():
    if not session.get('logged_in'):
        return redirect('/')

    try:
        p1_place = int(request.form['p1_place'])
        p2_place = int(request.form['p2_place'])

        if not (1 <= p1_place <= 8 and 1 <= p2_place <= 8):
            raise ValueError("Invalid position value")

        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO games 
            (player1_hero, player1_place, player2_hero, player2_place)
            VALUES (?, ?, ?, ?)
        ''', (
            request.form['p1_hero'].strip(),
            p1_place,
            request.form['p2_hero'].strip(),
            p2_place
        ))
        db.commit()

    except Exception as e:
        print(f"Error adding game: {str(e)}")

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == 'admin123':
        session['logged_in'] = True
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')