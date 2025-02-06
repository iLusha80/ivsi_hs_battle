import dataclasses
import json
from typing import Dict, Any

from flask import Blueprint, render_template

from app.services.stats_utils import generate_hero_stats_plot, generate_jiro_stats_plot

statistics_bp = Blueprint('statistics', __name__)

@dataclasses.dataclass
class DataStatBase:
    plot_name: str
    html_id: int
    json_plotly_data: Dict[str, Any]

@statistics_bp.route('/statistics')
def statistics():

    plot_name = 'Тестовое название'
    html_id = 'tst_plot'
    hero_plot = generate_hero_stats_plot()
    top4_data = DataStatBase(plot_name=plot_name, html_id=html_id, json_plotly_data=hero_plot)
    # jiro plot
    plot_name = 'Среднее место по героям'
    html_id = 'jiro_plot'
    jiro_plot = generate_jiro_stats_plot()
    jiro_data = DataStatBase(plot_name=plot_name, html_id=html_id, json_plotly_data=jiro_plot)

    data = [top4_data, jiro_data]

    return render_template('statistics.html',
                           data_list=data,
                           )