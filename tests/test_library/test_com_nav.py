from unittest.mock import MagicMock

from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from source.library.models import coord
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(*, no_enemies: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Default to the empty COM NAV setup; no_enemies selects its two-star variant."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_star_quantity(2 if no_enemies else 0)
        .set_coords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .build()
    )


def test_com_nav_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_nav(coord.Coord(0, 0), coord.Coord(0, 1))

    assert result is not None


def test_com_nav_has_contents():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    test_mock = random_factory
    test_mock.get_random_integer = MagicMock()
    test_mock.get_random_integer.side_effect = mock_random_int
    test_mock.get_random_coord = MagicMock()
    test_mock.get_random_coord.side_effect = mock_random_coord

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.com_nav(coord.Coord(0, 0), coord.Coord(0, 1))

    assert result.command_result == CommandResult.OK


def test_com_nav_damaged():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    test_mock = random_factory
    test_mock.get_random_integer = MagicMock()
    test_mock.get_random_integer.side_effect = mock_random_int
    test_mock.get_random_coord = MagicMock()
    test_mock.get_random_coord.side_effect = mock_random_coord

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3

    result = game_var.com_nav(coord.Coord(0, 0), coord.Coord(0, 1))

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.COM_NAV


def test_com_nav_verify_contents_x():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    test_mock = random_factory
    test_mock.get_random_integer = MagicMock()
    test_mock.get_random_integer.side_effect = mock_random_int
    test_mock.get_random_coord = MagicMock()
    test_mock.get_random_coord.side_effect = mock_random_coord

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    print(game_var.get_current_quadrant_formatted())

    result = game_var.com_nav(coord.Coord(2, 0), coord.Coord(0, 0))

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.COM_NAV
    assert result.com_nav.distance == 2.0
    assert result.com_nav.direction == 1


def test_com_nav_verify_contents_y():
    random_factory = RandomFactoryBuilder().with_defaults().build()
    test_mock = random_factory
    test_mock.get_random_integer = MagicMock()
    test_mock.get_random_integer.side_effect = mock_random_int
    test_mock.get_random_coord = MagicMock()
    test_mock.get_random_coord.side_effect = mock_random_coord

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    print(game_var.get_current_quadrant_formatted())

    result = game_var.com_nav(coord.Coord(0, 2), coord.Coord(0, 0))

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.COM_NAV
    assert result.com_nav.distance == 2.0
    assert result.com_nav.direction == 7


def mock_random_int(random_type: str):
    if random_type == gbl.RIT_STAR_QUANTITY:
        return 0
    if random_type == gbl.RIT_ENEMY_CHANCE:
        return 0
    if random_type == gbl.RIT_STARBASE_CHANCE:
        return 0
    if random_type == gbl.RIT_STARTING_MISSION_TIME:
        return 2450
    return -1


def mock_random_int_no_enemies(random_type: str):
    if random_type == gbl.RIT_STAR_QUANTITY:
        return 2
    if random_type == gbl.RIT_ENEMY_CHANCE:
        return 0
    if random_type == gbl.RIT_STARBASE_CHANCE:
        return 0
    if random_type == gbl.RIT_STARTING_MISSION_TIME:
        return 2450
    return -1


def mock_random_coord(random_type: str) -> coord.Coord:
    if random_type == gbl.RCT_STARSHIP_QUADRANT:
        return coord.Coord(0, 0)
    if random_type == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(0, 0)
    if random_type == gbl.RCT_ENEMY_LOCATION:
        mock_random_coord.counter += 1
        if mock_random_coord.counter > 2:
            mock_random_coord.counter = 0

        if mock_random_coord.counter == 0:
            return coord.Coord(0, 1)
        if mock_random_coord.counter == 1:
            return coord.Coord(0, 2)
        if mock_random_coord.counter == 2:
            return coord.Coord(0, 3)
        raise RuntimeError("Invalid counter")

    if random_type == gbl.RCT_STAR_LOCATION:
        return coord.Coord(7, 6)
    if random_type == gbl.RCT_STARBASE_LOCATION:
        return coord.Coord(0, 6)
    return coord.Coord(-10, -10)


mock_random_coord.counter = -1
