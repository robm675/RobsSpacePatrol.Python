# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_COM_NAV_InvalidQX_Range():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV 9 2 3 4")

    assert CLI_Messages.CPU_NAV_InvalidQX in res

def test_COM_NAV_InvalidQX_Alpha():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV a 2 3 4")

    assert CLI_Messages.CPU_NAV_InvalidCoord in res

def test_COM_NAV_InvalidQY_Range():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.executeCommandString("COM NAV 1 8 3 4")

    assert CLI_Messages.CPU_NAV_InvalidQY in res

def test_COM_NAV_InvalidQY_Alpha():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV 1 a 3 4")

    assert CLI_Messages.CPU_NAV_InvalidCoord in res

def test_COM_NAV_InvalidSX_Range():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV 1 2 9 4")

    assert CLI_Messages.CPU_NAV_InvalidSX in res

def test_COM_NAV_InvalidSX_Alpha():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV 1 2 a 4")

    assert CLI_Messages.CPU_NAV_InvalidCoord in res

def test_COM_NAV_InvalidSY_Range():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV 1 2 3 9")

    assert CLI_Messages.CPU_NAV_InvalidSY in res

def test_COM_NAV_InvalidSY_Alpha():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    res = cl.executeCommandString("COM NAV 1 2 3 a")

    assert CLI_Messages.CPU_NAV_InvalidCoord in res

def test_COM_NAV_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.executeCommandString("COM NAV 1 2 3 4")

    assert res != ""

def test_COM_NAV_Damaged():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET STARSHIP DEVICE COM -5")

    res = cl.executeCommandString("COM NAV 1 2 3 4")

    assert CLI_Messages.CPU_Damaged in res

def test_COM_NAV_VerifyContents():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.executeCommandString("COM NAV 1 2 3 4")

    assert CLI_Messages.CPU_NAV_Dir in res
    assert CLI_Messages.CPU_NAV_Dist in res


