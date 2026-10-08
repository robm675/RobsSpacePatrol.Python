from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_dam_basics():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("DAM")

    assert cli_messages.DAM_DAMAGE_REPORT_NO_DAMAGES in res


def test_dam_shows_damages():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE NAV -3")
    res = cl.execute_command_string("DAM")

    assert "Damaged" in res
