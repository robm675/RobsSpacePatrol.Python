from dataclasses import dataclass

from models import coord


@dataclass
class EnemyMoved:
    EnemyCoord_Orig: coord.Coord
    EnemyCoord_Dest: coord.Coord
    