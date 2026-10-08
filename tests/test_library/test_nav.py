from models.command_result import CommandResult
from models.commands import Commands
from models.nav_message import NavMessage
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(
    *, bottom_right: bool = False, object_in_way: bool = False, quadrant_visits: int = 1
) -> RandomFactory:
    """Choose the normal, bottom-right, or obstructed-route NAV scenario."""
    if bottom_right and object_in_way:
        raise ValueError("Choose bottom_right or object_in_way, not both")
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    stars = ((5, 0), (7, 6), (5, 6)) if object_in_way else ((7, 6), (7, 7))
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(*(7, 7) if bottom_right else (0, 0))
        .set_star_quantity(2)
        .set_coords(gbl.RCT_STAR_LOCATION, *stars * quadrant_visits)
        .build()
    )


def test_nav_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.nav(1, 1)

    assert result is not None


def test_nav_has_contents():
    test_mock = create_random_factory(quadrant_visits=2)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(1, 1)

    assert result.command_result == CommandResult.OK


def test_nav_bad_dir0():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(0, 1)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.INVALID_DIR


def test_nav_bad_dir9():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(9, 1)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.INVALID_DIR


def test_nav_bad_dist0():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(1, 0)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.INVALID_DIST


def test_nav_bad_dist9():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(1, 9)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.INVALID_DIST


def test_nav_damaged_bad_dist1():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.NAV).damage_level = -3

    result = game_var.nav(1, 1)

    assert result.command_result == CommandResult.DAMAGED


def test_nav_outside_galaxy_top():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(3, 1)

    assert result.command == Commands.NAV
    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.BAD_INPUT_OUTSIDE_GALAXY


def test_nav_outside_galaxy_left():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(5, 1)

    assert result.command == Commands.NAV
    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.BAD_INPUT_OUTSIDE_GALAXY


def test_nav_outside_galaxy_bottom():
    test_mock = create_random_factory(bottom_right=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(7, 1)

    assert result.command == Commands.NAV
    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.BAD_INPUT_OUTSIDE_GALAXY


def test_nav_outside_galaxy_right():
    test_mock = create_random_factory(bottom_right=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.nav(1, 1)

    assert result.command == Commands.NAV
    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.BAD_INPUT_OUTSIDE_GALAXY


def test_nav_not_enough_energy_shield_avail():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.energy_level = 10
    game_var.galaxy.starship.shield_level = 1000

    result = game_var.nav(1, 1)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.INSUFFICIENT_ENERGY_SHIELD_ENERGY_AVAILABLE


def test_nav_not_enough_energy():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.energy_level = 10
    game_var.galaxy.starship.shield_level = 0

    result = game_var.nav(1, 1)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.INSUFFICIENT_ENERGY


def test_nav_object_in_way():
    test_mock = create_random_factory(object_in_way=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print(game_var.get_current_quadrant_formatted())

    result = game_var.nav(1, 7)

    assert result.command_result == CommandResult.ERROR
    assert result.nav.nav_message == NavMessage.BAD_INPUT_OBJECT_HIT
    assert result.nav.distance_traveled != 0


def test_nav_damaged_good_inside_quadrant():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.NAV).damage_level = -3
    print(game_var.get_current_quadrant_formatted())

    result = game_var.nav(1, 0.1)

    assert result.command_result == CommandResult.OK
    assert result.nav.nav_message == NavMessage.TRANSIT_COMPLETE
    assert result.nav.distance_traveled != 0
    assert game_var.galaxy.starship.energy_level != gbl.MAX_STARSHIP_ENERGY


def test_nav_damaged_good_different_quadrant():
    test_mock = create_random_factory(quadrant_visits=2)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print(game_var.get_current_quadrant_formatted())

    result = game_var.nav(1, 7)

    assert result.command_result == CommandResult.OK
    assert result.nav.nav_message == NavMessage.TRANSIT_COMPLETE
    assert result.nav.distance_traveled != 0
    assert game_var.galaxy.starship.energy_level != gbl.MAX_STARSHIP_ENERGY


def test_nav_verify_starship_sector():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print(game_var.get_current_quadrant_formatted())

    result = game_var.nav(1, 0.5)

    assert result is not None
    assert game_var.galaxy.get_starship_sector().coord.x == 4
    assert game_var.galaxy.get_starship_sector().coord.y == 0


def test_nav_verify_location_after_warp1():
    test_mock = create_random_factory(quadrant_visits=2)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print(game_var.get_current_quadrant_formatted())

    result = game_var.nav(1, 1)

    assert result is not None
    assert game_var.galaxy.get_starship_sector().coord.x == 0
    assert game_var.galaxy.get_starship_sector().coord.y == 0
    assert game_var.galaxy.current_quadrant.coord.x == 1
    assert game_var.galaxy.current_quadrant.coord.y == 0


def test_nav_verify_location_after_warp1_point1():
    test_mock = create_random_factory(quadrant_visits=2)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print(game_var.get_current_quadrant_formatted())

    result = game_var.nav(1, 1.1)

    assert result is not None
    assert game_var.galaxy.get_starship_sector().coord.x == 1
    assert game_var.galaxy.get_starship_sector().coord.y == 0
    assert game_var.galaxy.current_quadrant.coord.x == 1
    assert game_var.galaxy.current_quadrant.coord.y == 0
