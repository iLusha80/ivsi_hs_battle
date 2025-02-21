import dataclasses
import json
from typing import Dict, Any
import importlib

from flask import Blueprint, render_template

statistics_bp = Blueprint('statistics', __name__)

@dataclasses.dataclass
class DataStatBase:
    plot_name: str
    html_id: str
    json_plotly_data: Dict[str, Any]
    width: int

@statistics_bp.route('/statistics')
def statistics():
    with open('app/static/data/statistic_config.json', 'r') as f:
        config = json.load(f)

    data = []
    for item in config:
        module_name = item['module']
        function_name = item['function']
        plot_name = item['name']
        html_id = item['id']
        width = item['width']

        module = importlib.import_module(f'app.services.for_stat.{module_name}')
        generate_plot = getattr(module, function_name)
        plot_data = generate_plot()

        data_item = DataStatBase(plot_name=plot_name, html_id=html_id, json_plotly_data=plot_data, width=width)
        data.append(data_item)

    return render_template('statistics.html', data_list=data)