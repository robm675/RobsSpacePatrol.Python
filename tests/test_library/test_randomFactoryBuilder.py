import pytest

from source import gbl
from source.library.factories.currentQuadrantFactory import CurrentQuadrantFactory
from source.library.factories.otherFactories import otherFactories
from tests.randomFactoryBuilder import RandomFactoryBuilder
from tests.test_cli.gameBuilder import GameBuilder


def test_constant_responses_repeat_and_coordinates_are_fresh():
    factory = (RandomFactoryBuilder()
               .SetEnemyChance(80)
               .SetStarshipSector(2, 3)
               .Build())
    assert [factory.GetRandomInteger(gbl.RIT_ENEMY_CHANCE) for _ in range(3)] == [80] * 3
    first = factory.GetRandomCoord(gbl.RCT_STARSHIP_SECTOR)
    first.x = 7
    second = factory.GetRandomCoord(gbl.RCT_STARSHIP_SECTOR)
    assert (second.x, second.y) == (2, 3)
    assert first is not second


def test_sequences_are_independent_between_builds_and_request_types():
    builder = (RandomFactoryBuilder()
               .SetIntegers(gbl.RIT_ENEMY_FIRED_AMOUNT, 10, 20)
               .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2)))
    first = builder.Build()
    second = builder.Build()
    assert first.GetRandomInteger(gbl.RIT_ENEMY_FIRED_AMOUNT) == 10
    assert first.GetRandomInteger(gbl.RIT_ENEMY_FIRED_AMOUNT) == 20
    assert second.GetRandomInteger(gbl.RIT_ENEMY_FIRED_AMOUNT) == 10
    assert first.GetRandomCoord(gbl.RCT_ENEMY_LOCATION).y == 1
    assert first.GetRandomCoord(gbl.RCT_ENEMY_LOCATION).y == 2
    assert second.GetRandomCoord(gbl.RCT_ENEMY_LOCATION).y == 1
    with pytest.raises(AssertionError, match="exhausted.*ENEMYFIREDAMOUNT"):
        first.GetRandomInteger(gbl.RIT_ENEMY_FIRED_AMOUNT)
    with pytest.raises(AssertionError, match="exhausted.*ENEMYLOCATION"):
        first.GetRandomCoord(gbl.RCT_ENEMY_LOCATION)


def test_single_element_sequence_does_not_repeat():
    factory = RandomFactoryBuilder().SetIntegers(gbl.RIT_ENEMY_CHANCE, 0).Build()
    assert factory.GetRandomInteger(gbl.RIT_ENEMY_CHANCE) == 0
    with pytest.raises(AssertionError, match="exhausted"):
        factory.GetRandomInteger(gbl.RIT_ENEMY_CHANCE)


def test_unconfigured_requests_and_raw_generator_fail():
    factory = RandomFactoryBuilder().Build()
    with pytest.raises(AssertionError, match="not configured|No test random response"):
        factory.GetRandomInteger(gbl.RIT_ENEMY_CHANCE)
    with pytest.raises(AssertionError, match="No test random response"):
        factory.GetRandomCoord(gbl.RCT_STAR_LOCATION)
    with pytest.raises(AssertionError, match="real random generator"):
        factory.GetRandomIntegerFromGenerator(0, 100)


def test_builder_changes_do_not_change_existing_factory():
    builder = RandomFactoryBuilder().SetEnemyChance(80)
    first = builder.Build()
    builder.SetEnemyChance(0)
    assert first.GetRandomInteger(gbl.RIT_ENEMY_CHANCE) == 80
    assert builder.Build().GetRandomInteger(gbl.RIT_ENEMY_CHANCE) == 0


def test_invalid_response_setup_fails_early():
    builder = RandomFactoryBuilder()
    with pytest.raises(ValueError):
        builder.SetIntegers(gbl.RIT_ENEMY_CHANCE)
    with pytest.raises(TypeError):
        builder.SetInteger(gbl.RIT_ENEMY_CHANCE, 1.5) # pyright: ignore[reportArgumentType]
    with pytest.raises(ValueError):
        builder.SetCoords(gbl.RCT_ENEMY_LOCATION)
    with pytest.raises(ValueError):
        builder.SetStarshipSector(8, 0)
    with pytest.raises(TypeError):
        builder.SetStarshipSector(0, 1.5) # pyright: ignore[reportArgumentType]


def test_defaults_create_game_with_injected_factory_and_no_random_calls(monkeypatch):
    def unexpected_random(*args):
        raise AssertionError("Real randomness was called")

    monkeypatch.setattr("random.randint", unexpected_random)
    factory = RandomFactoryBuilder().WithDefaults().Build()
    game = GameBuilder.getGame(factory)
    assert game.randomFactory is factory
    assert game.galaxy.MissionTime == 0
    assert game.galaxy.GetStarshipSector().coord.x == 0
    assert sum(quadrant.NumEnemies for quadrant in game.galaxy.Quadrants) == 0


def test_multiple_objects_use_distinct_configured_locations():
    factory = (RandomFactoryBuilder().WithDefaults()
               .SetStarQuantity(2)
               .SetEnemyChance(100)
               .SetStarbaseChance(100)
               .SetCoords(gbl.RCT_STAR_LOCATION, (7, 6), (7, 7))
               .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 6)
               .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
               .Build())
    galaxy = otherFactories.createGalaxy(factory, CurrentQuadrantFactory())
    sectors = galaxy.CurrentQuadrant.sectors
    assert sum(s.sectorContents.sectorContents == gbl.SECTOR_STAR for s in sectors) == 2
    assert sum(s.sectorContents.sectorContents == gbl.SECTOR_ENEMY for s in sectors) == 3
    assert sum(s.sectorContents.sectorContents == gbl.SECTOR_STARBASE for s in sectors) == 1
