from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_las_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    res = cl.execute_command_string("LAS 300")

    assert res != ""


def test_las_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE LAS -5")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")
    res = cl.execute_command_string("LAS 100")

    print(f"[{res}]")

    assert cli_messages.LAS_DAMAGED in res


def test_las_insufficient_energy():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP ENERGY 0")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("LAS 300")

    assert cli_messages.LAS_INSUFFICIENT_ENERGY in res


def test_las_no_enemies():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("LAS 300")

    assert cli_messages.LAS_NO_ENEMIES in res


def test_las_invalid_amount():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("LAS a300")

    assert cli_messages.LAS_INVALID_AMOUNT in res


def test_she_mission_time_changes():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    st_before = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")
    res = cl.execute_command_string("LAS 100")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    assert res is not None
    assert st_before != st_after


def test_las_verify_hit_result_destroyed():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 1")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 1")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("LAS 800")

    print(f"[{res}]")

    assert res.count(cli_messages.LAS_FIRED) == 3
    assert res.count(cli_messages.LAS_HIT) == 3
    assert res.count(cli_messages.LAS_ENEMY_DESTROYED) == 3

    assert "[(0,7)]" in res
    assert "[(0,6)]" in res
    assert "[(0,5)]" in res


def test_las_verify_hit_result_hit():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("LAS 10")

    assert res.count(cli_messages.LAS_FIRED) == 3
    assert res.count(cli_messages.LAS_HIT) == 3
    assert res.count(cli_messages.LAS_SENSORS_INDICATE) == 3
    assert res.count(cli_messages.LAS_REMAINING) == 3

    assert "[(0,7)] (Sensors" in res
    assert "[(0,6)] (Sensors" in res
    assert "[(0,5)] (Sensors" in res
