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
