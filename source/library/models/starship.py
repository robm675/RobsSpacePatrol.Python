# region imports
from enum import Enum

import source.library.models.device as dev
from source import gbl

# endregion


class eDevice(Enum):
    COM = 1
    LRS = 2 
    SRS = 3
    TOR = 4
    LAS = 5
    NAV = 6
    SHE = 7

class Starship:
    devices: list[dev.Device]

    def __init__(self):
        self.energyLevel = gbl.MAX_STARSHIP_ENERGY
        self.shieldLevel = 0
        self.torpsRemain = gbl.MAX_STARSHIP_TORP
        self.isDocked = False
        self.isDestroyed = False
        self.devices=[]
        for device in eDevice:
            newDevice = dev.Device(device.name, 0)
            self.devices.append(newDevice)

    def GetDevice(self, device: eDevice) -> dev.Device:
        data = [s for s in self.devices if s.name == device.name]
        return data[0]

    def GetDamgedDevices(self) -> list[dev.Device]:
        data = [s for s in self.devices if s.damageLevel < 0]
        if len(data) == 0:
            return []
        return data

    def UseTorpedo(self) -> None:
        self.torpsRemain -= 1

    def GetDeviceByStr(self, device:str) -> dev.Device:
        targetDev = eDevice[device]
        return self.GetDevice(targetDev)
