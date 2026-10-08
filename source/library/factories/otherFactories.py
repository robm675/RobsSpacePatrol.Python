# region imports
import sys
from unittest import mock
from unittest.mock import MagicMock, patch

from factories.currentQuadrantFactory import CurrentQuadrantFactory
from models import currentQuadrant, galaxy
sys.path.append("/pythontrek/source/library/")
import source.library.models.starship as ent
import source.library.models.coord as coord
import source.library.models.quadrant as q
import source.library.models.galaxy as gal
import factories.randomFactory as rf
import source.gbl as gbl
# endregion

class otherFactories:
    @staticmethod
    def createStarship() -> ent.Starship:
        return ent.Starship()

    @staticmethod
    def createQuadrant(coord: coord.Coord, randFact: rf.RandomFactory):
        numStars = randFact.GetRandomInteger(gbl.RIT_STAR_QUANTITY)
        enemyChance = randFact.GetRandomInteger(gbl.RIT_ENEMY_CHANCE)
        starbaseChance = randFact.GetRandomInteger(gbl.RIT_STARBASE_CHANCE)

        totalEnemies = 0
        if enemyChance > gbl.ENEMY_ZERO_ONE and enemyChance <= gbl.ENEMY_ONE_TWO:
            totalEnemies = 1
        if enemyChance > gbl.ENEMY_ONE_TWO and enemyChance <= gbl.ENEMY_TWO_THREE:
            totalEnemies = 2
        if enemyChance > gbl.ENEMY_TWO_THREE:
            totalEnemies = 3

        newQuadrant = q.Quadrant(coord, totalEnemies, numStars)
        newQuadrant.HasStarBase = False
        if starbaseChance > gbl.STARBASE_CHANCE:
            newQuadrant.HasStarBase = True


        return newQuadrant

    @staticmethod
    def getEnemiesRemaining(galaxy: galaxy.Galaxy) -> int:
        total = sum(p.NumEnemies for p in galaxy.Quadrants)
        return total

    @staticmethod
    def getStars(galaxy: galaxy.Galaxy) -> int:
        total = sum(p.NumStars for p in galaxy.Quadrants)
        return total

    @staticmethod
    def createGalaxy(randFact: rf.RandomFactory, curQuadFactory: CurrentQuadrantFactory) -> galaxy.Galaxy:
        newGalaxy = gal.Galaxy()
        newGalaxy.Quadrants = []

        for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
            for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
                newQuadrant = otherFactories.createQuadrant(coord.Coord(x,y), randFact)
                newGalaxy.Quadrants.append(newQuadrant)

        starshipQuadrantCoord = randFact.GetRandomCoord(gbl.RCT_STARSHIP_QUADRANT)
        starshipSectorCoord = randFact.GetRandomCoord(gbl.RCT_STARSHIP_SECTOR)

        # print(f"starshipQuadCoord x={starshipQuadrantCoord.x} y={starshipSectorCoord.y}")

        entQuadrant = newGalaxy.GetQuadrant(starshipQuadrantCoord.x, starshipQuadrantCoord.y)

        newGalaxy.CurrentQuadrant = curQuadFactory.CreateCurrentQuadrant(entQuadrant, randFact, starshipSectorCoord)

        entQuad = newGalaxy.GetQuadrant(starshipQuadrantCoord.x, starshipQuadrantCoord.y)
        entQuad.HasBeenExplored = True

        newGalaxy.Starship = ent.Starship()
        newGalaxy.MissionTime = 0
        newGalaxy.MissionTimeDeadline = newGalaxy.MissionTime + (otherFactories.getEnemiesRemaining(newGalaxy) * gbl.MISSION_TIME_PER_ENEMY_RATIO)

        return newGalaxy
