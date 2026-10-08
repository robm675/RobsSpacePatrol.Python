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

def find_device(devices, name):
    return next(d for d in devices if d.name == name)


def test_DAM_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.dam()

    assert result is not None

def test_DAM_HasContents():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.dam()

    assert result.CommandResult == CommandResult.OK

def test_DAM_VerifyContents():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.LRS).damageLevel = -2
    gameVar.galaxy.Starship.GetDevice(eDevice.SRS).damageLevel = -1
    gameVar.galaxy.Starship.GetDevice(eDevice.TOR).damageLevel = -1.5

    result = gameVar.dam()

    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.DAM

    dev1 = find_device(result.DAM.Devices, "SRS")
    dev2 = find_device(result.DAM.Devices, "LRS")
    dev3 = find_device(result.DAM.Devices, "TOR")

    assert dev1.damageLevel == -1
    assert dev2.damageLevel == -2
    assert dev3.damageLevel == -1.5
