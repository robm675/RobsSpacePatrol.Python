from dataclasses import dataclass

from models import (
    commandResult,
    commands,
    coord,
    device,
    directionToEnemy,
    dockingStatus,
    enemyFired,
    enemyMoved,
    gameStatus,
    navMessage,
    objectHitReport,
    quadrant,
    sector,
    starbaseRepairs,
)


@dataclass
class SRS:
    Sectors: list[sector.Sector]
    def ToString(self) -> str:
        outStr = "SRS:\n"
        for sect in self.Sectors:
            outStr += f"x={sect.coord.x},y={sect.coord.y},contents={sect.sectorContents.sectorContents},hasEnemy={sect.hasEnemy()}\n"
        return outStr

@dataclass
class LRS:
    Quadrants: list[quadrant.Quadrant] #Only explored quadrants are returned
    def ToString(self) -> str:
        outStr = "LRS:\n"
        for quad in self.Quadrants:
            outStr += f"x={quad.Coord.x},y={quad.Coord.y},hasStarbase={quad.HasStarBase},numStars={quad.NumStars},numEnemies={quad.NumEnemies},hasBeenExplored={quad.HasBeenExplored}\n"
        return outStr

@dataclass
class COM_REC:
    Quadrants: list[quadrant.Quadrant]
    def ToString(self) -> str:
        outStr = "COM_REC:\n"
        for quad in self.Quadrants:
            outStr += f"x={quad.Coord.x},y={quad.Coord.y},hasStarbase={quad.HasStarBase},numStars={quad.NumStars},numEnemies={quad.NumEnemies},hasBeenExplored={quad.HasBeenExplored}\n"
        return outStr

@dataclass
class COM_STA:
    MissionTime: float
    QuadrantCoord: coord.Coord
    SectorCoord: coord.Coord
    DamagedDevices: list[device.Device]
    EnemiesRemaining: int
    StarbasesRemaining: int
    EnergyRemaining: int
    ShieldLevel: int
    TorpsRemaining: int
    Docked:bool
    MissionTimeDeadline: float
    def ToString(self) -> str:
        outStr = "COM_STA:\n"

        outStr += f"Mission Time={self.MissionTime}\n"
        outStr += f"QuadrantCoord={self.QuadrantCoord.ToString()}\n"
        outStr += f"SectorCoord={self.SectorCoord.ToString()}\n"
        outStr += f"DamagedDevices={len(self.DamagedDevices)}\n"
        outStr += f"EnemiesRemaining={self.EnemiesRemaining}\n"
        outStr += f"StarbasesRemaining={self.StarbasesRemaining}\n"
        outStr += f"EnergyRemaining={self.EnergyRemaining}\n"
        outStr += f"ShieldLevel={self.ShieldLevel}\n"
        outStr += f"TorpsRemaining={self.TorpsRemaining}\n"
        outStr += f"Mission Time Deadline={self.MissionTimeDeadline}\n"

        return outStr

@dataclass
class COM_STB:
    Direction:float
    Distance:float
    StarbaseCoord: coord.Coord
    def ToString(self) -> str:
        outStr = "COM_STB:\n"
        outStr += f"Direction={self.Direction}\n"
        outStr += f"Distance={self.Distance}\n"
        outStr += f"StarbaseCoord={self.StarbaseCoord.ToString()}\n"
        return outStr

@dataclass
class COM_TOR:
    DirectionToEnemies: list[directionToEnemy.DirectionToEnemy]
    def ToString(self) -> str:
        outStr = "COM_TOR:\n"
        for dte in self.DirectionToEnemies:
            outStr += f"enemy dir={dte.Direction} dist={dte.Distance}\n"
        return outStr

@dataclass
class COM_NAV:
    Direction: float
    Distance: float
    def ToString(self) -> str:
        outStr = "COM_NAV:\n"
        outStr += f"Direction={self.Direction}\n"
        outStr += f"Distance={self.Distance}\n"
        return outStr

@dataclass
class DAM:
    Devices: list[device.Device]
    def ToString(self) -> str:
        outStr = "DAM:\n"
        if self.Devices is None or  len(self.Devices) == 0:
            outStr += "No damaged Devices"
        else:
            for dam in self.Devices:
                outStr += f"damaged device: {dam.name} level={dam.damageLevel}\n"
        return outStr

@dataclass
class SHE:
    ErrorMessage:str
    def ToString(self) -> str:
        outStr = "SHE:\n"
        outStr += f"ErrorMessage: [{self.ErrorMessage}]"
        return outStr

@dataclass
class TOR:
    ObjectHitReport: objectHitReport.ObjectHitReport
    def ToString(self) -> str:
        outStr = "TOR:\n"
        if self.ObjectHitReport is None:
            outStr += "No objects hit\n"
        else:
            outStr += f"object hit report\t object=[{self.ObjectHitReport.ObjectHit}]\tUnit=[{self.ObjectHitReport.UnitHit}]"
            outStr += f"\tcoord=[{self.ObjectHitReport.Coord.ToString()}]\tMissed=[{self.ObjectHitReport.Missed}]"
            outStr += f"\tDestroyed=[{self.ObjectHitReport.Destroyed}]\tShieldRemaining=[{self.ObjectHitReport.ShieldRemaining}]"
            outStr += f"\tStarSurvived=[{self.ObjectHitReport.StarSurvived}]"
        return outStr

@dataclass
class LAS:
    ObjectHitReport: list[objectHitReport.ObjectHitReport]
    def ToString(self) -> str:
        outStr = "LAS:\n"
        if self.ObjectHitReport is None or len(self.ObjectHitReport) == 0:
            outStr += "No Enemies"
        else:
            for ohr in self.ObjectHitReport:
                outStr += f"object hit report\t object=[{ohr.ObjectHit}]\tUnit=[{ohr.UnitHit}]"
                outStr += f"\tcoord=[{ohr.Coord.ToString()}]\tMissed=[{ohr.Missed}]"
                outStr += f"\tDestroyed=[{ohr.Destroyed}]\tShieldRemaining=[{ohr.ShieldRemaining}]"
                outStr += f"\tStarSurvived=[{ohr.StarSurvived}]\n"
        return outStr

@dataclass
class NAV:
    NavMessage: navMessage.NavMessage
    DistanceTraveled: float
    def ToString(self) -> str:
        outStr = "NAV:\n"
        outStr += f"NavMessage: [{self.NavMessage}] "
        outStr += f"DistanceTraveled: [{self.DistanceTraveled}] \n"
        return outStr

@dataclass
class MaintResult:
    NewMissionTime: float
    DevicesRepairStatusChanged: list[device.Device]
    EnemiesFired: list[enemyFired.EnemyFired]
    EnemiesMoved: list[enemyMoved.EnemyMoved]
    DockingStatus: dockingStatus.DockingStatus
    StarbaseRepairsAvailable: starbaseRepairs.StarbaseRepairs | None
    GameStatus: gameStatus.GameStatus


class Result:
    SRS: SRS
    LRS: LRS
    COM_REC: COM_REC
    COM_STA: COM_STA
    COM_STB: COM_STB
    COM_TOR: COM_TOR
    COM_NAV: COM_NAV
    DAM: DAM
    SHE: SHE
    TOR: TOR
    LAS: LAS
    NAV: NAV
    MaintResult: MaintResult
    Command: commands.Commands
    CommandResult: commandResult.CommandResult

