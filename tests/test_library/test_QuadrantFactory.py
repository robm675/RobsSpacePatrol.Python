# region imports
import sys
from unittest.mock import MagicMock

sys.path.append("/pythontrek/source/library/")

import source.library.factories.otherFactories as of
from tests.randomFactoryBuilder import RandomFactoryBuilder
from source import gbl
from source.library.models import coord

from source.library.factories.randomFactory import RandomFactory

# endregion


def create_random_factory() -> RandomFactory:
    """Create a quadrant with three stars, one enemy, and a starbase."""
    return (
        RandomFactoryBuilder().WithDefaults()
        .SetStarQuantity(3).SetEnemyChance(76).SetStarbaseChance(97)
        .SetCoords(gbl.RCT_STAR_LOCATION, (0, 1), (1, 1), (2, 1))
        .SetCoord(gbl.RCT_ENEMY_LOCATION, 1, 0)
        .SetCoord(gbl.RCT_STARBASE_LOCATION, 0, 2)
        .Build()
    )


def test_QuadrantFactory():
    qx = 3
    qy = 4
    testMock = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    testMock.GetRandomInteger= MagicMock()
    testMock.GetRandomInteger.side_effect = MockRandomInt


    newQuad = of.otherFactories.createQuadrant(coord.Coord(qx, qy), testMock)


    assert newQuad.Coord.x == qx
    assert newQuad.Coord.y == qy
    assert newQuad.NumEnemies == 1
    assert newQuad.HasStarBase == True
    assert newQuad.NumStars == 3



def MockRandomInt(randomType: str):
    if randomType == gbl.RIT_STAR_QUANTITY:
        return 3
    if randomType == gbl.RIT_ENEMY_CHANCE:
        return 76
    if randomType == gbl.RIT_STARBASE_CHANCE:
        return 97
    return coord.Coord(-1,-1)
