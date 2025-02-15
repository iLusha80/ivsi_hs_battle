from collections import defaultdict

import plotly
import plotly.graph_objs as go
import json

from app.models import Game

import plotly.graph_objs as go
import numpy as np
import json
from typing import Dict, Any, List


class PlotlyGraphs:
    def __init__(self, hero_stats: Dict[str, Any], y: List[int|float] = []):
        self.hero_stats = hero_stats
        self.x = list(hero_stats.keys())
        self.y = y if y else [stats['top4'] / stats['games'] for stats in hero_stats.values()]

    def classic_dark_blue(self) -> go.Figure:
        """Классический темно-синий стиль с градиентом"""
        fig = go.Figure(data=[
            go.Bar(
                x=self.x,
                y=self.y,
                name='Винрейт',
                marker_color='#1f77b4',
                marker=dict(
                    line=dict(color='#0a3d62', width=1.5),
                    opacity=0.9
                )
            )
        ])
        self._apply_base_layout(fig, "Классический стиль")
        return fig

    def shadow_accent(self) -> go.Figure:
        """Стиль с тенями и акцентами"""
        fig = go.Figure(data=[
            go.Bar(
                x=self.x,
                y=self.y,
                name='Винрейт',
                marker=dict(
                    color='#003366',
                    line=dict(color='#001a33', width=2),
                    opacity=0.85
                )
            )
        ])
        self._apply_base_layout(fig, "Стиль с тенями")
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0.1)')
        return fig

    def horizontal_gradient(self) -> go.Figure:
        """Горизонтальные бары с градиентом"""
        fig = go.Figure(data=[
            go.Bar(
                y=self.x,
                x=self.y,
                name='Винрейт',
                orientation='h',
                marker=dict(
                    color=self.y,
                    colorscale='Blues',
                    line=dict(color='#003366', width=1)
                )
            )
        ])
        self._apply_base_layout(fig, "Горизонтальные бары")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        return fig

    def highlighted_max(self) -> go.Figure:
        """С подсветкой максимального значения"""
        colors = ['#003366'] * len(self.x)
        max_idx = self.y.index(max(self.y))
        colors[max_idx] = '#66b3ff'

        fig = go.Figure(data=[
            go.Bar(
                x=self.x,
                y=self.y,
                name='Винрейт',
                marker=dict(
                    color=colors,
                    line=dict(color='#001a33', width=1.5)
                )
            )
        ])
        self._apply_base_layout(fig, "С подсветкой максимума")
        return fig

    def trend_line(self) -> go.Figure:
        """С прозрачными барами и линией тренда"""
        # Линия тренда
        z = np.polyfit(range(len(self.x)), self.y, 1)
        trend = np.poly1d(z)(range(len(self.x)))

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=self.x,
            y=self.y,
            name='Винрейт',
            marker=dict(
                color='#003366',
                opacity=0.7,
                line=dict(width=0)
            )
        ))
        fig.add_trace(go.Scatter(
            x=self.x,
            y=trend,
            name='Тренд',
            line=dict(color='#66b3ff', dash='dot', width=3)
        ))
        self._apply_base_layout(fig, "С линией тренда")
        return fig

    def _apply_base_layout(self, fig: go.Figure, title: str):
        """Базовые настройки для всех графиков"""
        fig.update_layout(
            title=dict(text=title, x=0.5, font=dict(size=20)),
            xaxis=dict(title='Герои', tickangle=-45),
            yaxis=dict(title='Винрейт'),
            template='plotly_dark',
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(b=100),
            hoverlabel=dict(font_size=14)
        )

def generate_hero_stats_plot():
    # Собираем данные из БД
    hero_stats = defaultdict(lambda: {'games': 0, 'top4': 0})
    games = Game.query.all()
    for game in games:
        hero_stats[game.player1_hero.name]['games'] += 1
        hero_stats[game.player2_hero.name]['games'] += 1
        if game.player1_place <= 4:
            hero_stats[game.player1_hero.name]['top4'] += 1
        if game.player2_place <= 4:
            hero_stats[game.player2_hero.name]['top4'] += 1

    # Создаем график
    plotter = PlotlyGraphs(hero_stats)

    fig = plotter.trend_line()

    # Конвертируем в JSON для передачи в шаблон
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON






def generate_jiro_stats_plot():
    """
    Генерация среднегено места по каждому герою
    :return:
    """
    # Собираем данные из БД
    jiro_stats = defaultdict(lambda: {'games': 0,'mean_place': 0})
    games = Game.query.all()
    for game in games:
        jiro_stats[game.player1_hero.name]['games'] += 1
        jiro_stats[game.player2_hero.name]['games'] += 1
        jiro_stats[game.player1_hero.name]['mean_place'] += game.player1_place
        jiro_stats[game.player2_hero.name]['mean_place'] += game.player2_place

    # Считаем среднее место
    for hero_name, stats in jiro_stats.items():
        stats['mean_place'] /= stats['games']

    # Сортируем по среднему значению
    jiro_stats = dict(sorted(jiro_stats.items(), key=lambda item: item[1]['mean_place']))

    # Обрезаем лишние элементы
    jiro_stats = dict(list(jiro_stats.items()))  # Только первые 10 героев с самым большим средним значением места

    # Обрезаем нулевые значения
    jiro_stats = {hero: stats for hero, stats in jiro_stats.items() if stats['mean_place'] > 0}

    # Обрезаем героев, которые не участвовали в играх
    y = [jiro_stats[key]['mean_place'] for key in jiro_stats]

    # Создаем график
    plotter = PlotlyGraphs(jiro_stats, y=y)

    fig = plotter.shadow_accent()

    # Конвертируем в JSON для передачи в шаблон
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def generate_unit_types_circle():
    # Собираем данные из БД
    unit_types = defaultdict(lambda: {'games': 0})
    games = Game.query.all()
    for game in games:
        unit_types[game.player1_unit_type.name]['games'] += 1
        unit_types[game.player2_unit_type.name]['games'] += 1
    # Создаем график
    labels = list(unit_types.keys())
    values = [unit_types[label]['games'] for label in labels]

    # Создаем круговую диаграмму
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    # Настраиваем внешний вид диаграммы
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(line=dict(color='#000000', width=2)))

    fig.update_layout(title_text='Распределение игр по типам юнитов', title_x=0.5)

    # Конвертируем в JSON для передачи в шаблон
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON