# region imports
import sys
from unittest.mock import MagicMock

from models.commandResult import CommandResult
from models.commands import Commands
from tests.randomFactoryBuilder import RandomFactoryBuilder
from models.starship import eDevice

sys.path.append("/pythontrek/source/library/")

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.otherFactories as otherFact
from source import gbl
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, no_enemies: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Build fresh responses; allow one placement sequence per quadrant visit."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3)
        .SetStarshipSector(0, 0)
        .SetStarQuantity(2)
        .SetEnemyChance(0 if no_enemies else 100)
        .SetStarbaseChance(0 if no_enemies else 100)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *((0, 1), (0, 2), (0, 3)) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .Build()
    )

def find_enemy(direction_to_enemies, x, y):
    return next(
        e for e in direction_to_enemies
        if e.Coord.x == x and e.Coord.y == y
    )


def test_COM_TOR_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.com_tor()

    assert result is not None

def test_COM_TOR_HasContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.com_tor()

    assert result.CommandResult == CommandResult.OK

def test_COM_TOR_Damaged():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3
    result = gameVar.com_tor()

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.COM_TOR

def test_COM_TOR_VerifyContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.com_tor()

    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.COM_TOR
    assert len(result.COM_TOR.DirectionToEnemies) == 3
    enemy1 = find_enemy(result.COM_TOR.DirectionToEnemies, 0, 1)
    enemy2 = find_enemy(result.COM_TOR.DirectionToEnemies, 0, 2)
    enemy3 = find_enemy(result.COM_TOR.DirectionToEnemies, 0, 3)
    assert enemy1.Direction == 7
    assert enemy1.Distance == 1
    assert enemy2.Direction == 7
    assert enemy2.Distance == 2
    assert enemy3.Direction == 7
    assert enemy3.Distance == 3


def test_COM_TOR_NoEnemies():
    testMock = create_random_factory(no_enemies=True)

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.com_tor()

    assert result.CommandResult == CommandResult.No_Enemies_Present
    assert result.Command == Commands.COM_TOR

