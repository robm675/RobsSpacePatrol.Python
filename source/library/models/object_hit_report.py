from dataclasses import dataclass

from models import coord, object_hit


@dataclass
class ObjectHitReport:
    object_hit: object_hit.ObjectHit
    destroyed: bool
    coord: coord.Coord
    shield_remaining: int
    unit_hit: int
    missed: bool
    star_survived: bool
