from utils import read_json_file


cards = read_json_file('data.json')

for card in cards:
    rus_name, lat_name, image_url, save_as = card
    print(f"{rus_name}: {lat_name}")
    print(f"Image URL: {image_url}")
    print(f"Save as: {save_as}")
    print('-'*77)