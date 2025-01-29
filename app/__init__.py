from flask import Flask
from .database import init_db
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'u12y31oi23g12p;983gt1:2p98tg3i1uge1'

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