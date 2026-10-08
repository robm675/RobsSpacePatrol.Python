# region imports
import sys

from models.detectedObject import detectedObject

sys.path.append("/pythontrek/source/library/")
sys.path.append("/pythontrek/source/")
from typing import List
import models.coord as coord
import models.sector as sector
import models.currentQuadrant as currentQuadrant
import math
import gbl as gbl
import source.library.utils.calculationUtilities as cu
import source.library.models.detectedObject as detObj
# endregion

class DetectObject:
    @staticmethod
    def detectObjectNoDist(currentQuadrant: currentQuadrant.CurrentQuadrant, startingSector: coord.Coord, isNavigation: bool,  dir: float) -> detObj.detectedObject:
        return DetectObject.detectObjectWithDist(currentQuadrant, startingSector, isNavigation, dir, 99)

    @staticmethod
    def detectObjectWithDist(currentQuadrant: currentQuadrant.CurrentQuadrant, startingSector: coord.Coord, isNavigation: bool,  dir: float, dist:float) -> detObj.detectedObject:
        trackingCoords = []

        distUniv = dist * 8

        angle = -(math.pi * (dir - 1.0) / 4.0)

        dx = round(distUniv * math.cos(angle), 5)
        dy = round(distUniv * math.sin(angle), 5)

        vx = dx / 1000
        vy = dy / 1000

        targetX = float(startingSector.x)
        targetY = float(startingSector.y)

        lastGoodSectX = float(startingSector.x)
        lastGoodSectY = float(startingSector.y)

        lastTrackingX = float(startingSector.x)
        lastTrackingY = float(startingSector.y)

        trackingCoords.append(coord.Coord(lastTrackingX, lastTrackingY))

        for counter in range(1000):
            targetX += vx
            targetY += vy

            tempSectX = int(targetX)
            tempSectY = int(targetY)

            if (tempSectX != lastTrackingX or tempSectY != lastTrackingY):
                lastTrackingX = lastGoodSectX
                lastTrackingY = lastGoodSectY
                if not DetectObject.coordAlreadyExists(trackingCoords, coord.Coord(lastTrackingX, lastTrackingY)):
                    trackingCoords.append(coord.Coord(lastTrackingX, lastTrackingY))

            if tempSectX < 0 or tempSectX > gbl.MAX_QUADRANT_SECTOR_XY -1 or tempSectY < 0 or tempSectY > gbl.MAX_QUADRANT_SECTOR_XY - 1:
                break

            targetSector = currentQuadrant.GetSector(tempSectX, tempSectY)

            if not targetSector.sectorContents.isEmpty() and not targetSector.sectorContents.hasStarship():
                finalCoord = coord.Coord(tempSectX, tempSectY)

                if isNavigation:
                    if not targetSector.sectorContents.isEmpty() and not targetSector.sectorContents.hasStarship():
                        finalCoord = trackingCoords[-1]


                if not DetectObject.coordAlreadyExists(trackingCoords, coord.Coord(tempSectX, tempSectY)):
                    trackingCoords.append(coord.Coord(tempSectX, tempSectY))

                distanceMoved = cu.calculationUtils.GetDistance(startingSector, finalCoord)

                objectHit = targetSector.sectorContents.sectorContents

                return detectedObject(objectHit, distanceMoved, finalCoord, trackingCoords)

        return detectedObject(gbl.SECTOR_EMPTY, -1, None, trackingCoords)

    @staticmethod
    def coordAlreadyExists(listIn: List[coord.Coord], testCoord) -> bool:
        return any(tc.x == testCoord and tc.y == testCoord for tc in listIn)
