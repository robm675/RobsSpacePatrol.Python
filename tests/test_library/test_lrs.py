# region imports
import sys
from unittest.mock import MagicMock

from models.commandResult import CommandResult
from models.commands import Commands
from models.starship import eDevice
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")

from source import gbl
from source.library.factories.currentQuadrantFactory import (
    CurrentQuadrantFactory as currentQuadrantFactory,
)
from source.library.factories.otherFactories import otherFactories as otherFactory
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, corner: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Use quadrant (2, 2), or (0, 0) for the corner-range scenario."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(*(0, 0) if corner else (2, 2))
        .SetStarshipSector(4, 5)
        .SetStarQuantity(2).SetEnemyChance(76).SetStarbaseChance(96)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((0, 1), (1, 1)) * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *((0, 0),) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .Build()
    )


def test_LRS_ResultsNotNull():
    curQuad = currentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFactory.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.lrs()

    assert result is not None

def test_LRS_HasContents():
    curQuad = currentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFactory.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.lrs()

    assert result.CommandResult == CommandResult.OK

def test_LRS_Damaged():
    curQuad = currentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFactory.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.LRS).damageLevel = -3
    result = gameVar.lrs()

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.LRS

def test_LRS_VerifyContents():
    testMock = create_random_factory()

    curQuad = currentQuadrantFactory()
    galaxy = otherFactory.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    result = gameVar.lrs()
    print("\n" + gameVar.getGalaxyFormatted())

    lrsRES = result.LRS.Quadrants

    assert len(lrsRES) == 9

def test_LRS_MarkedExplored():
    testMock = create_random_factory()



    curQuad = currentQuadrantFactory()
    galaxy = otherFactory.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    result = gameVar.lrs()

    exploredQuads = [q for q in galaxy.Quadrants if q.HasBeenExplored]


    assert len(exploredQuads) == 9
    assert result is not None

def test_LRS_CornerCorrectNumber():
    testMock = create_random_factory(corner=True)



    curQuad = currentQuadrantFactory()
    galaxy = otherFactory.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    result = gameVar.lrs()

    exploredQuads = [q for q in galaxy.Quadrants if q.HasBeenExplored]


    assert len(exploredQuads) == 4
    assert result is not None

