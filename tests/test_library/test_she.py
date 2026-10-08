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


def test_she_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.she(100)

    assert result is not None


def test_she_has_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.she(100)

    assert result.command_result == CommandResult.OK


def test_she_damaged():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.SHE).damage_level = -3
    result = game_var.she(100)

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.SHE


def test_she_verify_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.she(100)

    assert result is not None
    assert game_var.galaxy.starship.energy_level == gbl.MAX_STARSHIP_ENERGY - 100
    assert game_var.galaxy.starship.shield_level == 100


def test_she_bad_value():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.she(4000)

    assert result.command_result == CommandResult.ERROR
    assert result.she.error_message == gbl.SHE_ERRORMESSAGE
    assert result.command == Commands.SHE
