# import sqlite3
#
# db = sqlite3.connect('games.db')
#
# # # Добавить столбец fl_calculated в базу по умолчанию False
# # cursor = db.cursor()
# # cursor.execute('''
# #     ALTER TABLE games ADD COLUMN fl_calculated BOOLEAN DEFAULT 0
# # ''')
# # db.commit()
# # db.close()
# # print('Added column!')
#
# ################################################################################
#
# # Заполнить таблицу heroes
# # with open('app/static/data/heroes.txt', 'r') as f:
# #     heroes = f.read().splitlines()
# #
# #
# # cursor = db.cursor()
# # cursor.executemany('''
# #     INSERT INTO heroes (name) VALUES (?)
# # ''', [(hero,) for hero in heroes])
# # db.commit()
# # print('Heroes added!')
#
#
# # Заполнить таблицу unit_types
#
# unit_types = [
#     'Смешанные',
#     'Демоны',
#     'Драконы',
#     'Звери',
#     'Механизмы',
#     'Мурлоки',
#     'Наги',
#     'Нежить',
#     'Пираты',
#     'Свинобразы',
#     'Элементали'
# ]
# cursor = db.cursor()
# cursor.executemany('''
#     INSERT INTO unit_types (name) VALUES (?)
# ''', [(unit_type,) for unit_type in unit_types])
# db.commit()
# print('Unit types added!')
#
# db.close()


import sqlite3

db = sqlite3.connect('games.db')

# Добавить столбецы player1_unit_type и player2_unit_type в базу по умолчанию 1
cursor = db.cursor()
cursor.execute('''
    ALTER TABLE games ADD COLUMN player2_unit_type INTEGER DEFAULT 1
''')
db.commit()
print('Added columns!')
