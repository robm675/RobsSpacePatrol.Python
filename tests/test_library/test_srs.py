from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def test_srs_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.srs()

    assert result is not None


def test_srs_has_contents():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.srs()

    assert result.command_result == CommandResult.OK


def test_srs_damaged():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.SRS).damage_level = -3
    result = game_var.srs()

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.SRS


def test_srs_verify_contents():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)
    result = game_var.srs()

    srs_res = result.srs.sectors

    assert len(srs_res) == gbl.MAX_QUADRANT_SECTOR_XY * gbl.MAX_QUADRANT_SECTOR_XY
