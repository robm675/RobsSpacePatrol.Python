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
import source.library.factories.randomFactory as rf
from source import gbl
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, no_enemies: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Default to the empty COM NAV setup; no_enemies selects its two-star variant."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarQuantity(2 if no_enemies else 0)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .Build()
    )


def test_COM_NAV_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.com_nav(coord.Coord(0, 0), coord.Coord(0, 1))

    assert result is not None

def test_COM_NAV_HasContents():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )    
    testMock = randomFactory
    testMock.GetRandomInteger= MagicMock()
    testMock.GetRandomInteger.side_effect = MockRandomInt
    testMock.GetRandomCoord= MagicMock()
    testMock.GetRandomCoord.side_effect = MockRandomCoord


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.com_nav(coord.Coord(0, 0), coord.Coord(0, 1))


    assert result.CommandResult == CommandResult.OK

def test_COM_NAV_Damaged():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )    
    testMock = randomFactory
    testMock.GetRandomInteger= MagicMock()
    testMock.GetRandomInteger.side_effect = MockRandomInt
    testMock.GetRandomCoord= MagicMock()
    testMock.GetRandomCoord.side_effect = MockRandomCoord


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3


    result = gameVar.com_nav(coord.Coord(0, 0), coord.Coord(0, 1))


    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.COM_NAV

def test_COM_NAV_VerifyContents_X():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )    
    testMock = randomFactory
    testMock.GetRandomInteger= MagicMock()
    testMock.GetRandomInteger.side_effect = MockRandomInt
    testMock.GetRandomCoord= MagicMock()
    testMock.GetRandomCoord.side_effect = MockRandomCoord

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.com_nav(coord.Coord(2,0), coord.Coord(0,0))


    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.COM_NAV
    assert result.COM_NAV.Distance == 2.0
    assert result.COM_NAV.Direction == 1

def test_COM_NAV_VerifyContents_Y():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )    
    testMock = randomFactory
    testMock.GetRandomInteger= MagicMock()
    testMock.GetRandomInteger.side_effect = MockRandomInt
    testMock.GetRandomCoord= MagicMock()
    testMock.GetRandomCoord.side_effect = MockRandomCoord

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.com_nav(coord.Coord(0,2), coord.Coord(0,0))


    assert result.CommandResult == CommandResult.OK
    assert result.Command == Commands.COM_NAV
    assert result.COM_NAV.Distance == 2.0
    assert result.COM_NAV.Direction == 7






def MockRandomInt(randomType: str):
    if randomType == gbl.RIT_STAR_QUANTITY:
        return 0
    if randomType == gbl.RIT_ENEMY_CHANCE:
        return 0
    if randomType == gbl.RIT_STARBASE_CHANCE:
        return 0
    if randomType == gbl.RIT_STARTING_MISSION_TIME:
        return 2450
    return -1

def MockRandomIntNoEnemies(randomType: str):
    if randomType == gbl.RIT_STAR_QUANTITY:
        return 2
    if randomType == gbl.RIT_ENEMY_CHANCE:
        return 0
    if randomType == gbl.RIT_STARBASE_CHANCE:
        return 0
    if randomType == gbl.RIT_STARTING_MISSION_TIME:
        return 2450
    return -1

def MockRandomCoord(randomType: str) -> coord.Coord:
    if randomType == gbl.RCT_STARSHIP_QUADRANT:
        return coord.Coord(0,0)
    if randomType == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(0,0)
    if randomType == gbl.RCT_ENEMY_LOCATION:
        MockRandomCoord.counter += 1
        if MockRandomCoord.counter > 2:
            MockRandomCoord.counter = 0

        if MockRandomCoord.counter == 0:
            return coord.Coord(0,1)
        if MockRandomCoord.counter == 1:
            return coord.Coord(0,2)
        if MockRandomCoord.counter == 2:
            return coord.Coord(0,3)
        raise RuntimeError("Invalid counter")

    if randomType == gbl.RCT_STAR_LOCATION:
        return coord.Coord(7,6)
    if randomType == gbl.RCT_STARBASE_LOCATION:
        return coord.Coord(0,6)
    return coord.Coord(-10,-10)

MockRandomCoord.counter = -1
