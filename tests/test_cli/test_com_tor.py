from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_com_tor_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM TOR")

    assert res != ""


def test_com_tor_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE COM -5")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM TOR")

    assert cli_messages.CPU_DAMAGED in res


def test_com_tor_check_directions():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM TOR")

    assert "[(0,7)]" in res
    assert "[(0,6)]" in res
    assert "[(0,5)]" in res
    assert res.count("is bearing") == 3


def test_com_tor_no_enemies():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("COM TOR")

    assert cli_messages.CPU_TOR_NO_ENEMIES in res
