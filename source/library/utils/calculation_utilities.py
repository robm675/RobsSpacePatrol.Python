import math
from typing import NamedTuple

import gbl as gbl
import models.coord as coord
import models.current_quadrant as current_quadrant
import models.final_destination as final_dest
import models.sector as sector


class QuadSector(NamedTuple):
    quadrant: coord.Coord
    sector: coord.Coord


class QuadSectorInt(NamedTuple):
    quad: int
    sect: int


class CalculationUtils:
    @staticmethod
    def qs2_univ(quad: int, sect: int) -> int:
        return quad * gbl.MAX_QUADRANT_SECTOR_XY + sect

    @staticmethod
    def univ2_qs(univ_coord: int) -> QuadSectorInt:
        temp_num = float(univ_coord) / gbl.MAX_QUADRANT_SECTOR_XY
        quad = int(float(univ_coord) / gbl.MAX_QUADRANT_SECTOR_XY)
        sect = int((temp_num - quad) * gbl.MAX_QUADRANT_SECTOR_XY)

        return QuadSectorInt(quad, sect)

    @staticmethod
    def univ2_qs_coord(x: int, y: int) -> QuadSector:
        x_coord = CalculationUtils.univ2_qs(x)
        y_coord = CalculationUtils.univ2_qs(y)

        return QuadSector(
            coord.Coord(x_coord.quad, y_coord.quad), coord.Coord(x_coord.sect, y_coord.sect)
        )

    @staticmethod
    def get_distance(coord1: coord.Coord, coord2: coord.Coord) -> float:
        x = coord2.x - coord1.x
        y = coord2.y - coord1.y
        return round(math.sqrt(x * x + y * y), 1)

    @staticmethod
    def get_direction(coord1: coord.Coord, coord2: coord.Coord) -> float:
        dir = 0
        if coord1.x == coord2.x:
            if coord1.y < coord2.y:
                dir = 7
            else:
                dir = 3
        elif coord1.y == coord2.y:
            if coord1.x < coord2.x:
                dir = 1
            else:
                dir = 5
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
    def get_enemy_shield_hit(
        number_enemies: int,
        energy_of_shot: int,
        distance_to_enemy: float,
        energy_factor_to_reduce_per_sector: int,
    ):
        laser_amount_per_enemy = int(round(energy_of_shot / number_enemies, 0))
        laser_energy_to_reduce_due_to_dist = int(
            distance_to_enemy * energy_factor_to_reduce_per_sector
        )
        total_energy_hit_on_enemy_shields = int(
            laser_amount_per_enemy - laser_energy_to_reduce_due_to_dist
        )
        if total_energy_hit_on_enemy_shields < 0:
            total_energy_hit_on_enemy_shields = 0
        return total_energy_hit_on_enemy_shields

    @staticmethod
    def calculate_starship_hit_from_enemy(
        random_enemy_fired_amount: int, distance: float, energy_factor_to_reduce_per_sector: int
    ):
        return random_enemy_fired_amount - int(distance * energy_factor_to_reduce_per_sector)

    @staticmethod
    def distance_to_energy(distance: float):
        change_amount = int(distance * gbl.SECTOR_TO_ENERGY_CONV)
        if change_amount < 1:
            change_amount = 1
        return change_amount

    @staticmethod
    def distance_to_energy_coord(start: coord.Coord, end: coord.Coord):
        dist = CalculationUtils.get_distance(start, end)
        return CalculationUtils.distance_to_energy(dist)

    @staticmethod
    def distance2_energy(
        start_q: coord.Coord, start_s: coord.Coord, final_q: coord.Coord, final_s: coord.Coord
    ):
        start_ux = CalculationUtils.qs2_univ(start_q.x, start_s.x)
        start_uy = CalculationUtils.qs2_univ(start_q.y, start_s.y)
        final_ux = CalculationUtils.qs2_univ(final_q.x, final_s.x)
        final_uy = CalculationUtils.qs2_univ(final_q.y, final_s.y)
        return CalculationUtils.distance_to_energy_coord(
            coord.Coord(start_ux, start_uy), coord.Coord(final_ux, final_uy)
        )

    @staticmethod
    def get_coord_range(center: coord.Coord) -> tuple[coord.Coord, coord.Coord]:
        if center.x - 1 < 0:
            left_x = 0
        else:
            left_x = center.x - 1

        if center.x + 1 > 7:
            right_x = 7
        else:
            right_x = center.x + 1

        if center.y - 1 < 0:
            top_y = 0
        else:
            top_y = center.y - 1

        if center.y + 1 > 7:
            bottom_y = 7
        else:
            bottom_y = center.y + 1

        return (coord.Coord(left_x, top_y), coord.Coord(right_x, bottom_y))

    @staticmethod
    def distance2_time(distance: float) -> float:
        return distance * gbl.SECTOR_TO_TIME_CONV

    @staticmethod
    def get_final_destination(
        dir: float,
        dist: float,
        starship_sector: sector.Sector,
        current_quadrant: current_quadrant.CurrentQuadrant,
    ) -> final_dest.FinalDestination:
        ent_sx = starship_sector.coord.x
        ent_sy = starship_sector.coord.y
        ent_qx = current_quadrant.coord.x
        ent_qy = current_quadrant.coord.y

        est_final_univ_x = CalculationUtils.qs2_univ(ent_qx, ent_sx)
        est_final_univ_y = CalculationUtils.qs2_univ(ent_qy, ent_sy)

        dist_univ = dist * 8

        angle = -(math.pi * (dir - 1.0) / 4.0)

        dx = round(dist_univ * math.cos(angle), 5)
        dy = round(dist_univ * math.sin(angle), 5)

        vx = dx / 1000
        vy = dy / 1000

        last_good_sx = -1
        last_good_sy = -1
        last_good_qx = -1
        last_good_qy = -1

        for counter in range(1000):
            est_final_univ_x += vx
            est_final_univ_y += vy

            temp_x = CalculationUtils.univ2_qs(int(est_final_univ_x))
            temp_y = CalculationUtils.univ2_qs(int(est_final_univ_y))

            if (
                temp_x.quad < 0
                or temp_x.quad > gbl.MAX_QUADRANT_SECTOR_XY - 1
                or temp_y.quad < 0
                or temp_y.quad > gbl.MAX_QUADRANT_SECTOR_XY - 1
            ):
                return final_dest.FinalDestination(
                    coord.Coord(last_good_qx, last_good_qy),
                    coord.Coord(last_good_sx, last_good_sy),
                    True,
                    False,
                )

            if (
                temp_x.sect < 0
                or temp_x.sect > gbl.MAX_QUADRANT_SECTOR_XY
                or temp_y.sect < 0
                or temp_y.sect > gbl.MAX_QUADRANT_SECTOR_XY - 1
            ):
                return final_dest.FinalDestination(
                    coord.Coord(last_good_qx, last_good_qy),
                    coord.Coord(last_good_sx, last_good_sy),
                    True,
                    False,
                )

            if temp_x.quad == ent_qx and temp_y.quad == ent_qy:
                target_sector = coord.Coord(temp_x.sect, temp_y.sect)
                cur_sector = current_quadrant.get_sector(target_sector.x, target_sector.y)

                if (
                    not cur_sector.sector_contents.is_empty()
                    and not cur_sector.sector_contents.has_starship()
                ):
                    return final_dest.FinalDestination(
                        current_quadrant.coord, coord.Coord(last_good_sx, last_good_sy), False, True
                    )

            last_good_sx = temp_x.sect
            last_good_sy = temp_y.sect
            last_good_qx = temp_x.quad
            last_good_qy = temp_y.quad

        final = CalculationUtils.univ2_qs_coord(round(est_final_univ_x), round(est_final_univ_y))

        max_num_squared = gbl.MAX_QUADRANT_SECTOR_XY * gbl.MAX_QUADRANT_SECTOR_XY - 1
        if (
            est_final_univ_x < 0
            or est_final_univ_x >= max_num_squared
            or est_final_univ_y < 0
            or est_final_univ_y >= max_num_squared
        ):
            raise Exception("this is happening for some reason")

        return final_dest.FinalDestination(final.quadrant, final.sector, False, False)
