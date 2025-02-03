from app import app, db
from app.models import Hero, UnitType, Game

from app.services.download_img.utils import read_json_file



with app.app_context():
    db.create_all()
    # Вставка данных для справочника героев
    cards = read_json_file('/home/i80/PycharmProjects/ivsi_hs_battle/app/services/download_img/data.json')
    for card in cards:
        rus_name, lat_name, image_url, save_as = card
        prefix_dir = 'images/heroes/'
        hero = Hero(name=rus_name, image_url=prefix_dir+save_as)
        db.session.add(hero)
        db.session.commit()

inserts_unit_types = """
INSERT INTO unit_types (name, image_url) VALUES
('Смешанные', 'images/unit_types/all.png'),
('Демоны', 'images/unit_types/demons.png'),
('Драконы', 'images/unit_types/dragons.png'),
('Звери', 'images/unit_types/beasts.png'),
('Механизмы', 'images/unit_types/mechs.png'),
('Мурлоки', 'images/unit_types/murlocs.png'),
('Наги', 'images/unit_types/naga.png'),
('Нежить', 'images/unit_types/undead.png'),
('Пираты', 'images/unit_types/pirates.png'),
('Свинобразы', 'images/unit_types/quillboars.png'),
('Элементали', 'images/unit_types/elementals.png');
"""




print('Done!')
