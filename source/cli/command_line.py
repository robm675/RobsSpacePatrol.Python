import gbl
from cli import cli_messages, debug_commands
from game.game import Game
from models import object_hit
from models.command_result import CommandResult
from models.coord import Coord
from models.game_status import GameStatus
from models.nav_message import NavMessage
from models.quadrant import Quadrant
from models.sector import Sector
from utils.calculation_utilities import CalculationUtils


class CommandLine:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.debug = debug_commands.DebugCommands(game)

    new_quadrant: bool = False
    game_over: bool = False

    def execute_command_string(self, command: str) -> str:
        for char in "[],=:":
            command = command.replace(char, " ")

        if command.strip() == "":
            return ""

        commands = command.split()

        active_command = commands[0].upper().strip()
        match active_command:
            case "DEBUG":
                return self.debug.run_debug_command(commands)
            case "SRS":
                return self.run_srs()
            case "LRS":
                return self.run_lrs()
            case "SHE":
                return self.run_she(commands)
            case "LAS":
                return self.run_las(commands)
            case "TOR":
                return self.run_tor(commands)
            case "COM":
                return self.run_com(commands)
            case "NAV":
                return self.run_nav(commands)
            case "DAM":
                return self.run_dam()
            case _:
                out_str = ""
                if active_command == "":
                    out_str += cli_messages.UNKNOWN_COMMAND + "\n"
                    out_str += self.show_help_main() + "\n"
                return out_str + self.get_routine_maint(0, True)

        return "**ERROR**"

    def intro_message(self) -> str:
        out_msg = ""
        com_sta = self.game.com_sta()

        total_mission_time = com_sta.com_sta.mission_time_deadline - com_sta.com_sta.mission_time

        out_msg += "Hello Captain!\n"
        out_msg += "\n"
        out_msg += f"Mission: Destroy {com_sta.com_sta.enemies_remaining} enemies in less than {total_mission_time!s} mission time units.\n"
        out_msg += "\n"
        out_msg += "Good luck!\n"

        enemy_sectors = self.game.galaxy.current_quadrant.get_enemy_sectors()

        if enemy_sectors is not None and len(enemy_sectors) > 0:
            out_msg += "\n"
            out_msg += "\n"
            out_msg += cli_messages.WARNING_MESSAGE_SHIELD_DOWN_IN_COMBAT_AREA + "\n"

        return out_msg

    def show_help_main(self) -> str:
        str_out = ""

        str_out += "The following is a list of the available command along with their function\n"
        str_out += "\n"
        str_out += "NAV <direction> <distance> - Moves the starship in the specified direction and distance.  Enter without parameters to view the direction guide. \n"
        str_out += "SRS - Displays the current sector in a graphical format \n"
        str_out += "LRS - Displays the neighboring quadrants in a graphical format\n"
        str_out += "SHE <amount> - Set shield level.  Set to 0 to drop shields \n"
        str_out += "LAS <amount> - Fires the lasers at the specified amount, which is divided between each of the enemies in the current quadrant, it also will reduce the further the enemy is \n"
        str_out += "TOR <direction> - Fires the torpedos in a given direction, give the command without any parameters for the direction guide \n"
        str_out += "COM REC - Displays the galaxy in a graphical format showing the quadrants contents, any unexplored quadrants will be hidden \n"
        str_out += "COM STA - Displays the current status \n"
        str_out += (
            "COM TOR - Calculates the directions to each of the enemies in the current quadrant \n"
        )
        str_out += "COM STB - Calculates the direction and distance to the starbase in the current quadrant \n"
        str_out += "COM NAV <quadrant-x> <quadrant-y> <sector-x> <sector-y> - Calculates the direction and distance from your position to the given quadrant and sector coordinates \n"
        str_out += "DAM - Displays all of the damaged devices as well as the amount of Mission Time before it's repaired. \n"
        str_out += "QUIT / EXIT - Exit the game. \n"
        str_out += "\n"

        return str_out

    def show_help_navtor(self, is_nav: bool) -> str:
        str_out = ""

        str_out += "\n"
        str_out += "Direction:\n\n"
        str_out += "  4    3    2\n"
        str_out += "   `.  :  .'\n"
        str_out += "     `.:.'\n"
        str_out += "  5---<*>---1\n"
        str_out += "     .':'.\n"
        str_out += "   .'  :  '.\n"
        str_out += "  6    7    8\n"

        if is_nav:
            str_out += "\n"
            str_out += "Warp speed is 1 to 8, impulse power is 0.1 to 0.9"

        return str_out

    def get_srs_formatted(self, sectors: list[Sector]) -> str:
        out_string = ""
        for y in range(-1, gbl.MAX_QUADRANT_SECTOR_XY):
            if y == -1:
                out_string += "###\t\t"
            else:
                out_string += f"{y}\t\t"
        out_string += "\n"

        for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
            out_row_string = ""
            for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                data = [s for s in sectors if s.coord.x == x and s.coord.y == y]
                out_row_string += self.get_sector_formatted(data[0]) + "\t\t"
            out_string += f"{y}\t\t{out_row_string}\n"

        return out_string

    def get_lrs_formatted(self, quadrants: list[Quadrant], ent_qx: int, ent_qy: int) -> str:
        line = "+-----+-----+-----+\n"
        out_str = "  <------- X ------->\n"

        out_str += "^ " + line
        for y in range(ent_qy - 1, ent_qy + 2):
            if y != ent_qy - 1:
                out_str += "| " + line

            if y == ent_qy:
                out_str += "Y "
            else:
                out_str += "| "

            for x in range(ent_qx - 1, ent_qx + 2):
                if (
                    y < 0
                    or y > gbl.MAX_QUADRANT_SECTOR_XY - 1
                    or x < 0
                    or x > gbl.MAX_QUADRANT_SECTOR_XY - 1
                ):
                    out_str += "| *** "
                else:
                    data = [q for q in quadrants if q.coord.x == x and q.coord.y == y]
                    if len(data) == 0:
                        raise RuntimeError(f"In getLRSFormatted - NotFound x={x} y={y}")
                    out_str += self.get_quadrant_for_galaxy_formatted(data[0], False)
            out_str += "|\n"
        out_str += "v " + line
        return out_str

    def get_quadrant_for_galaxy_formatted(self, quadrant: Quadrant | None, mark_starship: bool):
        if quadrant is None:
            return "***"
        if not quadrant.has_been_explored:
            return "| *** "
        ent_marker_start = " "
        ent_marker_end = " "

        if mark_starship:
            ent_marker_start = ">"
            ent_marker_end = "<"

        outstr = ""
        outstr += "|" + ent_marker_start
        outstr += str(quadrant.num_enemies)
        if quadrant.has_star_base:
            outstr += "1"
        else:
            outstr += "0"

        outstr += str(quadrant.num_stars)
        outstr += ent_marker_end
        return outstr

    def get_sector_formatted(self, sector: Sector) -> str:
        match sector.sector_contents.sector_contents:
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

    def get_galaxy_formatted(self) -> str:
        x_header = "  <-----------------------X----------------------->\n"
        line = "+-----+-----+-----+-----+-----+-----+-----+-----+\n"

        out_str = x_header
        for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
            match y:
                case 0:
                    out_str += "^"
                case 4:
                    out_str += "Y"
                case _:
                    out_str += "|"

            out_str += " " + line
            out_str += "| "

            for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                quad = self.game.galaxy.get_quadrant(x, y)
                if (
                    quad.coord.x == self.game.galaxy.current_quadrant.coord.x
                    and quad.coord.y == self.game.galaxy.current_quadrant.coord.y
                ):
                    out_str += self.get_quadrant_for_galaxy_formatted(quad, True)
                else:
                    out_str += self.get_quadrant_for_galaxy_formatted(quad, False)
            out_str += "|\n"

        out_str += "v " + line
        return out_str

    def get_routine_maint(self, mission_time: float, enemies_fire: bool):
        res = self.game.routine_maint(mission_time, enemies_fire)
        data = res.maint_result
        if data is None:
            return cli_messages.INTERNAL_ERROR_MESSAGE
        if data.docking_status is None:
            return cli_messages.INTERNAL_ERROR_MESSAGE

        out_string = "\n"

        if data.game_status != GameStatus.NORMAL:
            self.game_over = True
            match data.game_status:
                case GameStatus.STARSHIP_DESTROYED:
                    return cli_messages.END_MISSION_FAILED_STARSHIP_DESTROYED
                case GameStatus.RAN_OUT_OF_ENERGY:
                    return cli_messages.END_MISSION_FAILED_RAN_OUT_OF_ENERGY
                case GameStatus.RAN_OUT_OF_TIME:
                    return cli_messages.END_MISSION_FAILED_RAN_OUT_OF_TIME
                case GameStatus.OUT_OF_ENERGY_SHIELD_ENERGY_AVAILABLE:
                    out_string += cli_messages.END_ENERGY_GONE_SHIELD_ENERGY_AVAIL
                case GameStatus.MISSION_OVER:
                    return "\n" + cli_messages.END_MISSION_ACCOMPLISHED
                case _:
                    return cli_messages.INTERNAL_ERROR_MESSAGE

        if not data.docking_status.previous_status and data.docking_status.current_status:
            out_string += cli_messages.MAINT_DOCKED + "\n"

        if data.starbase_repairs_available is not None:
            out_string += cli_messages.MAINT_TECH_WAITING + cli_messages.MAINT_IT_WILL_TAKE
            out_string += str(abs(data.starbase_repairs_available.mission_time_to_repair))
            out_string += cli_messages.MAINT_MISSION_TIME + "\n"
            out_string += cli_messages.MAINT_REPLY_YES

        if len(data.devices_repair_status_changed) > 0:
            for device in data.devices_repair_status_changed:
                if device.damage_level == 100:
                    out_string += cli_messages.MAINT_REPAIRS_COMPLETE + device.name + "\n"
                    device.damage_level = 0

        starship_destroyed_message_sent = False

        if len(data.enemies_moved) != 0:
            for enemy in data.enemies_moved:
                outline = ""
                msg = cli_messages.MAINT_ENEMY_MOVED.format(
                    enemy.enemy_coord_orig.to_string(), enemy.enemy_coord_dest.to_string()
                )
                outline += msg
                out_string += "\n" + outline

        if data.enemies_fired is not None:
            outline = ""
            for enemy_fired in data.enemies_fired:
                if starship_destroyed_message_sent:
                    continue
                if outline.strip():
                    outline += "\n"

                if not data.docking_status.current_status:
                    if enemy_fired.starship_destroyed:
                        outline += cli_messages.MAINT_ENEMY_FIRED_STARSHIP_DESTROYED.format(
                            enemy_fired.enemy_fired_amount,
                            enemy_fired.enemy_coord.to_string(),
                            enemy_fired.starship_new_shield_amount,
                        )
                        starship_destroyed_message_sent = True
                    else:
                        outline += cli_messages.MAINT_ENEMY_FIRED_SHIELD_HIT.format(
                            str(enemy_fired.enemy_fired_amount),
                            enemy_fired.enemy_coord.to_string(),
                            str(enemy_fired.starship_new_shield_amount),
                        )
                        if (
                            enemy_fired.device_damaged is not None
                            and enemy_fired.device_damaged_amount is not None
                        ):
                            outline += (
                                "\n"
                                + enemy_fired.device_damaged.name
                                + cli_messages.MAINT_DEVICE_DAMAGED
                                + str(round(abs(enemy_fired.device_damaged_amount), 1))
                                + cli_messages.MAINT_MISSION_TIME_TO_REPAIR
                            )
                else:
                    outline += (
                        cli_messages.MAINT_ENEMY_FIRED_PROTECTED.format(
                            enemy_fired.enemy_fired_amount, enemy_fired.enemy_coord.to_string()
                        )
                        + cli_messages.MAINT_STARBASE_SHIELDS_PROTECTED
                    )

            out_string += "\n" + outline

        enemy_list = self.game.galaxy.current_quadrant.get_enemy_sectors()
        if not data.docking_status.current_status and not starship_destroyed_message_sent:
            shield_level = self.game.galaxy.starship.shield_level
            if shield_level < 50 and enemy_list is not None and len(enemy_list) > 0:
                out_string += "\n" + cli_messages.WARNING_MESSAGE_SHIELD_DOWN_IN_COMBAT_AREA

        if enemy_list is not None and len(enemy_list) > 0 and self.new_quadrant:
            out_string += "\n" + cli_messages.MAINT_NEW_QUADRANT_ENEMIES_RED_ALERT

        return out_string

    def run_srs(self) -> str:
        result = self.game.srs()
        if result.command_result == CommandResult.DAMAGED:
            return cli_messages.SRS_DAMAGED
        return self.get_srs_formatted(result.srs.sectors) + self.get_routine_maint(0.1, True)

    def run_lrs(self) -> str:
        result = self.game.lrs()
        if result.command_result == CommandResult.DAMAGED:
            return cli_messages.LRS_DAMAGED
        cq_coord = self.game.galaxy.current_quadrant.coord
        return self.get_lrs_formatted(
            result.lrs.quadrants, cq_coord.x, cq_coord.y
        ) + self.get_routine_maint(0.1, True)

    def run_she(self, commands: list[str]) -> str:
        if len(commands) == 1:
            return cli_messages.SHE_MISSING_AMOUNT

        she_int = self.game.str2int(commands[1])
        if she_int is None:
            return cli_messages.SHE_INVALID_AMOUNT

        if she_int < 0:
            return cli_messages.SHE_INVALID_AMOUNT

        result = self.game.she(she_int)
        if result.command_result == CommandResult.DAMAGED:
            return cli_messages.SHE_DAMAGED

        if result.command_result == CommandResult.ERROR:
            return cli_messages.SHE_INVALID_AMOUNT + str(she_int) + "\n" + result.she.error_message

        return cli_messages.SHE_CHANGED + str(she_int) + self.get_routine_maint(0.1, True)

    def run_las(self, commands: list[str]) -> str:
        if len(commands) == 1:
            return cli_messages.LAS_MISSING_AMOUNT

        las_amount = self.game.str2int(commands[1])
        if las_amount is None:
            return cli_messages.LAS_INVALID_AMOUNT

        if las_amount <= 0:
            return cli_messages.LAS_INVALID_AMOUNT

        res = self.game.las(las_amount)

        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.LAS_DAMAGED

        if res.command_result == CommandResult.NO_ENEMIES_PRESENT:
            return cli_messages.LAS_NO_ENEMIES

        if res.command_result == CommandResult.INSUFFICIENT_INVENTORY:
            return cli_messages.LAS_INSUFFICIENT_ENERGY

        out_msg = ""
        if res.command_result == CommandResult.OK:
            for obj_hit in res.las.object_hit_report:
                obj_hit_coord = obj_hit.coord.to_string()

                if out_msg == "":
                    out_msg += "\n"

                out_msg += (
                    cli_messages.LAS_FIRED
                    + str(obj_hit.unit_hit)
                    + cli_messages.LAS_HIT
                    + obj_hit_coord
                )

                if obj_hit.destroyed:
                    out_msg += cli_messages.LAS_ENEMY_DESTROYED
                else:
                    out_msg += (
                        cli_messages.LAS_SENSORS_INDICATE
                        + str(obj_hit.shield_remaining)
                        + cli_messages.LAS_REMAINING
                    )

        return out_msg + self.get_routine_maint(0.1, True)

    def run_tor(self, commands: list[str]) -> str:
        if len(commands) == 1:
            return cli_messages.TOR_MISSING_DIRECTION

        tor_dir = self.game.str2float(commands[1])
        if tor_dir is None:
            return cli_messages.TOR_INVALID_DIRECTION

        if tor_dir < 0 or tor_dir >= 9:
            return cli_messages.TOR_INVALID_DIRECTION + self.show_help_navtor(False)

        res = self.game.tor(tor_dir)

        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.TOR_DAMAGED

        if res.command_result == CommandResult.NO_ENEMIES_PRESENT:
            return cli_messages.TOR_NO_ENEMIES

        if res.command_result == CommandResult.INSUFFICIENT_INVENTORY:
            return cli_messages.TOR_EXPENDED

        if res.command_result == CommandResult.TOR_MISSED:
            return cli_messages.TOR_MISSED

        out_msg = ""
        if res.command_result == CommandResult.OK:
            match res.tor.object_hit_report.object_hit:
                case object_hit.ObjectHit.ENEMY:
                    out_msg += (
                        cli_messages.TOR_FIRED
                        + cli_messages.TOR_ENEMY_AT_SECTOR
                        + res.tor.object_hit_report.coord.to_string()
                        + cli_messages.TOR_DESTROYED
                    )
                case object_hit.ObjectHit.STAR:
                    if res.tor.object_hit_report.destroyed:
                        out_msg += cli_messages.TOR_FIRED + cli_messages.TOR_STAR_DESTROYED
                    else:
                        out_msg += cli_messages.TOR_FIRED + cli_messages.TOR_STAR_ABSORBED_TORP
                case object_hit.ObjectHit.STARBASE:
                    out_msg += cli_messages.TOR_FIRED + cli_messages.TOR_STARBASE_DESTROYED
                case _:
                    return cli_messages.INTERNAL_ERROR_MESSAGE

        return out_msg + self.get_routine_maint(0.1, True)

    def run_com(self, commands: list[str]) -> str:
        if len(commands) < 2:
            return cli_messages.CPU_INVALID_COMMAND

        match commands[1].upper():
            case "REC":
                return self.run_com_rec()
            case "TOR":
                return self.run_com_tor()
            case "NAV":
                return self.run_com_nav(commands)
            case "STB":
                return self.run_com_stb()
            case "STA":
                return self.run_com_sta()
            case _:
                return cli_messages.CPU_INVALID_COMMAND

    def run_com_rec(self) -> str:
        res = self.game.com_rec()
        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.CPU_DAMAGED

        return self.get_galaxy_formatted()

    def run_com_tor(self) -> str:
        res = self.game.com_tor()
        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.CPU_DAMAGED
        if res.command_result == CommandResult.NO_ENEMIES_PRESENT:
            return cli_messages.CPU_TOR_NO_ENEMIES

        out_str = ""
        for dte in res.com_tor.direction_to_enemies:
            if out_str == "":
                out_str += "\n"

            out_str += (
                cli_messages.CPU_TOR_ENEMY_AT_SECTOR
                + dte.coord.to_string()
                + cli_messages.CPU_TOR_IS_BEARING
                + str(round(dte.direction, 1))
            )

        return out_str

    def run_com_nav(self, commands: list[str]) -> str:

        if len(commands) != 6:
            return cli_messages.CPU_NAV_INVALID

        qx = self.game.str2int(commands[2])
        if qx is None:
            return cli_messages.CPU_NAV_INVALID_COORD
        if qx < 0 or qx > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return cli_messages.CPU_NAV_INVALID_QX

        qy = self.game.str2int(commands[3])
        if qy is None:
            return cli_messages.CPU_NAV_INVALID_COORD
        if qy < 0 or qy > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return cli_messages.CPU_NAV_INVALID_QY

        sx = self.game.str2int(commands[4])
        if sx is None:
            return cli_messages.CPU_NAV_INVALID_COORD
        if sx < 0 or sx > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return cli_messages.CPU_NAV_INVALID_SX

        sy = self.game.str2int(commands[5])
        if sy is None:
            return cli_messages.CPU_NAV_INVALID_COORD
        if sy < 0 or sy > gbl.MAX_QUADRANT_SECTOR_XY - 1:
            return cli_messages.CPU_NAV_INVALID_SY

        res = self.game.com_nav(Coord(qx, qy), Coord(sx, sy))
        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.CPU_DAMAGED

        return (
            cli_messages.CPU_NAV_DIR
            + str(round(res.com_nav.direction, 1))
            + cli_messages.CPU_NAV_DIST
            + str(round(res.com_nav.distance, 1))
        )

    def run_com_stb(self) -> str:
        res = self.game.com_stb()
        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.CPU_DAMAGED

        if res.command_result == CommandResult.CPU_STB_NO_STARBASE_PRESENT:
            return cli_messages.CPU_STB_NO_STARBASES

        out_str = ""
        out_str += cli_messages.CPU_STB_STARBASE_FOUND_IN_SECTOR
        out_str += cli_messages.CPU_STB_DIR
        out_str += str(round(res.com_stb.direction, 1))
        out_str += cli_messages.CPU_STB_DIST
        out_str += str(round(res.com_stb.distance, 1))

        return out_str

    def run_com_sta(self) -> str:
        res = self.game.com_sta()
        if res.command_result == CommandResult.DAMAGED:
            return cli_messages.CPU_DAMAGED

        out_str = ""

        out_str += (
            cli_messages.CPU_STA_MISSION_TIME + str(round(res.com_sta.mission_time, 1)) + "\n"
        )
        out_str += cli_messages.CPU_STA_QUADRANT + res.com_sta.quadrant_coord.to_string() + "\n"
        out_str += cli_messages.CPU_STA_SECTOR + res.com_sta.sector_coord.to_string() + "\n"
        out_str += cli_messages.CPU_STA_DEVICE_STATUS + "\n"
        for device in self.game.galaxy.starship.devices:
            msg = ""
            if device.damage_level < 0:
                msg += (
                    "Damaged - " + str(abs(round(device.damage_level, 1))) + " mission time units"
                )
            else:
                msg += "Fully functional"
            out_str += "\t" + device.name.ljust(30) + msg + "\n"
        out_str += (
            cli_messages.CPU_STA_ENEMIES_REMAINING + str(res.com_sta.enemies_remaining) + "\n"
        )
        out_str += (
            cli_messages.CPU_STA_STARBASES_REMAINING + str(res.com_sta.starbases_remaining) + "\n"
        )
        out_str += cli_messages.CPU_STA_ENERGY_REMAINING + str(res.com_sta.energy_remaining) + "\n"
        out_str += cli_messages.CPU_STA_SHIELD_LEVEL + str(res.com_sta.shield_level) + "\n"
        out_str += cli_messages.CPU_STA_TORP_REMAINING + str(res.com_sta.torps_remaining) + "\n"
        out_str += cli_messages.CPU_STA_DOCKED
        if res.com_sta.docked:
            out_str += "Docked"
        else:
            out_str += "Not docked"
        out_str += "\n"
        out_str += (
            cli_messages.CPU_STA_MISSION_TIME_REMAINING
            + str(round(res.com_sta.mission_time_deadline - res.com_sta.mission_time, 1))
            + "\n"
        )

        return out_str

    def run_nav(self, commands: list[str]) -> str:
        if len(commands) != 3:
            return cli_messages.NAV_INVALID_COMMAND

        dir = self.game.str2float(commands[1])
        if dir is None:
            return cli_messages.NAV_INVALID_DIR + commands[1]
        if dir < 0 or dir >= 9:
            return cli_messages.NAV_INVALID_DIR + str(dir) + self.show_help_navtor(True)

        dist = self.game.str2float(commands[2])
        if dist is None:
            return cli_messages.NAV_INVALID_DIST + commands[2]
        if dist < 0 or dist > 8:
            return cli_messages.NAV_INVALID_DIST + str(round(dist, 1)) + self.show_help_navtor(True)

        before_coord = self.game.galaxy.current_quadrant.coord
        res = self.game.nav(dir, dist)
        after_coord = self.game.galaxy.current_quadrant.coord

        if before_coord.x != after_coord.x or before_coord.y != after_coord.y:
            self.new_quadrant = True

        if res.command_result == CommandResult.DAMAGED and dist > 0.2:
            return cli_messages.NAV_WARP_DRIVE_DAMAGED

        if (
            res.command_result == CommandResult.ERROR
            and res.nav.nav_message == NavMessage.INSUFFICIENT_ENERGY_SHIELD_ENERGY_AVAILABLE
        ):
            return cli_messages.NAV_NOT_ENOUGH_ENERGY_SHIELD_ENERGY_AVAIL

        if (
            res.command_result == CommandResult.ERROR
            and res.nav.nav_message == NavMessage.BAD_INPUT_OUTSIDE_GALAXY
        ):
            return cli_messages.NAV_OUTSIDE_GALAXY

        if (
            res.command_result == CommandResult.ERROR
            and res.nav.nav_message == NavMessage.BAD_INPUT_OBJECT_HIT
        ):
            return (
                cli_messages.NAV_IMPULSE_ENGINE_SHUT_DOWN
                + self.game.galaxy.get_starship_sector().coord.to_string()
                + cli_messages.NAV_BAD_NAVIGATION
            )

        time_traveled = CalculationUtils.distance2_time(res.nav.distance_traveled)
        if res.command_result == CommandResult.OK and dist < 1:
            return cli_messages.NAV_IMPULSE_ENGAGED + self.get_routine_maint(time_traveled, False)
        else:
            return cli_messages.NAV_WARP_ENGAGED + self.get_routine_maint(time_traveled, False)

    def run_dam(self) -> str:
        res = self.game.dam()
        if res.command_result != CommandResult.OK:
            return cli_messages.INTERNAL_ERROR_MESSAGE

        out_msg = ""
        out_msg += cli_messages.DAM_DAMAGE_REPORT + "\n"

        for device in res.dam.devices:
            msg = ""
            if device.damage_level < 0:
                msg = "Damaged - " + str(round(device.damage_level, 1))
                msg += " mission time units"
            else:
                msg += "Fully functional"
            out_msg += "\t" + device.name.ljust(30) + msg

        if len(res.dam.devices) == 0:
            out_msg = cli_messages.DAM_DAMAGE_REPORT_NO_DAMAGES

        return out_msg
