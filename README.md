# Описание проекта

Этот проект представляет собой веб-приложение для учета игровой статистики.

## Модели данных

### Hero

Модель Hero представляет героя в игре.

**Поля:**

*   `id` (Integer, primary\_key=True): Уникальный идентификатор героя.
*   `name` (String(128), nullable=False): Имя героя.
*   `image_url` (String(256)): URL изображения героя.

### UnitType

Модель UnitType представляет тип юнита в игре.

**Поля:**

*   `id` (Integer, primary\_key=True): Уникальный идентификатор типа юнита.
*   `name` (String(128), nullable=False): Имя типа юнита.
*   `image_url` (String(256)): URL изображения типа юнита.

### Game

Модель Game представляет игровую сессию.

**Поля:**

*   `id` (Integer, primary\_key=True): Уникальный идентификатор игры.
*   `timestamp` (DateTime, nullable=False, default=db.func.current\_timestamp()): Временная метка игры.
*   `player1_hero_id` (Integer, db.ForeignKey('heroes.id')): ID героя первого игрока.
*   `player1_place` (Integer, nullable=False): Место первого игрока.
*   `player1_unit_type_id` (Integer, db.ForeignKey('unit_types.id')): ID типа юнита первого игрока.
*   `player2_hero_id` (Integer, db.ForeignKey('heroes.id')): ID героя второго игрока.
*   `player2_place` (Integer, nullable=False): Место второго игрока.
*   `player2_unit_type_id` (Integer, db.ForeignKey('unit_types.id'), default=1): ID типа юнита второго игрока.
*   `fl_calculated` (Boolean, default=False): Флаг, указывающий, рассчитана ли игра.

**Отношения:**

*   `player1_hero` (Hero): Герой первого игрока.
*   `player2_hero` (Hero): Герой второго игрока.
*   `player1_unit_type` (UnitType): Тип юнита первого игрока.
*   `player2_unit_type` (UnitType): Тип юнита второго игрока.