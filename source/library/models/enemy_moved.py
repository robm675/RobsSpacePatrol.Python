from dataclasses import dataclass

from models import coord


@dataclass
class EnemyMoved:
    enemy_coord_orig: coord.Coord
    enemy_coord_dest: coord.Coord
