# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_COM_STA_Working():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    res = cl.executeCommandString("COM STA")

    assert res != ""

def test_COM_STA_Damaged():
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


    res = cl.executeCommandString("COM STA")


    assert CLI_Messages.CPU_Damaged in res

def test_COM_TOR_CheckDirections():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.executeCommandString("COM STA")

    assert CLI_Messages.CPU_STA_DeviceStatus in res
    assert CLI_Messages.CPU_STA_Docked in res
    assert CLI_Messages.CPU_STA_EnemiesRemaining in res
    assert CLI_Messages.CPU_STA_EnergyRemaining in res
    assert CLI_Messages.CPU_STA_Quadrant in res
    assert CLI_Messages.CPU_STA_Sector in res
    assert CLI_Messages.CPU_STA_ShieldLevel in res
    assert CLI_Messages.CPU_STA_StarbasesRemaining in res
    assert CLI_Messages.CPU_STA_MissionTime in res
    assert CLI_Messages.CPU_STA_MissionTimeRemaining in res
    assert CLI_Messages.CPU_STA_TorpRemaining in res

