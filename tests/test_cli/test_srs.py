from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_srs_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("SRS")

    assert res != ""


def test_srs_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE SRS -3")
    res = cl.execute_command_string("SRS")

    assert res == cli_messages.SRS_DAMAGED


def test_srs_mission_time_changes():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    st_before = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")
    res = cl.execute_command_string("SRS")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert st_before != st_after


def test_srs_contents():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)
    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 1 2 STAR")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 3 4 STAR")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 5 7 STAR")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 1 1 STARBASE")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 7 1 ENEMY")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 7 3 ENEMY")
    res = cl.execute_command_string("SRS")

    print(game.get_current_quadrant_formatted())

    print(res)

    assert res.count("***") == 3
    assert res.count("XXX") == 2
    assert res.count("EEE") == 1
    assert res.count("BBB") == 1
