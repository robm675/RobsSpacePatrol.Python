from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_lrs_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("LRS")

    assert res != ""


def test_lrs_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE LRS -3")
    res = cl.execute_command_string("LRS")

    assert res == cli_messages.LRS_DAMAGED


def test_lrs_mission_time_changes():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    st_before = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")
    res = cl.execute_command_string("LRS")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert st_before != st_after


def test_lrs_contents():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)
    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")

    cl.execute_command_string("DEBUG SET QUADRANT 0 0 NUMSTARS 5")
    cl.execute_command_string("DEBUG SET QUADRANT 0 0 STARBASE 0")
    cl.execute_command_string("DEBUG SET QUADRANT 0 0 NUMENEMIES 3")

    cl.execute_command_string("DEBUG SET QUADRANT 1 0 NUMSTARS 1")
    cl.execute_command_string("DEBUG SET QUADRANT 1 0 STARBASE 1")
    cl.execute_command_string("DEBUG SET QUADRANT 1 0 NUMENEMIES 0")

    cl.execute_command_string("DEBUG SET QUADRANT 0 1 NUMSTARS 1")
    cl.execute_command_string("DEBUG SET QUADRANT 0 1 STARBASE 1")
    cl.execute_command_string("DEBUG SET QUADRANT 0 1 NUMENEMIES 0")

    cl.execute_command_string("DEBUG SET QUADRANT 1 1 NUMSTARS 9")
    cl.execute_command_string("DEBUG SET QUADRANT 1 1 STARBASE 0")
    cl.execute_command_string("DEBUG SET QUADRANT 1 1 NUMENEMIES 4")

    res = cl.execute_command_string("LRS")

    print(res)

    assert res != ""
    lines = res.split("\n")

    assert len(lines) > 3
    assert lines[2] == "| | *** | *** | *** |"
    assert lines[4] == "Y | *** | 305 | 011 |"
    assert lines[6] == "| | *** | 011 | 409 |"
