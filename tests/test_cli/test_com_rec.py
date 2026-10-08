from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_com_rec_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("COM REC")

    print("\n")
    print(res)
    assert res != ""


def test_com_rec_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE COM -5")

    res = cl.execute_command_string("COM REC")

    assert cli_messages.CPU_DAMAGED in res
