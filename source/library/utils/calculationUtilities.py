# region imports
import sys
sys.path.append("/pythontrek/source/library/")
sys.path.append("/pythontrek/source/")
from typing import NamedTuple
import models.coord as coord
import models.sector as sector
import models.currentQuadrant as currentQuadrant
import math
import gbl as gbl
import models.finalDestination as finalDest
# endregion

class QuadSector(NamedTuple):
    quadrant: coord.Coord
    sector: coord.Coord

class QuadSectorInt(NamedTuple):
    quad:int
    sect:int

class calculationUtils:
    @staticmethod
    def QS2Univ(Quad:int, Sect:int) -> int:
        return Quad * gbl.MAX_QUADRANT_SECTOR_XY + Sect
    
    @staticmethod
    def Univ2QS(univCoord: int)  -> QuadSectorInt:
        tempNum = float(univCoord) / gbl.MAX_QUADRANT_SECTOR_XY
        quad = int(float(univCoord) / gbl.MAX_QUADRANT_SECTOR_XY)
        sect = int((tempNum - quad) * gbl.MAX_QUADRANT_SECTOR_XY)
        # sect = float(univCoord) % gbl.MAX_QUADRANT_SECTOR_XY
        #
        # if univCoord < 0:
        #     sect = -sect

        # print(f"univCoord = [{univCoord}]")
        # print(f"quad = [{quad}]")
        # print(f"sect = [{sect}]")

        return QuadSectorInt(quad, sect)

    @staticmethod
    def Univ2QSCoord(x: int, y:int) -> QuadSector:
        xCoord = calculationUtils.Univ2QS(x)
        yCoord = calculationUtils.Univ2QS(y)

        # print(f"univ2QSCoord: {x}.{y}")

        return QuadSector(coord.Coord(xCoord.quad, yCoord.quad), coord.Coord(xCoord.sect, yCoord.sect))
    
    @staticmethod
    def GetDistance(coord1: coord.Coord, coord2: coord.Coord) -> float:
        x = coord2.x - coord1.x
        y = coord2.y - coord1.y
        return round(math.sqrt(x * x + y * y),1)

    @staticmethod
    def GetDirection(coord1: coord.Coord, coord2: coord.Coord) -> float:
        dir = 0
        if coord1.x == coord2.x:
            if coord1.y < coord2.y:
                dir = 7
            else:
                dir=3
        elif coord1.y == coord2.y:
            if coord1.x < coord2.x:
                dir = 1
            else:
                dir=5
        else:
            dy = abs(coord2.y - coord1.y)
            dx = abs(coord2.x - coord1.x)
            angle = math.atan2(dy, dx)
            if coord1.x < coord2.x:
                if coord1.y < coord2.y:
                    dir = 9.0 - 4.0 * angle / math.pi
                else:
                    dir = 1.0 + 4.0 * angle / math.pi
            else:
                if coord1.y < coord2.y:
                    dir = 5.0 + 4.0 * angle / math.pi
                else:
                    dir = 5.0 - 4.0 * angle / math.pi
        return dir
    
    @staticmethod
    def GetEnemyShieldHit(numberEnemies: int, energyOfShot: int, distanceToEnemy:float, EnergyFactorToReducePerSector:int):
        laserAmountPerEnemy = int(round(energyOfShot / numberEnemies,0))
        laserEnergyToReduceDueToDist = int(distanceToEnemy * EnergyFactorToReducePerSector)
        totalEnergyHitOnEnemyShields = int(laserAmountPerEnemy - laserEnergyToReduceDueToDist)
        if totalEnergyHitOnEnemyShields < 0:
            totalEnergyHitOnEnemyShields = 0
        return totalEnergyHitOnEnemyShields

    @staticmethod
    def CalculateStarshipHitFromEnemy(randomEnemyFiredAmount: int, distance:float, energyFactorToReducePerSector:int):
        return randomEnemyFiredAmount - int(distance * energyFactorToReducePerSector)
    
    @staticmethod
    def DistanceToEnergy(distance: float):
        changeAmount = int(distance * gbl.SECTOR_TO_ENERGY_CONV)
        if changeAmount < 1:
            changeAmount = 1
        return changeAmount

    @staticmethod
    def DistanceToEnergyCoord(start: coord.Coord, end: coord.Coord):
        dist = calculationUtils.GetDistance(start, end)
        # print(dist)
        return calculationUtils.DistanceToEnergy(dist)
    
    @staticmethod
    def Distance2Energy(startQ: coord.Coord, startS: coord.Coord, finalQ: coord.Coord, finalS: coord.Coord):
        startUX = calculationUtils.QS2Univ(startQ.x, startS.x)
        startUY = calculationUtils.QS2Univ(startQ.y, startS.y)
        finalUX = calculationUtils.QS2Univ(finalQ.x, finalS.x)
        finalUY = calculationUtils.QS2Univ(finalQ.y, finalS.y)
        return calculationUtils.DistanceToEnergyCoord(coord.Coord(startUX, startUY), coord.Coord(finalUX, finalUY) )

    @staticmethod
    def GetCoordRange(center: coord.Coord) -> tuple[coord.Coord, coord.Coord]:
        if center.x - 1 < 0:
            leftX = 0
        else:
            leftX = center.x - 1

        if center.x +1 > 7:
            rightX = 7
        else:
            rightX = center.x + 1

        if center.y - 1 < 0:
            topY = 0
        else:
            topY = center.y -1

        if center.y + 1 > 7:
            bottomY = 7
        else:
            bottomY = center.y + 1

        return (coord.Coord(leftX, topY), coord.Coord(rightX, bottomY))

    @staticmethod
    def Distance2Time(distance: float) -> float:
        return distance * gbl.SECTOR_TO_TIME_CONV

    @staticmethod
    def GetFinalDestination(dir: float, dist:float, starshipSector: sector.Sector, currentQuadrant: currentQuadrant.CurrentQuadrant) -> finalDest.FinalDestination:
        entSX = starshipSector.coord.x
        entSY = starshipSector.coord.y
        entQX = currentQuadrant.coord.x
        entQY = currentQuadrant.coord.y

        # print("\n\n")
        # print(f"entSX={entSX}")
        # print(f"entSY={entSY}")
        # print(f"entQX={entQX}")
        # print(f"entQY={entQY}")



        estFinalUnivX = calculationUtils.QS2Univ(entQX, entSX)
        estFinalUnivY = calculationUtils.QS2Univ(entQY, entSY)

        distUniv = dist * 8

        angle = -(math.pi * (dir - 1.0) / 4.0)

        dx = round(distUniv * math.cos(angle), 5)
        dy = round(distUniv * math.sin(angle), 5)

        # print(f"dx={dx}")
        # print(f"dy={dy}")

        vx = dx / 1000
        vy = dy / 1000

        # print(f"vx={vx}")
        # print(f"vy={vy}")


        lastGoodSX = -1
        lastGoodSY = -1
        lastGoodQX = -1
        lastGoodQY = -1

        for counter in range(1000):
            estFinalUnivX += vx
            estFinalUnivY += vy

            # print(f"estFinalUnivX={estFinalUnivX}")
            # print(f"estFinalUnivY={estFinalUnivY}")

            tempX = calculationUtils.Univ2QS(int(estFinalUnivX))
            tempY = calculationUtils.Univ2QS(int(estFinalUnivY))

            # print(f"counter={counter}")
            # print(f"tempX={tempX}")
            # print(f"tempY={tempY}")

            if tempX.quad < 0 or tempX.quad > gbl.MAX_QUADRANT_SECTOR_XY - 1 or tempY.quad < 0 or tempY.quad  > gbl.MAX_QUADRANT_SECTOR_XY - 1:
                return finalDest.FinalDestination(coord.Coord(lastGoodQX, lastGoodQY), coord.Coord(lastGoodSX, lastGoodSY), True, False)

            if tempX.sect < 0 or tempX.sect > gbl.MAX_QUADRANT_SECTOR_XY or tempY.sect < 0 or tempY.sect > gbl.MAX_QUADRANT_SECTOR_XY - 1:
                return finalDest.FinalDestination(coord.Coord(lastGoodQX, lastGoodQY), coord.Coord(lastGoodSX, lastGoodSY), True, False)

            if tempX.quad == entQX and tempY.quad == entQY:
                targetSector = coord.Coord(tempX.sect, tempY.sect)
                curSector = currentQuadrant.GetSector(targetSector.x, targetSector.y)

                # if curSector.coord.x == 5:
                #     print(curSector.sectorContents.sectorContents)
                #     print(curSector.sectorContents.isEmpty())
                #     print(curSector.sectorContents.hasStarship())

                if not curSector.sectorContents.isEmpty() and not curSector.sectorContents.hasStarship():
                    return finalDest.FinalDestination(currentQuadrant.coord, coord.Coord(lastGoodSX, lastGoodSY), False, True)
                    
            lastGoodSX = tempX.sect
            lastGoodSY = tempY.sect
            lastGoodQX = tempX.quad
            lastGoodQY = tempY.quad

        final = calculationUtils.Univ2QSCoord(round(estFinalUnivX), round(estFinalUnivY))
        # print(f"final quadrant: {final.quadrant.ToString()}")
        # print(f"final sector: {final.sector.ToString()}")


        maxNumSquared = gbl.MAX_QUADRANT_SECTOR_XY * gbl.MAX_QUADRANT_SECTOR_XY - 1 
        if estFinalUnivX < 0 or estFinalUnivX >= maxNumSquared or estFinalUnivY < 0 or estFinalUnivY >= maxNumSquared:
            # print(f"estFinalUnivX={estFinalUnivX}")
            # print(f"estFinalUnivY={estFinalUnivY}")
            # print(f"maxNumSquared={maxNumSquared}")
            raise Exception("this is happening for some reason")

        return finalDest.FinalDestination(final.quadrant, final.sector, False, False)

