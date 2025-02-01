from typing import List, Set
import sqlite3


def super_search(search_input: str, db: sqlite3.Connection) -> Set[str]:
    """
    Выполняет поиск героев по имени или части имени.
    :param search_input: Строка для поиска.
    :param db: Соединение с базой данных SQLite.
    :return: Список строк, соответствующих критериям поиска.
    """
    # Преобразуем входные данные в нижний регистр для сравнения без учета регистра
    search_input = search_input.lower()

    # SQL-запрос для получения всех имен героев
    cursor = db.cursor()
    cursor.execute("SELECT name FROM heroes")
    all_names = [row[0] for row in cursor.fetchall()]

    # Результаты поиска
    results = []

    # 1. Точное совпадение
    exact_match = [name for name in all_names if name.lower() == search_input]
    if exact_match:
        return set(exact_match)

    # 2. Начинается с search_input
    starts_with = [name for name in all_names if name.lower().startswith(search_input)]
    if starts_with:
        results.extend(starts_with)

    # 3. Хотя бы одно слово начинается с search_input
    contains_word_starting_with = [
        name for name in all_names
        if any(word.lower().startswith(search_input) for word in name.split())
    ]
    if contains_word_starting_with:
        results.extend(contains_word_starting_with)

    # 4. Содержит search_input
    contains = [name for name in all_names if search_input in name.lower()]
    if contains:
        results.extend(contains)

    # Удаляем дубликаты и возвращаем результат
    return set(results)