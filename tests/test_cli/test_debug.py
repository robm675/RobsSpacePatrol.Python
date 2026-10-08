from cli import cli_messages, command_line

from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli import game_builder


def test_debug_check_ok():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    resp = cl.execute_command_string("DEBUG CHECK")

    assert resp == cli_messages.DEBUG_COMMAND_OK


def test_debug_check_lower_case_ok():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    resp = cl.execute_command_string("debug check")

    assert resp == cli_messages.DEBUG_COMMAND_OK


def test_debug_set_get_sector_contents():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    contents = "STARSHIP"

    resp = cl.execute_command_string(f"DEBUG SET CURRENTQUADRANT SECTOR 0 0 {contents}")
    data = cl.execute_command_string("DEBUG GET CURRENTQUADRANT SECTOR 0 0")

    assert resp is not None
    assert data == contents


def test_debug_set_get_sector_enemy():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    shield_level = "1000"

    resp = cl.execute_command_string(f"DEBUG SET CURRENTQUADRANT ENEMY 0 0 {shield_level}")
    data = cl.execute_command_string("DEBUG GET CURRENTQUADRANT ENEMY 0 0")

    assert resp is not None
    assert data == "ENEMY:" + shield_level


def test_debug_set_get_quadrant_num_enemies():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    num_enemies = "3"

    resp = cl.execute_command_string(f"DEBUG SET QUADRANT 0 0 NUMENEMIES {num_enemies}")
    data = cl.execute_command_string("DEBUG GET QUADRANT 0 0 NUMENEMIES")

    assert resp is not None
    assert data == num_enemies


def test_debug_set_get_quadrant_num_stars():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = "5"

    resp = cl.execute_command_string(f"DEBUG SET QUADRANT 0 0 NUMSTARS {value}")
    data = cl.execute_command_string("DEBUG GET QUADRANT 0 0 NUMSTARS")

    assert resp is not None
    assert data == value


def test_debug_set_get_quadrant_starbase():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = "1"

    resp = cl.execute_command_string(f"DEBUG SET QUADRANT 0 0 STARBASE {value}")
    data = cl.execute_command_string("DEBUG GET QUADRANT 0 0 STARBASE")

    assert resp is not None
    assert data == value


def test_debug_set_get_quadrant_explored():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = "1"

    resp = cl.execute_command_string(f"DEBUG SET QUADRANT 0 0 EXPLORED {value}")
    data = cl.execute_command_string("DEBUG GET QUADRANT 0 0 EXPLORED")

    assert resp is not None
    assert data == value


def test_debug_set_get_starship_energy():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = 2000

    resp = cl.execute_command_string(f"DEBUG SET STARSHIP ENERGY {value}")
    data = cl.execute_command_string("DEBUG GET STARSHIP ENERGY")

    assert resp is not None
    assert data == str(value)


def test_debug_set_get_starship_shield():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = 2000

    resp = cl.execute_command_string(f"DEBUG SET STARSHIP SHIELD {value}")
    data = cl.execute_command_string("DEBUG GET STARSHIP SHIELD")

    assert resp is not None
    assert data == str(value)


def test_debug_set_get_starship_torp():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = 2000

    resp = cl.execute_command_string(f"DEBUG SET STARSHIP TORP {value}")
    data = cl.execute_command_string("DEBUG GET STARSHIP TORP")

    assert resp is not None
    assert data == str(value)


def test_debug_set_get_starship_device_damage():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    device_name = "TOR"
    damage_amt = "-3.0"

    resp = cl.execute_command_string(f"DEBUG SET STARSHIP DEVICE {device_name} {damage_amt}")
    data = cl.execute_command_string(f"DEBUG GET STARSHIP DEVICE {device_name}")

    assert resp is not None
    assert data == damage_amt


def test_debug_set_get_starship_sector():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    x = "1"
    y = "2"

    resp = cl.execute_command_string(f"DEBUG SET STARSHIP SECTOR {x} {y}")
    data = cl.execute_command_string("DEBUG GET STARSHIP SECTOR")

    assert resp is not None
    assert data == f"{x}.{y}"


def test_debug_set_get_starship_quadrant():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    x = "2"
    y = "3"

    resp = cl.execute_command_string(f"DEBUG SET STARSHIP QUADRANT {x} {y}")
    data = cl.execute_command_string("DEBUG GET STARSHIP QUADRANT")

    assert resp is not None
    assert data == f"{x}.{y}"


def test_debug_set_get_galaxy_mission_time():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = "1234.0"

    resp = cl.execute_command_string(f"DEBUG SET GALAXY MISSION_TIME {value}")
    data = cl.execute_command_string("DEBUG GET GALAXY MISSION_TIME")

    assert resp is not None
    assert data == value


def test_debug_set_get_galaxy_mission_time_deadline():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    value = "1234.0"

    resp = cl.execute_command_string(f"DEBUG SET GALAXY MISSIONTIMEDEADLINE {value}")
    data = cl.execute_command_string("DEBUG GET GALAXY MISSIONTIMEDEADLINE")

    assert resp is not None
    assert data == value


def test_debug_set_clear_sector_all():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ ALL")

    # if it doesn't get an error, then we're good


def test_debug_set_clear_sector_not_all():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    game = game_builder.GameBuilder.get_game(random_factory)
    cl = command_line.CommandLine(game)

    cl.execute_command_string("DEBUG SET CLEARCQ")

    # if it doesn't get an error, then we're good
