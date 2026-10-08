from dataclasses import dataclass

from models import coord


@dataclass
class DirectionToEnemy:
    direction: float
    distance: float
    coord: coord.Coord
