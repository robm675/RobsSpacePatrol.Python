from dataclasses import dataclass

from models import coord, device


@dataclass
class EnemyFired:
    enemy_coord: coord.Coord
    starship_new_shield_amount: int
    starship_destroyed: bool
    device_damaged: device.Device | None
    enemy_fired_amount: int
    device_damaged_amount: float | None
    starship_docked: bool
