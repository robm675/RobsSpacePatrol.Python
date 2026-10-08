from unittest.mock import MagicMock

import pytest
from models import current_quadrant
from utils.calculation_utilities import CalculationUtils

import source.library.factories.current_quadrant_factory as cqf
import source.library.factories.random_factory as rf
import source.library.models.sector_contents as sc
import source.library.utils.calculation_utilities as cu
from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.models import coord, quadrant, sector
from tests.random_factory_builder import RandomFactoryBuilder


def create_random_factory() -> RandomFactory:
    """Provide the empty-sector lookup's expected coordinate (1, 2)."""
    return RandomFactoryBuilder().with_defaults().set_starship_sector(1, 2).build()


def test_qs2univ():
    result = cu.CalculationUtils.qs2_univ(1, 2)
    assert result == 10


@pytest.mark.parametrize(
    "univ, q, s",
    [
        (11, 1, 3),
        (12, 1, 4),
        (15, 1, 7),
        (16, 2, 0),
        (63, 7, 7),
    ],
)
def test_univ2qs(univ: int, q: int, s: int):
    result = cu.CalculationUtils.univ2_qs(univ)
    assert result.quad == q
    assert result.sect == s


def test_univ2_qs_coord():
    univ_x = cu.CalculationUtils.qs2_univ(1, 5)
    univ_y = cu.CalculationUtils.qs2_univ(3, 4)
    result = cu.CalculationUtils.univ2_qs_coord(univ_x, univ_y)

    assert 1 == result.quadrant.x
    assert 5 == result.sector.x
    assert 3 == result.quadrant.y
    assert 4 == result.sector.y


def test_univ2_qs_coord_negative():
    univ_x = cu.CalculationUtils.qs2_univ(-1, -5)
    univ_y = cu.CalculationUtils.qs2_univ(-3, -4)
    result = cu.CalculationUtils.univ2_qs_coord(univ_x, univ_y)

    assert result.quadrant.x == -1
    assert result.sector.x == -5
    assert result.quadrant.y == -3
    assert result.sector.y == -4


def test_get_distance():
    coord1_x = 1
    coord1_y = 2
    coord2_x = 3
    coord2_y = 7

    result = cu.CalculationUtils.get_distance(
        coord.Coord(coord1_x, coord1_y), coord.Coord(coord2_x, coord2_y)
    )

    assert 5.4 == result


def test_get_distance_small_distance():
    coord1_x = 0
    coord1_y = 0
    coord2_x = 0
    coord2_y = 1

    result = cu.CalculationUtils.get_distance(
        coord.Coord(coord1_x, coord1_y), coord.Coord(coord2_x, coord2_y)
    )

    assert result == 1


@pytest.mark.parametrize(
    "x1, y1, x2, y2, expecteddir",
    [
        (3, 3, 4, 3, 1.0),
        (3, 3, 4, 2, 2.0),
        (3, 3, 3, 2, 3.0),
        (3, 3, 2, 2, 4.0),
        (3, 3, 2, 3, 5.0),
        (3, 3, 2, 4, 6.0),
        (3, 3, 3, 4, 7.0),
        (3, 3, 4, 4, 8.0),
    ],
)
def test_get_direction(x1: int, y1: int, x2: int, y2: int, expecteddir: float):
    result = cu.CalculationUtils.get_direction(coord.Coord(x1, y1), coord.Coord(x2, y2))
    assert expecteddir == result


def test_get_enemy_shield_hit():
    num_enemies = 2
    energy_of_shot = 500
    dist_to_enemy = 10
    energy_factor_to_reduce = 5
    enemy_shield_hit = cu.CalculationUtils.get_enemy_shield_hit(
        num_enemies, energy_of_shot, dist_to_enemy, energy_factor_to_reduce
    )

    assert 200 == enemy_shield_hit


def test_calculate_starship_hit_from_enemy():
    random_enemy_fired_amount = 300
    distance = 10
    energy_factor_to_reduce_per_sector = 5

    result = cu.CalculationUtils.calculate_starship_hit_from_enemy(
        random_enemy_fired_amount, distance, energy_factor_to_reduce_per_sector
    )

    assert 250 == result


def test_dist2_energy():
    result = cu.CalculationUtils.distance_to_energy(5.4)
    assert int(5.4 * gbl.SECTOR_TO_ENERGY_CONV) == result


def test_dist2_energy_coord():
    result = cu.CalculationUtils.distance_to_energy_coord(coord.Coord(1, 2), coord.Coord(3, 7))

    assert 21 == result


@pytest.mark.parametrize(
    "sx, sy, qx, qy, dir, dist, final_sx, final_sy, final_qx, final_qy, outside_galaxy_sw",
    [
        (2, 2, 2, 2, 5.0, 4.0, 0, 2, 0, 2, True),
        (6, 6, 6, 6, 1.0, 4.0, 7, 6, 7, 6, True),
        (2, 6, 2, 6, 5.0, 4.0, 0, 6, 0, 6, True),
        (6, 1, 6, 1, 1.0, 4.0, 7, 1, 7, 1, True),
        (7, 7, 7, 7, 7.0, 1.0, 7, 7, 7, 7, True),
        (7, 7, 7, 7, 1.0, 1.0, 7, 7, 7, 7, True),
        (0, 0, 0, 0, 3.0, 1.0, 0, 0, 0, 0, True),
        (0, 0, 0, 0, 5.0, 1.0, 0, 0, 0, 0, True),
        (7, 0, 7, 0, 3.0, 1.0, 7, 0, 7, 0, True),
        (7, 0, 7, 0, 1.0, 1.0, 7, 0, 7, 0, True),
        (0, 7, 0, 7, 5.0, 1.0, 0, 7, 0, 7, True),
        (0, 7, 0, 7, 7.0, 1.0, 0, 7, 0, 7, True),
        (0, 0, 0, 0, 1.0, 1.0, 0, 0, 1, 0, False),
    ],
)
def test_get_final_destination(
    sx: int,
    sy: int,
    qx: int,
    qy: int,
    dir: float,
    dist: float,
    final_sx: int,
    final_sy: int,
    final_qx: int,
    final_qy: int,
    outside_galaxy_sw: bool,
):
    starship_sector = sector.Sector(coord.Coord(sx, sy), sc.SectorContents(gbl.SECTOR_STARSHIP))
    temp_sectors = []
    temp_sectors.append(starship_sector)

    target_coord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(target_coord, 0, 0)

    test_mock = rf.RandomFactory()

    cur_quad = cqf.CurrentQuadrantFactory.create_current_quadrant(
        quad, test_mock, coord.Coord(sx, sy)
    )

    fdo = cu.CalculationUtils.get_final_destination(dir, dist, starship_sector, cur_quad)

    assert outside_galaxy_sw == fdo.out_side_galaxy
    assert not fdo.object_hit
    assert final_sx == fdo.final_sector.x
    assert final_sy == fdo.final_sector.y
    assert final_qx == fdo.final_quadrant.x
    assert final_qy == fdo.final_quadrant.y


def test_get_random_empty_sector():
    sectors = []
    x = 0
    while x < gbl.MAX_QUADRANT_SECTOR_XY:
        y = 0
        while y < gbl.MAX_QUADRANT_SECTOR_XY:
            sectors.append(sector.Sector(coord.Coord(x, y), sc.SectorContents(gbl.SECTOR_EMPTY)))
            y += 1
        x += 1

    cq = current_quadrant.CurrentQuadrant(coord.Coord(1, 1), sectors)

    test_mock = rf.RandomFactory()
    test_mock.get_random_coord = MagicMock()
    test_mock.get_random_coord.side_effect = mock_random_coord

    empty_sector = cqf.CurrentQuadrantFactory.get_random_empty_sector(
        test_mock, cq, gbl.RCT_STARSHIP_SECTOR
    )

    assert 1 == empty_sector.coord.x
    assert 2 == empty_sector.coord.y


def test_univ2_qs():
    est_final_uni_x = 0.8
    est_final_uni_y = 0.0

    est_final_uni_x_int = round(est_final_uni_x)
    est_final_uni_y_int = round(est_final_uni_y)

    assert est_final_uni_x_int == 1
    assert est_final_uni_y_int == 0

    res = CalculationUtils.univ2_qs_coord(est_final_uni_x_int, est_final_uni_y_int)

    assert res.quadrant.x == 0
    assert res.quadrant.y == 0
    assert res.sector.x == 1
    assert res.sector.y == 0


def mock_random_coord(random_type: str):
    if random_type == gbl.RCT_STARSHIP_SECTOR:
        return coord.Coord(1, 2)
    return coord.Coord(-1, -1)
