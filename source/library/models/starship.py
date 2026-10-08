from enum import Enum

import source.library.models.device as dev
from source import gbl


class DeviceType(Enum):
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
        self.energy_level = gbl.MAX_STARSHIP_ENERGY
        self.shield_level = 0
        self.torps_remain = gbl.MAX_STARSHIP_TORP
        self.is_docked = False
        self.is_destroyed = False
        self.devices = []
        for device in DeviceType:
            new_device = dev.Device(device.name, 0)
            self.devices.append(new_device)

    def get_device(self, device: DeviceType) -> dev.Device:
        data = [s for s in self.devices if s.name == device.name]
        return data[0]

    def get_damaged_devices(self) -> list[dev.Device]:
        data = [s for s in self.devices if s.damage_level < 0]
        if len(data) == 0:
            return []
        return data

    def use_torpedo(self) -> None:
        self.torps_remain -= 1

    def get_device_by_str(self, device: str) -> dev.Device:
        target_dev = DeviceType[device]
        return self.get_device(target_dev)
