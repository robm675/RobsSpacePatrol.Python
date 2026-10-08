# region imports
import math
import sys

import gbl
from factories import currentQuadrantFactory, randomFactory
from factories.otherFactories import otherFactories
from models import enemyFired
from models.commandResult import CommandResult
from models.commands import Commands
from models.coord import Coord
from models.device import Device
from models.directionToEnemy import DirectionToEnemy
from models.dockingStatus import DockingStatus
from models.enemyFired import EnemyFired
from models.enemyMoved import EnemyMoved
from models.starship import eDevice
from models.galaxy import Galaxy
from models.gameStatus import GameStatus
from models.navMessage import NavMessage
from models.objectHit import ObjectHit
from models.objectHitReport import ObjectHitReport
from models.quadrant import Quadrant
from models.result import (
    COM_NAV,
    COM_REC,
    COM_STA,
    COM_STB,
    COM_TOR,
    DAM,
    LRS,
    NAV,
    LAS,
    SHE,
    SRS,
    TOR,
    MaintResult,
    Result,
)
from models.sector import Sector
from models.starbaseRepairs import StarbaseRepairs
from utils.calculationUtilities import calculationUtils
from utils.detectObject import DetectObject

sys.path.append("/pythontrek/source/library/")
sys.path.append("/pythontrek/source/models/")
# endregion


class Game:
    skipEnemyMove: bool
    forceEnemyMove: bool
    preventEnemyFire: bool = False

    def __init__(self, galaxy: Galaxy, randFact: randomFactory.RandomFactory, currentQuadFact: currentQuadrantFactory.CurrentQuadrantFactory) -> None:
        self.galaxy = galaxy
        self.randomFactory = randFact
        self.currentQuadrantFactory = currentQuadrantFactory
        self.skipEnemyMove = False
        self.forceEnemyMove = False

    # region commands
    def srs(self) -> Result:
        if self.getDamageLevel(eDevice.SRS) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.SRS
            return res

        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.SRS
        res.SRS = SRS(self.galaxy.CurrentQuadrant.sectors)
        return res

    def lrs(self) -> Result:
        if self.getDamageLevel(eDevice.LRS) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.LRS
            return res

        # quadCoord = self.galaxy.CurrentQuadrant.coord
        lowerX = self.galaxy.CurrentQuadrant.coord.x - gbl.LRS_RANGE
        upperX = self.galaxy.CurrentQuadrant.coord.x + gbl.LRS_RANGE

        lowerY = self.galaxy.CurrentQuadrant.coord.y - gbl.LRS_RANGE
        upperY = self.galaxy.CurrentQuadrant.coord.y + gbl.LRS_RANGE

        # print(f"Current x,y: {quadCoord.ToString()}")
        # print(f"lowerX:{lowerX}")
        # print(f"upperX:{upperX}")
        # print(f"lowerY:{lowerY}")
        # print(f"upperY:{upperY}")

        max_coord = gbl.MAX_QUADRANT_SECTOR_XY - 1

        lowerX = max(0, lowerX)
        upperX = min(max_coord, upperX)
        lowerY = max(0, lowerY)
        upperY = min(max_coord, upperY)


        quadrants = []
        for x in range(lowerX, upperX + 1):
            for y in range(lowerY, upperY + 1):
                # print(f"x:{x} y:{y}")
                quad = self.galaxy.GetQuadrant(x,y)
                quad.HasBeenExplored = True
                quadrants.append(quad)

        result = Result()
        result.LRS = LRS(quadrants)
        result.Command = Commands.LRS
        result.CommandResult = CommandResult.OK

        return result

    def com_rec(self) -> Result:
        if self.getDamageLevel(eDevice.COM) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.COM_REC
            return res

        result = Result()
        result.COM_REC = COM_REC(self.galaxy.GetExploredQuadrant())
        result.Command = Commands.COM_REC
        result.CommandResult = CommandResult.OK

        return result

    def com_sta(self) -> Result:
        if self.getDamageLevel(eDevice.COM) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.COM_STA
            return res

        missionTime = self.galaxy.MissionTime
        quadCoord = self.galaxy.CurrentQuadrant.coord
        entSector = self.galaxy.CurrentQuadrant.GetSectorByContents(gbl.SECTOR_STARSHIP)

        if entSector is None:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.COM_STA
            return res

        damagedDevices = self.galaxy.Starship.GetDamgedDevices()
        enemiesRemain = otherFactories.getEnemiesRemaining(self.galaxy)
        starbasesRemaing = self.galaxy.GetStarbasesRemaining()
        energyRemaing = self.galaxy.Starship.energyLevel
        shieldLevel = self.galaxy.Starship.shieldLevel
        torpRemain = self.galaxy.Starship.torpsRemain
        isDocked = self.galaxy.Starship.isDocked
        missionTimeDeadline = self.galaxy.MissionTimeDeadline

        comsta = COM_STA(missionTime, quadCoord, entSector.coord, damagedDevices, enemiesRemain, starbasesRemaing,
                         energyRemaing, shieldLevel, torpRemain, isDocked, missionTimeDeadline)

        result = Result()
        result.COM_STA = comsta
        result.Command = Commands.COM_STA
        result.CommandResult = CommandResult.OK

        return result

    def com_stb(self) -> Result:
        if self.getDamageLevel(eDevice.COM) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.COM_STB
            return res

        starbaseSector = self.galaxy.CurrentQuadrant.GetSectorByContents(gbl.SECTOR_STARBASE)
        starshipSector = self.galaxy.CurrentQuadrant.GetSectorByContents(gbl.SECTOR_STARSHIP)

        if starbaseSector == None:
            res = Result()
            res.CommandResult = CommandResult.CPU_STB_No_Starbase_Present
            res.Command = Commands.COM_STB
            return res
        if starshipSector == None:
            raise RuntimeError("Starship Sector was none")
        
        DIR = calculationUtils.GetDirection(starshipSector.coord, starbaseSector.coord)
        DIST = calculationUtils.GetDistance(starshipSector.coord, starbaseSector.coord)

        res = Result()
        res.COM_STB = COM_STB(DIR, DIST, starbaseSector.coord)

        res.CommandResult = CommandResult.OK
        res.Command = Commands.COM_STB
        return res

    def com_tor(self) -> Result:
        if self.getDamageLevel(eDevice.COM) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.COM_TOR
            return res

        starshipSector = self.galaxy.CurrentQuadrant.GetSectorByContents(gbl.SECTOR_STARSHIP)

        enemySectors = self.galaxy.CurrentQuadrant.GetEnemySectors()
        if enemySectors is None:
            res = Result()
            res.CommandResult = CommandResult.No_Enemies_Present
            res.Command = Commands.COM_TOR
            return res

        enemyDirList = []
        for enemySector in enemySectors:
            if starshipSector == None:
                raise RuntimeError("Starship Sector was none") 
                       
            dir = calculationUtils.GetDirection(starshipSector.coord, enemySector.coord)
            dist = calculationUtils.GetDistance(starshipSector.coord, enemySector.coord)
            dirToEnemy = DirectionToEnemy(dir, dist, enemySector.coord)
            enemyDirList.append(dirToEnemy)

        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.COM_TOR
        res.COM_TOR = COM_TOR(enemyDirList)
        return res

    def com_nav(self, destQuadrant: Coord, destSector: Coord) -> Result:
        if self.getDamageLevel(eDevice.COM) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.COM_NAV
            return res

        starshipSector = self.galaxy.CurrentQuadrant.GetSectorByContents(gbl.SECTOR_STARSHIP)
        currentQuadrantCoord = self.galaxy.CurrentQuadrant.coord

        if starshipSector == None:
            raise RuntimeError("Starship Sector was none")
        
        startUX = calculationUtils.QS2Univ(currentQuadrantCoord.x, starshipSector.coord.x)
        startUY = calculationUtils.QS2Univ(currentQuadrantCoord.y, starshipSector.coord.y)
        targetUX = calculationUtils.QS2Univ(destQuadrant.x, destSector.x)
        targetUY = calculationUtils.QS2Univ(destQuadrant.y, destSector.y)

        dir = calculationUtils.GetDirection(Coord(startUX, startUY), Coord(targetUX, targetUY))
        dist = calculationUtils.GetDistance(Coord(startUX, startUY), Coord(targetUX, targetUY)) / 8

        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.COM_NAV
        res.COM_NAV = COM_NAV(dir, dist)
        return res

    def dam(self) -> Result:
        devices = self.galaxy.Starship.GetDamgedDevices()
        res = Result()
        if len(devices) == 0:
            res.DAM = DAM([])
        else:
            res.DAM = DAM(devices)
        res.CommandResult = CommandResult.OK
        res.Command = Commands.DAM
        return res

    def she(self, newShieldLevel: int) -> Result:
        if self.getDamageLevel(eDevice.SHE) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.SHE
            return res

        if newShieldLevel < 0:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.SHE
            data = SHE(gbl.SHE_INVALIDAMOUNT)
            res.SHE = data
            return res            

        currentEnergyLevel = self.galaxy.Starship.energyLevel + self.galaxy.Starship.shieldLevel
        if (newShieldLevel > currentEnergyLevel):
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.SHE
            data = SHE(gbl.SHE_ERRORMESSAGE)
            res.SHE = data
            return res

        self.galaxy.Starship.energyLevel = currentEnergyLevel - newShieldLevel
        self.galaxy.Starship.shieldLevel = newShieldLevel
        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.SHE
        res.SHE = SHE("")
        return res

    def tor(self, dir: float) -> Result:
        if self.getDamageLevel(eDevice.TOR) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.TOR
            return res

        enemySectors = self.galaxy.CurrentQuadrant.GetEnemySectors()
        if enemySectors is None or  len(enemySectors) == 0:
            res = Result()
            res.CommandResult = CommandResult.No_Enemies_Present
            res.Command = Commands.TOR
            return res

        if self.galaxy.Starship.torpsRemain <= 0:
            res = Result()
            res.CommandResult = CommandResult.InsufficientInventory
            res.Command = Commands.TOR
            return res

        self.galaxy.Starship.UseTorpedo()

        starshipSector = self.galaxy.GetStarshipSector()
        CFO = DetectObject.detectObjectNoDist(self.galaxy.CurrentQuadrant, starshipSector.coord, False, dir)

        if CFO.object == gbl.SECTOR_EMPTY:
            res = Result()
            res.CommandResult = CommandResult.TOR_Missed
            res.Command = Commands.TOR
            return res

        targetSector = self.galaxy.CurrentQuadrant.GetSectorByCoord(CFO.finalCoord)
        starshipQuadrant = self.galaxy.GetQuadrantByCoord(self.galaxy.CurrentQuadrant.coord)

        if CFO.object == gbl.SECTOR_ENEMY:
            return self.tor_enemy(targetSector, starshipQuadrant)

        if CFO.object == gbl.SECTOR_STARBASE:
            return self.tor_starbase(targetSector, starshipQuadrant)

        if CFO.object == gbl.SECTOR_STAR:
            return self.tor_star(targetSector, starshipQuadrant)


        res = Result()
        res.CommandResult = CommandResult.Error
        res.Command = Commands.TOR

        return res
    def tor_enemy(self, targetSector: Sector, entQuadrant: Quadrant) -> Result:
        targetSector.sectorContents.sectorContents = gbl.SECTOR_EMPTY
        targetSector.enemy = None
        entQuadrant.NumEnemies -= 1
        ohr = ObjectHitReport(ObjectHit.Enemy, True, targetSector.coord, -1, -1, False, False)
        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.TOR
        res.TOR = TOR(ohr)
        return res
    def tor_starbase(self, targetSector: Sector, entQuadrant: Quadrant) -> Result:
        targetSector.sectorContents.sectorContents = gbl.SECTOR_EMPTY
        entQuadrant.HasStarBase = False
        ohr = ObjectHitReport(ObjectHit.Starbase, True, targetSector.coord, -1, -1, False, False)
        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.TOR
        res.TOR = TOR(ohr)
        return res
    def tor_star(self, targetSector: Sector, entQuadrant: Quadrant) -> Result:
        randChance = self.randomFactory.GetRandomInteger(gbl.RIT_STAR_DESTROYED_CHANCE)
        if randChance > gbl.STAR_DESTROYED_CHANCE:
            targetSector.sectorContents.sectorContents = gbl.SECTOR_EMPTY
            entQuadrant.NumStars -= 1
            starDestroyed = True
            starSurvived = False
        else:
            starDestroyed = False
            starSurvived = True

        ohr = ObjectHitReport(ObjectHit.Star, starDestroyed, targetSector.coord, -1, -1, False, starSurvived)
        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.TOR
        res.TOR = TOR(ohr)
        return res

    def las(self, energy: int) -> Result:
        if self.getDamageLevel(eDevice.LAS) < 0:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.LAS
            return res

        if energy < 0:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.SHE
            data = SHE(gbl.LAS_INVALIDAMOUNT)
            res.SHE = data
            return res           

        if self.galaxy.Starship.energyLevel < energy:
            res = Result()
            res.CommandResult = CommandResult.InsufficientInventory
            res.Command = Commands.LAS
            return res

        enemySectors = self.galaxy.CurrentQuadrant.GetEnemySectors()
        if enemySectors is None or len(enemySectors) == 0:
            res = Result()
            res.CommandResult = CommandResult.No_Enemies_Present
            res.Command = Commands.LAS
            return res

        starshipQuadrant = self.galaxy.GetQuadrantByCoord(self.galaxy.CurrentQuadrant.coord)
        starshipSector = self.galaxy.GetStarshipSector()
        enemyHitReports = []

        self.galaxy.Starship.energyLevel -= energy

        for enemySector in enemySectors:
            target_enemy = enemySector.enemy

            if target_enemy is None:
                raise RuntimeError(f"Sector {enemySector.coord.ToString()} is marked as enemy but has no enemy object")

            if target_enemy.shieldLevel is None:
                target_enemy.shieldLevel = 0

                
            if self.getDamageLevel(eDevice.COM) < 0:
                randInt = self.randomFactory.GetRandomInteger(gbl.RIT_LASER_MISS_CHANCE)
                if randInt > gbl.LASER_MISS_CHANCE_CPU_DOWN:



                    ohr = ObjectHitReport(ObjectHit.Nothing, False, enemySector.coord, target_enemy.shieldLevel, 0, True, False)
                    enemyHitReports.append(ohr)
                    continue

            distToEnemy = calculationUtils.GetDistance(starshipSector.coord, enemySector.coord)
            energyHitEnemy = calculationUtils.GetEnemyShieldHit(len(enemySectors), energy, distToEnemy, gbl.SECTOR_TO_ENERGY_CONV)
            wasDestroyed = self.galaxy.CurrentQuadrant.EnemyHit(enemySector.coord, energyHitEnemy)
            if wasDestroyed:
                enemySector.sectorContents.sectorContents = gbl.SECTOR_EMPTY
                enemySector.enemy = None
                starshipQuadrant.NumEnemies -= 1
                ohr = ObjectHitReport(ObjectHit.Enemy, True, enemySector.coord, 0, 0, False, False)
                enemyHitReports.append(ohr)
                continue
            else:
                ohr = ObjectHitReport(ObjectHit.Enemy, False, enemySector.coord, target_enemy.shieldLevel, energyHitEnemy, False, False)
                enemyHitReports.append(ohr)
                continue

        res = Result()
        res.LAS = LAS(enemyHitReports)
        res.CommandResult = CommandResult.OK
        res.Command = Commands.LAS
        return res

    def nav(self, dir: float, dist: float) -> Result:
        dir = round(dir, 1)
        dist = round(dist, 1)


        if dir < 0.1 or dir >= 9:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.NAV
            res.NAV = NAV(NavMessage.InvalidDIR, -1)
            return res

        if dist < 0.1 or dist > 8:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.NAV
            res.NAV = NAV(NavMessage.InvalidDIST, -1)
            return res

        if self.getDamageLevel(eDevice.NAV) < 0 and dist > 0.2:
            res = Result()
            res.CommandResult = CommandResult.Damaged
            res.Command = Commands.NAV
            return res

        starshipQuadrant = self.galaxy.GetQuadrantByCoord(self.galaxy.CurrentQuadrant.coord)
        starshipSector = self.galaxy.GetStarshipSector()

        fdo = calculationUtils.GetFinalDestination(dir, dist, starshipSector, self.galaxy.CurrentQuadrant)
        if fdo.OutSideGalaxy:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.NAV
            res.NAV = NAV(NavMessage.BadInput_OutsideGalaxy, -1)
            return res

        estEnergyForTrip = calculationUtils.Distance2Energy(self.galaxy.CurrentQuadrant.coord, starshipSector.coord, fdo.FinalQuadrant, fdo.FinalSector)

        if self.galaxy.Starship.energyLevel < estEnergyForTrip:
            if self.galaxy.Starship.energyLevel + self.galaxy.Starship.shieldLevel > estEnergyForTrip:
                res = Result()
                res.CommandResult = CommandResult.Error
                res.Command = Commands.NAV
                res.NAV = NAV(NavMessage.InsufficientEnergy_ShieldEnergyAvailable, -1)
                return res
            else:
                res = Result()
                res.CommandResult = CommandResult.Error
                res.Command = Commands.NAV
                res.NAV = NAV(NavMessage.InsufficientEnergy, -1)
                return res

        # print(f"b4 x={self.galaxy.GetStarshipSector().coord.x}")
        # print(f"b4 y={self.galaxy.GetStarshipSector().coord.y}")

        navMsg = self.checkRouteAndMoveStarship(dir, dist, estEnergyForTrip, starshipQuadrant.Coord,
                                                  fdo.FinalQuadrant, fdo.FinalSector)

        # print(f"af x={self.galaxy.GetStarshipSector().coord.x}")
        # print(f"af y={self.galaxy.GetStarshipSector().coord.y}")


        if fdo.ObjectHit:
            res = Result()
            res.CommandResult = CommandResult.Error
            res.Command = Commands.NAV
            distTraveled = calculationUtils.GetDistance(starshipSector.coord, fdo.FinalSector)
            res.NAV = NAV(NavMessage.BadInput_ObjectHit, distTraveled)
            return res


        if starshipQuadrant.Coord.x != fdo.FinalQuadrant.x or starshipQuadrant.Coord.y != fdo.FinalQuadrant.y:
            distTraveled = calculationUtils.GetDistance(starshipQuadrant.Coord, fdo.FinalQuadrant) * 8
        else:
            distTraveled = calculationUtils.GetDistance(starshipSector.coord, fdo.FinalSector) * 8


        res = Result()
        res.CommandResult = CommandResult.OK
        res.Command = Commands.NAV
        res.NAV = NAV(navMsg, distTraveled)
        return res

    def routine_maint(self, changeMissionTime: float, enemiesFire: bool):
        dockingStatus = DockingStatus(self.galaxy.Starship.isDocked, False)
        self.galaxy.Starship.isDocked = False

        if self.galaxy.Starship.shieldLevel == 0 and self.canBeDocked():
            dockingStatus.CurrentStatus = True
            self.galaxy.Starship.isDocked = True
            self.galaxy.Starship.energyLevel = gbl.MAX_STARSHIP_ENERGY
            self.galaxy.Starship.torpsRemain = gbl.MAX_STARSHIP_TORP
        else:
            if self.galaxy.Starship.shieldLevel != 0 and self.galaxy.Starship.isDocked:
                dockingStatus.CurrentStatus = False
                self.galaxy.Starship.isDocked = False

        gameStatus = GameStatus.Normal

        if self.galaxy.MissionTime > self.galaxy.MissionTimeDeadline:
            gameStatus = GameStatus.RanOutOfTime
        if self.galaxy.Starship.isDestroyed:
            gameStatus = GameStatus.StarshipDestroyed
        if self.galaxy.Starship.energyLevel == 0 and self.galaxy.Starship.shieldLevel == 0:
            gameStatus = GameStatus.Normal.RanOutOfEnergy
        if self.galaxy.Starship.energyLevel ==0 and self.galaxy.Starship.shieldLevel > 0 and self.getDamageLevel(eDevice.SHE) >= 0:
            gameStatus = GameStatus.OutOfEnergyShieldEnergyAvailable
        if self.galaxy.Starship.energyLevel ==0 and self.galaxy.Starship.shieldLevel > 0 and self.getDamageLevel(eDevice.SHE) < 0:
            gameStatus = GameStatus.RanOutOfEnergy
        if otherFactories.getEnemiesRemaining(self.galaxy) == 0:
            gameStatus = GameStatus.MissionOver

        enemiesFired = []
        if not self.preventEnemyFire and enemiesFire:
            enemiesFired = self.enemiesFired()

        if self.galaxy.Starship.isDestroyed:
            gameStatus = GameStatus.StarshipDestroyed

        enemiesMoved = self.enemiesMoved()

        res = Result()
        res.MaintResult = MaintResult(self.updateMissionTime(changeMissionTime),
                                      self.updateDamagedDevicesWithMissionTime(changeMissionTime),
                                      enemiesFired,
                                      enemiesMoved,
                                      dockingStatus,
                                      self.StarbaseRepairs(),
                                      gameStatus)
        return res

    def RunStarbaseRepair(self):
        timeToRepair = self.StarbaseRepairs()
        if timeToRepair is None:
            raise RuntimeError("timeToRepair is null")
        self.executeStarbaseRepair(timeToRepair.MissionTimeToRepair)
        
    # endregion

    # region Utils
    def str2int(self, string:str) -> int|None:
        try:
            xInt = int(string)
        except ValueError:
            return None
        return xInt

    def str2float(self, string:str) -> float|None:
        try:
            xFloat = float(string)
            if not math.isfinite(xFloat):
                return None
        except ValueError:
            return None
        return xFloat

    def enemiesFired(self) -> list[EnemyFired]:
        enemySectors = self.galaxy.CurrentQuadrant.GetEnemySectors()
        if enemySectors is None:
            return []

        enemiesFiredReturn = []
        for enemySector in enemySectors:
            enemyHitAmount = self.randomFactory.GetRandomInteger(gbl.RIT_ENEMY_FIRED_AMOUNT)

            if self.galaxy.Starship.isDocked:
                enemyFire = enemyFired.EnemyFired(enemySector.coord,
                                                  self.galaxy.Starship.shieldLevel,
                                                  False,
                                                  None,
                                                  enemyHitAmount,
                                                  None,
                                                  True)
                enemiesFiredReturn.append(enemyFire)
            else:
                self.galaxy.Starship.shieldLevel -= enemyHitAmount
                if self.galaxy.Starship.shieldLevel < 0 and not self.galaxy.Starship.isDocked:
                    self.galaxy.Starship.isDestroyed = True
                    enemyFire = enemyFired.EnemyFired(enemySector.coord,
                                                      self.galaxy.Starship.shieldLevel,
                                                      True,
                                                      None,
                                                      enemyHitAmount,
                                                      None,
                                                      False)
                    enemiesFiredReturn.append(enemyFire)
                    return enemiesFiredReturn

                damagedDevice: Device | None = None
                if self.randomFactory.GetRandomInteger(gbl.RIT_DAMAGE_DEVICE_CHANCE) > gbl.DAMAGE_DEVICE_RANDOM_NUMBER_THRESHOLD:
                    while True:
                        damagedDeviceNum = self.randomFactory.GetRandomInteger(gbl.RIT_DAMAGE_DEVICE)
                        targetDevice = self.galaxy.Starship.GetDevice(eDevice(damagedDeviceNum))
                        if targetDevice.damageLevel >= 0:
                            damagedDevice = targetDevice
                            break

                    damagedDeviceMissionTime = self.randomFactory.GetRandomInteger(gbl.RIT_DAMAGE_DEVICE_AMOUNT)
                    damagedDevice.damageLevel = damagedDeviceMissionTime * -1
                    enemyFire = enemyFired.EnemyFired(enemySector.coord,
                                                      self.galaxy.Starship.shieldLevel,
                                                      True,
                                                      damagedDevice,
                                                      enemyHitAmount,
                                                      damagedDeviceMissionTime,
                                                      False)
                    enemiesFiredReturn.append(enemyFire)
                    continue

                enemyFire = enemyFired.EnemyFired(enemySector.coord,
                                                  self.galaxy.Starship.shieldLevel,
                                                  False,
                                                  None,
                                                  enemyHitAmount,
                                                  None,
                                                  False)
                enemiesFiredReturn.append(enemyFire)

        return enemiesFiredReturn

    def enemiesMoved(self) -> list[EnemyMoved]:
        enemySectors = self.galaxy.CurrentQuadrant.GetEnemySectors()
        if enemySectors is None:
            return []
        if self.skipEnemyMove:
            return []

        enemiesMoved = []
        for enemySector in enemySectors:
            enemyMoveChance = self.randomFactory.GetRandomInteger(gbl.RIT_ENEMY_MOVE_CHANCE)

            if enemyMoveChance < gbl.ENEMY_MOVE_CHANCE and not self.forceEnemyMove:
                continue

            mt_sector = self.currentQuadrantFactory.CurrentQuadrantFactory.GetRandomEmptySector(self.randomFactory, self.galaxy.CurrentQuadrant, gbl.RCT_ENEMY_LOCATION)

            self.moveObjectInsideQuadrant(enemySector.coord, mt_sector.coord)
            enemyMoved = EnemyMoved(enemySector.coord, mt_sector.coord)
            enemiesMoved.append(enemyMoved)

        return enemiesMoved

    def updateDamagedDevicesWithMissionTime(self, missionTime: float) -> list[Device]:
        damagedDevices = self.galaxy.Starship.GetDamgedDevices()
        for device in damagedDevices:
            device.damageLevel += missionTime
            device.damageLevel = round(device.damageLevel, 1)
            if round(device.damageLevel >= 0):
                device.damageLevel = 100
        return damagedDevices

    def updateMissionTime(self, changeMissionTime: float) -> float:
        self.galaxy.MissionTime += changeMissionTime
        return self.galaxy.MissionTime

    def checkRouteAndMoveStarship(self, dir: float, dist: float, estEnergyForTrip:int, startSectorCoord: Coord, FinalQuadrant: Coord, FinalSector: Coord) -> NavMessage:
        cfo = DetectObject.detectObjectWithDist(self.galaxy.CurrentQuadrant, startSectorCoord, True, dir, dist)
        starshipSector = self.galaxy.GetStarshipSector()
        if cfo.object == gbl.SECTOR_EMPTY:
            if FinalQuadrant.x == self.galaxy.CurrentQuadrant.coord.x and FinalQuadrant.y == self.galaxy.CurrentQuadrant.coord.y:
                self.moveObjectInsideQuadrant(starshipSector.coord, FinalSector)
            else:
                destQuadrant = self.galaxy.GetQuadrantByCoord(FinalQuadrant)
                self.moveStarshipQuadrant(destQuadrant, FinalSector)
            self.galaxy.Starship.energyLevel -= estEnergyForTrip
            return NavMessage.TransitComplete
        else:
            nextToLastCoord = cfo.trackingCoords[-1]
            estEnergyForAbortedTrip = calculationUtils.Distance2Energy(self.galaxy.CurrentQuadrant.coord,
                                                                       starshipSector.coord,
                                                                       self.galaxy.CurrentQuadrant.coord,
                                                                       nextToLastCoord)
            self.moveObjectInsideQuadrant(starshipSector.coord, nextToLastCoord)
            self.galaxy.Starship.energyLevel -= estEnergyForAbortedTrip
            return NavMessage.BadInput_ObjectHit

    def moveStarshipQuadrant(self, newQuadrant:Quadrant, sectorCoord: Coord) -> None:
        self.galaxy.CurrentQuadrant = self.currentQuadrantFactory.CurrentQuadrantFactory.CreateCurrentQuadrant(newQuadrant, self.randomFactory, sectorCoord)

    def canBeDocked(self) -> bool:
        starshipSector = self.galaxy.GetStarshipSector()
        (topLeft, botRight) = calculationUtils.GetCoordRange(starshipSector.coord)

        for x in range(topLeft.x, botRight.x + 1):
            for y in range(topLeft.y, botRight.y + 1):
                # print(f"x = {x}, y = {y}\n")
                sect = self.galaxy.CurrentQuadrant.GetSector(x,y)
                if sect.sectorContents.hasStarbase():
                    return True
        return False

    def setDamageLevel(self, device: eDevice, damageLevel:float) -> None:
        targetDev = self.galaxy.Starship.GetDevice(device)
        targetDev.damageLevel = damageLevel

    def getDamageLevel(self, device: eDevice) -> float:
        targetDev = self.galaxy.Starship.GetDevice(device)
        return targetDev.damageLevel

    def getFormattedCoord(self, Coord):
        return f"[{Coord.x},{Coord.y}]"

    def getSectorFormatted(self, sector: Sector) -> str:
        match sector.sectorContents.sectorContents:
            case gbl.SECTOR_STAR:
                return "***"
            case gbl.SECTOR_STARSHIP:
                return "EEE"
            case gbl.SECTOR_EMPTY:
                return "   "
            case gbl.SECTOR_ENEMY:
                return "XXX"
            case gbl.SECTOR_STARBASE:
                return "BBB"
            case _:
                return "???"

    def executeStarbaseRepair(self, missionTime: float) -> None:
        self.galaxy.MissionTime += abs(missionTime)
        for device in self.galaxy.Starship.devices:
            device.damageLevel = 0

    def StarbaseRepairs(self) -> StarbaseRepairs|None:
        if not self.galaxy.Starship.isDocked:
            return None
        damagedDevices = self.galaxy.Starship.GetDamgedDevices()
        if len(damagedDevices) == 0:
            return None
        minValue = min(obj.damageLevel for obj in damagedDevices)
        return StarbaseRepairs(abs(minValue))

    def getCurrentQuadrantFormatted(self) -> str:
        outString = f"Current Quadrant Coord {self.getFormattedCoord(self.galaxy.CurrentQuadrant.coord)}\n"
        for y in range(-1, gbl.MAX_QUADRANT_SECTOR_XY):
            if y == -1:
                outString += "###\t\t"
            else:
                outString += f"{y}\t\t"
        outString += "\n"

        for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
            outRowString = ""
            for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                item = self.galaxy.CurrentQuadrant.GetSector(x,y)
                outRowString += self.getSectorFormatted(item) + "\t\t"
            outString += f"{y}\t\t{outRowString}\n"

        return outString

    def getQuadrantForGalaxyFormatted(self, quadrant: Quadrant, markStarship:bool) -> str:
        outstr = ""
        if not quadrant.HasBeenExplored:
            return "| *** "

        entMarkerStart = " "
        entMarkerEnd = " "
        if markStarship:
            entMarkerStart = "<"
            entMarkerEnd = ">"

        outstr += "|" + entMarkerStart
        outstr += str(quadrant.NumEnemies)
        if quadrant.HasStarBase:
            outstr += "1"
        else:
            outstr += "0"

        outstr += str(quadrant.NumStars)
        outstr += entMarkerEnd
        return outstr

    def moveObjectInsideQuadrant(self, source:Coord, dest:Coord) -> None:
        if source.x == dest.x and source.y == dest.y:
            return

        sourceSector = self.galaxy.CurrentQuadrant.GetSectorByCoord(source)
        destSector = self.galaxy.CurrentQuadrant.GetSectorByCoord(dest)

        destSector.sectorContents.sectorContents = sourceSector.sectorContents.sectorContents
        if sourceSector.enemy is not None:
            destSector.enemy =  sourceSector.enemy
            sourceSector.enemy = None
        sourceSector.sectorContents.sectorContents = gbl.SECTOR_EMPTY

    def getGalaxyFormatted(self) -> str:
        xHeader = "  <-----------------------X----------------------->\n"
        line = "+-----+-----+-----+-----+-----+-----+-----+-----+\n"

        outStr = xHeader
        for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
            match y:
                case 0:
                    outStr += "^"
                case 4:
                    outStr += "Y"
                case _:
                    outStr += "|"

            outStr += " " + line
            outStr += "| "

            for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                quad = self.galaxy.GetQuadrant(x,y)

                if quad.Coord.x == self.galaxy.CurrentQuadrant.coord.x and quad.Coord.y == self.galaxy.CurrentQuadrant.coord.y:
                    outStr += self.getQuadrantForGalaxyFormatted(quad, True)
                else:
                    outStr += self.getQuadrantForGalaxyFormatted(quad, False)

            outStr += "|\n"

        outStr += "v " + line
        return outStr
    # endregion

