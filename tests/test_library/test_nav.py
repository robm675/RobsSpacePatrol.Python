# region imports
import sys
from unittest.mock import MagicMock

from models.commandResult import CommandResult
from models.commands import Commands
from models.starship import eDevice
from models.navMessage import NavMessage
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.otherFactories as otherFact
from source import gbl
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory(*, bottom_right: bool = False, object_in_way: bool = False,
                          quadrant_visits: int = 1) -> RandomFactory:
    """Choose the normal, bottom-right, or obstructed-route NAV scenario."""
    if bottom_right and object_in_way:
        raise ValueError("Choose bottom_right or object_in_way, not both")
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    stars = ((5, 0), (7, 6) ,(5, 6)) if object_in_way else ((7, 6), (7, 7))
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(*(7, 7) if bottom_right else (0, 0))
        .SetStarQuantity(2)
        .SetCoords(gbl.RCT_STAR_LOCATION, *stars * quadrant_visits)
        .Build()
    )


def test_NAV_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.nav(1,1)

    assert result is not None

def test_NAV_HasContents():
    testMock = create_random_factory(quadrant_visits=2)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.nav(1,1)

    assert result.CommandResult == CommandResult.OK

def test_NAV_BadDIR0():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.nav(0,1)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.InvalidDIR

def test_NAV_BadDIR9():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.nav(9,1)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.InvalidDIR

def test_NAV_BadDIST0():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.nav(1,0)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.InvalidDIST

def test_NAV_BadDIST9():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.nav(1,9)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.InvalidDIST

def test_NAV_Damaged_BadDIST1():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.NAV).damageLevel = -3


    result = gameVar.nav(1,1)


    assert result.CommandResult == CommandResult.Damaged

def test_NAV_OutsideGalaxy_Top():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.nav(3,1)


    assert result.Command == Commands.NAV
    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.BadInput_OutsideGalaxy

def test_NAV_OutsideGalaxy_Left():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.nav(5,1)


    assert result.Command == Commands.NAV
    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.BadInput_OutsideGalaxy

def test_NAV_OutsideGalaxy_Bottom():
    testMock = create_random_factory(bottom_right=True)



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.nav(7,1)


    assert result.Command == Commands.NAV
    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.BadInput_OutsideGalaxy

def test_NAV_OutsideGalaxy_Right():
    testMock = create_random_factory(bottom_right=True)



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.nav(1,1)


    assert result.Command == Commands.NAV
    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.BadInput_OutsideGalaxy

def test_NAV_NotEnoughEnergy_ShieldAvail():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.energyLevel = 10
    gameVar.galaxy.Starship.shieldLevel = 1000

    result = gameVar.nav(1,1)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.InsufficientEnergy_ShieldEnergyAvailable

def test_NAV_NotEnoughEnergy():
    testMock = create_random_factory()



    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.energyLevel = 10
    gameVar.galaxy.Starship.shieldLevel = 0

    result = gameVar.nav(1,1)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.InsufficientEnergy

def test_NAV_ObjectInWay():
    testMock = create_random_factory(object_in_way=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.nav(1,7)

    assert result.CommandResult == CommandResult.Error
    assert result.NAV.NavMessage == NavMessage.BadInput_ObjectHit
    assert result.NAV.DistanceTraveled != 0

def test_NAV_Damaged_Good_InsideQuadrant():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.NAV).damageLevel = -3
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.nav(1,.1)


    assert result.CommandResult == CommandResult.OK
    assert result.NAV.NavMessage == NavMessage.TransitComplete
    assert result.NAV.DistanceTraveled != 0
    assert gameVar.galaxy.Starship.energyLevel != gbl.MAX_STARSHIP_ENERGY

def test_NAV_Damaged_Good_DifferentQuadrant():
    testMock = create_random_factory(quadrant_visits=2)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.nav(1,7)


    assert result.CommandResult == CommandResult.OK
    assert result.NAV.NavMessage == NavMessage.TransitComplete
    assert result.NAV.DistanceTraveled != 0
    assert gameVar.galaxy.Starship.energyLevel != gbl.MAX_STARSHIP_ENERGY

def test_NAV_VerifyStarshipSector():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.nav(1,0.5)

    assert result is not None
    assert gameVar.galaxy.GetStarshipSector().coord.x == 4
    assert gameVar.galaxy.GetStarshipSector().coord.y == 0

def test_NAV_VerifyLocationAfterWarp1():
    testMock = create_random_factory(quadrant_visits=2)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.nav(1,1)


    assert result is not None
    assert gameVar.galaxy.GetStarshipSector().coord.x == 0
    assert gameVar.galaxy.GetStarshipSector().coord.y == 0
    assert gameVar.galaxy.CurrentQuadrant.coord.x == 1
    assert gameVar.galaxy.CurrentQuadrant.coord.y == 0

def test_NAV_VerifyLocationAfterWarp1Point1():
    testMock = create_random_factory(quadrant_visits=2)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.nav(1,1.1)


    assert result is not None
    assert gameVar.galaxy.GetStarshipSector().coord.x == 1
    assert gameVar.galaxy.GetStarshipSector().coord.y == 0
    assert gameVar.galaxy.CurrentQuadrant.coord.x == 1
    assert gameVar.galaxy.CurrentQuadrant.coord.y == 0
