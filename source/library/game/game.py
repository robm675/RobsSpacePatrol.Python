import math

import gbl
from factories import current_quadrant_factory, random_factory
from factories.other_factories import OtherFactories
from models import enemy_fired
from models.command_result import CommandResult
from models.commands import Commands
from models.coord import Coord
from models.device import Device
from models.direction_to_enemy import DirectionToEnemy
from models.docking_status import DockingStatus
from models.enemy_fired import EnemyFired
from models.enemy_moved import EnemyMoved
from models.galaxy import Galaxy
from models.game_status import GameStatus
from models.nav_message import NavMessage
from models.object_hit import ObjectHit
from models.object_hit_report import ObjectHitReport
from models.quadrant import Quadrant
from models.result import (
    ComNavResult,
    ComRecResult,
    ComStaResult,
    ComStbResult,
    ComTorResult,
    DamResult,
    LasResult,
    LrsResult,
    MaintResult,
    NavResult,
    Result,
    SheResult,
    SrsResult,
    TorResult,
)
from models.sector import Sector
from models.starbase_repairs import StarbaseRepairs
from models.starship import DeviceType
from utils.calculation_utilities import CalculationUtils
from utils.detect_object import DetectObject


class Game:
    skip_enemy_move: bool
    force_enemy_move: bool
    prevent_enemy_fire: bool = False

    def __init__(
        self,
        galaxy: Galaxy,
        rand_fact: random_factory.RandomFactory,
        current_quad_fact: current_quadrant_factory.CurrentQuadrantFactory,
    ) -> None:
        self.galaxy = galaxy
        self.random_factory = rand_fact
        self.current_quadrant_factory = current_quadrant_factory
        self.skip_enemy_move = False
        self.force_enemy_move = False

    def srs(self) -> Result:
        if self.get_damage_level(DeviceType.SRS) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.SRS
            return res

        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.SRS
        res.srs = SrsResult(self.galaxy.current_quadrant.sectors)
        return res

    def lrs(self) -> Result:
        if self.get_damage_level(DeviceType.LRS) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.LRS
            return res

        lower_x = self.galaxy.current_quadrant.coord.x - gbl.LRS_RANGE
        upper_x = self.galaxy.current_quadrant.coord.x + gbl.LRS_RANGE

        lower_y = self.galaxy.current_quadrant.coord.y - gbl.LRS_RANGE
        upper_y = self.galaxy.current_quadrant.coord.y + gbl.LRS_RANGE

        max_coord = gbl.MAX_QUADRANT_SECTOR_XY - 1

        lower_x = max(0, lower_x)
        upper_x = min(max_coord, upper_x)
        lower_y = max(0, lower_y)
        upper_y = min(max_coord, upper_y)

        quadrants = []
        for x in range(lower_x, upper_x + 1):
            for y in range(lower_y, upper_y + 1):
                quad = self.galaxy.get_quadrant(x, y)
                quad.has_been_explored = True
                quadrants.append(quad)

        result = Result()
        result.lrs = LrsResult(quadrants)
        result.command = Commands.LRS
        result.command_result = CommandResult.OK

        return result

    def com_rec(self) -> Result:
        if self.get_damage_level(DeviceType.COM) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.COM_REC
            return res

        result = Result()
        result.com_rec = ComRecResult(self.galaxy.get_explored_quadrant())
        result.command = Commands.COM_REC
        result.command_result = CommandResult.OK

        return result

    def com_sta(self) -> Result:
        if self.get_damage_level(DeviceType.COM) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.COM_STA
            return res

        mission_time = self.galaxy.mission_time
        quad_coord = self.galaxy.current_quadrant.coord
        ent_sector = self.galaxy.current_quadrant.get_sector_by_contents(gbl.SECTOR_STARSHIP)

        if ent_sector is None:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.COM_STA
            return res

        damaged_devices = self.galaxy.starship.get_damaged_devices()
        enemies_remain = OtherFactories.get_enemies_remaining(self.galaxy)
        starbases_remaing = self.galaxy.get_starbases_remaining()
        energy_remaing = self.galaxy.starship.energy_level
        shield_level = self.galaxy.starship.shield_level
        torp_remain = self.galaxy.starship.torps_remain
        is_docked = self.galaxy.starship.is_docked
        mission_time_deadline = self.galaxy.mission_time_deadline

        comsta = ComStaResult(
            mission_time,
            quad_coord,
            ent_sector.coord,
            damaged_devices,
            enemies_remain,
            starbases_remaing,
            energy_remaing,
            shield_level,
            torp_remain,
            is_docked,
            mission_time_deadline,
        )

        result = Result()
        result.com_sta = comsta
        result.command = Commands.COM_STA
        result.command_result = CommandResult.OK

        return result

    def com_stb(self) -> Result:
        if self.get_damage_level(DeviceType.COM) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.COM_STB
            return res

        starbase_sector = self.galaxy.current_quadrant.get_sector_by_contents(gbl.SECTOR_STARBASE)
        starship_sector = self.galaxy.current_quadrant.get_sector_by_contents(gbl.SECTOR_STARSHIP)

        if starbase_sector is None:
            res = Result()
            res.command_result = CommandResult.CPU_STB_NO_STARBASE_PRESENT
            res.command = Commands.COM_STB
            return res
        if starship_sector is None:
            raise RuntimeError("Starship Sector was none")

        dir = CalculationUtils.get_direction(starship_sector.coord, starbase_sector.coord)
        dist = CalculationUtils.get_distance(starship_sector.coord, starbase_sector.coord)

        res = Result()
        res.com_stb = ComStbResult(dir, dist, starbase_sector.coord)

        res.command_result = CommandResult.OK
        res.command = Commands.COM_STB
        return res

    def com_tor(self) -> Result:
        if self.get_damage_level(DeviceType.COM) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.COM_TOR
            return res

        starship_sector = self.galaxy.current_quadrant.get_sector_by_contents(gbl.SECTOR_STARSHIP)

        enemy_sectors = self.galaxy.current_quadrant.get_enemy_sectors()
        if enemy_sectors is None:
            res = Result()
            res.command_result = CommandResult.NO_ENEMIES_PRESENT
            res.command = Commands.COM_TOR
            return res

        enemy_dir_list = []
        for enemy_sector in enemy_sectors:
            if starship_sector is None:
                raise RuntimeError("Starship Sector was none")

            dir = CalculationUtils.get_direction(starship_sector.coord, enemy_sector.coord)
            dist = CalculationUtils.get_distance(starship_sector.coord, enemy_sector.coord)
            dir_to_enemy = DirectionToEnemy(dir, dist, enemy_sector.coord)
            enemy_dir_list.append(dir_to_enemy)

        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.COM_TOR
        res.com_tor = ComTorResult(enemy_dir_list)
        return res

    def com_nav(self, dest_quadrant: Coord, dest_sector: Coord) -> Result:
        if self.get_damage_level(DeviceType.COM) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.COM_NAV
            return res

        starship_sector = self.galaxy.current_quadrant.get_sector_by_contents(gbl.SECTOR_STARSHIP)
        current_quadrant_coord = self.galaxy.current_quadrant.coord

        if starship_sector is None:
            raise RuntimeError("Starship Sector was none")

        start_ux = CalculationUtils.qs2_univ(current_quadrant_coord.x, starship_sector.coord.x)
        start_uy = CalculationUtils.qs2_univ(current_quadrant_coord.y, starship_sector.coord.y)
        target_ux = CalculationUtils.qs2_univ(dest_quadrant.x, dest_sector.x)
        target_uy = CalculationUtils.qs2_univ(dest_quadrant.y, dest_sector.y)

        dir = CalculationUtils.get_direction(Coord(start_ux, start_uy), Coord(target_ux, target_uy))
        dist = (
            CalculationUtils.get_distance(Coord(start_ux, start_uy), Coord(target_ux, target_uy))
            / 8
        )

        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.COM_NAV
        res.com_nav = ComNavResult(dir, dist)
        return res

    def dam(self) -> Result:
        devices = self.galaxy.starship.get_damaged_devices()
        res = Result()
        if len(devices) == 0:
            res.dam = DamResult([])
        else:
            res.dam = DamResult(devices)
        res.command_result = CommandResult.OK
        res.command = Commands.DAM
        return res

    def she(self, new_shield_level: int) -> Result:
        if self.get_damage_level(DeviceType.SHE) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.SHE
            return res

        if new_shield_level < 0:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.SHE
            data = SheResult(gbl.SHE_INVALIDAMOUNT)
            res.she = data
            return res

        current_energy_level = self.galaxy.starship.energy_level + self.galaxy.starship.shield_level
        if new_shield_level > current_energy_level:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.SHE
            data = SheResult(gbl.SHE_ERRORMESSAGE)
            res.she = data
            return res

        self.galaxy.starship.energy_level = current_energy_level - new_shield_level
        self.galaxy.starship.shield_level = new_shield_level
        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.SHE
        res.she = SheResult("")
        return res

    def tor(self, dir: float) -> Result:
        if self.get_damage_level(DeviceType.TOR) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.TOR
            return res

        enemy_sectors = self.galaxy.current_quadrant.get_enemy_sectors()
        if enemy_sectors is None or len(enemy_sectors) == 0:
            res = Result()
            res.command_result = CommandResult.NO_ENEMIES_PRESENT
            res.command = Commands.TOR
            return res

        if self.galaxy.starship.torps_remain <= 0:
            res = Result()
            res.command_result = CommandResult.INSUFFICIENT_INVENTORY
            res.command = Commands.TOR
            return res

        self.galaxy.starship.use_torpedo()

        starship_sector = self.galaxy.get_starship_sector()
        cfo = DetectObject.detect_object_no_dist(
            self.galaxy.current_quadrant, starship_sector.coord, False, dir
        )

        if cfo.object == gbl.SECTOR_EMPTY:
            res = Result()
            res.command_result = CommandResult.TOR_MISSED
            res.command = Commands.TOR
            return res

        target_sector = self.galaxy.current_quadrant.get_sector_by_coord(cfo.final_coord)
        starship_quadrant = self.galaxy.get_quadrant_by_coord(self.galaxy.current_quadrant.coord)

        if cfo.object == gbl.SECTOR_ENEMY:
            return self.tor_enemy(target_sector, starship_quadrant)

        if cfo.object == gbl.SECTOR_STARBASE:
            return self.tor_starbase(target_sector, starship_quadrant)

        if cfo.object == gbl.SECTOR_STAR:
            return self.tor_star(target_sector, starship_quadrant)

        res = Result()
        res.command_result = CommandResult.ERROR
        res.command = Commands.TOR

        return res

    def tor_enemy(self, target_sector: Sector, ent_quadrant: Quadrant) -> Result:
        target_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY
        target_sector.enemy = None
        ent_quadrant.num_enemies -= 1
        ohr = ObjectHitReport(ObjectHit.ENEMY, True, target_sector.coord, -1, -1, False, False)
        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.TOR
        res.tor = TorResult(ohr)
        return res

    def tor_starbase(self, target_sector: Sector, ent_quadrant: Quadrant) -> Result:
        target_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY
        ent_quadrant.has_star_base = False
        ohr = ObjectHitReport(ObjectHit.STARBASE, True, target_sector.coord, -1, -1, False, False)
        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.TOR
        res.tor = TorResult(ohr)
        return res

    def tor_star(self, target_sector: Sector, ent_quadrant: Quadrant) -> Result:
        rand_chance = self.random_factory.get_random_integer(gbl.RIT_STAR_DESTROYED_CHANCE)
        if rand_chance > gbl.STAR_DESTROYED_CHANCE:
            target_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY
            ent_quadrant.num_stars -= 1
            star_destroyed = True
            star_survived = False
        else:
            star_destroyed = False
            star_survived = True

        ohr = ObjectHitReport(
            ObjectHit.STAR, star_destroyed, target_sector.coord, -1, -1, False, star_survived
        )
        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.TOR
        res.tor = TorResult(ohr)
        return res

    def las(self, energy: int) -> Result:
        if self.get_damage_level(DeviceType.LAS) < 0:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.LAS
            return res

        if energy < 0:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.SHE
            data = SheResult(gbl.LAS_INVALIDAMOUNT)
            res.she = data
            return res

        if self.galaxy.starship.energy_level < energy:
            res = Result()
            res.command_result = CommandResult.INSUFFICIENT_INVENTORY
            res.command = Commands.LAS
            return res

        enemy_sectors = self.galaxy.current_quadrant.get_enemy_sectors()
        if enemy_sectors is None or len(enemy_sectors) == 0:
            res = Result()
            res.command_result = CommandResult.NO_ENEMIES_PRESENT
            res.command = Commands.LAS
            return res

        starship_quadrant = self.galaxy.get_quadrant_by_coord(self.galaxy.current_quadrant.coord)
        starship_sector = self.galaxy.get_starship_sector()
        enemy_hit_reports = []

        self.galaxy.starship.energy_level -= energy

        for enemy_sector in enemy_sectors:
            target_enemy = enemy_sector.enemy

            if target_enemy is None:
                raise RuntimeError(
                    f"Sector {enemy_sector.coord.to_string()} is marked as enemy but has no enemy object"
                )

            if target_enemy.shield_level is None:
                target_enemy.shield_level = 0

            if self.get_damage_level(DeviceType.COM) < 0:
                rand_int = self.random_factory.get_random_integer(gbl.RIT_LASER_MISS_CHANCE)
                if rand_int > gbl.LASER_MISS_CHANCE_CPU_DOWN:
                    ohr = ObjectHitReport(
                        ObjectHit.NOTHING,
                        False,
                        enemy_sector.coord,
                        target_enemy.shield_level,
                        0,
                        True,
                        False,
                    )
                    enemy_hit_reports.append(ohr)
                    continue

            dist_to_enemy = CalculationUtils.get_distance(starship_sector.coord, enemy_sector.coord)
            energy_hit_enemy = CalculationUtils.get_enemy_shield_hit(
                len(enemy_sectors), energy, dist_to_enemy, gbl.SECTOR_TO_ENERGY_CONV
            )
            was_destroyed = self.galaxy.current_quadrant.enemy_hit(
                enemy_sector.coord, energy_hit_enemy
            )
            if was_destroyed:
                enemy_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY
                enemy_sector.enemy = None
                starship_quadrant.num_enemies -= 1
                ohr = ObjectHitReport(ObjectHit.ENEMY, True, enemy_sector.coord, 0, 0, False, False)
                enemy_hit_reports.append(ohr)
                continue
            else:
                ohr = ObjectHitReport(
                    ObjectHit.ENEMY,
                    False,
                    enemy_sector.coord,
                    target_enemy.shield_level,
                    energy_hit_enemy,
                    False,
                    False,
                )
                enemy_hit_reports.append(ohr)
                continue

        res = Result()
        res.las = LasResult(enemy_hit_reports)
        res.command_result = CommandResult.OK
        res.command = Commands.LAS
        return res

    def nav(self, dir: float, dist: float) -> Result:
        dir = round(dir, 1)
        dist = round(dist, 1)

        if dir < 0.1 or dir >= 9:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.NAV
            res.nav = NavResult(NavMessage.INVALID_DIR, -1)
            return res

        if dist < 0.1 or dist > 8:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.NAV
            res.nav = NavResult(NavMessage.INVALID_DIST, -1)
            return res

        if self.get_damage_level(DeviceType.NAV) < 0 and dist > 0.2:
            res = Result()
            res.command_result = CommandResult.DAMAGED
            res.command = Commands.NAV
            return res

        starship_quadrant = self.galaxy.get_quadrant_by_coord(self.galaxy.current_quadrant.coord)
        starship_sector = self.galaxy.get_starship_sector()

        fdo = CalculationUtils.get_final_destination(
            dir, dist, starship_sector, self.galaxy.current_quadrant
        )
        if fdo.out_side_galaxy:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.NAV
            res.nav = NavResult(NavMessage.BAD_INPUT_OUTSIDE_GALAXY, -1)
            return res

        est_energy_for_trip = CalculationUtils.distance2_energy(
            self.galaxy.current_quadrant.coord,
            starship_sector.coord,
            fdo.final_quadrant,
            fdo.final_sector,
        )

        if self.galaxy.starship.energy_level < est_energy_for_trip:
            if (
                self.galaxy.starship.energy_level + self.galaxy.starship.shield_level
                > est_energy_for_trip
            ):
                res = Result()
                res.command_result = CommandResult.ERROR
                res.command = Commands.NAV
                res.nav = NavResult(NavMessage.INSUFFICIENT_ENERGY_SHIELD_ENERGY_AVAILABLE, -1)
                return res
            else:
                res = Result()
                res.command_result = CommandResult.ERROR
                res.command = Commands.NAV
                res.nav = NavResult(NavMessage.INSUFFICIENT_ENERGY, -1)
                return res

        nav_msg = self.check_route_and_move_starship(
            dir,
            dist,
            est_energy_for_trip,
            starship_quadrant.coord,
            fdo.final_quadrant,
            fdo.final_sector,
        )

        if fdo.object_hit:
            res = Result()
            res.command_result = CommandResult.ERROR
            res.command = Commands.NAV
            dist_traveled = CalculationUtils.get_distance(starship_sector.coord, fdo.final_sector)
            res.nav = NavResult(NavMessage.BAD_INPUT_OBJECT_HIT, dist_traveled)
            return res

        if (
            starship_quadrant.coord.x != fdo.final_quadrant.x
            or starship_quadrant.coord.y != fdo.final_quadrant.y
        ):
            dist_traveled = (
                CalculationUtils.get_distance(starship_quadrant.coord, fdo.final_quadrant) * 8
            )
        else:
            dist_traveled = (
                CalculationUtils.get_distance(starship_sector.coord, fdo.final_sector) * 8
            )

        res = Result()
        res.command_result = CommandResult.OK
        res.command = Commands.NAV
        res.nav = NavResult(nav_msg, dist_traveled)
        return res

    def routine_maint(self, change_mission_time: float, enemies_fire: bool):
        docking_status = DockingStatus(self.galaxy.starship.is_docked, False)
        self.galaxy.starship.is_docked = False

        if self.galaxy.starship.shield_level == 0 and self.can_be_docked():
            docking_status.current_status = True
            self.galaxy.starship.is_docked = True
            self.galaxy.starship.energy_level = gbl.MAX_STARSHIP_ENERGY
            self.galaxy.starship.torps_remain = gbl.MAX_STARSHIP_TORP
        else:
            if self.galaxy.starship.shield_level != 0 and self.galaxy.starship.is_docked:
                docking_status.current_status = False
                self.galaxy.starship.is_docked = False

        game_status = GameStatus.NORMAL

        if self.galaxy.mission_time > self.galaxy.mission_time_deadline:
            game_status = GameStatus.RAN_OUT_OF_TIME
        if self.galaxy.starship.is_destroyed:
            game_status = GameStatus.STARSHIP_DESTROYED
        if self.galaxy.starship.energy_level == 0 and self.galaxy.starship.shield_level == 0:
            game_status = GameStatus.RAN_OUT_OF_ENERGY
        if (
            self.galaxy.starship.energy_level == 0
            and self.galaxy.starship.shield_level > 0
            and self.get_damage_level(DeviceType.SHE) >= 0
        ):
            game_status = GameStatus.OUT_OF_ENERGY_SHIELD_ENERGY_AVAILABLE
        if (
            self.galaxy.starship.energy_level == 0
            and self.galaxy.starship.shield_level > 0
            and self.get_damage_level(DeviceType.SHE) < 0
        ):
            game_status = GameStatus.RAN_OUT_OF_ENERGY
        if OtherFactories.get_enemies_remaining(self.galaxy) == 0:
            game_status = GameStatus.MISSION_OVER

        enemies_fired = []
        if not self.prevent_enemy_fire and enemies_fire:
            enemies_fired = self.enemies_fired()

        if self.galaxy.starship.is_destroyed:
            game_status = GameStatus.STARSHIP_DESTROYED

        enemies_moved = self.enemies_moved()

        res = Result()
        res.maint_result = MaintResult(
            self.update_mission_time(change_mission_time),
            self.update_damaged_devices_with_mission_time(change_mission_time),
            enemies_fired,
            enemies_moved,
            docking_status,
            self.starbase_repairs(),
            game_status,
        )
        return res

    def run_starbase_repair(self):
        time_to_repair = self.starbase_repairs()
        if time_to_repair is None:
            raise RuntimeError("timeToRepair is null")
        self.execute_starbase_repair(time_to_repair.mission_time_to_repair)

    def str2int(self, string: str) -> int | None:
        try:
            x_int = int(string)
        except ValueError:
            return None
        return x_int

    def str2float(self, string: str) -> float | None:
        try:
            x_float = float(string)
            if not math.isfinite(x_float):
                return None
        except ValueError:
            return None
        return x_float

    def enemies_fired(self) -> list[EnemyFired]:
        enemy_sectors = self.galaxy.current_quadrant.get_enemy_sectors()
        if enemy_sectors is None:
            return []

        enemies_fired_return = []
        for enemy_sector in enemy_sectors:
            enemy_hit_amount = self.random_factory.get_random_integer(gbl.RIT_ENEMY_FIRED_AMOUNT)

            if self.galaxy.starship.is_docked:
                enemy_fire = enemy_fired.EnemyFired(
                    enemy_sector.coord,
                    self.galaxy.starship.shield_level,
                    False,
                    None,
                    enemy_hit_amount,
                    None,
                    True,
                )
                enemies_fired_return.append(enemy_fire)
            else:
                self.galaxy.starship.shield_level -= enemy_hit_amount
                if self.galaxy.starship.shield_level < 0 and not self.galaxy.starship.is_docked:
                    self.galaxy.starship.is_destroyed = True
                    enemy_fire = enemy_fired.EnemyFired(
                        enemy_sector.coord,
                        self.galaxy.starship.shield_level,
                        True,
                        None,
                        enemy_hit_amount,
                        None,
                        False,
                    )
                    enemies_fired_return.append(enemy_fire)
                    return enemies_fired_return

                damaged_device: Device | None = None
                if (
                    self.random_factory.get_random_integer(gbl.RIT_DAMAGE_DEVICE_CHANCE)
                    > gbl.DAMAGE_DEVICE_RANDOM_NUMBER_THRESHOLD
                ):
                    while True:
                        damaged_device_num = self.random_factory.get_random_integer(
                            gbl.RIT_DAMAGE_DEVICE
                        )
                        target_device = self.galaxy.starship.get_device(
                            DeviceType(damaged_device_num)
                        )
                        if target_device.damage_level >= 0:
                            damaged_device = target_device
                            break

                    damaged_device_mission_time = self.random_factory.get_random_integer(
                        gbl.RIT_DAMAGE_DEVICE_AMOUNT
                    )
                    damaged_device.damage_level = damaged_device_mission_time * -1
                    enemy_fire = enemy_fired.EnemyFired(
                        enemy_sector.coord,
                        self.galaxy.starship.shield_level,
                        True,
                        damaged_device,
                        enemy_hit_amount,
                        damaged_device_mission_time,
                        False,
                    )
                    enemies_fired_return.append(enemy_fire)
                    continue

                enemy_fire = enemy_fired.EnemyFired(
                    enemy_sector.coord,
                    self.galaxy.starship.shield_level,
                    False,
                    None,
                    enemy_hit_amount,
                    None,
                    False,
                )
                enemies_fired_return.append(enemy_fire)

        return enemies_fired_return

    def enemies_moved(self) -> list[EnemyMoved]:
        enemy_sectors = self.galaxy.current_quadrant.get_enemy_sectors()
        if enemy_sectors is None:
            return []
        if self.skip_enemy_move:
            return []

        enemies_moved = []
        for enemy_sector in enemy_sectors:
            enemy_move_chance = self.random_factory.get_random_integer(gbl.RIT_ENEMY_MOVE_CHANCE)

            if enemy_move_chance < gbl.ENEMY_MOVE_CHANCE and not self.force_enemy_move:
                continue

            mt_sector = (
                self.current_quadrant_factory.CurrentQuadrantFactory.get_random_empty_sector(
                    self.random_factory, self.galaxy.current_quadrant, gbl.RCT_ENEMY_LOCATION
                )
            )

            self.move_object_inside_quadrant(enemy_sector.coord, mt_sector.coord)
            enemy_moved = EnemyMoved(enemy_sector.coord, mt_sector.coord)
            enemies_moved.append(enemy_moved)

        return enemies_moved

    def update_damaged_devices_with_mission_time(self, mission_time: float) -> list[Device]:
        damaged_devices = self.galaxy.starship.get_damaged_devices()
        for device in damaged_devices:
            device.damage_level += mission_time
            device.damage_level = round(device.damage_level, 1)
            if round(device.damage_level >= 0):
                device.damage_level = 100
        return damaged_devices

    def update_mission_time(self, change_mission_time: float) -> float:
        self.galaxy.mission_time += change_mission_time
        return self.galaxy.mission_time

    def check_route_and_move_starship(
        self,
        dir: float,
        dist: float,
        est_energy_for_trip: int,
        start_sector_coord: Coord,
        final_quadrant: Coord,
        final_sector: Coord,
    ) -> NavMessage:
        cfo = DetectObject.detect_object_with_dist(
            self.galaxy.current_quadrant, start_sector_coord, True, dir, dist
        )
        starship_sector = self.galaxy.get_starship_sector()
        if cfo.object == gbl.SECTOR_EMPTY:
            if (
                final_quadrant.x == self.galaxy.current_quadrant.coord.x
                and final_quadrant.y == self.galaxy.current_quadrant.coord.y
            ):
                self.move_object_inside_quadrant(starship_sector.coord, final_sector)
            else:
                dest_quadrant = self.galaxy.get_quadrant_by_coord(final_quadrant)
                self.move_starship_quadrant(dest_quadrant, final_sector)
            self.galaxy.starship.energy_level -= est_energy_for_trip
            return NavMessage.TRANSIT_COMPLETE
        else:
            next_to_last_coord = cfo.tracking_coords[-1]
            est_energy_for_aborted_trip = CalculationUtils.distance2_energy(
                self.galaxy.current_quadrant.coord,
                starship_sector.coord,
                self.galaxy.current_quadrant.coord,
                next_to_last_coord,
            )
            self.move_object_inside_quadrant(starship_sector.coord, next_to_last_coord)
            self.galaxy.starship.energy_level -= est_energy_for_aborted_trip
            return NavMessage.BAD_INPUT_OBJECT_HIT

    def move_starship_quadrant(self, new_quadrant: Quadrant, sector_coord: Coord) -> None:
        self.galaxy.current_quadrant = (
            self.current_quadrant_factory.CurrentQuadrantFactory.create_current_quadrant(
                new_quadrant, self.random_factory, sector_coord
            )
        )

    def can_be_docked(self) -> bool:
        starship_sector = self.galaxy.get_starship_sector()
        (top_left, bot_right) = CalculationUtils.get_coord_range(starship_sector.coord)

        for x in range(top_left.x, bot_right.x + 1):
            for y in range(top_left.y, bot_right.y + 1):
                sect = self.galaxy.current_quadrant.get_sector(x, y)
                if sect.sector_contents.has_starbase():
                    return True
        return False

    def set_damage_level(self, device: DeviceType, damage_level: float) -> None:
        target_dev = self.galaxy.starship.get_device(device)
        target_dev.damage_level = damage_level

    def get_damage_level(self, device: DeviceType) -> float:
        target_dev = self.galaxy.starship.get_device(device)
        return target_dev.damage_level

    def get_formatted_coord(self, coord):
        return f"[{coord.x},{coord.y}]"

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

    def execute_starbase_repair(self, mission_time: float) -> None:
        self.galaxy.mission_time += abs(mission_time)
        for device in self.galaxy.starship.devices:
            device.damage_level = 0

    def starbase_repairs(self) -> StarbaseRepairs | None:
        if not self.galaxy.starship.is_docked:
            return None
        damaged_devices = self.galaxy.starship.get_damaged_devices()
        if len(damaged_devices) == 0:
            return None
        min_value = min(obj.damage_level for obj in damaged_devices)
        return StarbaseRepairs(abs(min_value))

    def get_current_quadrant_formatted(self) -> str:
        out_string = f"Current Quadrant Coord {self.get_formatted_coord(self.galaxy.current_quadrant.coord)}\n"
        for y in range(-1, gbl.MAX_QUADRANT_SECTOR_XY):
            if y == -1:
                out_string += "###\t\t"
            else:
                out_string += f"{y}\t\t"
        out_string += "\n"

        for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
            out_row_string = ""
            for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
                item = self.galaxy.current_quadrant.get_sector(x, y)
                out_row_string += self.get_sector_formatted(item) + "\t\t"
            out_string += f"{y}\t\t{out_row_string}\n"

        return out_string

    def get_quadrant_for_galaxy_formatted(self, quadrant: Quadrant, mark_starship: bool) -> str:
        outstr = ""
        if not quadrant.has_been_explored:
            return "| *** "

        ent_marker_start = " "
        ent_marker_end = " "
        if mark_starship:
            ent_marker_start = "<"
            ent_marker_end = ">"

        outstr += "|" + ent_marker_start
        outstr += str(quadrant.num_enemies)
        if quadrant.has_star_base:
            outstr += "1"
        else:
            outstr += "0"

        outstr += str(quadrant.num_stars)
        outstr += ent_marker_end
        return outstr

    def move_object_inside_quadrant(self, source: Coord, dest: Coord) -> None:
        if source.x == dest.x and source.y == dest.y:
            return

        source_sector = self.galaxy.current_quadrant.get_sector_by_coord(source)
        dest_sector = self.galaxy.current_quadrant.get_sector_by_coord(dest)

        dest_sector.sector_contents.sector_contents = source_sector.sector_contents.sector_contents
        if source_sector.enemy is not None:
            dest_sector.enemy = source_sector.enemy
            source_sector.enemy = None
        source_sector.sector_contents.sector_contents = gbl.SECTOR_EMPTY

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
                quad = self.galaxy.get_quadrant(x, y)

                if (
                    quad.coord.x == self.galaxy.current_quadrant.coord.x
                    and quad.coord.y == self.galaxy.current_quadrant.coord.y
                ):
                    out_str += self.get_quadrant_for_galaxy_formatted(quad, True)
                else:
                    out_str += self.get_quadrant_for_galaxy_formatted(quad, False)

            out_str += "|\n"

        out_str += "v " + line
        return out_str
