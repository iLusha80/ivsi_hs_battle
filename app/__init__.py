from flask import Flask
from datetime import datetime

from .database import init_db
from ..config import load_config

config = load_config()
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Добавляем фильтр для форматирования даты
@app.template_filter('datetimeformat')
def datetimeformat_filter(value, format='%d.%m.%Y %H:%M'):
    if isinstance(value, str):
        # Конвертируем строку из SQLite в datetime объект
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            return value
    return value.strftime(format)

# Инициализация БД
with app.app_context():
    init_db(app)

from .routers import *  #← Импорт маршрутов после создания app