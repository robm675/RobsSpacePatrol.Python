from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(*, no_enemies: bool = False, quadrant_visits: int = 1) -> RandomFactory:
    """Build fresh responses; allow one placement sequence per quadrant visit."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_starship_sector(0, 0)
        .set_star_quantity(2)
        .set_enemy_chance(0 if no_enemies else 100)
        .set_starbase_chance(0 if no_enemies else 100)
        .set_coords(gbl.RCT_STAR_LOCATION, *((7, 6), (7, 7)) * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *((0, 1), (0, 2), (0, 3)) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .build()
    )


def find_enemy(direction_to_enemies, x, y):
    return next(e for e in direction_to_enemies if e.coord.x == x and e.coord.y == y)


def test_com_tor_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_tor()

    assert result is not None


def test_com_tor_has_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.com_tor()

    assert result.command_result == CommandResult.OK


def test_com_tor_damaged():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3
    result = game_var.com_tor()

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.COM_TOR


def test_com_tor_verify_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    print(game_var.get_current_quadrant_formatted())

    result = game_var.com_tor()

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.COM_TOR
    assert len(result.com_tor.direction_to_enemies) == 3
    enemy1 = find_enemy(result.com_tor.direction_to_enemies, 0, 1)
    enemy2 = find_enemy(result.com_tor.direction_to_enemies, 0, 2)
    enemy3 = find_enemy(result.com_tor.direction_to_enemies, 0, 3)
    assert enemy1.direction == 7
    assert enemy1.distance == 1
    assert enemy2.direction == 7
    assert enemy2.distance == 2
    assert enemy3.direction == 7
    assert enemy3.distance == 3


def test_com_tor_no_enemies():
    test_mock = create_random_factory(no_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.com_tor()

    assert result.command_result == CommandResult.NO_ENEMIES_PRESENT
    assert result.command == Commands.COM_TOR
