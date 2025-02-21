import pandas as pd
import plotly.express as px
import json
import plotly

def generate_top_heroes_plot():
    # Здесь должна быть логика для получения данных о самых популярных героях
    # Временные данные для примера
    data = {'hero': ['Герой 1', 'Герой 2', 'Герой 3', 'Герой 4', 'Герой 5'],
            'count': [100, 80, 60, 40, 20]}
    df = pd.DataFrame(data)

    fig = px.bar(df, x='hero', y='count', title='Топ-5 самых популярных героев', labels={'hero': 'Герой', 'count': 'Количество'}, template="plotly_dark")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON