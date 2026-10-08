from unittest.mock import MagicMock

import source.library.factories.current_quadrant_factory as cqf
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.models import coord, quadrant
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory() -> RandomFactory:
    """Provide the existing quadrant builder's non-overlapping object locations."""
    return (
        RandomFactoryBuilder()
        .with_defaults()
        .set_starship_quadrant(2, 3)
        .set_starship_sector(4, 5)
        .set_coords(gbl.RCT_STAR_LOCATION, (0, 1), (1, 1))
        .set_coord(gbl.RCT_ENEMY_LOCATION, 0, 0)
        .set_coord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .build()
    )


def test_current_quadrant_factory(mocker):
    qx = 0
    qy = 3
    sx = 0
    sy = 5

    target_coord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(target_coord, 0, 1)

    test_mock = RandomFactoryBuilder().with_defaults().build()
    test_mock.get_random_coord = MagicMock()
    test_mock.get_random_coord.side_effect = mock_random_coord

    cur_quad = cqf.CurrentQuadrantFactory.create_current_quadrant(
        quad, test_mock, coord.Coord(sx, sy)
    )

    assert qx == cur_quad.coord.x
    assert qy == cur_quad.coord.y
    ent_sector = cur_quad.get_sector(sx, sy)
    assert gbl.SECTOR_STARSHIP == ent_sector.sector_contents.sector_contents
    assert quad.has_been_explored is True


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
