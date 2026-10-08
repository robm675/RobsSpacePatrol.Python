# region imports
import sys

sys.path.append("/pythontrek/source/library/")

import source.library.factories.currentQuadrantFactory as cqf
import source.library.factories.randomFactory as rf
import source.library.models.sectorContents as sc
import source.library.utils.detectObject as do
from source import gbl
from source.library.models import coord, quadrant, sector
from tests.randomFactoryBuilder import RandomFactoryBuilder

# endregion


def test_DetectObject_Navigation():
    sx = 4
    sy = 3
    qx = 0
    qy = 0
    starX = 5
    starY = 3

    starshipSector = sector.Sector(coord.Coord(sx, sy), sc.SectorContents(gbl.SECTOR_STARSHIP))
    targetCoord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(targetCoord, 0, 0)

    testMock = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )

    curQuad = cqf.CurrentQuadrantFactory.CreateCurrentQuadrant(quad, testMock, coord.Coord(sx, sy))
    curQuad.GetSector(starX,starY).sectorContents.sectorContents = gbl.SECTOR_STAR

    detObj = do.DetectObject.detectObjectWithDist(curQuad, starshipSector.coord, True, 1 , .3)

    assert detObj.object == gbl.SECTOR_STAR
    assert detObj.finalCoord.x == sx
    assert detObj.finalCoord.y == sy


def test_DetectObject_NOT_Navigation():
    sx = 4
    sy = 3
    qx = 0
    qy = 0
    starX = 5
    starY = 3

    starshipSector = sector.Sector(coord.Coord(sx, sy), sc.SectorContents(gbl.SECTOR_STARSHIP))
    targetCoord = coord.Coord(qx, qy)
    quad = quadrant.Quadrant(targetCoord, 0, 0)

    testMock = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )

    curQuad = cqf.CurrentQuadrantFactory.CreateCurrentQuadrant(quad, testMock, coord.Coord(sx, sy))
    curQuad.GetSector(starX,starY).sectorContents.sectorContents = gbl.SECTOR_STAR

    detObj = do.DetectObject.detectObjectWithDist(curQuad, starshipSector.coord, False, 1 , .3)

    assert detObj.object == gbl.SECTOR_STAR
    assert detObj.finalCoord.x == starX
    assert detObj.finalCoord.y == sy
