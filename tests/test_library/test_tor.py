from models import object_hit
from models.command_result import CommandResult
from models.commands import Commands
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
    hit_star: bool = False,
    hit_starbase: bool = False,
    star_survives: bool = False,
    quadrant_visits: int = 1,
) -> RandomFactory:
    """Configure TOR targets while retaining each scenario's first obstacle."""
    if hit_star and hit_starbase:
        raise ValueError("Choose hit_star or hit_starbase, not both")
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    enemies = ((5, 1), (5, 2), (5, 3)) if hit_star or hit_starbase else ((0, 1), (0, 2), (0, 3))
    stars = ((0, 2), (7, 6)) if hit_star else ((4, 2), (7, 6)) if hit_starbase else ((7, 6), (7, 7))
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_star_quantity(2)
        .set_enemy_chance(0 if no_enemies else 100)
        .set_starbase_chance(0 if no_enemies else 100)
        .set_integer(gbl.RIT_STAR_DESTROYED_CHANCE, 0 if star_survives else 100)
        .set_coords(gbl.RCT_STAR_LOCATION, *stars * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *enemies * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .build()
    )


def test_tor_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.tor(0)

    assert result is not None


def test_tor_has_contents():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.tor(7)

    assert result.command_result == CommandResult.OK


def test_tor_damaged():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.TOR).damage_level = -3
    result = game_var.tor(7)

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.TOR


def test_tor_verify_contents_hit_enemy():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.tor(7)

    assert result.command_result == CommandResult.OK
    assert result.command == Commands.TOR
    assert result.tor.object_hit_report.object_hit == object_hit.ObjectHit.ENEMY
    assert result.tor.object_hit_report.destroyed is True
    assert game_var.galaxy.starship.torps_remain == gbl.MAX_STARSHIP_TORP - 1
    assert result.tor.object_hit_report.coord.x == 0
    assert result.tor.object_hit_report.coord.y == 1


def test_tor_verify_contents_miss_enemy():
    test_mock = create_random_factory()

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.tor(1)

    assert result.command_result == CommandResult.TOR_MISSED
    assert result.command == Commands.TOR
    assert game_var.galaxy.starship.torps_remain == gbl.MAX_STARSHIP_TORP - 1


def test_tor_verify_contents_hit_star_destroyed():
    test_mock = create_random_factory(star_survives=False, hit_star=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.tor(7)

    assert result.command == Commands.TOR
    assert game_var.galaxy.starship.torps_remain == gbl.MAX_STARSHIP_TORP - 1
    assert result.command_result == CommandResult.OK
    assert result.tor.object_hit_report.object_hit == object_hit.ObjectHit.STAR
    assert result.tor.object_hit_report.destroyed is True
    assert result.tor.object_hit_report.star_survived is False
    assert result.tor.object_hit_report.coord.x == 0
    assert result.tor.object_hit_report.coord.y == 2


def test_tor_verify_contents_hit_star_survives():
    test_mock = create_random_factory(hit_star=True, star_survives=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.tor(7)

    assert result.command == Commands.TOR
    assert game_var.galaxy.starship.torps_remain == gbl.MAX_STARSHIP_TORP - 1
    assert result.command_result == CommandResult.OK
    assert result.tor.object_hit_report.object_hit == object_hit.ObjectHit.STAR
    assert result.tor.object_hit_report.destroyed is False
    assert result.tor.object_hit_report.star_survived is True
    assert result.tor.object_hit_report.coord.x == 0
    assert result.tor.object_hit_report.coord.y == 2


def test_tor_no_enemies():
    test_mock = create_random_factory(no_enemies=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)

    result = game_var.tor(7)

    assert result.command_result == CommandResult.NO_ENEMIES_PRESENT
    assert result.command == Commands.TOR


def test_tor_verify_contents_hit_starbase():
    test_mock = create_random_factory(hit_starbase=True)

    cur_quad = cqf.CurrentQuadrantFactory()
    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)
    game_var = game.Game(galaxy, test_mock, cur_quad)
    print("\n" + game_var.get_current_quadrant_formatted())

    result = game_var.tor(7)

    assert result.command == Commands.TOR
    assert game_var.galaxy.starship.torps_remain == gbl.MAX_STARSHIP_TORP - 1
    assert result.command_result == CommandResult.OK
    assert result.tor.object_hit_report.object_hit == object_hit.ObjectHit.STARBASE
    assert result.tor.object_hit_report.destroyed is True
    assert result.tor.object_hit_report.coord.x == 0
    assert result.tor.object_hit_report.coord.y == 6
