from app import app, db
from app.models import Hero, UnitType, Game

from app.services.download_img.utils import read_json_file


cards = read_json_file('/home/i80/PycharmProjects/ivsi_hs_battle/app/services/download_img/data.json')
with app.app_context():
    db.create_all()
    for card in cards:
        rus_name, lat_name, image_url, save_as = card
        prefix_dir = 'images/heroes/'
        hero = Hero(name=rus_name, image_url=prefix_dir+save_as)
        db.session.add(hero)
        db.session.commit()





print('Done!')
