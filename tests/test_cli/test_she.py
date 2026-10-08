from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_she_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("SHE 1000")

    assert cli_messages.SHE_CHANGED in res
    assert "1000" in res


def test_she_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE SHE -3")
    res = cl.execute_command_string("SHE 100")

    assert res == cli_messages.SHE_DAMAGED


def test_she_mission_time_changes():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    st_before = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")
    res = cl.execute_command_string("SHE 100")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert st_before != st_after
