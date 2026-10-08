from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_com_stb_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM STB")

    assert res != ""


def test_com_stb_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP DEVICE COM -5")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE")

    res = cl.execute_command_string("COM STB")

    assert cli_messages.CPU_DAMAGED in res


def test_com_stb_check_directions():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 1 0 STARBASE")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM STB")

    print(f"[{res}]")
    assert cli_messages.CPU_STB_DIR in res
    assert cli_messages.CPU_STB_DIST in res
    assert cli_messages.CPU_STB_STARBASE_FOUND_IN_SECTOR in res


def test_com_tor_no_starbase():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM STB")

    assert cli_messages.CPU_STB_NO_STARBASES in res
