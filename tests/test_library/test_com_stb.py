from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(*, no_starbase: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Preserve the starbase-bearing scenario or select its no-starbase variant."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_star_quantity(2)
        .set_enemy_chance(100)
        .set_starbase_chance(0 if no_starbase else 100)
        .set_coords(gbl.RCT_STAR_LOCATION, *((7, 6), (6, 6)) * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *((7, 7), (6, 7), (5, 7)) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .build()
    )


def test_com_stb_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_stb()

    assert result is not None


def test_com_stb_has_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.com_stb()

    assert result.command_result == CommandResult.OK


def test_com_stb_damaged():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3
    result = game_var.com_stb()

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.COM_STB


def test_com_stb_verify_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.com_stb()

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.COM_STB
    assert result.com_stb.direction == 7
    assert result.com_stb.distance == 6


def test_com_stb_no_starbase():
    test_mock = create_random_factory(no_starbase=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.com_stb()

    assert result.command_result == CommandResult.CPU_STB_NO_STARBASE_PRESENT
    assert result.command == Commands.COM_STB
