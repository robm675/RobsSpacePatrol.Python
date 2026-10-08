import sys

import gbl
from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_routine_maint_enemy_fired_coords():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_enemy_chance(80)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.execute_command_string("SRS")

    print(res, file=sys.stderr)

    assert "0,5" in res


def test_routine_maint_enemy_destroyed_no_warning_message():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 0")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("SRS")

    print(f"[{res}]")
    assert cli_messages.WARNING_MESSAGE_SHIELD_DOWN_IN_COMBAT_AREA not in res


def test_routine_maint_three_enemies_fired():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_enemy_chance(80)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.execute_command_string("SRS")

    print(f"[{res}]")

    assert "0,5" in res
    assert "0,6" in res
    assert "0,7" in res


def test_routine_maint_protected_by_starbase():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_enemy_chance(80)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.execute_command_string("SRS")

    assert cli_messages.MAINT_STARBASE_SHIELDS_PROTECTED in res


def test_routine_maint_protected_by_starbase_repeatedly():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_enemy_chance(80)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = ""
    res += cl.execute_command_string("SRS")
    res += cl.execute_command_string("SRS")
    res += cl.execute_command_string("SRS")
    res += cl.execute_command_string("SRS")

    assert cli_messages.MAINT_STARBASE_SHIELDS_PROTECTED in res
    assert res.count(cli_messages.MAINT_STARBASE_SHIELDS_PROTECTED) == 12


def test_routine_maint_device_repaired():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_enemy_chance(80)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")
    cl.execute_command_string("DEBUG SET STARSHIP DEVICE TOR -.1")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.execute_command_string("SRS")

    assert cli_messages.MAINT_REPAIRS_COMPLETE in res


def test_routine_maint_device_repaired_not_repeated():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")
    cl.execute_command_string("DEBUG SET STARSHIP DEVICE TOR -.1")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")

    print(game.get_current_quadrant_formatted())

    res = cl.execute_command_string("SRS")
    res = cl.execute_command_string("SRS")

    assert cli_messages.MAINT_REPAIRS_COMPLETE not in res


def test_routine_maint_enemies_moved():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_enemy_chance(80)
        .set_coords(
            gbl.RCT_ENEMY_LOCATION,
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (1, 1),
            (1, 2),
        )
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.execute_command_string("DEBUG SET ENEMYMOVE FORCE")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.execute_command_string("SRS")

    assert "Enemy moved!" in res
    assert cli_messages.MAINT_TECH_WAITING not in res
