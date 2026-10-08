# region imports
import sys
from unittest.mock import MagicMock

from models.commandResult import CommandResult
from models.commands import Commands
from models.starship import eDevice
from models.objectHit import ObjectHit
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.otherFactories as otherFact
import source.library.factories.randomFactory as rf
from source import gbl
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, no_enemies: bool = False, laser_miss: bool = False,
                          star_survives: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Configure the laser scenario without negative fallback shield values."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3)
        .SetStarQuantity(2)
        .SetEnemyChance(0 if no_enemies else 100)
        .SetStarbaseChance(0 if no_enemies else 100)
        .SetInteger(gbl.RIT_ENEMY_SHIELD_LEVEL, 300)
        .SetInteger(gbl.RIT_LASER_MISS_CHANCE, 100 if laser_miss else 0)
        .SetInteger(gbl.RIT_STAR_DESTROYED_CHANCE, 0 if star_survives else 100)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *((0, 1), (0, 2), (0, 3)) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .Build()
    )

def find_by_coord(items, x, y):
    return next(
        item for item in items
        if item.Coord.x == x and item.Coord.y == y
)


def test_LAS_ResultsNotNull():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )    
    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.las(10)

    assert result is not None

def test_LAS_HasContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.las(7)

    assert result.CommandResult == CommandResult.OK

def test_LAS_Damaged():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.LAS).damageLevel = -3
    result = gameVar.las(7)

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.LAS

def test_LAS_VerifyContents_HIT_Enemy():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.las(400)

    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.LAS
    assert gameVar.galaxy.Starship.energyLevel == gbl.MAX_STARSHIP_ENERGY - 400

    assert len(result.LAS.ObjectHitReport) == 3
    enemy1 = find_by_coord(result.LAS.ObjectHitReport, 0, 1)
    enemy2 = find_by_coord(result.LAS.ObjectHitReport, 0, 2)
    enemy3 = find_by_coord(result.LAS.ObjectHitReport, 0, 3)

    assert enemy1.Missed is False
    assert enemy1.Missed == False
    assert enemy2.Missed == False
    assert enemy3.Missed == False

    assert enemy1.Destroyed == False
    assert enemy2.Destroyed == False
    assert enemy3.Destroyed == False

    assert enemy1.UnitHit != 0
    assert enemy2.UnitHit != 0
    assert enemy3.UnitHit != 0

    assert enemy1.ObjectHit == ObjectHit.Enemy
    assert enemy2.ObjectHit == ObjectHit.Enemy
    assert enemy3.ObjectHit == ObjectHit.Enemy

def test_LAS_VerifyContents_MISS_Enemy():
    testMock = create_random_factory(laser_miss=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3


    result = gameVar.las(100)


    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.LAS
    assert gameVar.galaxy.Starship.energyLevel == gbl.MAX_STARSHIP_ENERGY - 100

    assert len(result.LAS.ObjectHitReport) == 3
    enemy1 = find_by_coord(result.LAS.ObjectHitReport, 0, 1)
    enemy2 = find_by_coord(result.LAS.ObjectHitReport, 0, 2)
    enemy3 = find_by_coord(result.LAS.ObjectHitReport, 0, 3)    

    assert enemy1.Missed == True
    assert enemy2.Missed == True
    assert enemy3.Missed == True

    assert enemy1.Destroyed == False
    assert enemy2.Destroyed == False
    assert enemy3.Destroyed == False

    assert enemy1.UnitHit == 0
    assert enemy2.UnitHit == 0
    assert enemy3.UnitHit == 0

    assert enemy1.ObjectHit == ObjectHit.Nothing
    assert enemy2.ObjectHit == ObjectHit.Nothing
    assert enemy3.ObjectHit == ObjectHit.Nothing
