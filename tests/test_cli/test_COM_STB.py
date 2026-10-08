# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_COM_STB_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")


    res = cl.executeCommandString("COM STB")

    assert res != ""

def test_COM_STB_Damaged():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP DEVICE COM -5")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE")


    res = cl.executeCommandString("COM STB")


    assert CLI_Messages.CPU_Damaged in res

def test_COM_STB_CheckDirections():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 1 0 STARBASE")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")


    res = cl.executeCommandString("COM STB")

    print(f"[{res}]")
    assert CLI_Messages.CPU_STB_Dir in res
    assert CLI_Messages.CPU_STB_Dist in res
    assert CLI_Messages.CPU_STB_StarbaseFoundInSector in res

def test_COM_TOR_NoStarbase():
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

    res = cl.executeCommandString("COM STB")

    assert CLI_Messages.CPU_STB_NoStarbases in res

