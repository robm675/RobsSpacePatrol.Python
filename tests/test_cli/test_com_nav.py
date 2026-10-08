from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_com_nav_invalid_qx_range():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV 9 2 3 4")

    assert cli_messages.CPU_NAV_INVALID_QX in res


def test_com_nav_invalid_qx_alpha():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV a 2 3 4")

    assert cli_messages.CPU_NAV_INVALID_COORD in res


def test_com_nav_invalid_qy_range():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("COM NAV 1 8 3 4")

    assert cli_messages.CPU_NAV_INVALID_QY in res


def test_com_nav_invalid_qy_alpha():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV 1 a 3 4")

    assert cli_messages.CPU_NAV_INVALID_COORD in res


def test_com_nav_invalid_sx_range():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV 1 2 9 4")

    assert cli_messages.CPU_NAV_INVALID_SX in res


def test_com_nav_invalid_sx_alpha():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV 1 2 a 4")

    assert cli_messages.CPU_NAV_INVALID_COORD in res


def test_com_nav_invalid_sy_range():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV 1 2 3 9")

    assert cli_messages.CPU_NAV_INVALID_SY in res


def test_com_nav_invalid_sy_alpha():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    res = cl.execute_command_string("COM NAV 1 2 3 a")

    assert cli_messages.CPU_NAV_INVALID_COORD in res


def test_com_nav_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("COM NAV 1 2 3 4")

    assert res != ""


def test_com_nav_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET STARSHIP DEVICE COM -5")

    res = cl.execute_command_string("COM NAV 1 2 3 4")

    assert cli_messages.CPU_DAMAGED in res


def test_com_nav_verify_contents():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("COM NAV 1 2 3 4")

    assert cli_messages.CPU_NAV_DIR in res
    assert cli_messages.CPU_NAV_DIST in res
