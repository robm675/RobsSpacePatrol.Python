# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_COM_TOR_Working():
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
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")


    res = cl.executeCommandString("COM TOR")

    assert res != ""

def test_COM_TOR_Damaged():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE COM -5")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")


    res = cl.executeCommandString("COM TOR")


    assert CLI_Messages.CPU_Damaged in res

def test_COM_TOR_CheckDirections():
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
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")


    res = cl.executeCommandString("COM TOR")

    assert "[(0,7)]" in res
    assert "[(0,6)]" in res
    assert "[(0,5)]" in res
    assert res.count("is bearing") == 3

def test_COM_TOR_NoEnemies():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.executeCommandString("COM TOR")

    assert CLI_Messages.CPU_TOR_NoEnemies in res

