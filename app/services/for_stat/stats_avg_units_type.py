import pandas as pd
import plotly.express as px
import json
import plotly

def generate_hero_stats_plot():
    # Здесь должна быть логика для получения статистики по героям
    # Временные данные для примера
    data = {'hero': ['Герой A', 'Герой B', 'Герой C'],
            'wins': [50, 30, 20]}
    df = pd.DataFrame(data)

    fig = px.bar(df, x='hero', y='wins', title='Статистика по героям', labels={'hero': 'Герой', 'wins': 'Количество побед'}, template="plotly_dark")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def generate_jiro_stats_plot():
    # Здесь должна быть логика для получения среднего места по героям
    # Временные данные для примера
    data = {'hero': ['Герой A', 'Герой B', 'Герой C'],
            'avg_place': [2.5, 3.0, 3.5]}
    df = pd.DataFrame(data)

    fig = px.line(df, x='hero', y='avg_place', title='Среднее место по героям', labels={'hero': 'Герой', 'avg_place': 'Среднее место'}, template="plotly_dark")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def generate_unit_types_circle():
    # Здесь должна быть логика для получения типов юнитов
    # Временные данные для примера
    data = {'unit_type': ['Тип 1', 'Тип 2', 'Тип 3'],
            'count': [40, 30, 30]}
    df = pd.DataFrame(data)

    fig = px.pie(df, values='count', names='unit_type', title='Типы юнитов', labels={'unit_type': 'Тип юнита', 'count': 'Количество'}, template="plotly_dark")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON