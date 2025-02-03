import aiohttp
import asyncio
from time import perf_counter

from utils import read_json_file


async def download_image(image_url: str, save_as: str) -> None:
    """
    Загружает изображение по URL и сохраняет его в указанный файл

    :param image_url: URL изображения
    :param save_as: Путь куда сохранять изображение
    :return:
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url, ssl=False) as response:
                if response.status == 200:
                    with open(save_as, 'wb') as file:
                        file.write(await response.read())
                    print(f"Изображение успешно сохранено как {save_as}")
                else:
                    print(f"Ошибка при скачивании изображения: {response.status}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


async def download_images(cards: list, prefix_dir: str = 'imgs/') -> None:
    """
    Загружает изображения из списка карт

    :param cards: Список карт, где каждый элемент - это кортеж (rus_name, lat_name, image_url, save_as)
    :return:
    """
    tasks = []
    for card in cards:
        rus_name, lat_name, image_url, save_as = card
        save_as = prefix_dir + save_as
        tasks.append(download_image(image_url, save_as))

    # Запускаем все задачи
    await asyncio.gather(*tasks)


cards = read_json_file('data.json')

start_time = perf_counter()


prefix_dir = '/home/i80/PycharmProjects/ivsi_hs_battle/app/static/images/heroes/'

asyncio.run(download_images(cards=cards, prefix_dir=prefix_dir))

end_time = perf_counter()

print(f'Время загрузки изображений: {end_time - start_time:.2f} сек.')
