# import sys
# sys.path.append("/pythontrek/source/library/")
# import models.coord as coord
# import models.currentQuadrant as currentQuad
# import models.enemy as enemy
# import models.sectorContents as sectorContents
# import models.sector as sector

# for path in sys.path:
#     print(path)
#
# def runStuff():
#     c = coord.Coord(1,1)
#     sc = sectorContents.SectorContents("test")
#     sectors = [sector.Sector(coord.Coord(1,1), sc, 100)]
#     cq = currentQuad.CurrentQuadrant(coord.Coord(0,0), sectors)
#     e = enemy.Enemy(123)
#
#
#     print(c.id)
#
#     print(c.x)
#     print(c.y)
#
#     print(sc.sectorContents)
#
#
#     print(sectors[0].coord.x)
#     print(sectors[0].coord.y)
#     print(f"shieldLevel:   {sectors[0].enemy.shieldLevel}")
#     print(sectors[0].id)
#     print(sectors[0].sectorContents.sectorContents)
#     print(sectors[0].hasEnemy())
#
#     print(e.shieldLevel)