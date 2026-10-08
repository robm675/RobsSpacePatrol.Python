import gbl
from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_nav_invalid_num_parms():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("NAV")

    assert cli_messages.NAV_INVALID_COMMAND in res


def test_nav_invalid_dir_parm_range():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("NAV 9 1")

    assert cli_messages.NAV_INVALID_DIR + "9" in res


def test_nav_invalid_dir_parm_alpha():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("NAV a 1")

    assert cli_messages.NAV_INVALID_DIR + "a" in res


def test_nav_invalid_dist_parm_range():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("NAV 1 9")

    assert cli_messages.NAV_INVALID_DIST + "9" in res


def test_nav_invalid_dist_parm_alpha():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    res = cl.execute_command_string("NAV 1 a")

    assert cli_messages.NAV_INVALID_DIST + "a" in res


def test_nav_working():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ")
    res = cl.execute_command_string("NAV 1 2")

    assert res != ""


def test_nav_working_verify_location_e2_w():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("NAV 1 2")
    data = cl.execute_command_string("DEBUG GET STARSHIP QUADRANT")

    assert res is not None
    assert "2.0" in data


def test_nav_working_verify_location_n2_s():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("NAV 7 2")
    data = cl.execute_command_string("DEBUG GET STARSHIP QUADRANT")

    assert res is not None
    assert "0.2" in data


def test_nav_damaged_warp_drive_dist_to_large():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE NAV -3")
    res = cl.execute_command_string("NAV 1 2")

    assert cli_messages.NAV_WARP_DRIVE_DAMAGED in res


def test_nav_damaged_warp_drive_dist_ok():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP DEVICE NAV -3")
    res = cl.execute_command_string("NAV 1 .2")

    assert cli_messages.NAV_IMPULSE_ENGAGED in res


def test_nav_mission_time_changes_warp_drive():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    st_before = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")
    res = cl.execute_command_string("NAV 1 7")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    print(f"[{res}")

    assert st_before != st_after
    assert cli_messages.NAV_WARP_ENGAGED in res


def test_nav_mission_time_changes_impulse():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    st_before = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")
    res = cl.execute_command_string("NAV 1 .7")
    st_after = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    print(f"[{res}")

    assert st_before != st_after


def test_nav_outside_galaxy():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")

    res = cl.execute_command_string("NAV 5 1")

    assert cli_messages.NAV_OUTSIDE_GALAXY in res


def test_nav_impulse_drive_shut_down():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 7 0 STAR")

    res = cl.execute_command_string("NAV 1 2")

    assert cli_messages.NAV_IMPULSE_ENGINE_SHUT_DOWN in res
    assert cli_messages.NAV_BAD_NAVIGATION in res


def test_nav_not_enough_energy_for_trip_shield_energy_avail():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET STARSHIP ENERGY 0")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")

    res = cl.execute_command_string("NAV 1 1")

    print(f"[{res}]")

    assert cli_messages.NAV_NOT_ENOUGH_ENERGY_SHIELD_ENERGY_AVAIL in res


def test_nav_arrive_in_new_quadrant_enemy_present_no_shields_get_warning_message():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET STARSHIP SECTOR 0 0")
    cl.execute_command_string("DEBUG SET QUADRANT 1 0 NUMENEMIES 3")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")
    cl.execute_command_string("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.execute_command_string("NAV 1 1")

    assert cli_messages.WARNING_MESSAGE_SHIELD_DOWN_IN_COMBAT_AREA in res


def test_nav_arrive_in_new_quadrant_enemy_present_get_read_alert():
    random_factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET STARSHIP QUADRANT 0 0")
    cl.execute_command_string("DEBUG SET CLEARCQ ALL")
    cl.execute_command_string("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP")
    cl.execute_command_string("DEBUG SET STARSHIP SECTOR 0 0")
    cl.execute_command_string("DEBUG SET STARSHIP SHIELD 1000")
    cl.execute_command_string("DEBUG SET QUADRANT 1 0 NUMENEMIES 3")
    cl.execute_command_string("DEBUG SET PREVENTENEMYFIRE ON")
    cl.execute_command_string("DEBUG SET ENEMYMOVE OFF")

    res = cl.execute_command_string("NAV 1 1")

    assert cli_messages.MAINT_NEW_QUADRANT_ENEMIES_RED_ALERT in res
