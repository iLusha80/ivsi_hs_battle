from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import load_config

config = load_config()

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# app.secret_key = config.SECRET_KEY

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
    db.create_all()

from .routers import register_routes #← Импорт маршрутов после создания app
register_routes(app)
