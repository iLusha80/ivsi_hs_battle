from typing import List, Tuple
from app.models import Hero
from utils import read_json_file
from app import app, db


def update_heroes_dictionary(file_path: str) -> Tuple[int, int]:
    """
    Обновляет справочник героев в базе данных из JSON файла.

    Args:
        file_path (str): Путь к JSON файлу с данными героев

    Returns:
        Tuple[int, int]: Кортеж с количеством добавленных и недобавленных героев
    """
    # Константы лучше вынести отдельно
    IMAGE_PREFIX = 'images/heroes/'

    with app.app_context():
        try:
            # Чтение JSON файла
            cards: List[Tuple[str, str, str, str]] = read_json_file(file_path)

            count_added = 0
            count_not_added = 0

            # Массовое получение существующих имен для минимизации запросов к БД
            existing_heroes = set(
                hero.name for hero in Hero.query.with_entities(Hero.name).all()
            )

            # Список для массовой вставки
            new_heroes = []

            for rus_name, lat_name, image_url, save_as in cards:
                if rus_name in existing_heroes:
                    count_not_added += 1
                    continue

                # Создание объекта без немедленного коммита
                hero = Hero(
                    name=rus_name,
                    image_url=f"{IMAGE_PREFIX}{save_as}"
                )
                new_heroes.append(hero)
                count_added += 1

            # Массовая вставка всех новых героев одним запросом
            if new_heroes:
                db.session.bulk_save_objects(new_heroes)
                db.session.commit()

                for hero in new_heroes:
                    print(f"Hero '{hero.name}' added to database.")

            print('Heroes dictionary Updated!')
            print(f"Added: {count_added}, Not added: {count_not_added}")

            return count_added, count_not_added

        except Exception as e:
            db.session.rollback()
            print(f"Error updating heroes: {str(e)}")
            raise

        finally:
            db.session.close()


if __name__ == "__main__":
    FILE_PATH = '/home/i80/PycharmProjects/ivsi_hs_battle/app/services/download_img/data_2.json'
    update_heroes_dictionary(FILE_PATH)
