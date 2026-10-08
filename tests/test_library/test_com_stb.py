# region imports
import sys
from unittest.mock import MagicMock

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


def create_random_factory(*, no_starbase: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Preserve the starbase-bearing scenario or select its no-starbase variant."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3)
        .SetStarQuantity(2).SetEnemyChance(100)
        .SetStarbaseChance(0 if no_starbase else 100)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((7, 6), (6, 6)) * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *((7, 7), (6, 7), (5, 7)) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .Build()
    )


def test_COM_STB_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.com_stb()

    assert result is not None

def test_COM_STB_HasContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.com_stb()

    assert result.CommandResult == CommandResult.OK

def test_COM_STB_Damaged():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3
    result = gameVar.com_stb()

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.COM_STB

def test_COM_STB_VerifyContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.com_stb()

    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.COM_STB
    assert result.COM_STB.Direction == 7
    assert result.COM_STB.Distance == 6

def test_COM_STB_NoStarbase():
    testMock = create_random_factory(no_starbase=True)

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.com_stb()

    assert result.CommandResult == CommandResult.CPU_STB_No_Starbase_Present
    assert result.Command == Commands.COM_STB
