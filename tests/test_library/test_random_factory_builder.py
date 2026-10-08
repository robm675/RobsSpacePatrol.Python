import pytest

from source import gbl
from source.library.factories.current_quadrant_factory import CurrentQuadrantFactory
from source.library.factories.other_factories import OtherFactories
from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli.game_builder import GameBuilder


def test_constant_responses_repeat_and_coordinates_are_fresh():
    factory = RandomFactoryBuilder().set_enemy_chance(80).set_starship_sector(2, 3).build()
    assert [factory.get_random_integer(gbl.RIT_ENEMY_CHANCE) for _ in range(3)] == [80] * 3
    first = factory.get_random_coord(gbl.RCT_STARSHIP_SECTOR)
    first.x = 7
    second = factory.get_random_coord(gbl.RCT_STARSHIP_SECTOR)
    assert (second.x, second.y) == (2, 3)
    assert first is not second


def test_sequences_are_independent_between_builds_and_request_types():
    builder = (
        RandomFactoryBuilder()
        .set_integers(gbl.RIT_ENEMY_FIRED_AMOUNT, 10, 20)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2))
    )
    first = builder.build()
    second = builder.build()
    assert first.get_random_integer(gbl.RIT_ENEMY_FIRED_AMOUNT) == 10
    assert first.get_random_integer(gbl.RIT_ENEMY_FIRED_AMOUNT) == 20
    assert second.get_random_integer(gbl.RIT_ENEMY_FIRED_AMOUNT) == 10
    assert first.get_random_coord(gbl.RCT_ENEMY_LOCATION).y == 1
    assert first.get_random_coord(gbl.RCT_ENEMY_LOCATION).y == 2
    assert second.get_random_coord(gbl.RCT_ENEMY_LOCATION).y == 1
    with pytest.raises(AssertionError, match="exhausted.*ENEMYFIREDAMOUNT"):
        first.get_random_integer(gbl.RIT_ENEMY_FIRED_AMOUNT)
    with pytest.raises(AssertionError, match="exhausted.*ENEMYLOCATION"):
        first.get_random_coord(gbl.RCT_ENEMY_LOCATION)


def test_single_element_sequence_does_not_repeat():
    factory = RandomFactoryBuilder().set_integers(gbl.RIT_ENEMY_CHANCE, 0).build()
    assert factory.get_random_integer(gbl.RIT_ENEMY_CHANCE) == 0
    with pytest.raises(AssertionError, match="exhausted"):
        factory.get_random_integer(gbl.RIT_ENEMY_CHANCE)


def test_unconfigured_requests_and_raw_generator_fail():
    factory = RandomFactoryBuilder().build()
    with pytest.raises(AssertionError, match="not configured|No test random response"):
        factory.get_random_integer(gbl.RIT_ENEMY_CHANCE)
    with pytest.raises(AssertionError, match="No test random response"):
        factory.get_random_coord(gbl.RCT_STAR_LOCATION)
    with pytest.raises(AssertionError, match="real random generator"):
        factory.get_random_integer_from_generator(0, 100)


def test_builder_changes_do_not_change_existing_factory():
    builder = RandomFactoryBuilder().set_enemy_chance(80)
    first = builder.build()
    builder.set_enemy_chance(0)
    assert first.get_random_integer(gbl.RIT_ENEMY_CHANCE) == 80
    assert builder.build().get_random_integer(gbl.RIT_ENEMY_CHANCE) == 0


def test_invalid_response_setup_fails_early():
    builder = RandomFactoryBuilder()
    with pytest.raises(ValueError):
        builder.set_integers(gbl.RIT_ENEMY_CHANCE)
    with pytest.raises(TypeError):
        builder.set_integer(gbl.RIT_ENEMY_CHANCE, 1.5)  # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        builder.set_coords(gbl.RCT_ENEMY_LOCATION)
    with pytest.raises(ValueError):
        builder.set_starship_sector(8, 0)
    with pytest.raises(TypeError):
        builder.set_starship_sector(0, 1.5)  # pyright: ignore[reportArgumentType]


def test_defaults_create_game_with_injected_factory_and_no_random_calls(monkeypatch):
    def unexpected_random(*args):
        raise AssertionError("Real randomness was called")

    monkeypatch.setattr("random.randint", unexpected_random)
    factory = RandomFactoryBuilder().with_defaults().build()
    game = GameBuilder.get_game(factory)
    assert game.random_factory is factory
    assert game.galaxy.mission_time == 0
    assert game.galaxy.get_starship_sector().coord.x == 0
    assert sum(quadrant.num_enemies for quadrant in game.galaxy.quadrants) == 0


def test_multiple_objects_use_distinct_configured_locations():
    factory = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_star_quantity(2)
        .set_enemy_chance(100)
        .set_starbase_chance(100)
        .set_coords(gbl.RCT_STAR_LOCATION, (7, 6), (7, 7))
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 6)
        .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .build()
    )
    galaxy = OtherFactories.create_galaxy(factory, CurrentQuadrantFactory())
    sectors = galaxy.current_quadrant.sectors
    assert sum(s.sector_contents.sector_contents == gbl.SECTOR_STAR for s in sectors) == 2
    assert sum(s.sector_contents.sector_contents == gbl.SECTOR_ENEMY for s in sectors) == 3
    assert sum(s.sector_contents.sector_contents == gbl.SECTOR_STARBASE for s in sectors) == 1
