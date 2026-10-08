from models.command_result import CommandResult
from models.commands import Commands
from models.starship import DeviceType

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source.library.game import game
from tests.random_factory_builder import RandomFactoryBuilder


def test_com_rec_results_not_null():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_rec()

    assert result is not None


def test_com_rec_has_contents():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_rec()

    assert result.command_result == CommandResult.OK


def test_com_rec_damaged():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)
    game_var.galaxy.starship.get_device(DeviceType.COM).damage_level = -3
    result = game_var.com_rec()

    assert result.command_result == CommandResult.DAMAGED
    assert result.command == Commands.COM_REC


def test_com_rec_verify_contents():
    cur_quad = cqf.CurrentQuadrantFactory()
    random_factory = RandomFactoryBuilder().with_defaults().build()
    galaxy = other_fact.OtherFactories.create_galaxy(random_factory, cur_quad)
    game_var = game.Game(galaxy, random_factory, cur_quad)

    result = game_var.com_rec()

    assert len(result.com_rec.quadrants) != 0
