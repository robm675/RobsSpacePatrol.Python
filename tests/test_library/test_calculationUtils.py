# region imports
import sys
from unittest.mock import MagicMock

from models import currentQuadrant
from utils.calculationUtilities import calculationUtils

sys.path.append("/pythontrek/source/library/")
import pytest

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.randomFactory as rf
import source.library.models.sectorContents as sc
import source.library.utils.calculationUtilities as cu
from source import gbl
from source.library.models import coord, quadrant, sector

from source.library.factories.randomFactory import RandomFactory
from tests.randomFactoryBuilder import RandomFactoryBuilder

# endregion


def create_random_factory() -> RandomFactory:
    """Provide the empty-sector lookup's expected coordinate (1, 2)."""
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipSector(1, 2)
        .Build()
    )

# for path in sys.path:
#     print(path)

def test_qs2univ():
    result = cu.calculationUtils.QS2Univ(1,2)
    assert result == 10

@pytest.mark.parametrize("univ, q, s", [
    (11, 1, 3),
    (12, 1, 4),
    (15, 1, 7),
    (16, 2, 0),
    (63, 7, 7),
])
def test_univ2qs(univ: int, q: int, s:int):
    result = cu.calculationUtils.Univ2QS(univ)
    assert result.quad == q
    assert result.sect == s

def test_Univ2QSCoord():
    univX = cu.calculationUtils.QS2Univ(1,5)
    univY = cu.calculationUtils.QS2Univ(3,4)
    result = cu.calculationUtils.Univ2QSCoord(univX, univY)

    # print(univX)
    # print(univY)

    assert 1 == result.quadrant.x
    assert 5 == result.sector.x
    assert 3 == result.quadrant.y
    assert 4 == result.sector.y

def test_Univ2QSCoord_Negative():
    univX = cu.calculationUtils.QS2Univ(-1,-5)
    univY = cu.calculationUtils.QS2Univ(-3,-4)
    result = cu.calculationUtils.Univ2QSCoord(univX, univY)

    # print(univX)
    # print(univY)

    assert result.quadrant.x == -1
    assert result.sector.x == -5
    assert result.quadrant.y == -3
    assert result.sector.y == -4

def test_GetDistance():
    coord1X = 1
    coord1Y = 2
    coord2X = 3
    coord2Y = 7
    
    result = cu.calculationUtils.GetDistance(coord.Coord(coord1X, coord1Y), coord.Coord(coord2X, coord2Y))

    assert 5.4 == result

def test_GetDistance_SmallDistance():
    coord1X = 0
    coord1Y = 0
    coord2X = 0
    coord2Y = 1

    result = cu.calculationUtils.GetDistance(coord.Coord(coord1X, coord1Y), coord.Coord(coord2X, coord2Y))

    assert result == 1

@pytest.mark.parametrize("x1, y1, x2, y2, expecteddir",[
    (3,3,4,3,1.0),
    
    (3,3,4,2,2.0),
    (3,3,3,2,3.0),
    (3,3,2,2,4.0),

    (3,3,2,3,5.0),

    (3,3,2,4,6.0),
    (3,3,3,4,7.0),
    (3,3,4,4,8.0)
])
def test_GetDirection(x1: int, y1:int, x2:int, y2:int, expecteddir: float):
    result = cu.calculationUtils.GetDirection(coord.Coord(x1, y1), coord.Coord(x2, y2))
    assert expecteddir == result

def test_GetEnemyShieldHit():
    numEnemies = 2
    energyOfShot = 500
    distToEnemy = 10
    energyFactorToReduce = 5
    enemyShieldHit = cu.calculationUtils.GetEnemyShieldHit(numEnemies, energyOfShot, distToEnemy, energyFactorToReduce)

    assert 200 == enemyShieldHit

def test_CalculateStarshipHitFromEnemy():
    randomEnemyFiredAmount = 300
    distance = 10
    energyFactorToReducePerSector = 5

    result = cu.calculationUtils.CalculateStarshipHitFromEnemy(randomEnemyFiredAmount, distance, energyFactorToReducePerSector)

    assert 250 == result

def test_Dist2Energy():
    result = cu.calculationUtils.DistanceToEnergy(5.4)
    assert int(5.4 * gbl.SECTOR_TO_ENERGY_CONV) == result

def test_Dist2EnergyCoord():
    result = cu.calculationUtils.DistanceToEnergyCoord(coord.Coord(1,2), coord.Coord(3,7))

    assert 21 == result

@pytest.mark.parametrize("sx, sy, qx, qy, dir, dist, finalSX, finalSY, finalQX, finalQY, outsideGalaxySW",[
    (2,2,2,2, 5.0, 4.0, 0,2,0,2, True),
    (6,6,6,6, 1.0, 4.0, 7,6,7,6, True),
    (2,6,2,6, 5.0, 4.0, 0,6,0,6, True),
    (6,1,6,1, 1.0, 4.0, 7,1,7,1, True),

    (7,7,7,7, 7.0, 1.0, 7,7,7,7, True),
    (7,7,7,7, 1.0, 1.0, 7,7,7,7, True),
    (0,0,0,0, 3.0, 1.0, 0,0,0,0, True),
    (0,0,0,0, 5.0, 1.0, 0,0,0,0, True),

    (7,0,7,0, 3.0, 1.0, 7,0,7,0, True),
    (7,0,7,0, 1.0, 1.0, 7,0,7,0, True),
    (0,7,0,7, 5.0, 1.0, 0,7,0,7, True),
    (0,7,0,7, 7.0, 1.0, 0,7,0,7, True),

    (0,0,0,0, 1.0, 1.0, 0,0,1,0, False),
])
def test_GetFinalDestination(sx: int, sy: int, qx:int, qy:int, dir:float, dist:float, finalSX:int, finalSY:int, finalQX: int, finalQY:int, outsideGalaxySW:bool):
    starshipSector = sector.Sector(coord.Coord(sx, sy), sc.SectorContents(gbl.SECTOR_STARSHIP))
    tempSectors = []
    tempSectors.append(starshipSector)

    targetCoord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(targetCoord, 0, 0)

    testMock = rf.RandomFactory()

    curQuad = cqf.CurrentQuadrantFactory.CreateCurrentQuadrant(quad, testMock, coord.Coord(sx, sy))

    fdo = cu.calculationUtils.GetFinalDestination(dir, dist, starshipSector, curQuad)

    assert outsideGalaxySW == fdo.OutSideGalaxy
    assert not fdo.ObjectHit
    assert finalSX == fdo.FinalSector.x
    assert finalSY == fdo.FinalSector.y
    assert finalQX == fdo.FinalQuadrant.x
    assert finalQY == fdo.FinalQuadrant.y

def test_GetRandomEmptySector():
    sectors = []
    x = 0
    while x < gbl.MAX_QUADRANT_SECTOR_XY:
        y = 0
        while y < gbl.MAX_QUADRANT_SECTOR_XY:
            sectors.append(sector.Sector(coord.Coord(x, y), sc.SectorContents(gbl.SECTOR_EMPTY)))
            y += 1
        x += 1

    cq = currentQuadrant.CurrentQuadrant(coord.Coord(1,1), sectors)

    testMock = rf.RandomFactory()
    testMock.GetRandomCoord= MagicMock()
    testMock.GetRandomCoord.side_effect = MockRandomCoord

    emptySector = cqf.CurrentQuadrantFactory.GetRandomEmptySector(testMock, cq, gbl.RCT_STARSHIP_SECTOR)

    assert 1 == emptySector.coord.x
    assert 2 == emptySector.coord.y

def test_Univ2QS():
    estFinalUniX = 0.8
    estFinalUniY = 0.0

    estFinalUniX_Int = round(estFinalUniX)
    estFinalUniY_Int = round(estFinalUniY)

    assert estFinalUniX_Int == 1
    assert estFinalUniY_Int == 0

    res = calculationUtils.Univ2QSCoord(estFinalUniX_Int, estFinalUniY_Int)


    assert res.quadrant.x == 0
    assert res.quadrant.y == 0
    assert res.sector.x == 1
    assert res.sector.y == 0


def MockRandomCoord(randomType: str):
    if randomType == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(1,2)
    return coord.Coord(-1,-1)
