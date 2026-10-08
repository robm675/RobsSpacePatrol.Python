from dataclasses import dataclass

from models import coord, device


@dataclass
class EnemyFired:
    EnemyCoord: coord.Coord
    StarshipNewShieldAmount: int
    StarshipDestroyed: bool
    DeviceDamaged: device.Device | None
    EnemyFiredAmount: int
    DeviceDamagedAmount: float | None
    StarshipDocked: bool