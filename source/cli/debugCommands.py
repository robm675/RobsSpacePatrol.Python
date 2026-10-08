# region imports
import sys

import gbl
from cli import CLI_Messages
from game.game import Game
from models.coord import Coord
from models.quadrant import Quadrant
from models.sector import Sector

# endregion

class DebugCommands:
    game: Game

    def __init__(self, game: Game):
        self.game = game

    def debugMenu(self) -> str:
        stringout = ""

        stringout += "SET\n"
        stringout += "\tCLEARCQ\n"
        stringout += "\t\tALL\n"
        stringout += ""
        stringout += "SET or SET\n"
        stringout += "\tCURRENTQUADRANT\n"
        stringout += "\t\tSECTOR\n"
        stringout += "\t\tENEMY\n"
        stringout += "\n"
        stringout += "\tQUADRANT\n"
        stringout += "\t\tNUMENEMIES\n"
        stringout += "\t\tNUMSTARS\n"
        stringout += "\t\tSTARBASE\n"
        stringout += "\t\tEXPLORED\n"
        stringout += "\n"
        stringout += "\tSTARSHIP"
        stringout += "\t\tENERGY\n"
        stringout += "\t\tSHIELD\n"
        stringout += "\t\tTORP\n"
        stringout += "\t\tDEVICE\n"
        stringout += "\t\tSECTOR\n"
        stringout += "\t\tQUADRANT\n"
        stringout += "\n"
        stringout += "\tGALAXY\n"
        stringout += "\t\tMISSION_TIME\n"
        stringout += "\t\tMISSIONTIMEDEADLINE\n"
        stringout += "\n\n"
        stringout += "CHECK\n"
        stringout += "\n"

        return stringout

    def runDEBUG_Command(self, commands: list[str]) -> str:
        if len(commands) < 2:
            return CLI_Messages.DebugErrorInCommand + "\n" + self.debugMenu()

        commands = [cmd.upper() for cmd in commands]

        match commands[1]:
            case "SET":
                return self.run_SET_Debug(commands)
            case "GET":
                return self.run_GET_Debug(commands)
            case "CHECK":
                return CLI_Messages.DebugCommandOK
            case _:
                return CLI_Messages.DebugUnknownCommand

    def str2int(self, string:str) -> int|None:
        try:
            xInt = int(string)
        except ValueError:
            return None
        return xInt

    def str2float(self, string:str) -> float|None:
        try:
            xFloat = float(string)
        except ValueError:
            return None
        return xFloat

    def getCoordByXY(self, x: str, y: str) -> Coord | None:
        xInt = -1
        yInt = -1
        try:
            xInt = int(x)
        except ValueError:
            return None

        try:
            yInt = int(y)
        except ValueError:
            return None

        return Coord(xInt, yInt)

    def getCoordByCoord(self, coord: Coord) -> str:
        return f"{coord.x}.{coord.y}"

    def getSector(self, x:str, y: str) -> Sector | None:
        coord = self.getCoordByXY(x, y)
        if coord is None:
            return None
        targetSector = self.game.galaxy.CurrentQuadrant.GetSectorByCoord(coord)
        return targetSector

    def getQuadrant(self, x: str, y: str) -> Quadrant | None:
        coord = self.getCoordByXY(x, y)
        if coord is None:
            return None
        targetQuadrant = self.game.galaxy.GetQuadrantByCoord(coord)
        return targetQuadrant

    def result(self, result: bool) -> str:
        if result:
            return CLI_Messages.DebugErrorInCommand
        else:
            return CLI_Messages.DebugCommandOK

    def resultWithParm(self, result: bool, msg: str) ->str:
        if result:
            return CLI_Messages.DebugErrorInCommand
        else:
            return msg

    def run_GET_Debug(self, commands: list[str]) -> str:
        if len(commands) < 3:
            return CLI_Messages.DebugInvalidCommand

        match commands[2]:
            case "CURRENTQUADRANT":
                if len(commands) < 4:
                    return CLI_Messages.DebugInvalidCommand
                match commands[3]:
                    case "SECTOR":
                        return self.getSectorContents(commands)
                    case "ENEMY":
                        return self.getSectorEnemy(commands)
                    case _:
                        return CLI_Messages.DebugInvalidCommand
            case "QUADRANT":
                return self.getQudrantContents(commands)
            case "STARSHIP":
                return self.getStarship(commands)
            case "GALAXY":
                return self.getGalaxy(commands)
            case _:
                return CLI_Messages.DebugInvalidCommand

    def run_SET_Debug(self, commands: list[str]) -> str:
        if len(commands) < 3:
            return CLI_Messages.DebugInvalidCommand

        match commands[2]:
            case "PREVENTENEMYFIRE":
                match commands[3]:
                    case "ON":
                        self.game.preventEnemyFire = True
                        return self.result(False)
                    case "OFF":
                        self.game.preventEnemyFire = False
                        return self.result(False)
                    case _:
                        return CLI_Messages.DebugInvalidCommand
            case "ENEMYMOVE":
                match commands[3]:
                    case "ON":
                        self.game.skipEnemyMove = False
                        self.game.forceEnemyMove = False
                        return self.result(False)
                    case "OFF":
                        self.game.skipEnemyMove = True
                        self.game.forceEnemyMove = False
                        return self.result(False)
                    case "FORCE":
                        self.game.skipEnemyMove = False
                        self.game.forceEnemyMove = True
                        return self.result(False)
                    case _:
                        return CLI_Messages.DebugInvalidCommand
            case "CURRENTQUADRANT":
                if len(commands) < 4:
                    return CLI_Messages.DebugInvalidCommand
                match commands[3]:
                    case "SECTOR":
                        return self.setSectorContents(commands)
                    case "ENEMY":
                        return self.setSectorEnemy(commands)
                    case _:
                        return CLI_Messages.DebugInvalidCommand
            case "QUADRANT":
                return self.setQudrantContents(commands)
            case "STARSHIP":
                return self.setStarship(commands)
            case "GALAXY":
                return self.setGalaxy(commands)
            case "CLEARCQ":
                allSW = False
                if len(commands) > 3 and commands[3] == "ALL":
                    allSW = True

                for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                    for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
                        coord = Coord(x,y)
                        targetSector = self.game.galaxy.CurrentQuadrant.GetSectorByCoord(coord)
                        if allSW:
                            targetSector.sectorContents.sectorContents = gbl.SECTOR_EMPTY
                        else:
                            if targetSector.sectorContents.sectorContents != gbl.SECTOR_STARSHIP:
                                targetSector.sectorContents.sectorContents = gbl.SECTOR_EMPTY

                nonEmptySectors = self.game.galaxy.CurrentQuadrant.GetSectorsNotEmpty()
                if allSW and len(nonEmptySectors) != 0:
                    raise RuntimeError("Error - Current Quadrant was not cleared correctly")
                if not allSW and len(nonEmptySectors) != 1:
                    print(f"allSw={allSW} len(nonEmptySectors)={len(nonEmptySectors)}", file=sys.stderr)
                    raise RuntimeError("Error - Current Quadrant was not cleared correctly")

            case _:
                return CLI_Messages.DebugInvalidCommand
        return "**ERROR**"
    
    def setSectorContents(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return CLI_Messages.DebugInvalidCommand
        targetSector = self.getSector(commands[4], commands[5])
        if targetSector is None:
            raise RuntimeError("TargetSector is None")        
        targetSector.sectorContents.sectorContents = commands[6].upper().strip()
        return self.result(True)

    def getSectorContents(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return self.result(True)
        targetSector = self.getSector(commands[4], commands[5])
        if targetSector is None:
            raise RuntimeError("TargetSector is None")
        return self.resultWithParm(False, targetSector.sectorContents.sectorContents)

    def setSectorEnemy(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return CLI_Messages.DebugInvalidCommand
        targetSector = self.getSector(commands[4], commands[5])
        if targetSector is None:
            return CLI_Messages.DebugInvalidCommand
        shieldLevel = self.str2int(commands[6])
        if shieldLevel is None:
            return CLI_Messages.DebugInvalidCommand
        targetSector.setEnemy(shieldLevel)
        return self.result(True)

    def getSectorEnemy(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return self.result(True)
        targetSector = self.getSector(commands[4], commands[5])
        if targetSector is None:
            return CLI_Messages.DebugInvalidCommand
        if targetSector.enemy is None:
            return CLI_Messages.DebugInvalidCommand
        return self.resultWithParm(False, f"ENEMY:{targetSector.enemy.shieldLevel}")

    def getQudrantContents(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return CLI_Messages.DebugInvalidCommand

        quadrant = self.getQuadrant(commands[3], commands[4])
        if quadrant is None:
            return self.result(True)

        match commands[5]:
            case "NUMENEMIES":
                return self.resultWithParm(False, str(quadrant.NumEnemies))
            case "NUMSTARS":
                return self.resultWithParm(False, str(quadrant.NumStars))
            case "STARBASE":
                if quadrant.HasStarBase:
                    return self.resultWithParm(False, "1")
                else:
                    return self.resultWithParm(False, "0")
            case "EXPLORED":
                if quadrant.HasBeenExplored:
                    return self.resultWithParm(False, "1")
                else:
                    return self.resultWithParm(False, "0")
            case _:
                return CLI_Messages.DebugInvalidCommand

    def setQudrantContents(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return CLI_Messages.DebugInvalidCommand

        quadrant = self.getQuadrant(commands[3], commands[4])
        if quadrant is None:
            return self.result(True)

        value = self.str2int(commands[6])
        if value is None:
            return self.result(True)

        match commands[5]:
            case "NUMENEMIES":
                quadrant.NumEnemies =value
                return self.result(False)
            case "NUMSTARS":
                quadrant.NumStars =value
                return self.result(False)
            case "STARBASE":
                if value == 1:
                    quadrant.HasStarBase = True
                else:
                    quadrant.HasStarBase = False
                return self.result(False)
            case "EXPLORED":
                if value == 1:
                    quadrant.HasBeenExplored = True
                else:
                    quadrant.HasBeenExplored = False
                return self.result(False)
            case _:
                return CLI_Messages.DebugInvalidCommand

    def getStarship(self, commands: list[str]) -> str:
        if len(commands) < 4:
            return CLI_Messages.DebugInvalidCommand

        match commands[3]:
            case "ENERGY":
                value = self.game.galaxy.Starship.energyLevel
                return self.resultWithParm(False, str(value))
            case "SHIELD":
                value = self.game.galaxy.Starship.shieldLevel
                return self.resultWithParm(False, str(value))
            case "TORP":
                value = self.game.galaxy.Starship.torpsRemain
                return self.resultWithParm(False, str(value))
            case "DEVICE":
                dev = self.game.galaxy.Starship.GetDeviceByStr(commands[4])
                return self.resultWithParm(False, str(round(dev.damageLevel,1)))
            case "SECTOR":
                value = self.game.galaxy.GetStarshipSector()
                return self.resultWithParm(False, self.getCoordByCoord(value.coord))
            case "QUADRANT":
                value = self.game.galaxy.GetStarshipQuadrant()
                return self.resultWithParm(False, self.getCoordByCoord(value.Coord))
            case _:
                return CLI_Messages.DebugInvalidCommand

    def setStarship(self, commands:list[str]) -> str:
        if len(commands) < 5:
            return CLI_Messages.DebugInvalidCommand 

        match commands[3]:
            case "ENERGY":
                value = self.str2int(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.Starship.energyLevel = value
                return self.result(False)
            case "SHIELD":
                value = self.str2int(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.Starship.shieldLevel = value
                return self.result(False)
            case "TORP":
                value = self.str2int(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.Starship.torpsRemain = value
                return self.result(False)
            case "DEVICE":
                dev = self.game.galaxy.Starship.GetDeviceByStr(commands[4])
                damTemp = self.str2float(commands[5])
                if damTemp is None:
                    return self.result(True)
                dev.damageLevel = damTemp
                # return self.resultWithParm(False, str(round(dev.damageLevel,1)))
                return self.result(False)
            case "SECTOR":
                tempCoord = self.getCoordByXY(commands[4], commands[5])
                if tempCoord is None:
                    return self.result(True)
                entSector = self.game.galaxy.GetStarshipSector()
                self.game.moveObjectInsideQuadrant(entSector.coord, tempCoord)
                return self.result(False)
            case "QUADRANT":
                entSector = self.game.galaxy.GetStarshipSector()
                quadrant = self.getQuadrant(commands[4], commands[5])
                if quadrant is None:
                    return self.result(True)
                self.game.moveStarshipQuadrant(quadrant, entSector.coord)
                return self.result(False)
            case _:
                return CLI_Messages.DebugInvalidCommand

            

    def getGalaxy(self, commands: list[str]) -> str:
        if len(commands) < 4:
            return CLI_Messages.DebugInvalidCommand

        match commands[3]:
            case "MISSION_TIME":
                sd = self.game.galaxy.MissionTime
                return self.resultWithParm(False, str(round(sd,1)))
            case "MISSIONTIMEDEADLINE":
                sd = self.game.galaxy.MissionTimeDeadline
                return self.resultWithParm(False, str(round(sd,1)))
        return "**ERROR**"

    def setGalaxy(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return CLI_Messages.DebugInvalidCommand

        match commands[3]:
            case "MISSION_TIME":
                value = self.str2float(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.MissionTime = value
                return self.result(False)
            case "MISSIONTIMEDEADLINE":
                value = self.str2float(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.MissionTimeDeadline = value
                return self.result(False)
            
        return "**ERROR**"