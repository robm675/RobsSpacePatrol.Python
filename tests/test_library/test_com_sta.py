from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(*, quadrant_visits: int = 1) -> RandomFactory:
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_starship_sector(4, 5)
        .set_star_quantity(2)
        .set_enemy_chance(100)
        .set_starbase_chance(100)
        .set_coords(gbl.RCT_STAR_LOCATION, *((0, 1), (1, 1)) * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *((0, 0), (1, 0), (2, 0)) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 4, 6)
        .build()
    )


def test_com_sta_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_sta()

    assert result is not None


def test_com_sta_has_contents():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_sta()

    assert result.command_result == CommandResult.OK


def test_com_sta_damaged():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3
    result = game_var.com_sta()

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.COM_STA


def test_com_sta_verify_contents():
    test_mock = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_starship_sector(4, 5)
        .set_enemy_chance(100)
        .set_starbase_chance(100)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 0), (2, 2), (3, 3))
        .set_coords(gbl.RCT_STAR_LOCATION, (0, 1))
        .set_coords(gbl.RCT_STARBASE_LOCATION, (4, 6))
        .build()
    )

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.energy_level = 1234
    game_var.galaxy.starship.shield_level = 321
    game_var.galaxy.starship.torps_remain = 12
    game_var.galaxy.starship.is_docked = True

    result = game_var.com_sta()

    assert result.com_sta.mission_time == 0
    assert (
        result.com_sta.enemies_remaining
        == gbl.MAX_QUADRANT_SECTOR_XY * gbl.MAX_QUADRANT_SECTOR_XY * 3
    )
    assert result.com_sta.energy_remaining == 1234
    assert result.com_sta.shield_level == 321
    assert result.com_sta.torps_remaining == 12
    assert result.com_sta.starbases_remaining == 64
    assert result.com_sta.docked is True
    assert result.com_sta.quadrant_coord.x == 2
    assert result.com_sta.quadrant_coord.y == 3
    assert result.com_sta.sector_coord.x == 4
    assert result.com_sta.sector_coord.y == 5
    assert result.com_sta.mission_time_deadline == result.com_sta.mission_time + (
        result.com_sta.enemies_remaining * gbl.MISSION_TIME_PER_ENEMY_RATIO
    )
