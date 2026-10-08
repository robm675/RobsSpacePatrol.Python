# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")
# endregion

def test_TOR_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    res = cl.executeCommandString("TOR 5")

    assert res != ""

def test_TOR_DAMAGED():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE TOR -5")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")
    res = cl.executeCommandString("TOR 5")

    print(f"[{res}]")

    assert CLI_Messages.TOR_Damaged in res

def test_LAS_InsufficientInventory():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP TORP 0")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")


    res = cl.executeCommandString("TOR 5")

    assert CLI_Messages.TOR_Expended in res

def test_TOR_NoEnemies():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")


    res = cl.executeCommandString("TOR 5")

    assert CLI_Messages.TOR_NoEnemies in res

def test_TOR_InvalidDirection():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")


    res = cl.executeCommandString("TOR 10")

    assert CLI_Messages.TOR_InvalidDirection in res

def test_TOR_MissionTimeChanges():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    stBefore = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")
    res = cl.executeCommandString("TOR 7")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    print(res)
    assert stBefore != stAfter

def test_LAS_VerifyHitResult_Destroyed():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.executeCommandString("TOR 7")

    assert CLI_Messages.TOR_Fired in res
    assert CLI_Messages.TOR_EnemyAtSector in res
    assert CLI_Messages.TOR_Destroyed in res

def test_LAS_VerifyHitResult_StarbaseDestroyed():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 7 STARBASE")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 5 7 1")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.executeCommandString("TOR 7")

    assert CLI_Messages.TOR_Fired in res
    assert CLI_Messages.TOR_StarbaseDestroyed in res

def test_LAS_VerifyHitResult_Misssed():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.executeCommandString("TOR 3")

    assert CLI_Messages.TOR_Missed in res

def test_LAS_VerifyHitResult_Destroyed_Coords():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.executeCommandString("TOR 7")

    assert CLI_Messages.TOR_Fired in res
    assert CLI_Messages.TOR_EnemyAtSector in res
    assert CLI_Messages.TOR_Destroyed in res
    assert "[(0,7)]" in res


