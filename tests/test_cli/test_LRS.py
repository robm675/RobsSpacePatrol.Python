# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_LRS_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("LRS")

    assert res != ""

def test_LRS_DAMAGED():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE LRS -3")
    res = cl.executeCommandString("LRS")

    assert res == CLI_Messages.LRS_Damaged

def test_LRS_MissionTimeChanges():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    stBefore = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")
    res = cl.executeCommandString("LRS")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert stBefore != stAfter

def test_LRS_Contents():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)
    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")

    cl.executeCommandString("DEBUG SET QUADRANT 0 0 NUMSTARS 5")
    cl.executeCommandString("DEBUG SET QUADRANT 0 0 STARBASE 0")
    cl.executeCommandString("DEBUG SET QUADRANT 0 0 NUMENEMIES 3")

    cl.executeCommandString("DEBUG SET QUADRANT 1 0 NUMSTARS 1")
    cl.executeCommandString("DEBUG SET QUADRANT 1 0 STARBASE 1")
    cl.executeCommandString("DEBUG SET QUADRANT 1 0 NUMENEMIES 0")

    cl.executeCommandString("DEBUG SET QUADRANT 0 1 NUMSTARS 1")
    cl.executeCommandString("DEBUG SET QUADRANT 0 1 STARBASE 1")
    cl.executeCommandString("DEBUG SET QUADRANT 0 1 NUMENEMIES 0")

    cl.executeCommandString("DEBUG SET QUADRANT 1 1 NUMSTARS 9")
    cl.executeCommandString("DEBUG SET QUADRANT 1 1 STARBASE 0")
    cl.executeCommandString("DEBUG SET QUADRANT 1 1 NUMENEMIES 4")

    res = cl.executeCommandString("LRS")

    # print(game.getGalaxyFormatted())

    print(res)

    assert res != ""
    lines = res.split("\n")

    assert len(lines) > 3
    assert lines[2] == "| | *** | *** | *** |"
    assert lines[4] == "Y | *** | 305 | 011 |"
    assert lines[6] == "| | *** | 011 | 409 |"



