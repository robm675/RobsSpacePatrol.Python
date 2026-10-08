import uuid

import gbl
from models import coord, sector


class CurrentQuadrant:
    def __init__(self, coord: coord.Coord, sectors: list[sector.Sector]) -> None:
        self.id = uuid.uuid4()
        self.coord = coord
        self.sectors = sectors

    def get_sector(self, x: int, y: int) -> sector.Sector:
        data = [s for s in self.sectors if s.coord.x == x and s.coord.y == y]
        if len(data) == 0:
            raise RuntimeError(f"Sector not found: x={x}, y={y}")
        return data[0]

    def get_sector_by_coord(self, coord) -> sector.Sector:
        data = [s for s in self.sectors if s.coord.x == coord.x and s.coord.y == coord.y]
        return data[0]

    def get_sector_by_contents(self, sec_cont: str) -> sector.Sector | None:
        data = [s for s in self.sectors if s.sector_contents.sector_contents == sec_cont]
        if len(data) == 0:
            return None
        return data[0]

    def get_enemy_sectors(self) -> list[sector.Sector] | None:
        data = [s for s in self.sectors if s.sector_contents.sector_contents == gbl.SECTOR_ENEMY]
        if len(data) == 0:
            return None
        return data

    def move_starship_to_specified_sector(self, new_coord: coord.Coord) -> None:
        sector = self.get_sector_by_contents(gbl.SECTOR_STARSHIP)
        if sector is None:
            raise RuntimeError(f"Sector not found: {new_coord}")

        sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY
        new_sector = self.get_sector_by_coord(new_coord)
        new_sector.sector_contents.sector_contents = gbl.SECTOR_STARSHIP

    def enemy_hit(self, enemy_coord: coord.Coord, unit_hit: int) -> bool:
        enemy_sector = self.get_sector_by_coord(enemy_coord)
        if not enemy_sector.sector_contents.has_enemy():
            raise RuntimeError(f"Enemy not found in sector: {enemy_coord.to_string()}")

        if (
            enemy_sector is None
            or enemy_sector.enemy is None
            or enemy_sector.enemy.shield_level is None
        ):
            raise RuntimeError("EnemySector is null")

        enemy_sector.enemy.shield_level -= unit_hit
        return enemy_sector.enemy.shield_level < 0

    def get_sectors_not_empty(self) -> list[sector.Sector]:
        data = [s for s in self.sectors if s.sector_contents.sector_contents != gbl.SECTOR_EMPTY]
        return data
