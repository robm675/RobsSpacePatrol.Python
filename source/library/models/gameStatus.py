from enum import Enum


class GameStatus(Enum):
    Normal = 0
    StarshipDestroyed = 1
    RanOutOfEnergy = 2
    RanOutOfTime = 3
    OutOfEnergyShieldEnergyAvailable = 4
    MissionOver = 5