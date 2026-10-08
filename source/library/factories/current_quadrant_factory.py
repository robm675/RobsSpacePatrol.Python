import gbl as gbl
import random_factory as rf

import source.library.models.coord as coord
import source.library.models.quadrant as quadrant
from source.library.models.current_quadrant import CurrentQuadrant
from source.library.models.enemy import Enemy
from source.library.models.sector import Sector
from source.library.models.sector_contents import SectorContents


class CurrentQuadrantFactory:
    @staticmethod
    def get_random_empty_sector(
        rf: rf.RandomFactory, current_quadrant: CurrentQuadrant, random_coord_type: str
    ):
        count = 0
        while True:
            coord = rf.get_random_coord(random_coord_type)

            chosen_sector = current_quadrant.get_sector(coord.x, coord.y)

            count += 1
            if count > 10:
                raise Exception("Tried 10 times and failed to find an empty sector")

            if chosen_sector.sector_contents.is_empty():
                return chosen_sector

    @staticmethod
    def create_current_quadrant(
        quadrant: quadrant.Quadrant, rf: rf.RandomFactory, ent_sector_coord: coord.Coord
    ):
        sectors = []

        x = 0
        while x < gbl.MAX_QUADRANT_SECTOR_XY:
            y = 0
            while y < gbl.MAX_QUADRANT_SECTOR_XY:
                sectors.append(Sector(coord.Coord(x, y), SectorContents(gbl.SECTOR_EMPTY)))
                y += 1
            x += 1

        cur_quad = CurrentQuadrant(quadrant.coord, sectors)

        ent_sector = next(
            sect
            for sect in sectors
            if sect.coord.x == ent_sector_coord.x and sect.coord.y == ent_sector_coord.y
        )
        ent_sector_temp: Sector = ent_sector
        ent_sector_temp.sector_contents.sector_contents = gbl.SECTOR_STARSHIP

        for count in range(quadrant.num_stars):
            target_sector = CurrentQuadrantFactory.get_random_empty_sector(
                rf, cur_quad, gbl.RCT_STAR_LOCATION
            )
            target_sector.sector_contents.sector_contents = gbl.SECTOR_STAR

        if quadrant.has_star_base:
            target_sector = CurrentQuadrantFactory.get_random_empty_sector(
                rf, cur_quad, gbl.RCT_STARBASE_LOCATION
            )
            target_sector.sector_contents.sector_contents = gbl.SECTOR_STARBASE

        if quadrant.num_enemies > 0:
            for enemy in range(quadrant.num_enemies):
                target_sector = CurrentQuadrantFactory.get_random_empty_sector(
                    rf, cur_quad, gbl.RCT_ENEMY_LOCATION
                )
                target_sector.sector_contents.sector_contents = gbl.SECTOR_ENEMY
                new_shield_level = rf.get_random_integer(gbl.RIT_ENEMY_SHIELD_LEVEL)
                target_sector.enemy = Enemy(new_shield_level)

        quadrant.has_been_explored = True

        return cur_quad
