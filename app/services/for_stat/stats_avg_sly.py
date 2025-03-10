import json
import pandas as pd
import plotly.graph_objects as go
import plotly

from app.services.utils import get_data_from_query


def get_scl_sr_data():
    sql = '''
            SELECT
                "timestamp",
                player1_place,
                AVG(player1_place) OVER (
                    ORDER BY "timestamp"
                    ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
                )                                               AS scl_sr_10game
            FROM maindata.games
            ORDER BY 1;
    '''
    fetch_all_rows = get_data_from_query(sql=sql)

    if not fetch_all_rows:
        return {'date_time': [], 'player1_place': [], 'scl_sr_10game': []}

    data = {
        'date_time': [],
        'player1_place': [],
        'scl_sr_10game': []
    }

    for row in fetch_all_rows:
        data['date_time'].append(row[0])
        data['player1_place'].append(row[1])
        data['scl_sr_10game'].append(row[2])
    return data


def generate_scl_sr_data_plot():
    import pandas as pd
    import plotly.graph_objects as go
    import plotly
    # data = {
    #     'date_time': [],
    #     'player1_place': [],
    #     'scl_sr_10game': []
    # }

    data = get_scl_sr_data()

    del data['date_time']

    # Преобразуем данные в DataFrame, добавляя индекс как "номер наблюдения"
    df = pd.DataFrame(data)
    df.index = range(1, len(df) + 1)  # Индексы начинаются с 1 для удобства

    # Проверяем, что данные не пустые
    if df.empty:
        raise ValueError("Данные пусты, проверьте функцию get_scl_sr_data()")

    # Сохраняем DataFrame в CSV
    df.to_csv('TODOs/data_scl_sr.csv', index_label='Observation')

    # Создаем фигуру
    fig = go.Figure()

    # Добавляем гистограмму для player1_place
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['player1_place'],
        name='Место игрока',
        marker_color='blue',
        hovertemplate='<b>Номер наблюдения</b>: %{x}<br><b>Место</b>: %{y}'
    ))

    # Добавляем линию для scl_sr_10game
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['scl_sr_10game'],
        mode='lines',  # Только линия
        name='Среднее за 10 игр',
        line=dict(color='red', width=2),
        hovertemplate='<b>Номер наблюдения</b>: %{x}<br><b>Среднее</b>: %{y:.2f}'
    ))

    # Настраиваем оформление графика
    fig.update_layout(
        title='Результаты игр и скользящее среднее за 10 игр',
        xaxis_title='Номер наблюдения',
        yaxis_title='Место / Скользящее среднее',
        legend=dict(x=0.01, y=0.99),
        template='plotly_white',
        hovermode='x unified',
        yaxis=dict(range=[0, 10]),  # Устанавливаем пределы Y от 0 до 10, чтобы вместить места 1-8
        barmode='overlay'  # Убедимся, что гистограмма не перекрывает линию
    )

    # Преобразуем фигуру в JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
