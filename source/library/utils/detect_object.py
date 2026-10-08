import math
from typing import List

import gbl as gbl
import models.coord as coord
import models.current_quadrant as current_quadrant
from models.detected_object import DetectedObject

import source.library.models.detected_object as det_obj
import source.library.utils.calculation_utilities as cu


class DetectObject:
    @staticmethod
    def detect_object_no_dist(
        current_quadrant: current_quadrant.CurrentQuadrant,
        starting_sector: coord.Coord,
        is_navigation: bool,
        dir: float,
    ) -> det_obj.DetectedObject:
        return DetectObject.detect_object_with_dist(
            current_quadrant, starting_sector, is_navigation, dir, 99
        )

    @staticmethod
    def detect_object_with_dist(
        current_quadrant: current_quadrant.CurrentQuadrant,
        starting_sector: coord.Coord,
        is_navigation: bool,
        dir: float,
        dist: float,
    ) -> det_obj.DetectedObject:
        tracking_coords = []

        dist_univ = dist * 8

        angle = -(math.pi * (dir - 1.0) / 4.0)

        dx = round(dist_univ * math.cos(angle), 5)
        dy = round(dist_univ * math.sin(angle), 5)

        vx = dx / 1000
        vy = dy / 1000

        target_x = float(starting_sector.x)
        target_y = float(starting_sector.y)

        last_good_sect_x = float(starting_sector.x)
        last_good_sect_y = float(starting_sector.y)

        last_tracking_x = float(starting_sector.x)
        last_tracking_y = float(starting_sector.y)

        tracking_coords.append(coord.Coord(last_tracking_x, last_tracking_y))

        for counter in range(1000):
            target_x += vx
            target_y += vy

            temp_sect_x = int(target_x)
            temp_sect_y = int(target_y)

            if temp_sect_x != last_tracking_x or temp_sect_y != last_tracking_y:
                last_tracking_x = last_good_sect_x
                last_tracking_y = last_good_sect_y
                if not DetectObject.coord_already_exists(
                    tracking_coords, coord.Coord(last_tracking_x, last_tracking_y)
                ):
                    tracking_coords.append(coord.Coord(last_tracking_x, last_tracking_y))

            if (
                temp_sect_x < 0
                or temp_sect_x > gbl.MAX_QUADRANT_SECTOR_XY - 1
                or temp_sect_y < 0
                or temp_sect_y > gbl.MAX_QUADRANT_SECTOR_XY - 1
            ):
                break

            target_sector = current_quadrant.get_sector(temp_sect_x, temp_sect_y)

            if (
                not target_sector.sector_contents.is_empty()
                and not target_sector.sector_contents.has_starship()
            ):
                final_coord = coord.Coord(temp_sect_x, temp_sect_y)

                if is_navigation:
                    if (
                        not target_sector.sector_contents.is_empty()
                        and not target_sector.sector_contents.has_starship()
                    ):
                        final_coord = tracking_coords[-1]

                if not DetectObject.coord_already_exists(
                    tracking_coords, coord.Coord(temp_sect_x, temp_sect_y)
                ):
                    tracking_coords.append(coord.Coord(temp_sect_x, temp_sect_y))

                distance_moved = cu.CalculationUtils.get_distance(starting_sector, final_coord)

                object_hit = target_sector.sector_contents.sector_contents

                return DetectedObject(object_hit, distance_moved, final_coord, tracking_coords)

        return DetectedObject(gbl.SECTOR_EMPTY, -1, None, tracking_coords)

    @staticmethod
    def coord_already_exists(list_in: List[coord.Coord], test_coord) -> bool:
        return any(tc.x == test_coord and tc.y == test_coord for tc in list_in)
