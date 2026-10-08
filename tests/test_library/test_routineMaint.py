# region imports
import sys
from unittest.mock import MagicMock

from models.starship import eDevice
from models.gameStatus import GameStatus

sys.path.append("/pythontrek/source/library/")
import pytest

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.otherFactories as otherFact
import source.library.factories.randomFactory as rf
from source import gbl
from source.library.game import game
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory
from tests.randomFactoryBuilder import RandomFactoryBuilder

# endregion


def create_random_factory(*, with_enemies: bool = False, enemies_moving: bool = False,
                          quadrant_visits: int = 1) -> RandomFactory:
    """Configure maintenance, including a finite set of healthy-device selections."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    with_enemies = with_enemies or enemies_moving
    builder = (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(*(2, 3) if with_enemies else (0, 0))
        .SetStarQuantity(2).SetEnemyChance(100 if with_enemies else 0)
        .SetStarbaseChance(100)
        .SetCoords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 1, 1)
    )
    if with_enemies:
        builder.SetCoords(
            gbl.RCT_ENEMY_LOCATION,
            *((0, 1), (0, 2), (0, 3)) * quadrant_visits,
            (4, 3), (4, 4), (4, 5),
        )
        builder.SetInteger(gbl.RIT_ENEMY_SHIELD_LEVEL, 200)
        builder.SetInteger(gbl.RIT_ENEMY_FIRED_AMOUNT, 50)
        builder.SetInteger(gbl.RIT_DAMAGE_DEVICE_CHANCE, 100)
        builder.SetInteger(gbl.RIT_DAMAGE_DEVICE_AMOUNT, 10)
        builder.SetIntegers(gbl.RIT_DAMAGE_DEVICE, 1, 2, 3, 4, 5, 6, 7)
        builder.SetInteger(gbl.RIT_ENEMY_MOVE_CHANCE, 100 if enemies_moving else 0)
    return builder.Build()

@pytest.mark.parametrize("sbX, sbY",[
    (0,0),
    (1,0),
    (2,0),
    (0,1),
    (2,1),
    (0,2),
    (1,2),
    (2,2),
])
def test_DockingWorks(sbX: int, sbY: int):
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.moveObjectInsideQuadrant(coord.Coord(0,0), coord.Coord(sbX, sbY))
    # print(gameVar.getCurrentQuadrantFormatted())

    # print(gameVar.canBeDocked())
    result = gameVar.routine_maint(.4, False)


    assert result.MaintResult.DockingStatus.CurrentStatus == True

def test_NotDockedWithShieldsUp():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    # gameVar.moveObjectInsideQuadrant(coord.Coord(0,0), coord.Coord(sbX, sbY))
    print(gameVar.getCurrentQuadrantFormatted())
    gameVar.galaxy.Starship.shieldLevel = 1000

    # print(gameVar.canBeDocked())
    result = gameVar.routine_maint(.4, False)


    assert result.MaintResult.DockingStatus.CurrentStatus == False

@pytest.mark.parametrize("sbX, sbY",[
    (6,1),
    (7,1),
    (7,4),
    (4,3),
])
def test_NotDockedWorks(sbX: int, sbY: int):
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.moveObjectInsideQuadrant(coord.Coord(0,0), coord.Coord(sbX, sbY))
    # print(gameVar.getCurrentQuadrantFormatted())

    # print(gameVar.canBeDocked())
    result = gameVar.routine_maint(.4, False)


    assert result.MaintResult.DockingStatus.CurrentStatus == False

def test_MissionTimeChanges():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.routine_maint(.4, False)

    assert result is not None
    assert gameVar.galaxy.MissionTime ==  pytest.approx(0.4)

def test_NoRepairsAvailable():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)

    result = gameVar.routine_maint(.4, False)

    assert result.MaintResult.StarbaseRepairsAvailable is None
    assert result.MaintResult.DockingStatus.CurrentStatus == True

def test_RepairsAvailable():
    testMock = create_random_factory()

    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3


    result = gameVar.routine_maint(0, False)


    assert result.MaintResult.StarbaseRepairsAvailable is not None
    assert result.MaintResult.DockingStatus.CurrentStatus == True
    assert result.MaintResult.StarbaseRepairsAvailable.MissionTimeToRepair == 3.0

def test_ExecuteRepairsAvailable():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -3


    result = gameVar.routine_maint(0, False)
    gameVar.RunStarbaseRepair()


    assert result is not None
    assert gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel == 0
    assert gameVar.galaxy.MissionTime == 3

def test_DamagedDevicesRepairOnMissionTime():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel = -0.5


    result = gameVar.routine_maint(1, False)


    assert gameVar.galaxy.Starship.GetDevice(eDevice.COM).damageLevel == 100
    assert len(result.MaintResult.DevicesRepairStatusChanged) == 1

def test_EnemiesFired():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 1000
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.routine_maint(1, True)


    assert len(result.MaintResult.EnemiesFired) == 3

def test_EnemiesFiredDamaged():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 1000
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.routine_maint(0, True)


    assert len(result.MaintResult.EnemiesFired) == 3
    enemy1Fired = result.MaintResult.EnemiesFired[0].DeviceDamaged
    enemy2Fired = result.MaintResult.EnemiesFired[1].DeviceDamaged
    enemy3Fired = result.MaintResult.EnemiesFired[2].DeviceDamaged

    assert enemy1Fired is not None
    assert enemy2Fired is not None
    assert enemy3Fired is not None
    assert enemy1Fired.damageLevel == -10
    assert enemy2Fired.damageLevel == -10
    assert enemy3Fired.damageLevel == -10

def test_EnemiesFiredWhileDocked():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 0
    print(gameVar.getCurrentQuadrantFormatted())


    result = gameVar.routine_maint(0, True)


    assert result.MaintResult.DockingStatus.CurrentStatus == True
    assert gameVar.galaxy.Starship.isDocked == True
    assert gameVar.galaxy.Starship.isDestroyed == False
    assert len(result.MaintResult.EnemiesFired) == 3
    enemy1Fired = result.MaintResult.EnemiesFired[0]
    enemy2Fired = result.MaintResult.EnemiesFired[1]
    enemy3Fired = result.MaintResult.EnemiesFired[2]

    assert enemy1Fired.StarshipDocked == True
    assert enemy2Fired.StarshipDocked == True
    assert enemy3Fired.StarshipDocked == True

def test_GameStatus_RanOutOfTime():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.MissionTime = gameVar.galaxy.MissionTimeDeadline + 1

    result = gameVar.routine_maint(0, False)


    assert result.MaintResult.GameStatus == GameStatus.RanOutOfTime

def test_GameStatus_StarshipDestroyed():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 10

    result = gameVar.routine_maint(0, True)


    assert result.MaintResult.GameStatus == GameStatus.StarshipDestroyed

def test_GameStatus_NoEnergyNoShields():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 0
    gameVar.galaxy.Starship.energyLevel = 0
    gameVar.moveObjectInsideQuadrant(coord.Coord(0,0), coord.Coord(5,5))


    result = gameVar.routine_maint(0, False )


    assert result.MaintResult.GameStatus == GameStatus.RanOutOfEnergy

def test_GameStatus_NoEnergyShieldAvailNotDamaged():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 100
    gameVar.galaxy.Starship.energyLevel = 0
    gameVar.moveObjectInsideQuadrant(coord.Coord(0,0), coord.Coord(5,5))


    result = gameVar.routine_maint(0, False )


    assert result.MaintResult.GameStatus == GameStatus.OutOfEnergyShieldEnergyAvailable

def test_GameStatus_NoEnergyShieldAvailDamaged():
    testMock = create_random_factory(with_enemies=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)
    gameVar.galaxy.Starship.shieldLevel = 100
    gameVar.galaxy.Starship.energyLevel = 0
    gameVar.moveObjectInsideQuadrant(coord.Coord(0,0), coord.Coord(5,5))
    gameVar.galaxy.Starship.GetDevice(eDevice.SHE).damageLevel = -3


    result = gameVar.routine_maint(0, False )


    assert result.MaintResult.GameStatus == GameStatus.RanOutOfEnergy

def test_GameStatus_NoMoreEnemies():
    testMock = create_random_factory()


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.routine_maint(0, False )


    assert result.MaintResult.GameStatus == GameStatus.MissionOver

def test_EnemiesMoveDuringMaint():
    testMock = create_random_factory(with_enemies=True,enemies_moving=True)


    curQuad = cqf.CurrentQuadrantFactory()
    galaxy = otherFact.otherFactories.createGalaxy(testMock, curQuad)
    gameVar = game.Game(galaxy, testMock, curQuad)


    result = gameVar.routine_maint(0, False )


    assert len(result.MaintResult.EnemiesMoved) == 3

