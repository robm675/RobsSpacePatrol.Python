from models.command_result import CommandResult
from models.commands import Commands
from models.object_hit import ObjectHit
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(
    *,
    no_enemies: bool = False,
    laser_miss: bool = False,
    star_survives: bool = False,
    quadrant_visits: int = 1,
) -> RandomFactory:
    """Configure the laser scenario without negative fallback shield values."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_star_quantity(2)
        .set_enemy_chance(0 if no_enemies else 100)
        .set_starbase_chance(0 if no_enemies else 100)
        .set_integer(gbl.RIT_ENEMY_SHIELD_LEVEL, 300)
        .set_integer(gbl.RIT_LASER_MISS_CHANCE, 100 if laser_miss else 0)
        .set_integer(gbl.RIT_STAR_DESTROYED_CHANCE, 0 if star_survives else 100)
        .set_coords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *((0, 1), (0, 2), (0, 3)) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .build()
    )


def find_by_coord(items, x, y):
    return next(item for item in items if item.coord.x == x and item.coord.y == y)


def test_las_results_not_null():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.las(10)

    assert result is not None


def test_las_has_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.las(7)

    assert result.command_result == CommandResult.OK


def test_las_damaged():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.LAS).damage_level = -3
    result = game_var.las(7)

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.LAS


def test_las_verify_contents_hit_enemy():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.las(400)

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.LAS
    assert game_var.galaxy.starship.energy_level == gbl.MAX_STARSHIP_ENERGY - 400

    assert len(result.las.object_hit_report) == 3
    enemy1 = find_by_coord(result.las.object_hit_report, 0, 1)
    enemy2 = find_by_coord(result.las.object_hit_report, 0, 2)
    enemy3 = find_by_coord(result.las.object_hit_report, 0, 3)

    assert enemy1.missed is False
    assert enemy1.missed is False
    assert enemy2.missed is False
    assert enemy3.missed is False

    assert enemy1.destroyed is False
    assert enemy2.destroyed is False
    assert enemy3.destroyed is False

    assert enemy1.unit_hit != 0
    assert enemy2.unit_hit != 0
    assert enemy3.unit_hit != 0

    assert enemy1.object_hit == ObjectHit.ENEMY
    assert enemy2.object_hit == ObjectHit.ENEMY
    assert enemy3.object_hit == ObjectHit.ENEMY


def test_las_verify_contents_miss_enemy():
    test_mock = create_random_factory(laser_miss=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3

    result = game_var.las(100)

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.LAS
    assert game_var.galaxy.starship.energy_level == gbl.MAX_STARSHIP_ENERGY - 100

    assert len(result.las.object_hit_report) == 3
    enemy1 = find_by_coord(result.las.object_hit_report, 0, 1)
    enemy2 = find_by_coord(result.las.object_hit_report, 0, 2)
    enemy3 = find_by_coord(result.las.object_hit_report, 0, 3)

    assert enemy1.missed is True
    assert enemy2.missed is True
    assert enemy3.missed is True

    assert enemy1.destroyed is False
    assert enemy2.destroyed is False
    assert enemy3.destroyed is False

    assert enemy1.unit_hit == 0
    assert enemy2.unit_hit == 0
    assert enemy3.unit_hit == 0

    assert enemy1.object_hit == ObjectHit.NOTHING
    assert enemy2.object_hit == ObjectHit.NOTHING
    assert enemy3.object_hit == ObjectHit.NOTHING
