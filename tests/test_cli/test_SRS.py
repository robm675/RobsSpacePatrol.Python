# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")
# endregion

def test_SRS_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("SRS")

    assert res != ""

def test_SRS_DAMAGED():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE SRS -3")
    res = cl.executeCommandString("SRS")

    assert res == CLI_Messages.SRS_Damaged

def test_SRS_MissionTimeChanges():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    stBefore = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")
    res = cl.executeCommandString("SRS")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert stBefore != stAfter

def test_SRS_Contents():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)
    cl.executeCommandString("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 1 2 STAR")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 3 4 STAR")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 5 7 STAR")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 1 1 STARBASE")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 7 1 ENEMY")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 7 3 ENEMY")
    res = cl.executeCommandString("SRS")

    print(game.getCurrentQuadrantFormatted())

    print(res)

    assert res.count("***") == 3
    assert res.count("XXX") == 2
    assert res.count("EEE") == 1
    assert res.count("BBB") == 1
