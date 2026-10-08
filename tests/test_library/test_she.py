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


def test_SHE_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.she(100)

    assert result is not None

def test_SHE_HasContents():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.she(100)

    assert result.CommandResult == CommandResult.OK

def test_SHE_Damaged():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.SHE).damageLevel = -3
    result = gameVar.she(100)

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.SHE

def test_SHE_VerifyContents():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.she(100)


    assert result is not None
    assert gameVar.galaxy.Starship.energyLevel == gbl.MAX_STARSHIP_ENERGY - 100
    assert gameVar.galaxy.Starship.shieldLevel == 100

def test_SHE_BadValue():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.she(4000)

    assert result.CommandResult == CommandResult.Error
    assert result.SHE.ErrorMessage == gbl.SHE_ERRORMESSAGE
    assert result.Command == Commands.SHE

