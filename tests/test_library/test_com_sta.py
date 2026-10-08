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


def create_random_factory(*, quadrant_visits: int = 1) -> RandomFactory:
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3)
        .SetStarshipSector(4, 5)
        .SetStarQuantity(2).SetEnemyChance(100).SetStarbaseChance(100)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((0, 1), (1, 1)) * quadrant_visits)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, *((0, 0), (1, 0), (2, 0)) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 4, 6)
        .Build()
    )

def test_COM_STA_ResultsNotNull():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.com_sta()

    assert result is not None

def test_COM_STA_HasContents():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)

    result = gameVar.com_sta()

    assert result.CommandResult == CommandResult.OK

def test_COM_STA_Damaged():
    curQuad = cqf.CurrentQuadrantFactory()
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    galaxy = otherFact.otherFactories.createGalaxy(randomFactory, curQuad)
    gameVar = game.Game(galaxy, randomFactory, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3
    result = gameVar.com_sta()

    assert result.CommandResult == CommandResult.Damaged
    assert result.Command == Commands.COM_STA

def test_COM_STA_VerifyContents():
    testMock = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetStarshipQuadrant(2,3)
        .SetStarshipSector(4,5)
        .SetEnemyChance(100)
        .SetStarbaseChance(100)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0,0), (2,2), (3,3))
        .SetCoords(gbl.RCT_STAR_LOCATION, (0,1))
        .SetCoords(gbl.RCT_STARBASE_LOCATION, (4,6))
        .Build()
    )

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.energyLevel = 1234
    gameVar.galaxy.Starship.shieldLevel = 321
    gameVar.galaxy.Starship.torpsRemain = 12
    gameVar.galaxy.Starship.isDocked = True


    result = gameVar.com_sta()


    assert result.COM_STA.MissionTime == 0
    assert result.COM_STA.EnemiesRemaining == gbl.MAX_QUADRANT_SECTOR_XY * gbl.MAX_QUADRANT_SECTOR_XY * 3
    assert result.COM_STA.EnergyRemaining == 1234
    assert result.COM_STA.ShieldLevel == 321
    assert result.COM_STA.TorpsRemaining == 12
    assert result.COM_STA.StarbasesRemaining == 64
    assert result.COM_STA.Docked == True
    assert result.COM_STA.QuadrantCoord.x == 2
    assert result.COM_STA.QuadrantCoord.y == 3
    assert result.COM_STA.SectorCoord.x == 4
    assert result.COM_STA.SectorCoord.y == 5
    assert result.COM_STA.MissionTimeDeadline == result.COM_STA.MissionTime + (result.COM_STA.EnemiesRemaining * gbl.MISSION_TIME_PER_ENEMY_RATIO)
