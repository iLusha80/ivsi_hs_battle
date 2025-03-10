import dataclasses
from typing import Dict, Any

from flask import Blueprint, render_template

from app.services.for_stat.stats_avg_sly import generate_scl_sr_data_plot

statistics_bp = Blueprint('statistics', __name__)

@dataclasses.dataclass
class DataStatBase:
    plot_name: str
    html_id: str
    json_plotly_data: Dict[str, Any]
    width: int = 0

@statistics_bp.route('/statistics')
def statistics():
    plot_name = 'Скользунберг'
    json_plotly_data = generate_scl_sr_data_plot()
    html_id = 'scl_sr'
    data = DataStatBase(plot_name=plot_name, html_id=html_id, json_plotly_data=json_plotly_data)

    print(json_plotly_data)

    return render_template('statistics.html', data=data)