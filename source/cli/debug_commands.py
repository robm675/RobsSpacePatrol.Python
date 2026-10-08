import sys

import gbl
from cli import cli_messages
from game.game import Game
from models.coord import Coord
from models.quadrant import Quadrant
from models.sector import Sector


class DebugCommands:
    game: Game

    def __init__(self, game: Game):
        self.game = game

    def debug_menu(self) -> str:
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

    def run_debug_command(self, commands: list[str]) -> str:
        if len(commands) < 2:
            return cli_messages.DEBUG_ERROR_IN_COMMAND + "\n" + self.debug_menu()

        commands = [cmd.upper() for cmd in commands]

        match commands[1]:
            case "SET":
                return self.run_set_debug(commands)
            case "GET":
                return self.run_get_debug(commands)
            case "CHECK":
                return cli_messages.DEBUG_COMMAND_OK
            case _:
                return cli_messages.DEBUG_UNKNOWN_COMMAND

    def str2int(self, string: str) -> int | None:
        try:
            x_int = int(string)
        except ValueError:
            return None
        return x_int

    def str2float(self, string: str) -> float | None:
        try:
            x_float = float(string)
        except ValueError:
            return None
        return x_float

    def get_coord_by_xy(self, x: str, y: str) -> Coord | None:
        x_int = -1
        y_int = -1
        try:
            x_int = int(x)
        except ValueError:
            return None

        try:
            y_int = int(y)
        except ValueError:
            return None

        return Coord(x_int, y_int)

    def get_coord_by_coord(self, coord: Coord) -> str:
        return f"{coord.x}.{coord.y}"

    def get_sector(self, x: str, y: str) -> Sector | None:
        coord = self.get_coord_by_xy(x, y)
        if coord is None:
            return None
        target_sector = self.game.galaxy.current_quadrant.get_sector_by_coord(coord)
        return target_sector

    def get_quadrant(self, x: str, y: str) -> Quadrant | None:
        coord = self.get_coord_by_xy(x, y)
        if coord is None:
            return None
        target_quadrant = self.game.galaxy.get_quadrant_by_coord(coord)
        return target_quadrant

    def result(self, result: bool) -> str:
        if result:
            return cli_messages.DEBUG_ERROR_IN_COMMAND
        else:
            return cli_messages.DEBUG_COMMAND_OK

    def result_with_parm(self, result: bool, msg: str) -> str:
        if result:
            return cli_messages.DEBUG_ERROR_IN_COMMAND
        else:
            return msg

    def run_get_debug(self, commands: list[str]) -> str:
        if len(commands) < 3:
            return cli_messages.DEBUG_INVALID_COMMAND

        match commands[2]:
            case "CURRENTQUADRANT":
                if len(commands) < 4:
                    return cli_messages.DEBUG_INVALID_COMMAND
                match commands[3]:
                    case "SECTOR":
                        return self.get_sector_contents(commands)
                    case "ENEMY":
                        return self.get_sector_enemy(commands)
                    case _:
                        return cli_messages.DEBUG_INVALID_COMMAND
            case "QUADRANT":
                return self.get_quadrant_contents(commands)
            case "STARSHIP":
                return self.get_starship(commands)
            case "GALAXY":
                return self.get_galaxy(commands)
            case _:
                return cli_messages.DEBUG_INVALID_COMMAND

    def run_set_debug(self, commands: list[str]) -> str:
        if len(commands) < 3:
            return cli_messages.DEBUG_INVALID_COMMAND

        match commands[2]:
            case "PREVENTENEMYFIRE":
                match commands[3]:
                    case "ON":
                        self.game.prevent_enemy_fire = True
                        return self.result(False)
                    case "OFF":
                        self.game.prevent_enemy_fire = False
                        return self.result(False)
                    case _:
                        return cli_messages.DEBUG_INVALID_COMMAND
            case "ENEMYMOVE":
                match commands[3]:
                    case "ON":
                        self.game.skip_enemy_move = False
                        self.game.force_enemy_move = False
                        return self.result(False)
                    case "OFF":
                        self.game.skip_enemy_move = True
                        self.game.force_enemy_move = False
                        return self.result(False)
                    case "FORCE":
                        self.game.skip_enemy_move = False
                        self.game.force_enemy_move = True
                        return self.result(False)
                    case _:
                        return cli_messages.DEBUG_INVALID_COMMAND
            case "CURRENTQUADRANT":
                if len(commands) < 4:
                    return cli_messages.DEBUG_INVALID_COMMAND
                match commands[3]:
                    case "SECTOR":
                        return self.set_sector_contents(commands)
                    case "ENEMY":
                        return self.set_sector_enemy(commands)
                    case _:
                        return cli_messages.DEBUG_INVALID_COMMAND
            case "QUADRANT":
                return self.set_quadrant_contents(commands)
            case "STARSHIP":
                return self.set_starship(commands)
            case "GALAXY":
                return self.set_galaxy(commands)
            case "CLEARCQ":
                all_sw = False
                if len(commands) > 3 and commands[3] == "ALL":
                    all_sw = True

                for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                    for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
                        coord = Coord(x, y)
                        target_sector = self.game.galaxy.current_quadrant.get_sector_by_coord(coord)
                        if all_sw:
                            target_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY
                        else:
                            if target_sector.sector_contents.sector_contents != gbl.SECTOR_STARSHIP:
                                target_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY

                non_empty_sectors = self.game.galaxy.current_quadrant.get_sectors_not_empty()
                if all_sw and len(non_empty_sectors) != 0:
                    raise RuntimeError("Error - Current Quadrant was not cleared correctly")
                if not all_sw and len(non_empty_sectors) != 1:
                    print(
                        f"allSw={all_sw} len(nonEmptySectors)={len(non_empty_sectors)}",
                        file=sys.stderr,
                    )
                    raise RuntimeError("Error - Current Quadrant was not cleared correctly")

            case _:
                return cli_messages.DEBUG_INVALID_COMMAND
        return "**ERROR**"

    def set_sector_contents(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return cli_messages.DEBUG_INVALID_COMMAND
        target_sector = self.get_sector(commands[4], commands[5])
        if target_sector is None:
            raise RuntimeError("TargetSector is None")
        target_sector.sector_contents.sector_contents = commands[6].upper().strip()
        return self.result(True)

    def get_sector_contents(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return self.result(True)
        target_sector = self.get_sector(commands[4], commands[5])
        if target_sector is None:
            raise RuntimeError("TargetSector is None")
        return self.result_with_parm(False, target_sector.sector_contents.sector_contents)

    def set_sector_enemy(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return cli_messages.DEBUG_INVALID_COMMAND
        target_sector = self.get_sector(commands[4], commands[5])
        if target_sector is None:
            return cli_messages.DEBUG_INVALID_COMMAND
        shield_level = self.str2int(commands[6])
        if shield_level is None:
            return cli_messages.DEBUG_INVALID_COMMAND
        target_sector.set_enemy(shield_level)
        return self.result(True)

    def get_sector_enemy(self, commands: list[str]) -> str:
        if len(commands) < 6:
            return self.result(True)
        target_sector = self.get_sector(commands[4], commands[5])
        if target_sector is None:
            return cli_messages.DEBUG_INVALID_COMMAND
        if target_sector.enemy is None:
            return cli_messages.DEBUG_INVALID_COMMAND
        return self.result_with_parm(False, f"ENEMY:{target_sector.enemy.shield_level}")

    def get_quadrant_contents(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return cli_messages.DEBUG_INVALID_COMMAND

        quadrant = self.get_quadrant(commands[3], commands[4])
        if quadrant is None:
            return self.result(True)

        match commands[5]:
            case "NUMENEMIES":
                return self.result_with_parm(False, str(quadrant.num_enemies))
            case "NUMSTARS":
                return self.result_with_parm(False, str(quadrant.num_stars))
            case "STARBASE":
                if quadrant.has_star_base:
                    return self.result_with_parm(False, "1")
                else:
                    return self.result_with_parm(False, "0")
            case "EXPLORED":
                if quadrant.has_been_explored:
                    return self.result_with_parm(False, "1")
                else:
                    return self.result_with_parm(False, "0")
            case _:
                return cli_messages.DEBUG_INVALID_COMMAND

    def set_quadrant_contents(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return cli_messages.DEBUG_INVALID_COMMAND

        quadrant = self.get_quadrant(commands[3], commands[4])
        if quadrant is None:
            return self.result(True)

        value = self.str2int(commands[6])
        if value is None:
            return self.result(True)

        match commands[5]:
            case "NUMENEMIES":
                quadrant.num_enemies = value
                return self.result(False)
            case "NUMSTARS":
                quadrant.num_stars = value
                return self.result(False)
            case "STARBASE":
                if value == 1:
                    quadrant.has_star_base = True
                else:
                    quadrant.has_star_base = False
                return self.result(False)
            case "EXPLORED":
                if value == 1:
                    quadrant.has_been_explored = True
                else:
                    quadrant.has_been_explored = False
                return self.result(False)
            case _:
                return cli_messages.DEBUG_INVALID_COMMAND

    def get_starship(self, commands: list[str]) -> str:
        if len(commands) < 4:
            return cli_messages.DEBUG_INVALID_COMMAND

        match commands[3]:
            case "ENERGY":
                value = self.game.galaxy.starship.energy_level
                return self.result_with_parm(False, str(value))
            case "SHIELD":
                value = self.game.galaxy.starship.shield_level
                return self.result_with_parm(False, str(value))
            case "TORP":
                value = self.game.galaxy.starship.torps_remain
                return self.result_with_parm(False, str(value))
            case "DEVICE":
                dev = self.game.galaxy.starship.get_device_by_str(commands[4])
                return self.result_with_parm(False, str(round(dev.damage_level, 1)))
            case "SECTOR":
                value = self.game.galaxy.get_starship_sector()
                return self.result_with_parm(False, self.get_coord_by_coord(value.coord))
            case "QUADRANT":
                value = self.game.galaxy.get_starship_quadrant()
                return self.result_with_parm(False, self.get_coord_by_coord(value.coord))
            case _:
                return cli_messages.DEBUG_INVALID_COMMAND

    def set_starship(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return cli_messages.DEBUG_INVALID_COMMAND

        match commands[3]:
            case "ENERGY":
                value = self.str2int(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.starship.energy_level = value
                return self.result(False)
            case "SHIELD":
                value = self.str2int(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.starship.shield_level = value
                return self.result(False)
            case "TORP":
                value = self.str2int(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.starship.torps_remain = value
                return self.result(False)
            case "DEVICE":
                dev = self.game.galaxy.starship.get_device_by_str(commands[4])
                dam_temp = self.str2float(commands[5])
                if dam_temp is None:
                    return self.result(True)
                dev.damage_level = dam_temp
                return self.result(False)
            case "SECTOR":
                temp_coord = self.get_coord_by_xy(commands[4], commands[5])
                if temp_coord is None:
                    return self.result(True)
                ent_sector = self.game.galaxy.get_starship_sector()
                self.game.move_object_inside_quadrant(ent_sector.coord, temp_coord)
                return self.result(False)
            case "QUADRANT":
                ent_sector = self.game.galaxy.get_starship_sector()
                quadrant = self.get_quadrant(commands[4], commands[5])
                if quadrant is None:
                    return self.result(True)
                self.game.move_starship_quadrant(quadrant, ent_sector.coord)
                return self.result(False)
            case _:
                return cli_messages.DEBUG_INVALID_COMMAND

    def get_galaxy(self, commands: list[str]) -> str:
        if len(commands) < 4:
            return cli_messages.DEBUG_INVALID_COMMAND

        match commands[3]:
            case "MISSION_TIME":
                sd = self.game.galaxy.mission_time
                return self.result_with_parm(False, str(round(sd, 1)))
            case "MISSIONTIMEDEADLINE":
                sd = self.game.galaxy.mission_time_deadline
                return self.result_with_parm(False, str(round(sd, 1)))
        return "**ERROR**"

    def set_galaxy(self, commands: list[str]) -> str:
        if len(commands) < 5:
            return cli_messages.DEBUG_INVALID_COMMAND

        match commands[3]:
            case "MISSION_TIME":
                value = self.str2float(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.mission_time = value
                return self.result(False)
            case "MISSIONTIMEDEADLINE":
                value = self.str2float(commands[4])
                if value is None:
                    return self.result(True)
                self.game.galaxy.mission_time_deadline = value
                return self.result(False)

        return "**ERROR**"
