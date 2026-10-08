# region imports
import sys
from unittest.mock import MagicMock

from models import objectHit
from models.commandResult import CommandResult
from models.commands import Commands
from models.starship import eDevice
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.otherFactories as otherFact
from source import gbl
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, no_enemies: bool = False, hit_star: bool = False,
                          hit_starbase: bool = False, star_survives: bool = False,
                          quadrant_visits: int = 1) -> RandomFactory:
    """Configure TOR targets while retaining each scenario's first obstacle."""
    if hit_star and hit_starbase:
        raise ValueError("Choose hit_star or hit_starbase, not both")
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    enemies = ((5, 1), (5, 2), (5, 3)) if hit_star or hit_starbase else ((0, 1), (0, 2), (0, 3))
    stars = ((0, 2), (7, 6)) if hit_star else ((4, 2), (7, 6)) if hit_starbase else ((7, 6), (7, 7))
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3)
        .SetStarQuantity(2)
        .SetEnemyChance(0 if no_enemies else 100)
        .SetStarbaseChance(0 if no_enemies else 100)
        .SetInteger(gbl.RIT_STAR_DESTROYED_CHANCE, 0 if star_survives else 100)
        .SetCoords(gbl.RCT_STAR_LOCATION, *stars * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *enemies * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .Build()
    )


def test_TOR_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.tor(0)

    assert result is not None

def test_TOR_HasContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.tor(7)

    assert result.CommandResult == CommandResult.OK

def test_TOR_Damaged():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.TOR).damageLevel = -3
    result = gameVar.tor(7)

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.TOR

def test_TOR_VerifyContents_HIT_Enemy():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.tor(7)

    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.TOR
    assert result.TOR.ObjectHitReport.ObjectHit == objectHit.ObjectHit.Enemy
    assert result.TOR.ObjectHitReport.Destroyed == True
    assert gameVar.galaxy.Starship.torpsRemain == gbl.MAX_STARSHIP_TORP -1
    assert result.TOR.ObjectHitReport.Coord.x == 0
    assert result.TOR.ObjectHitReport.Coord.y == 1

def test_TOR_VerifyContents_MISS_Enemy():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.tor(1)

    assert result.CommandResult == CommandResult.TOR_Missed
    assert result.Command == Commands.TOR
    assert gameVar.galaxy.Starship.torpsRemain == gbl.MAX_STARSHIP_TORP -1

def test_TOR_VerifyContents_HIT_Star_Destroyed():
    testMock = create_random_factory(star_survives=False, hit_star=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.tor(7)

    assert result.Command == Commands.TOR
    assert gameVar.galaxy.Starship.torpsRemain == gbl.MAX_STARSHIP_TORP -1
    assert result.CommandResult == CommandResult.OK
    assert result.TOR.ObjectHitReport.ObjectHit == objectHit.ObjectHit.Star
    assert result.TOR.ObjectHitReport.Destroyed == True
    assert result.TOR.ObjectHitReport.StarSurvived == False
    assert result.TOR.ObjectHitReport.Coord.x == 0
    assert result.TOR.ObjectHitReport.Coord.y == 2

def test_TOR_VerifyContents_HIT_Star_Survives():
    testMock = create_random_factory(hit_star=True, star_survives=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.tor(7)

    assert result.Command == Commands.TOR
    assert gameVar.galaxy.Starship.torpsRemain == gbl.MAX_STARSHIP_TORP -1
    assert result.CommandResult == CommandResult.OK
    assert result.TOR.ObjectHitReport.ObjectHit == objectHit.ObjectHit.Star
    assert result.TOR.ObjectHitReport.Destroyed == False
    assert result.TOR.ObjectHitReport.StarSurvived == True
    assert result.TOR.ObjectHitReport.Coord.x == 0
    assert result.TOR.ObjectHitReport.Coord.y == 2

def test_TOR_NoEnemies():
    testMock = create_random_factory(no_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.tor(7)

    assert result.CommandResult == CommandResult.No_Enemies_Present
    assert result.Command == Commands.TOR

def test_TOR_VerifyContents_HIT_Starbase():
    testMock = create_random_factory(hit_starbase=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    print("\n" + gameVar.getCurrentQuadrantFormatted())

    result = gameVar.tor(7)

    assert result.Command == Commands.TOR
    assert gameVar.galaxy.Starship.torpsRemain == gbl.MAX_STARSHIP_TORP -1
    assert result.CommandResult == CommandResult.OK
    assert result.TOR.ObjectHitReport.ObjectHit == objectHit.ObjectHit.Starbase
    assert result.TOR.ObjectHitReport.Destroyed == True
    assert result.TOR.ObjectHitReport.Coord.x == 0
    assert result.TOR.ObjectHitReport.Coord.y == 6

