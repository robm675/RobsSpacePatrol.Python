import uuid

import gbl
from models import coord, enemy, sector_contents


class Sector:
    def __init__(
        self,
        coord: coord.Coord,
        sector_contents: sector_contents.SectorContents,
        enemy_shield_level: int = 0,
    ):
        self.id = uuid.uuid4()
        self.sector_contents = sector_contents
        if enemy_shield_level != 0:
            self.enemy = enemy.Enemy(enemy_shield_level)
        else:
            self.enemy = None
        self.coord = coord

    def has_enemy(self) -> bool:
        return enemy is not None

    def set_enemy(self, shield_level: int):
        self.enemy = enemy.Enemy(shield_level)
        self.sector_contents.sector_contents = gbl.SECTOR_ENEMY
