from dataclasses import dataclass
from datetime import datetime


@dataclass
class Hero:
    id: int
    name: str
    image_url: str


@dataclass
class UnitType:
    id: int
    name: str

@dataclass
class Game:
    id: int
    timestamp: datetime
    player1_hero: Hero
    player1_place: int
    player1_unit_type: UnitType
    player2_hero: Hero
    player2_place: int
    player2_unit_type: UnitType
    fl_calculated: int = 0

# Опиши варианты(самые разумные и удобные) структур хранения моделей данных, подключения к базе данных, и функций работы CRUD операций с данными в бд
# при создании веб приложения на Flask
# я не использую ORM
# я использую отдельные запросы и дата классы для обьектов таблиц
# А если прям в модели заложить функции добавления и прочего? можно же расширить дата классы функциями?
