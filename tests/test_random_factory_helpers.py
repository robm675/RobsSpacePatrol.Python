import importlib

import pytest

from source import gbl
from source.library.factories.current_quadrant_factory import CurrentQuadrantFactory
from source.library.factories.other_factories import OtherFactories

SCENARIOS = [
    ("test_galaxy_factory", {}),
    ("test_current_quadrant_builder", {}),
    ("test_quadrant_factory", {}),
    ("test_calculation_utils", {}),
    ("test_com_nav", {}),
    ("test_com_nav", {"no_enemies": True}),
    ("test_com_sta", {}),
    ("test_com_stb", {}),
    ("test_com_stb", {"no_starbase": True}),
    ("test_com_tor", {}),
    ("test_com_tor", {"no_enemies": True}),
    ("test_dam", {}),
    ("test_dam", {"no_enemies": True}),
    ("test_lrs", {}),
    ("test_lrs", {"corner": True}),
    ("test_nav", {}),
    ("test_nav", {"bottom_right": True}),
    ("test_nav", {"object_in_way": True}),
    ("test_las", {}),
    ("test_las", {"no_enemies": True}),
    ("test_las", {"laser_miss": True}),
    ("test_las", {"star_survives": True}),
    ("test_she", {}),
    ("test_she", {"no_enemies": True}),
    ("test_tor", {}),
    ("test_tor", {"no_enemies": True}),
    ("test_tor", {"hit_star": True}),
    ("test_tor", {"hit_star": True, "star_survives": True}),
    ("test_tor", {"hit_starbase": True, "star_survives": True}),
    ("routineMaint", {}),
    ("routineMaint", {"with_enemies": True}),
    ("routineMaint", {"enemies_moving": True}),
]


def load_helper(name):
    path = (
        "tests.test_library.test_routine_maint"
        if name == "routineMaint"
        else f"tests.test_library.{name}"
    )
    return importlib.import_module(path).create_random_factory


@pytest.mark.parametrize("module, options", SCENARIOS)
def test_helper_creates_consistent_galaxy_without_real_randomness(module, options, monkeypatch):
    def unexpected_random(*args):
        raise AssertionError("Helper called real randomness")

    monkeypatch.setattr("random.randint", unexpected_random)
    helper = load_helper(module)
    galaxies = []
    for _ in range(2):
        factory = helper(**options)
        galaxy = OtherFactories.create_galaxy(factory, CurrentQuadrantFactory())
        quadrant = galaxy.get_starship_quadrant()
        contents = [
            sector.sector_contents.sector_contents for sector in galaxy.current_quadrant.sectors
        ]
        assert contents.count(gbl.SECTOR_STARSHIP) == 1
        assert contents.count(gbl.SECTOR_STAR) == quadrant.num_stars
        assert contents.count(gbl.SECTOR_ENEMY) == quadrant.num_enemies
        assert contents.count(gbl.SECTOR_STARBASE) == int(quadrant.has_star_base)
        assert all(
            sector.enemy.shield_level > 0
            for sector in galaxy.current_quadrant.get_enemy_sectors() or []
        )
        galaxies.append(contents)
    assert galaxies[0] == galaxies[1]


def test_multiple_quadrant_visits_have_independent_placement_sequences():
    factory = load_helper("test_com_tor")(quadrant_visits=2)
    galaxy = OtherFactories.create_galaxy(factory, CurrentQuadrantFactory())
    next_quadrant = galaxy.get_quadrant(3, 3)
    current = CurrentQuadrantFactory.create_current_quadrant(
        next_quadrant,
        factory,
        galaxy.get_starship_sector().coord,
    )
    assert len(current.get_enemy_sectors()) == 3
    assert sum(s.sector_contents.sector_contents == gbl.SECTOR_STAR for s in current.sectors) == 2
    with pytest.raises(AssertionError, match="exhausted"):
        factory.get_random_coord(gbl.RCT_STAR_LOCATION)


def test_movement_and_device_selection_have_fresh_responses():
    helper = load_helper("routineMaint")
    first, second = helper(enemies_moving=True), helper(enemies_moving=True)
    OtherFactories.create_galaxy(first, CurrentQuadrantFactory())
    OtherFactories.create_galaxy(second, CurrentQuadrantFactory())
    assert first.get_random_coord(gbl.RCT_ENEMY_LOCATION).to_string() == "(4,3)"
    assert second.get_random_coord(gbl.RCT_ENEMY_LOCATION).to_string() == "(4,3)"
    assert first.get_random_integer(gbl.RIT_DAMAGE_DEVICE) == 1
    assert first.get_random_integer(gbl.RIT_DAMAGE_DEVICE) == 2
    assert second.get_random_integer(gbl.RIT_DAMAGE_DEVICE) == 1
