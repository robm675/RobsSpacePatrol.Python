# region imports
import sys

sys.path.append("/pythontrek/source/library/")

from unittest.mock import MagicMock

import source.library.factories.currentQuadrantFactory as cqf
from tests.randomFactoryBuilder import RandomFactoryBuilder

# import pytest_mock as mock
from source import gbl
from source.library.models import coord, quadrant

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory() -> RandomFactory:
    """Provide the existing quadrant builder's non-overlapping object locations."""
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarshipQuadrant(2, 3).SetStarshipSector(4, 5)
        .SetCoords(gbl.RCT_STAR_LOCATION, (0, 1), (1, 1))
        .SetCoord(gbl.RCT_ENEMY_LOCATION, 0, 0)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .Build()
    )

def test_CurrentQuadrantFactory(mocker):
    qx = 0
    qy = 3
    sx = 0
    sy = 5

    targetCoord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(targetCoord, 0, 1)

    testMock = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    testMock.GetRandomCoord= MagicMock()
    testMock.GetRandomCoord.side_effect = MockRandomCoord


    curQuad = cqf.CurrentQuadrantFactory.CreateCurrentQuadrant(quad, testMock, coord.Coord(sx, sy))

    assert qx ==  curQuad.coord.x
    assert qy ==  curQuad.coord.y
    entSector = curQuad.GetSector(sx, sy)
    assert gbl.SECTOR_STARSHIP == entSector.sectorContents.sectorContents
    assert quad.HasBeenExplored == True


def MockRandomCoord(randomType: str) -> coord.Coord:
    if randomType == gbl.RCT_STARSHIP_QUADRANT:
        return coord.Coord(2,3)
    if randomType == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(4,5)
    if randomType == gbl.RCT_ENEMY_LOCATION:
        return coord.Coord(0,0)
    if randomType == gbl.RCT_STAR_LOCATION:
        return coord.Coord(0,1)
    if randomType == gbl.RCT_STARBASE_LOCATION:
        return coord.Coord(0,2)
    return coord.Coord(-10,-10)
