# region imports
import sys

from cli import CLI_Messages, commandLine

import gbl
from tests.randomFactoryBuilder import RandomFactoryBuilder
from tests.test_cli import gameBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_NAV_InvalidNumParms():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("NAV")

    assert CLI_Messages.NAV_InvalidCommand in res

def test_NAV_InvalidDirParm_Range():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("NAV 9 1")

    assert CLI_Messages.NAV_Invalid_Dir + "9" in res

def test_NAV_InvalidDirParm_Alpha():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("NAV a 1")


    assert CLI_Messages.NAV_Invalid_Dir + "a" in res

def test_NAV_InvalidDistParm_Range():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("NAV 1 9")

    assert CLI_Messages.NAV_Invalid_Dist + "9" in res

def test_NAV_InvalidDistParm_Alpha():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("NAV 1 a")

    assert CLI_Messages.NAV_Invalid_Dist + "a" in res

def test_NAV_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ")
    res = cl.executeCommandString("NAV 1 2")

    assert res != ""

def test_NAV_Working_VerifyLocation_E2W():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.executeCommandString("NAV 1 2")
    data = cl.executeCommandString("DEBUG GET STARSHIP QUADRANT")

    assert res is not None
    assert "2.0" in data

def test_NAV_Working_VerifyLocation_N2S():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.executeCommandString("NAV 7 2")
    data = cl.executeCommandString("DEBUG GET STARSHIP QUADRANT")

    assert res is not None
    assert "0.2" in data

def test_NAV_DamagedWarpDrive_DistToLarge():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE NAV -3")
    res = cl.executeCommandString("NAV 1 2")


    assert CLI_Messages.NAV_WarpDriveDamaged in res

def test_NAV_DamagedWarpDrive_DistOK():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE NAV -3")
    res = cl.executeCommandString("NAV 1 .2")


    assert CLI_Messages.NAV_ImpulseEngaged in res

def test_NAV_MissionTimeChanges_WarpDrive():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    stBefore = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")
    res = cl.executeCommandString("NAV 1 7")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    print(f"[{res}")

    assert stBefore != stAfter
    assert CLI_Messages.NAV_WarpEngaged in res

def test_NAV_MissionTimeChanges_Impulse():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    stBefore = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")
    res = cl.executeCommandString("NAV 1 .7")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    print(f"[{res}")

    assert stBefore != stAfter

def test_NAV_OutsideGalaxy():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.executeCommandString("NAV 5 1")

    assert CLI_Messages.NAV_OutsideGalaxy in res

def test_NAV_ImpulseDriveShutDown():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 7 0 STAR")

    res = cl.executeCommandString("NAV 1 2")

    assert CLI_Messages.NAV_ImpulseEngineShutDown in res
    assert CLI_Messages.NAV_BadNavigation in res

def test_NAV_NotEnoughEnergyForTrip_ShieldEnergyAvail():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET STARSHIP ENERGY 0")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")

    res = cl.executeCommandString("NAV 1 1")

    print(f"[{res}]")

    assert CLI_Messages.NAV_NotEnoughEnergy_ShieldEnergyAvail in res

def test_NAV_ArriveInNewQuadrant_EnemyPresent_NoShields_GetWarningMessage():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET STARSHIP SECTOR 0 0")
    cl.executeCommandString("DEBUG SET QUADRANT 1 0 NUMENEMIES 3")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.executeCommandString("NAV 1 1")

    assert CLI_Messages.WarningMessageShieldDownInCombatArea in res

def test_NAV_ArriveInNewQuadrant_EnemyPresent_GetReadAlert():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET STARSHIP SECTOR 0 0")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")
    cl.executeCommandString("DEBUG SET QUADRANT 1 0 NUMENEMIES 3")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")


    res = cl.executeCommandString("NAV 1 1")

    assert CLI_Messages.MAINT_NewQuadrantEnemiesRedAlert in res
