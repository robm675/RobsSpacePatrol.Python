from dataclasses import dataclass

from models import coord


@dataclass
class DirectionToEnemy:
    Direction:float
    Distance:float
    Coord: coord.Coord