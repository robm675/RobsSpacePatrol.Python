from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_tor_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    res = cl.execute_command_string("TOR 5")

    assert res != ""


def test_tor_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE TOR -5")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")
    res = cl.execute_command_string("TOR 5")

    print(f"[{res}]")

    assert cli_messages.TOR_DAMAGED in res


def test_las_insufficient_inventory():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP TORP 0")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("TOR 5")

    assert cli_messages.TOR_EXPENDED in res


def test_tor_no_enemies():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("TOR 5")

    assert cli_messages.TOR_NO_ENEMIES in res


def test_tor_invalid_direction():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("TOR 10")

    assert cli_messages.TOR_INVALID_DIRECTION in res


def test_tor_mission_time_changes():
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
    res = cl.execute_command_string("TOR 7")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    print(res)
    assert st_before != st_after


def test_las_verify_hit_result_destroyed():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("TOR 7")

    assert cli_messages.TOR_FIRED in res
    assert cli_messages.TOR_ENEMY_AT_SECTOR in res
    assert cli_messages.TOR_DESTROYED in res


def test_las_verify_hit_result_starbase_destroyed():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 7 STARBASE")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 5 7 1")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("TOR 7")

    assert cli_messages.TOR_FIRED in res
    assert cli_messages.TOR_STARBASE_DESTROYED in res


def test_las_verify_hit_result_misssed():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("TOR 3")

    assert cli_messages.TOR_MISSED in res


def test_las_verify_hit_result_destroyed_coords():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 1")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")

    res = cl.execute_command_string("TOR 7")

    assert cli_messages.TOR_FIRED in res
    assert cli_messages.TOR_ENEMY_AT_SECTOR in res
    assert cli_messages.TOR_DESTROYED in res
    assert "[(0,7)]" in res
