# region imports
from random import Random
import sys

from source.library.models.sectorContents import SectorContents

sys.path.append("/pythontrek/source/library/factories/")
sys.path.append("/pythontrek/source/library/")
sys.path.append("/pythontrek/source/")
import randomFactory as rf
import source.library.models.quadrant as quadrant
import source.library.models.coord as coord
import gbl as gbl
from source.library.models.currentQuadrant import CurrentQuadrant
from source.library.models.sector import Sector
from source.library.models.enemy import Enemy
# endregion

class CurrentQuadrantFactory:
    @staticmethod
    def GetRandomEmptySector(rf: rf.RandomFactory, currentQuadrant: CurrentQuadrant, randomCoordType: str ):
        count = 0
        while True:
            coord = rf.GetRandomCoord(randomCoordType)

            chosenSector = currentQuadrant.GetSector(coord.x, coord.y)

            count+=1
            if count > 10:
                raise Exception("Tried 10 times and failed to find an empty sector")

            if chosenSector.sectorContents.isEmpty():
                return chosenSector

    @staticmethod
    def CreateCurrentQuadrant(quadrant: quadrant.Quadrant, rf: rf.RandomFactory, entSectorCoord: coord.Coord):
        sectors = []

        x = 0
        while x < gbl.MAX_QUADRANT_SECTOR_XY:
            y = 0
            while y < gbl.MAX_QUADRANT_SECTOR_XY:
                sectors.append(Sector(coord.Coord(x, y), SectorContents(gbl.SECTOR_EMPTY)))
                y += 1
            x += 1
        
        curQuad = CurrentQuadrant(quadrant.Coord, sectors)

        # print(f"sectorcount: {len(sectors)}")
        # print(f"entSector.x: {entSectorCoord.x}")
        # print(f"entSector.y: {entSectorCoord.y}")

        entSector = next(sect for sect in sectors if sect.coord.x == entSectorCoord.x and sect.coord.y == entSectorCoord.y )
        entSectorTemp:Sector  = entSector
        entSectorTemp.sectorContents.sectorContents = gbl.SECTOR_STARSHIP

        for count in range(quadrant.NumStars):
            targetSector = CurrentQuadrantFactory.GetRandomEmptySector(rf, curQuad, gbl.RCT_STAR_LOCATION)
            targetSector.sectorContents.sectorContents = gbl.SECTOR_STAR

        if quadrant.HasStarBase:
            targetSector = CurrentQuadrantFactory.GetRandomEmptySector(rf, curQuad, gbl.RCT_STARBASE_LOCATION)
            targetSector.sectorContents.sectorContents = gbl.SECTOR_STARBASE

        if quadrant.NumEnemies > 0:
            for enemy in range(quadrant.NumEnemies):
                targetSector = CurrentQuadrantFactory.GetRandomEmptySector(rf, curQuad, gbl.RCT_ENEMY_LOCATION)
                targetSector.sectorContents.sectorContents = gbl.SECTOR_ENEMY
                newShieldLevel = rf.GetRandomInteger(gbl.RIT_ENEMY_SHIELD_LEVEL)
                targetSector.enemy = Enemy(newShieldLevel)

        quadrant.HasBeenExplored = True

        return curQuad