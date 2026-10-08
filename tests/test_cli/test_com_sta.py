from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_com_sta_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("COM STA")

    assert res != ""


def test_com_sta_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP DEVICE COM -5")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("COM STA")

    assert cli_messages.CPU_DAMAGED in res


def test_com_tor_check_directions():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM STA")

    assert cli_messages.CPU_STA_DEVICE_STATUS in res
    assert cli_messages.CPU_STA_DOCKED in res
    assert cli_messages.CPU_STA_ENEMIES_REMAINING in res
    assert cli_messages.CPU_STA_ENERGY_REMAINING in res
    assert cli_messages.CPU_STA_QUADRANT in res
    assert cli_messages.CPU_STA_SECTOR in res
    assert cli_messages.CPU_STA_SHIELD_LEVEL in res
    assert cli_messages.CPU_STA_STARBASES_REMAINING in res
    assert cli_messages.CPU_STA_MISSION_TIME in res
    assert cli_messages.CPU_STA_MISSION_TIME_REMAINING in res
    assert cli_messages.CPU_STA_TORP_REMAINING in res
