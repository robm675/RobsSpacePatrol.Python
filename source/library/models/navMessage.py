from enum import Enum


class NavMessage(Enum):
    Empty = 0
    BadInput_OutsideGalaxy = 1
    BadInput_ObjectHit = 2
    InsufficientEnergy_ShieldEnergyAvailable = 3
    InsufficientEnergy = 4
    InvalidDIR = 5
    InvalidDIST = 6
    InternalError = 7
    TransitComplete = 8
