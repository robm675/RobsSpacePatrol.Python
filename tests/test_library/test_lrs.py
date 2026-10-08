from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

from source import gbl
from source.library.factories.current_quadrant_factory import (
    CurrentQuadrantFactory as CurrentQuadrantFactory,
)
from source.library.factories.other_factories import OtherFactories as OtherFactories
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(*, corner: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Use quadrant (2, 2), or (0, 0) for the corner-range scenario."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(*(0, 0) if corner else (2, 2))
        .set_starship_sector(4, 5)
        .set_star_quantity(2)
        .set_enemy_chance(76)
        .set_starbase_chance(96)
        .set_coords(gbl.RCT_STAR_LOCATION, *((0, 1), (1, 1)) * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *((0, 0),) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .build()
    )


def test_lrs_results_not_null():
    cur_quad = CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.lrs()

    assert result is not None


def test_lrs_has_contents():
    cur_quad = CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.lrs()

    assert result.command_result == CommandResult.OK


def test_lrs_damaged():
    cur_quad = CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.LRS).damage_level = -3
    result = game_var.lrs()

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.LRS


def test_lrs_verify_contents():
    test_mock = create_random_factory()

    cur_quad = CurrentQuadrantFactory()
    galaxy = OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    result = game_var.lrs()
    print("\n" + game_var.get_galaxy_formatted())

    lrs_res = result.lrs.quadrants

    assert len(lrs_res) == 9


def test_lrs_marked_explored():
    test_mock = create_random_factory()

    cur_quad = CurrentQuadrantFactory()
    galaxy = OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    result = game_var.lrs()

    explored_quads = [q for q in galaxy.quadrants if q.has_been_explored]

    assert len(explored_quads) == 9
    assert result is not None


def test_lrs_corner_correct_number():
    test_mock = create_random_factory(corner=True)

    cur_quad = CurrentQuadrantFactory()
    galaxy = OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    result = game_var.lrs()

    explored_quads = [q for q in galaxy.quadrants if q.has_been_explored]

    assert len(explored_quads) == 4
    assert result is not None
