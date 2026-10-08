# region imports

import sys

import gbl
from cli import CLI_Messages, debugCommands
from game.game import Game
from models import objectHit
from models.commandResult import CommandResult
from models.coord import Coord
from models.gameStatus import GameStatus
from models.navMessage import NavMessage
from models.quadrant import Quadrant
from models.sector import Sector
from utils.calculationUtilities import calculationUtils

# endregion

class CommandLine:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.debug = debugCommands.DebugCommands(game)
    newQuadrant: bool = False
    GameOver: bool = False

    def executeCommandString(self, command: str) -> str:
        for char in "[],=:":
            command = command.replace(char, " ")

        if command.strip() == "":
            return ""

        commands = command.split()

        activeCommand = commands[0].upper().strip()
        match activeCommand:
            case "DEBUG":
                return self.debug.runDEBUG_Command(commands)
            case "SRS":
                return self.runSRS()
            case "LRS":
                return self.runLRS()
            case "SHE":
                return self.runSHE(commands)
            case "LAS":
                return self.runLAS(commands)
            case "TOR":
                return self.runTOR(commands)
            case "COM":
                return self.runCOM(commands)
            case "NAV":
                return self.runNAV(commands)
            case "DAM":
                return self.runDAM()
            case _:
                outStr = ""
                if activeCommand == "":
                    outStr += CLI_Messages.UnknownCommand + "\n"
                    outStr += self.showHelpMain() + "\n"
                return outStr + self.getRoutineMaint(0, True)


        return "**ERROR**"

    def introMessage(self) -> str:
        outMsg = ""
        comSTA = self.game.com_sta()

        totalMissionTime = comSTA.COM_STA.MissionTimeDeadline - comSTA.COM_STA.MissionTime

        outMsg += "Hello Captain!\n"
        outMsg += "\n"
        outMsg += f"Mission: Destroy {comSTA.COM_STA.EnemiesRemaining} enemies in less than {totalMissionTime!s} mission time units.\n"
        outMsg += "\n"
        outMsg += "Good luck!\n"

        enemySectors = self.game.galaxy.CurrentQuadrant.GetEnemySectors()

        if enemySectors is not None and len(enemySectors) > 0:
            outMsg += "\n"
            outMsg += "\n"
            outMsg += CLI_Messages.WarningMessageShieldDownInCombatArea + "\n"

        return outMsg

    def showHelpMain(self) -> str:
        strOut = ""

        strOut += "The following is a list of the available command along with their function\n"
        strOut += "\n"
        strOut += "NAV <direction> <distance> - Moves the starship in the specified direction and distance.  Enter without parameters to view the direction guide. \n"
        strOut += "SRS - Displays the current sector in a graphical format \n"
        strOut += "LRS - Displays the neighboring quadrants in a graphical format\n"
        strOut += "SHE <amount> - Set shield level.  Set to 0 to drop shields \n"
        strOut += "LAS <amount> - Fires the lasers at the specified amount, which is divided between each of the enemies in the current quadrant, it also will reduce the further the enemy is \n"
        strOut += "TOR <direction> - Fires the torpedos in a given direction, give the command without any parameters for the direction guide \n"
        strOut += "COM REC - Displays the galaxy in a graphical format showing the quadrants contents, any unexplored quadrants will be hidden \n"
        strOut += "COM STA - Displays the current status \n"
        strOut += "COM TOR - Calculates the directions to each of the enemies in the current quadrant \n"
        strOut += "COM STB - Calculates the direction and distance to the starbase in the current quadrant \n"
        strOut += "COM NAV <quadrant-x> <quadrant-y> <sector-x> <sector-y> - Calculates the direction and distance from your position to the given quadrant and sector coordinates \n"
        strOut += "DAM - Displays all of the damaged devices as well as the amount of Mission Time before it's repaired. \n"
        strOut += "QUIT / EXIT - Exit the game. \n"
        strOut += "\n"


        return strOut

    def showHelpNAVTOR(self, isNav: bool) -> str:
        strOut = ""

        strOut += "\n"
        strOut += "Direction:\n\n"
        strOut += "  4    3    2\n"
        strOut += "   `.  :  .'\n"
        strOut += "     `.:.'\n"
        strOut += "  5---<*>---1\n"
        strOut += "     .':'.\n"
        strOut += "   .'  :  '.\n"
        strOut += "  6    7    8\n"

        if isNav:
            strOut += "\n"
            strOut += "Warp speed is 1 to 8, impulse power is 0.1 to 0.9"

        return strOut

    def getSRSFormatted(self, sectors:list[Sector]) -> str:
        outString = ""
        for y in range(-1, gbl.MAX_QUADRANT_SECTOR_XY):
            if y == -1:
                outString += "###\t\t"
            else:
                outString += f"{y}\t\t"
        outString += "\n"

        for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
            outRowString = ""
            for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                data = [s for s in sectors if s.coord.x == x and s.coord.y == y]
                outRowString += self.getSectorFormatted(data[0]) + "\t\t"
            outString += f"{y}\t\t{outRowString}\n"

        return outString

    def getLRSFormatted(self, quadrants: list[Quadrant], entQX: int, entQY: int) -> str:
        line = "+-----+-----+-----+\n"
        outStr = "  <------- X ------->\n"

        # print(f"entQX: {entQX} entQY:{entQY}")
        # for q in quadrants:
        #     print(f"quadrant: {q.Coord.ToString()}")


        outStr+="^ " + line
        for y in range(entQY -1, entQY + 2):
            if y != entQY -1:
                outStr += "| " + line

            if y == entQY:
                outStr += "Y "
            else:
                outStr += "| "

            for x in range(entQX - 1, entQX + 2):


                if y < 0 or y > gbl.MAX_QUADRANT_SECTOR_XY -1  or x < 0 or x > gbl.MAX_QUADRANT_SECTOR_XY -1:
                    outStr += "| *** "
                else:
                    data = [q for q in quadrants if q.Coord.x == x and q.Coord.y == y]
                    if len(data) == 0:
                        raise RuntimeError(f"In getLRSFormatted - NotFound x={x} y={y}")
                    outStr += self.getQuadrantForGalaxyFormatted(data[0], False)
            outStr += "|\n"
        outStr += "v " + line
        return outStr

    def getQuadrantForGalaxyFormatted(self, quadrant: Quadrant|None, markStarship: bool):
        if quadrant is None:
            return "***"
        if not quadrant.HasBeenExplored:
            return "| *** "
        entMarkerStart = " "
        entMarkerEnd = " "

        if markStarship:
            entMarkerStart = ">"
            entMarkerEnd = "<"

        outstr = ""
        outstr += "|" + entMarkerStart
        outstr += str(quadrant.NumEnemies)
        if quadrant.HasStarBase:
            outstr += "1"
        else:
            outstr += "0"

        outstr += str(quadrant.NumStars)
        outstr += entMarkerEnd
        return outstr

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
                quad = self.game.galaxy.GetQuadrant(x,y)
                if quad.Coord.x == self.game.galaxy.CurrentQuadrant.coord.x and quad.Coord.y == self.game.galaxy.CurrentQuadrant.coord.y:
                    outStr += self.getQuadrantForGalaxyFormatted(quad, True)
                else:
                    outStr += self.getQuadrantForGalaxyFormatted(quad, False)

                # print(f"[{self.getQuadrantForGalaxyFormatted(quad, True)}]")
            outStr += "|\n"

        outStr += "v " + line
        return outStr

    def getRoutineMaint(self, missionTime: float, enemiesFire: bool):
        res = self.game.routine_maint(missionTime, enemiesFire)
        data = res.MaintResult
        if data is None:
            return CLI_Messages.InternalErrorMessage
        if data.DockingStatus is None:
            return CLI_Messages.InternalErrorMessage

        outString = "\n"

        if data.GameStatus != GameStatus.Normal:
            self.GameOver = True
            match data.GameStatus:
                case GameStatus.StarshipDestroyed:
                    return CLI_Messages.END_MissionFailed_StarshipDestroyed
                case GameStatus.RanOutOfEnergy:
                    return CLI_Messages.END_MissionFailed_RanOutOfEnergy
                case GameStatus.RanOutOfTime:
                    return CLI_Messages.END_MissionFailed_RanOutOfTime
                case GameStatus.OutOfEnergyShieldEnergyAvailable:
                    outString += CLI_Messages.END_EnergyGoneShieldEnergyAvail
                case GameStatus.MissionOver:
                    return "\n" + CLI_Messages.END_MissionAccomplished
                case _:
                    return CLI_Messages.InternalErrorMessage

        if not data.DockingStatus.PreviousStatus and data.DockingStatus.CurrentStatus:
            outString += CLI_Messages.MAINT_Docked + "\n"

        if data.StarbaseRepairsAvailable is not None:
            outString += CLI_Messages.MAINT_TechWaiting + CLI_Messages.MAINT_ItWillTake
            outString += str(abs(data.StarbaseRepairsAvailable.MissionTimeToRepair))
            outString += CLI_Messages.MAINT_MissionTime + "\n"
            outString += CLI_Messages.MAINT_ReplyYes

        if len(data.DevicesRepairStatusChanged) > 0:
            for device in data.DevicesRepairStatusChanged:
                if device.damageLevel == 100:
                    outString += CLI_Messages.MAINT_RepairsComplete + device.name + "\n"
                    device.damageLevel = 0

        starshipDestroyedMessageSent = False

        if len(data.EnemiesMoved) != 0:
            for enemy in data.EnemiesMoved:
                outline = ""
                msg = CLI_Messages.MAINT_EnemyMoved.format(enemy.EnemyCoord_Orig.ToString(), enemy.EnemyCoord_Dest.ToString())
                outline += msg
                outString += "\n" + outline

        if data.EnemiesFired is not None:
            outline = ""
            for enemyFired in data.EnemiesFired:
                if starshipDestroyedMessageSent:
                    continue
                if outline.strip():
                    outline += "\n"

                if not data.DockingStatus.CurrentStatus:
                    if enemyFired.StarshipDestroyed:
                        outline += CLI_Messages.MAINT_EnemyFiredStarshipDestroyed.format(enemyFired.EnemyFiredAmount, enemyFired.EnemyCoord.ToString(), enemyFired.StarshipNewShieldAmount)
                        starshipDestroyedMessageSent = True
                    else:
                        outline += CLI_Messages.MAINT_EnemyFiredShieldHit.format(str(enemyFired.EnemyFiredAmount), enemyFired.EnemyCoord.ToString(), str(enemyFired.StarshipNewShieldAmount))
                        if enemyFired.DeviceDamaged is not None and enemyFired.DeviceDamagedAmount is not None:
                            outline += "\n" + enemyFired.DeviceDamaged.name + CLI_Messages.MAINT_DeviceDamaged + str(round(abs(enemyFired.DeviceDamagedAmount),1)) + CLI_Messages.MAINT_MissionTimeToRepair
                else:
                    outline += CLI_Messages.MAINT_EnemyFiredProtected.format(enemyFired.EnemyFiredAmount, enemyFired.EnemyCoord.ToString()) + CLI_Messages.MAINT_StarbaseShieldsProtected


            outString += "\n" + outline

        enemyList = self.game.galaxy.CurrentQuadrant.GetEnemySectors()
        if not data.DockingStatus.CurrentStatus and not starshipDestroyedMessageSent:
            shieldLevel = self.game.galaxy.Starship.shieldLevel
            if shieldLevel < 50 and enemyList is not None and len(enemyList)> 0:
                outString += "\n" + CLI_Messages.WarningMessageShieldDownInCombatArea

        if enemyList is not None and len(enemyList) > 0 and self.newQuadrant:
            outString += "\n" + CLI_Messages.MAINT_NewQuadrantEnemiesRedAlert

        return outString

    def runSRS(self) -> str:
        result = self.game.srs()
        if result.CommandResult == CommandResult.Damaged:
            return CLI_Messages.SRS_Damaged
        return self.getSRSFormatted(result.SRS.Sectors) + self.getRoutineMaint(0.1, True)

    def runLRS(self) -> str:
        result = self.game.lrs()
        if result.CommandResult == CommandResult.Damaged:
            return CLI_Messages.LRS_Damaged
        cqCoord = self.game.galaxy.CurrentQuadrant.coord
        return self.getLRSFormatted(result.LRS.Quadrants, cqCoord.x, cqCoord.y) + self.getRoutineMaint(0.1, True)

    def runSHE(self, commands: list[str]) -> str:
        if len(commands) == 1:
            return CLI_Messages.SHE_MissingAmount

        sheInt = self.game.str2int(commands[1])
        if sheInt is None:
            return CLI_Messages.SHE_InvalidAmount

        if sheInt < 0:
            return CLI_Messages.SHE_InvalidAmount

        result = self.game.she(sheInt)
        if result.CommandResult == CommandResult.Damaged:
            return CLI_Messages.SHE_Damaged

        if result.CommandResult == CommandResult.Error:
            return CLI_Messages.SHE_InvalidAmount + str(sheInt) + "\n" + result.SHE.ErrorMessage

        return CLI_Messages.SHE_Changed + str(sheInt) + self.getRoutineMaint(0.1, True)

    def runLAS(self, commands: list[str]) -> str:
        if len(commands) == 1:
            return CLI_Messages.LAS_MissingAmount

        lasAmount = self.game.str2int(commands[1])
        if lasAmount is None:
            return CLI_Messages.LAS_InvalidAmount

        if lasAmount <= 0:
            return CLI_Messages.LAS_InvalidAmount

        res = self.game.las(lasAmount)

        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.LAS_Damaged

        if res.CommandResult == CommandResult.No_Enemies_Present:
            return CLI_Messages.LAS_NoEnemies

        if res.CommandResult == CommandResult.InsufficientInventory:
            return CLI_Messages.LAS_InsufficientEnergy

        outMsg = ""
        if res.CommandResult == CommandResult.OK:
            for objHit in res.LAS.ObjectHitReport:
                objHitCoord = objHit.Coord.ToString()

                if outMsg == "":
                    outMsg += "\n"

                outMsg  += CLI_Messages.LAS_Fired + str(objHit.UnitHit) + CLI_Messages.LAS_Hit + objHitCoord

                if objHit.Destroyed:
                    outMsg += CLI_Messages.LAS_EnemyDestroyed
                else:
                    outMsg += CLI_Messages.LAS_SensorsIndicate + str(objHit.ShieldRemaining) + CLI_Messages.LAS_Remaining

        return outMsg + self.getRoutineMaint(0.1, True)

    def runTOR(self, commands: list[str]) -> str:
        if len(commands) == 1:
            return CLI_Messages.TOR_MissingDirection

        torDIR = self.game.str2float(commands[1])
        if torDIR is None:
            return CLI_Messages.TOR_InvalidDirection

        if torDIR <0 or torDIR >= 9:
            return CLI_Messages.TOR_InvalidDirection + self.showHelpNAVTOR(False)

        res = self.game.tor(torDIR)

        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.TOR_Damaged

        if res.CommandResult == CommandResult.No_Enemies_Present:
            return CLI_Messages.TOR_NoEnemies

        if res.CommandResult == CommandResult.InsufficientInventory:
            return CLI_Messages.TOR_Expended

        if res.CommandResult == CommandResult.TOR_Missed:
            return CLI_Messages.TOR_Missed

        outMsg = ""
        if res.CommandResult == CommandResult.OK:
            match res.TOR.ObjectHitReport.ObjectHit:
                case objectHit.ObjectHit.Enemy:
                    outMsg += CLI_Messages.TOR_Fired + CLI_Messages.TOR_EnemyAtSector + res.TOR.ObjectHitReport.Coord.ToString() + CLI_Messages.TOR_Destroyed
                case objectHit.ObjectHit.Star:
                    if res.TOR.ObjectHitReport.Destroyed:
                        outMsg += CLI_Messages.TOR_Fired + CLI_Messages.TOR_StarDestroyed
                    else:
                        outMsg += CLI_Messages.TOR_Fired + CLI_Messages.TOR_StarAbsorbedTorp
                case objectHit.ObjectHit.Starbase:
                    outMsg += CLI_Messages.TOR_Fired + CLI_Messages.TOR_StarbaseDestroyed
                case _:
                    return CLI_Messages.InternalErrorMessage

        return outMsg + self.getRoutineMaint(0.1, True)

    def runCOM(self, commands: list[str]) -> str:
        if len(commands) <2:
            return CLI_Messages.CPU_InvalidCommand

        match commands[1].upper():
            case "REC":
                return self.runCOM_REC()
            case "TOR":
                return self.runCOM_TOR()
            case "NAV":
                return self.runCOM_NAV(commands)
            case "STB":
                return self.runCOM_STB()
            case "STA":
                return self.runCOM_STA()
            case _:
                return CLI_Messages.CPU_InvalidCommand

    def runCOM_REC(self) -> str:
        res = self.game.com_rec()
        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.CPU_Damaged

        return self.getGalaxyFormatted()

    def runCOM_TOR(self) -> str:
        res = self.game.com_tor()
        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.CPU_Damaged
        if res.CommandResult == CommandResult.No_Enemies_Present:
            return CLI_Messages.CPU_TOR_NoEnemies

        outStr = ""
        for dte in res.COM_TOR.DirectionToEnemies:
            if outStr == "":
                outStr += "\n"

            outStr += CLI_Messages.CPU_TOR_EnemyAtSector + dte.Coord.ToString() + CLI_Messages.CPU_TOR_IsBearing + str(round(dte.Direction,1))

        return outStr

    def runCOM_NAV(self, commands: list[str]) -> str:

        if len(commands) != 6:
            return CLI_Messages.CPU_NAV_Invalid

        QX = self.game.str2int(commands[2])
        if QX is None:
            return CLI_Messages.CPU_NAV_InvalidCoord
        if QX < 0 or QX > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return CLI_Messages.CPU_NAV_InvalidQX

        QY = self.game.str2int(commands[3])
        if QY is None:
            return CLI_Messages.CPU_NAV_InvalidCoord
        if QY < 0 or QY > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return CLI_Messages.CPU_NAV_InvalidQY

        SX = self.game.str2int(commands[4])
        if SX is None:
            return CLI_Messages.CPU_NAV_InvalidCoord
        if SX < 0 or SX > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return CLI_Messages.CPU_NAV_InvalidSX

        SY = self.game.str2int(commands[5])
        if SY is None:
            return CLI_Messages.CPU_NAV_InvalidCoord
        if SY < 0 or SY > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return CLI_Messages.CPU_NAV_InvalidSY

        res = self.game.com_nav(Coord(QX, QY), Coord(SX, SY))
        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.CPU_Damaged

        return CLI_Messages.CPU_NAV_Dir + str(round(res.COM_NAV.Direction,1)) + CLI_Messages.CPU_NAV_Dist + str(round(res.COM_NAV.Distance,1))

    def runCOM_STB(self) -> str:
        res = self.game.com_stb()
        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.CPU_Damaged

        if res.CommandResult == CommandResult.CPU_STB_No_Starbase_Present:
            return CLI_Messages.CPU_STB_NoStarbases

        outStr = ""
        outStr += CLI_Messages.CPU_STB_StarbaseFoundInSector
        outStr += CLI_Messages.CPU_STB_Dir
        outStr += str(round(res.COM_STB.Direction,1))
        outStr += CLI_Messages.CPU_STB_Dist
        outStr += str(round(res.COM_STB.Distance,1))

        return outStr

    def runCOM_STA(self) -> str:
        res = self.game.com_sta()
        if res.CommandResult == CommandResult.Damaged:
            return CLI_Messages.CPU_Damaged

        outStr = ""

        outStr += CLI_Messages.CPU_STA_MissionTime + str(round(res.COM_STA.MissionTime,1)) + "\n"
        outStr += CLI_Messages.CPU_STA_Quadrant + res.COM_STA.QuadrantCoord.ToString() + "\n"
        outStr += CLI_Messages.CPU_STA_Sector + res.COM_STA.SectorCoord.ToString() + "\n"
        outStr += CLI_Messages.CPU_STA_DeviceStatus + "\n"
        for device in self.game.galaxy.Starship.devices:
            msg = ""
            if device.damageLevel < 0:
                msg += "Damaged - " + str(abs(round(device.damageLevel,1))) + " mission time units"
            else:
                msg += "Fully functional"
            outStr += "\t" + device.name.ljust(30) + msg + "\n"
        outStr += CLI_Messages.CPU_STA_EnemiesRemaining + str(res.COM_STA.EnemiesRemaining) + "\n"
        outStr += CLI_Messages.CPU_STA_StarbasesRemaining + str(res.COM_STA.StarbasesRemaining) + "\n"
        outStr += CLI_Messages.CPU_STA_EnergyRemaining + str(res.COM_STA.EnergyRemaining) + "\n"
        outStr += CLI_Messages.CPU_STA_ShieldLevel + str(res.COM_STA.ShieldLevel) + "\n"
        outStr += CLI_Messages.CPU_STA_TorpRemaining + str(res.COM_STA.TorpsRemaining) + "\n"
        outStr += CLI_Messages.CPU_STA_Docked
        if res.COM_STA.Docked:
            outStr += "Docked"
        else:
            outStr += "Not docked"
        outStr += "\n"
        outStr += CLI_Messages.CPU_STA_MissionTimeRemaining + str(round(res.COM_STA.MissionTimeDeadline - res.COM_STA.MissionTime,1)) + "\n"

        return outStr

    def runNAV(self, commands: list[str]) -> str:
        if len(commands) != 3:
            return CLI_Messages.NAV_InvalidCommand

        DIR = self.game.str2float(commands[1])
        if DIR is None:
            return CLI_Messages.NAV_Invalid_Dir + commands[1]
        if DIR < 0 or DIR >= 9:
            return CLI_Messages.NAV_Invalid_Dir + str(DIR) + self.showHelpNAVTOR(True)

        DIST = self.game.str2float(commands[2])
        if DIST is None:
            return CLI_Messages.NAV_Invalid_Dist + commands[2]
        if DIST < 0 or DIST > 8:
            return CLI_Messages.NAV_Invalid_Dist + str(round(DIST,1)) + self.showHelpNAVTOR(True)

        beforeCoord = self.game.galaxy.CurrentQuadrant.coord
        res = self.game.nav(DIR, DIST)
        afterCoord = self.game.galaxy.CurrentQuadrant.coord

        if beforeCoord.x != afterCoord.x or beforeCoord.y != afterCoord.y:
            self.newQuadrant = True

        if res.CommandResult == CommandResult.Damaged and DIST > 0.2:
            return CLI_Messages.NAV_WarpDriveDamaged

        if res.CommandResult == CommandResult.Error and res.NAV.NavMessage == NavMessage.InsufficientEnergy_ShieldEnergyAvailable:
            return CLI_Messages.NAV_NotEnoughEnergy_ShieldEnergyAvail

        if res.CommandResult == CommandResult.Error and res.NAV.NavMessage == NavMessage.BadInput_OutsideGalaxy:
            return CLI_Messages.NAV_OutsideGalaxy

        if res.CommandResult == CommandResult.Error and res.NAV.NavMessage == NavMessage.BadInput_ObjectHit:
            return CLI_Messages.NAV_ImpulseEngineShutDown + self.game.galaxy.GetStarshipSector().coord.ToString() + CLI_Messages.NAV_BadNavigation

        timeTraveled = calculationUtils.Distance2Time(res.NAV.DistanceTraveled)
        if res.CommandResult == CommandResult.OK and DIST < 1:
            return CLI_Messages.NAV_ImpulseEngaged + self.getRoutineMaint(timeTraveled, False)
        else:
            return CLI_Messages.NAV_WarpEngaged + self.getRoutineMaint(timeTraveled, False)

    def runDAM(self) -> str:
        res = self.game.dam()
        if res.CommandResult != CommandResult.OK:
            return CLI_Messages.InternalErrorMessage

        outMsg = ""
        outMsg += CLI_Messages.DAM_DamageReport + "\n"

        for device in res.DAM.Devices:
            msg = ""
            if device.damageLevel < 0:
                msg = "Damaged - " + str(round(device.damageLevel, 1))
                msg += " mission time units"
            else:
                msg += "Fully functional"
            outMsg += "\t" + device.name.ljust(30) + msg

        if len(res.DAM.Devices) ==0:
            outMsg = CLI_Messages.DAM_DamageReport_NoDamages

        return outMsg








