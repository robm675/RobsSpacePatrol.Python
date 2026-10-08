# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")
# endregion

def test_SHE_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("SHE 1000")

    assert CLI_Messages.SHE_Changed in res
    assert "1000" in res

def test_SHE_DAMAGED():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET STARSHIP DEVICE SHE -3")
    res = cl.executeCommandString("SHE 100")

    assert res == CLI_Messages.SHE_Damaged

def test_SHE_MissionTimeChanges():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    stBefore = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")
    res = cl.executeCommandString("SHE 100")
    stAfter = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert stBefore != stAfter
