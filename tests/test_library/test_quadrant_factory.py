from unittest.mock import MagicMock

import source.library.factories.other_factories as of
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.models import coord
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory() -> RandomFactory:
    """Create a quadrant with three stars, one enemy, and a starbase."""
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_star_quantity(3)
        .set_enemy_chance(76)
        .set_starbase_chance(97)
        .set_coords(gbl.RCT_STAR_LOCATION, (0, 1), (1, 1), (2, 1))
        .set_coord(gbl.RCT_ENEMY_LOCATION, 1, 0)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .build()
    )


def test_quadrant_factory():
    qx = 3
    qy = 4
    test_mock = RandomFactoryBuilder().with_defaults().build()
    test_mock.get_random_integer = MagicMock()
    test_mock.get_random_integer.side_effect = mock_random_int

    new_quad = of.OtherFactories.create_quadrant(coord.Coord(qx, qy), test_mock)

    assert new_quad.coord.x == qx
    assert new_quad.coord.y == qy
    assert new_quad.num_enemies == 1
    assert new_quad.has_star_base is True
    assert new_quad.num_stars == 3


def mock_random_int(random_type: str):
    if random_type == gbl.RIT_STAR_QUANTITY:
        return 3
    if random_type == gbl.RIT_ENEMY_CHANCE:
        return 76
    if random_type == gbl.RIT_STARBASE_CHANCE:
        return 97
    return coord.Coord(-1, -1)
