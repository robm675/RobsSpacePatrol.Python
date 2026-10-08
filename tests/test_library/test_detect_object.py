import source.library.factories.current_quadrant_factory as cqf
import source.library.models.sector_contents as sc
import source.library.utils.detect_object as do
from source import gbl
from source.library.models import coord, quadrant, sector
from tests.random_factory_builder import RandomFactoryBuilder


def test_detect_object_navigation():
    sx = 4
    sy = 3
    qx = 0
    qy = 0
    star_x = 5
    star_y = 3

    starship_sector = sector.Sector(coord.Coord(sx, sy), sc.SectorContents(gbl.SECTOR_STARSHIP))
    target_coord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(target_coord, 0, 0)

    test_mock = RandomFactoryBuilder().with_defaults().build()

    cur_quad = cqf.CurrentQuadrantFactory.create_current_quadrant(
        quad, test_mock, coord.Coord(sx, sy)
    )
    cur_quad.get_sector(star_x, star_y).sector_contents.sector_contents = gbl.SECTOR_STAR

    det_obj = do.DetectObject.detect_object_with_dist(cur_quad, starship_sector.coord, True, 1, 0.3)

    assert det_obj.object == gbl.SECTOR_STAR
    assert det_obj.final_coord.x == sx
    assert det_obj.final_coord.y == sy


def test_detect_object_not_navigation():
    sx = 4
    sy = 3
    qx = 0
    qy = 0
    star_x = 5
    star_y = 3

    starship_sector = sector.Sector(coord.Coord(sx, sy), sc.SectorContents(gbl.SECTOR_STARSHIP))
    target_coord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(target_coord, 0, 0)

    test_mock = RandomFactoryBuilder().with_defaults().build()

    cur_quad = cqf.CurrentQuadrantFactory.create_current_quadrant(
        quad, test_mock, coord.Coord(sx, sy)
    )
    cur_quad.get_sector(star_x, star_y).sector_contents.sector_contents = gbl.SECTOR_STAR

    det_obj = do.DetectObject.detect_object_with_dist(
        cur_quad, starship_sector.coord, False, 1, 0.3
    )

    assert det_obj.object == gbl.SECTOR_STAR
    assert det_obj.final_coord.x == star_x
    assert det_obj.final_coord.y == sy
