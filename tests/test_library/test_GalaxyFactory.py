# region imports
import sys
from unittest.mock import MagicMock

sys.path.append("/pythontrek/source/library/")

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.otherFactories as otherFact
from source import gbl
from source.library.models import coord
from tests.randomFactoryBuilder import RandomFactoryBuilder

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, quadrant_visits: int = 1) -> RandomFactory:
    """Create the original one-enemy, two-star, starbase galaxy scenario."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3).SetStarshipSector(4, 5)
        .SetStarQuantity(2).SetEnemyChance(76).SetStarbaseChance(96)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((0, 1), (1, 1)) * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *((0, 0),) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .Build()
    )


def test_GalaxyFactory():
    testMock = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetStarQuantity(2)
        .SetStarshipQuadrant(2,3)
        .SetStarshipSector(4,5)
        .SetEnemyChance(76)
        .SetCoords(gbl.RCT_STAR_LOCATION, (7, 6), (7, 7), (6, 6))
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (5, 6), (5, 7), (5, 6))
        .Build()
    )    
    #testMock.GetRandomInteger= MagicMock()
    #testMock.GetRandomInteger.side_effect = MockRandomInt
    #testMock.GetRandomCoord= MagicMock()
    #testMock.GetRandomCoord.side_effect = MockRandomCoord

    curQuad = cqf.CurrentQuadrantFactory()

    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)

    assert len(galaxy.Quadrants) == 64
    assert galaxy.MissionTime == 0
    assert galaxy.CurrentQuadrant.coord.x == 2
    assert galaxy.CurrentQuadrant.coord.y == 3
    assert galaxy.Starship.energyLevel == gbl.MAX_STARSHIP_ENERGY
    assert galaxy.Starship.torpsRemain == gbl.MAX_STARSHIP_TORP
    assert galaxy.Starship.shieldLevel == 0

    entQuad = galaxy.GetQuadrant(2,3)
    assert entQuad.HasBeenExplored == True

    entSector = galaxy.CurrentQuadrant.GetSector(4,5)
    assert entSector.sectorContents.sectorContents == gbl.SECTOR_STARSHIP
    assert otherFact.otherFactories.getEnemiesRemaining(galaxy) == 64
    assert otherFact.otherFactories.getStars(galaxy) == 128

def MockRandomInt(randomType: str):
    if randomType == gbl.RIT_STAR_QUANTITY:
        return 2
    if randomType == gbl.RIT_ENEMY_CHANCE:
        return 76
    if randomType == gbl.RIT_STARBASE_CHANCE:
        return 96
    if randomType == gbl.RIT_STARTING_MISSION_TIME:
        return 2450
    return -1

def MockRandomCoord(randomType: str) -> coord.Coord:
    if randomType == gbl.RCT_STARSHIP_QUADRANT:
        return coord.Coord(2,3)
    if randomType == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(4,5)
    if randomType == gbl.RCT_ENEMY_LOCATION:
        return coord.Coord(0,0)
    if randomType == gbl.RCT_STAR_LOCATION:
        return coord.Coord(0,1)
    if randomType == gbl.RCT_STARBASE_LOCATION:
        return coord.Coord(0,2)
    return coord.Coord(-10,-10)
