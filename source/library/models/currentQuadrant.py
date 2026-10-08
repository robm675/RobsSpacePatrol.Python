import uuid

import gbl
from models import coord, sector


class CurrentQuadrant:
    def __init__(self, coord: coord.Coord, sectors:list[sector.Sector]) -> None:
        self.id = uuid.uuid4()
        self.coord = coord
        self.sectors = sectors

    def GetSector(self, x:int, y:int) -> sector.Sector:
        data = [s for s in self.sectors if s.coord.x == x and s.coord.y == y]
        if len(data) == 0:
            raise RuntimeError(f"Sector not found: x={x}, y={y}")

        # print(f"x={x} y={y}")
        return data[0]

    def GetSectorByCoord(self, coord) -> sector.Sector:
        data = [s for s in self.sectors if s.coord.x == coord.x and s.coord.y == coord.y]
        # print(f"x={x} y={y}")
        return data[0]

    def GetSectorByContents(self, secCont: str) -> sector.Sector | None:
        data = [s for s in self.sectors if s.sectorContents.sectorContents == secCont]
        if len(data) == 0:
            return None
        return data[0]

    def GetEnemySectors(self) -> list[sector.Sector] | None:
        data = [s for s in self.sectors if s.sectorContents.sectorContents == gbl.SECTOR_ENEMY]
        if len(data) == 0:
            return None
        return data

    def MoveStarshipToSpecifiedSector(self, newCoord: coord.Coord) -> None:
        sector = self.GetSectorByContents(gbl.SECTOR_STARSHIP)
        if sector is None:
            raise RuntimeError(f"Sector not found: {newCoord}")

        sector.sectorContents.sectorContents = gbl.SECTOR_EMPTY
        newSector = self.GetSectorByCoord(newCoord)
        newSector.sectorContents.sectorContents = gbl.SECTOR_STARSHIP

    def EnemyHit(self, enemyCoord: coord.Coord, unitHit: int) -> bool:
        enemySector = self.GetSectorByCoord(enemyCoord)
        if not enemySector.sectorContents.hasEnemy():
            raise RuntimeError(f"Enemy not found in sector: {enemyCoord.ToString()}")

        if enemySector is None or enemySector.enemy is None or enemySector.enemy.shieldLevel is None:
            raise RuntimeError("EnemySector is null")

        enemySector.enemy.shieldLevel -= unitHit
        return enemySector.enemy.shieldLevel < 0

    def GetSectorsNotEmpty(self) -> list[sector.Sector]:
        data = [s for s in self.sectors if s.sectorContents.sectorContents != gbl.SECTOR_EMPTY]
        return data
