from dataclasses import dataclass

from models import coord, objectHit


@dataclass
class ObjectHitReport:
    ObjectHit: objectHit.ObjectHit
    Destroyed: bool
    Coord: coord.Coord
    ShieldRemaining: int
    UnitHit: int
    Missed: bool
    StarSurvived: bool
