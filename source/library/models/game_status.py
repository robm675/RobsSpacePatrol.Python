from enum import Enum


class GameStatus(Enum):
    NORMAL = 0
    STARSHIP_DESTROYED = 1
    RAN_OUT_OF_ENERGY = 2
    RAN_OUT_OF_TIME = 3
    OUT_OF_ENERGY_SHIELD_ENERGY_AVAILABLE = 4
    MISSION_OVER = 5
