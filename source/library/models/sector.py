import uuid

import gbl
from models import coord, enemy, sectorContents


class Sector:
    def __init__(self, coord: coord.Coord, sectorContents: sectorContents.SectorContents, enemyShieldLevel: int = 0):
        self.id = uuid.uuid4()
        self.sectorContents = sectorContents
        if enemyShieldLevel != 0:
            self.enemy = enemy.Enemy(enemyShieldLevel)
        else:
            self.enemy = None
        self.coord = coord

    def hasEnemy(self) -> bool:
        return enemy is not None
    
    def setEnemy(self, shieldLevel: int):
        self.enemy = enemy.Enemy(shieldLevel)
        self.sectorContents.sectorContents = gbl.SECTOR_ENEMY