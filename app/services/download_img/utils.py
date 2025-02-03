import json
from typing import List
from transliterate import translit
import re


def translate_to_latin(rus_string: str) -> str:
    cleaned_string = re.sub(r"[^\w\s]", "", rus_string)
    cleaned_string = cleaned_string.lower()
    cleaned_string = cleaned_string.replace(" ", "_")

    # Переводим строку на латиницу
    latin_string = translit(cleaned_string, 'ru', reversed=True)

    return latin_string.replace("'", "")


def read_json_file(file_path: str) -> List:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [(card['name'], translate_to_latin(card['name']), card['battlegrounds']['image'],
             f"{translate_to_latin(card['name'])}.png") for card in data if card['battlegrounds']['hero']]


def check_card_set(set_name: str) -> bool:
    return set_name in read_json_file('data.json')