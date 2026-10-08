from dataclasses import dataclass

from models import (
    command_result,
    commands,
    coord,
    device,
    direction_to_enemy,
    docking_status,
    enemy_fired,
    enemy_moved,
    game_status,
    nav_message,
    object_hit_report,
    quadrant,
    sector,
    starbase_repairs,
)


@dataclass
class SrsResult:
    sectors: list[sector.Sector]

    def to_string(self) -> str:
        out_str = "SRS:\n"
        for sect in self.sectors:
            out_str += f"x={sect.coord.x},y={sect.coord.y},contents={sect.sector_contents.sector_contents},hasEnemy={sect.has_enemy()}\n"
        return out_str


@dataclass
class LrsResult:
    quadrants: list[quadrant.Quadrant]  # Only explored quadrants are returned

    def to_string(self) -> str:
        out_str = "LRS:\n"
        for quad in self.quadrants:
            out_str += f"x={quad.coord.x},y={quad.coord.y},hasStarbase={quad.has_star_base},numStars={quad.num_stars},numEnemies={quad.num_enemies},hasBeenExplored={quad.has_been_explored}\n"
        return out_str


@dataclass
class ComRecResult:
    quadrants: list[quadrant.Quadrant]

    def to_string(self) -> str:
        out_str = "COM_REC:\n"
        for quad in self.quadrants:
            out_str += f"x={quad.coord.x},y={quad.coord.y},hasStarbase={quad.has_star_base},numStars={quad.num_stars},numEnemies={quad.num_enemies},hasBeenExplored={quad.has_been_explored}\n"
        return out_str


@dataclass
class ComStaResult:
    mission_time: float
    quadrant_coord: coord.Coord
    sector_coord: coord.Coord
    damaged_devices: list[device.Device]
    enemies_remaining: int
    starbases_remaining: int
    energy_remaining: int
    shield_level: int
    torps_remaining: int
    docked: bool
    mission_time_deadline: float

    def to_string(self) -> str:
        out_str = "COM_STA:\n"

        out_str += f"Mission Time={self.mission_time}\n"
        out_str += f"QuadrantCoord={self.quadrant_coord.to_string()}\n"
        out_str += f"SectorCoord={self.sector_coord.to_string()}\n"
        out_str += f"DamagedDevices={len(self.damaged_devices)}\n"
        out_str += f"EnemiesRemaining={self.enemies_remaining}\n"
        out_str += f"StarbasesRemaining={self.starbases_remaining}\n"
        out_str += f"EnergyRemaining={self.energy_remaining}\n"
        out_str += f"ShieldLevel={self.shield_level}\n"
        out_str += f"TorpsRemaining={self.torps_remaining}\n"
        out_str += f"Mission Time Deadline={self.mission_time_deadline}\n"

        return out_str


@dataclass
class ComStbResult:
    direction: float
    distance: float
    starbase_coord: coord.Coord

    def to_string(self) -> str:
        out_str = "COM_STB:\n"
        out_str += f"Direction={self.direction}\n"
        out_str += f"Distance={self.distance}\n"
        out_str += f"StarbaseCoord={self.starbase_coord.to_string()}\n"
        return out_str


@dataclass
class ComTorResult:
    direction_to_enemies: list[direction_to_enemy.DirectionToEnemy]

    def to_string(self) -> str:
        out_str = "COM_TOR:\n"
        for dte in self.direction_to_enemies:
            out_str += f"enemy dir={dte.direction} dist={dte.distance}\n"
        return out_str


@dataclass
class ComNavResult:
    direction: float
    distance: float

    def to_string(self) -> str:
        out_str = "COM_NAV:\n"
        out_str += f"Direction={self.direction}\n"
        out_str += f"Distance={self.distance}\n"
        return out_str


@dataclass
class DamResult:
    devices: list[device.Device]

    def to_string(self) -> str:
        out_str = "DAM:\n"
        if self.devices is None or len(self.devices) == 0:
            out_str += "No damaged Devices"
        else:
            for dam in self.devices:
                out_str += f"damaged device: {dam.name} level={dam.damage_level}\n"
        return out_str


@dataclass
class SheResult:
    error_message: str

    def to_string(self) -> str:
        out_str = "SHE:\n"
        out_str += f"ErrorMessage: [{self.error_message}]"
        return out_str


@dataclass
class TorResult:
    object_hit_report: object_hit_report.ObjectHitReport

    def to_string(self) -> str:
        out_str = "TOR:\n"
        if self.object_hit_report is None:
            out_str += "No objects hit\n"
        else:
            out_str += f"object hit report\t object=[{self.object_hit_report.object_hit}]\tUnit=[{self.object_hit_report.unit_hit}]"
            out_str += f"\tcoord=[{self.object_hit_report.coord.to_string()}]\tMissed=[{self.object_hit_report.missed}]"
            out_str += f"\tDestroyed=[{self.object_hit_report.destroyed}]\tShieldRemaining=[{self.object_hit_report.shield_remaining}]"
            out_str += f"\tStarSurvived=[{self.object_hit_report.star_survived}]"
        return out_str


@dataclass
class LasResult:
    object_hit_report: list[object_hit_report.ObjectHitReport]

    def to_string(self) -> str:
        out_str = "LAS:\n"
        if self.object_hit_report is None or len(self.object_hit_report) == 0:
            out_str += "No Enemies"
        else:
            for ohr in self.object_hit_report:
                out_str += f"object hit report\t object=[{ohr.object_hit}]\tUnit=[{ohr.unit_hit}]"
                out_str += f"\tcoord=[{ohr.coord.to_string()}]\tMissed=[{ohr.missed}]"
                out_str += (
                    f"\tDestroyed=[{ohr.destroyed}]\tShieldRemaining=[{ohr.shield_remaining}]"
                )
                out_str += f"\tStarSurvived=[{ohr.star_survived}]\n"
        return out_str


@dataclass
class NavResult:
    nav_message: nav_message.NavMessage
    distance_traveled: float

    def to_string(self) -> str:
        out_str = "NAV:\n"
        out_str += f"NavMessage: [{self.nav_message}] "
        out_str += f"DistanceTraveled: [{self.distance_traveled}] \n"
        return out_str


@dataclass
class MaintResult:
    new_mission_time: float
    devices_repair_status_changed: list[device.Device]
    enemies_fired: list[enemy_fired.EnemyFired]
    enemies_moved: list[enemy_moved.EnemyMoved]
    docking_status: docking_status.DockingStatus
    starbase_repairs_available: starbase_repairs.StarbaseRepairs | None
    game_status: game_status.GameStatus


class Result:
    srs: SrsResult
    lrs: LrsResult
    com_rec: ComRecResult
    com_sta: ComStaResult
    com_stb: ComStbResult
    com_tor: ComTorResult
    com_nav: ComNavResult
    dam: DamResult
    she: SheResult
    tor: TorResult
    las: LasResult
    nav: NavResult
    maint_result: MaintResult
    command: commands.Commands
    command_result: command_result.CommandResult
