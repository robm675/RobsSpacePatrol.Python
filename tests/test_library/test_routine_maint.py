import pytest
from models.game_status import GameStatus
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from source.library.models import coord
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(
    *, with_enemies: bool = False, enemies_moving: bool = False, quadrant_visits: int = 1
) -> RandomFactory:
    """Configure maintenance, including a finite set of healthy-device selections."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    with_enemies = with_enemies or enemies_moving
    builder = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(*(2, 3) if with_enemies else (0, 0))
        .set_star_quantity(2)
        .set_enemy_chance(100 if with_enemies else 0)
        .set_starbase_chance(100)
        .set_coords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 1, 1)
    )
    if with_enemies:
        builder.set_coords(
            gbl.RCT_ENEMY_LOCATION,
            *((0, 1), (0, 2), (0, 3)) * quadrant_visits,
            (4, 3),
            (4, 4),
            (4, 5),
        )
        builder.set_integer(gbl.RIT_ENEMY_SHIELD_LEVEL, 200)
        builder.set_integer(gbl.RIT_ENEMY_FIRED_AMOUNT, 50)
        builder.set_integer(gbl.RIT_DAMAGE_DEVICE_CHANCE, 100)
        builder.set_integer(gbl.RIT_DAMAGE_DEVICE_AMOUNT, 10)
        builder.set_integers(gbl.RIT_DAMAGE_DEVICE, 1, 2, 3, 4, 5, 6, 7)
        builder.set_integer(gbl.RIT_ENEMY_MOVE_CHANCE, 100 if enemies_moving else 0)
    return builder.build()


@pytest.mark.parametrize(
    "sb_x, sb_y",
    [
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 1),
        (2, 1),
        (0, 2),
        (1, 2),
        (2, 2),
    ],
)
def test_docking_works(sb_x: int, sb_y: int):
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.move_object_inside_quadrant(coord.Coord(0, 0), coord.Coord(sb_x, sb_y))
    result = game_var.routine_maint(0.4, False)

    assert result.maint_result.docking_status.current_status is True


def test_not_docked_with_shields_up():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print(game_var.get_current_quadrant_formatted())
    game_var.galaxy.starship.shield_level = 1000
    result = game_var.routine_maint(0.4, False)

    assert result.maint_result.docking_status.current_status is False


@pytest.mark.parametrize(
    "sb_x, sb_y",
    [
        (6, 1),
        (7, 1),
        (7, 4),
        (4, 3),
    ],
)
def test_not_docked_works(sb_x: int, sb_y: int):
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.move_object_inside_quadrant(coord.Coord(0, 0), coord.Coord(sb_x, sb_y))
    result = game_var.routine_maint(0.4, False)

    assert result.maint_result.docking_status.current_status is False


def test_mission_time_changes():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.routine_maint(0.4, False)

    assert result is not None
    assert game_var.galaxy.mission_time == pytest.approx(0.4)


def test_no_repairs_available():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.routine_maint(0.4, False)

    assert result.maint_result.starbase_repairs_available is None
    assert result.maint_result.docking_status.current_status is True


def test_repairs_available():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3

    result = game_var.routine_maint(0, False)

    assert result.maint_result.starbase_repairs_available is not None
    assert result.maint_result.docking_status.current_status is True
    assert result.maint_result.starbase_repairs_available.mission_time_to_repair == 3.0


def test_execute_repairs_available():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3

    result = game_var.routine_maint(0, False)
    game_var.run_starbase_repair()

    assert result is not None
    assert game_var.galaxy.starship.get_device(DeviceType.COM).damage_level == 0
    assert game_var.galaxy.mission_time == 3


def test_damaged_devices_repair_on_mission_time():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -0.5

    result = game_var.routine_maint(1, False)

    assert game_var.galaxy.starship.get_device(DeviceType.COM).damage_level == 100
    assert len(result.maint_result.devices_repair_status_changed) == 1


def test_enemies_fired():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 1000
    print(game_var.get_current_quadrant_formatted())

    result = game_var.routine_maint(1, True)

    assert len(result.maint_result.enemies_fired) == 3


def test_enemies_fired_damaged():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 1000
    print(game_var.get_current_quadrant_formatted())

    result = game_var.routine_maint(0, True)

    assert len(result.maint_result.enemies_fired) == 3
    enemy1_fired = result.maint_result.enemies_fired[0].device_damaged
    enemy2_fired = result.maint_result.enemies_fired[1].device_damaged
    enemy3_fired = result.maint_result.enemies_fired[2].device_damaged

    assert enemy1_fired is not None
    assert enemy2_fired is not None
    assert enemy3_fired is not None
    assert enemy1_fired.damage_level == -10
    assert enemy2_fired.damage_level == -10
    assert enemy3_fired.damage_level == -10


def test_enemies_fired_while_docked():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 0
    print(game_var.get_current_quadrant_formatted())

    result = game_var.routine_maint(0, True)

    assert result.maint_result.docking_status.current_status is True
    assert game_var.galaxy.starship.is_docked is True
    assert game_var.galaxy.starship.is_destroyed is False
    assert len(result.maint_result.enemies_fired) == 3
    enemy1_fired = result.maint_result.enemies_fired[0]
    enemy2_fired = result.maint_result.enemies_fired[1]
    enemy3_fired = result.maint_result.enemies_fired[2]

    assert enemy1_fired.starship_docked is True
    assert enemy2_fired.starship_docked is True
    assert enemy3_fired.starship_docked is True


def test_game_status_ran_out_of_time():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.mission_time = game_var.galaxy.mission_time_deadline + 1

    result = game_var.routine_maint(0, False)

    assert result.maint_result.game_status == GameStatus.RAN_OUT_OF_TIME


def test_game_status_starship_destroyed():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 10

    result = game_var.routine_maint(0, True)

    assert result.maint_result.game_status == GameStatus.STARSHIP_DESTROYED


def test_game_status_no_energy_no_shields():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 0
    game_var.galaxy.starship.energy_level = 0
    game_var.move_object_inside_quadrant(coord.Coord(0, 0), coord.Coord(5, 5))

    result = game_var.routine_maint(0, False)

    assert result.maint_result.game_status == GameStatus.RAN_OUT_OF_ENERGY


def test_game_status_no_energy_shield_avail_not_damaged():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 100
    game_var.galaxy.starship.energy_level = 0
    game_var.move_object_inside_quadrant(coord.Coord(0, 0), coord.Coord(5, 5))

    result = game_var.routine_maint(0, False)

    assert result.maint_result.game_status == GameStatus.OUT_OF_ENERGY_SHIELD_ENERGY_AVAILABLE


def test_game_status_no_energy_shield_avail_damaged():
    test_mock = create_random_factory(with_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.shield_level = 100
    game_var.galaxy.starship.energy_level = 0
    game_var.move_object_inside_quadrant(coord.Coord(0, 0), coord.Coord(5, 5))
    game_var.galaxy.starship.get_device(DeviceType.SHE).damage_level = -3

    result = game_var.routine_maint(0, False)

    assert result.maint_result.game_status == GameStatus.RAN_OUT_OF_ENERGY


def test_game_status_no_more_enemies():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.routine_maint(0, False)

    assert result.maint_result.game_status == GameStatus.MISSION_OVER


def test_enemies_move_during_maint():
    test_mock = create_random_factory(with_enemies=True, enemies_moving=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.routine_maint(0, False)

    assert len(result.maint_result.enemies_moved) == 3
