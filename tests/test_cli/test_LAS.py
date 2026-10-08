# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")

# endregion

def test_LAS_Working():
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
    res = cl.executeCommandString("LAS 300")

    assert res != ""

def test_LAS_DAMAGED():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE LAS -5")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")
    res = cl.executeCommandString("LAS 100")

    print(f"[{res}]")

    assert CLI_Messages.LAS_Damaged in res

def test_LAS_InsufficientEnergy():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP ENERGY 0")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")


    res = cl.executeCommandString("LAS 300")

    assert CLI_Messages.LAS_InsufficientEnergy in res

def test_LAS_NoEnemies():
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


    res = cl.executeCommandString("LAS 300")

    assert CLI_Messages.LAS_NoEnemies in res

def test_LAS_InvalidAmount():
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


    res = cl.executeCommandString("LAS a300")

    assert CLI_Messages.LAS_InvalidAmount in res

def test_SHE_MissionTimeChanges():
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
    res = cl.executeCommandString("LAS 100")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
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
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 1")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 1")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")

    res = cl.executeCommandString("LAS 800")

    print(f"[{res}]")

    assert res.count(CLI_Messages.LAS_Fired) == 3
    assert res.count(CLI_Messages.LAS_Hit) == 3
    assert res.count(CLI_Messages.LAS_EnemyDestroyed) == 3

    assert "[(0,7)]" in res
    assert "[(0,6)]" in res
    assert "[(0,5)]" in res

def test_LAS_VerifyHitResult_Hit():
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

    res = cl.executeCommandString("LAS 10")

    assert res.count(CLI_Messages.LAS_Fired) == 3
    assert res.count(CLI_Messages.LAS_Hit) == 3
    assert res.count(CLI_Messages.LAS_SensorsIndicate) == 3
    assert res.count(CLI_Messages.LAS_Remaining) == 3

    assert "[(0,7)] (Sensors" in res
    assert "[(0,6)] (Sensors" in res
    assert "[(0,5)] (Sensors" in res

