import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.other_factories as other_fact
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.models import coord
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory(*, quadrant_visits: int = 1) -> RandomFactory:
    """Create the original one-enemy, two-star, starbase galaxy scenario."""
    if type(quadrant_visits) is not int or quadrant_visits < 1:
        raise ValueError("quadrant_visits must be a positive integer")
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_starship_sector(4, 5)
        .set_star_quantity(2)
        .set_enemy_chance(76)
        .set_starbase_chance(96)
        .set_coords(gbl.RCT_STAR_LOCATION, *((0, 1), (1, 1)) * quadrant_visits)
        .set_coords(gbl.RCT_ENEMY_LOCATION, *((0, 0),) * quadrant_visits)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .build()
    )


def test_galaxy_factory():
    test_mock = (
        RandomFactoryBuilder()
        .with_defaults()
        .set_star_quantity(2)
        .set_starship_quadrant(2, 3)
        .set_starship_sector(4, 5)
        .set_enemy_chance(76)
        .set_coords(gbl.RCT_STAR_LOCATION, (7, 6), (7, 7), (6, 6))
        .set_coords(gbl.RCT_ENEMY_LOCATION, (5, 6), (5, 7), (5, 6))
        .build()
    )

    cur_quad = cqf.CurrentQuadrantFactory()

    galaxy = other_fact.OtherFactories.create_galaxy(test_mock, cur_quad)

    assert len(galaxy.quadrants) == 64
    assert galaxy.mission_time == 0
    assert galaxy.current_quadrant.coord.x == 2
    assert galaxy.current_quadrant.coord.y == 3
    assert galaxy.starship.energy_level == gbl.MAX_STARSHIP_ENERGY
    assert galaxy.starship.torps_remain == gbl.MAX_STARSHIP_TORP
    assert galaxy.starship.shield_level == 0

    ent_quad = galaxy.get_quadrant(2, 3)
    assert ent_quad.has_been_explored is True

    ent_sector = galaxy.current_quadrant.get_sector(4, 5)
    assert ent_sector.sector_contents.sector_contents == gbl.SECTOR_STARSHIP
    assert other_fact.OtherFactories.get_enemies_remaining(galaxy) == 64
    assert other_fact.OtherFactories.get_stars(galaxy) == 128


def mock_random_int(random_type: str):
    if random_type == gbl.RIT_STAR_QUANTITY:
        return 2
    if random_type == gbl.RIT_ENEMY_CHANCE:
        return 76
    if random_type == gbl.RIT_STARBASE_CHANCE:
        return 96
    if random_type == gbl.RIT_STARTING_MISSION_TIME:
        return 2450
    return -1


def mock_random_coord(random_type: str) -> coord.Coord:
    if random_type == gbl.RCT_STARSHIP_QUADRANT:
        return coord.Coord(2, 3)
    if random_type == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(4, 5)
    if random_type == gbl.RCT_ENEMY_LOCATION:
        return coord.Coord(0, 0)
    if random_type == gbl.RCT_STAR_LOCATION:
        return coord.Coord(0, 1)
    if random_type == gbl.RCT_STARBASE_LOCATION:
        return coord.Coord(0, 2)
    return coord.Coord(-10, -10)
