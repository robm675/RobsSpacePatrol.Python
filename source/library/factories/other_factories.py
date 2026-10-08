import factories.random_factory as rf
from factories.current_quadrant_factory import CurrentQuadrantFactory
from models import galaxy

import source.gbl as gbl
import source.library.models.coord as coord
import source.library.models.galaxy as gal
import source.library.models.quadrant as q
import source.library.models.starship as ent


class OtherFactories:
    @staticmethod
    def create_starship() -> ent.Starship:
        return ent.Starship()

    @staticmethod
    def create_quadrant(coord: coord.Coord, rand_fact: rf.RandomFactory):
        num_stars = rand_fact.get_random_integer(gbl.RIT_STAR_QUANTITY)
        enemy_chance = rand_fact.get_random_integer(gbl.RIT_ENEMY_CHANCE)
        starbase_chance = rand_fact.get_random_integer(gbl.RIT_STARBASE_CHANCE)

        total_enemies = 0
        if enemy_chance > gbl.ENEMY_ZERO_ONE and enemy_chance <= gbl.ENEMY_ONE_TWO:
            total_enemies = 1
        if enemy_chance > gbl.ENEMY_ONE_TWO and enemy_chance <= gbl.ENEMY_TWO_THREE:
            total_enemies = 2
        if enemy_chance > gbl.ENEMY_TWO_THREE:
            total_enemies = 3

        new_quadrant = q.Quadrant(coord, total_enemies, num_stars)
        new_quadrant.has_star_base = False
        if starbase_chance > gbl.STARBASE_CHANCE:
            new_quadrant.has_star_base = True

        return new_quadrant

    @staticmethod
    def get_enemies_remaining(galaxy: galaxy.Galaxy) -> int:
        total = sum(p.num_enemies for p in galaxy.quadrants)
        return total

    @staticmethod
    def get_stars(galaxy: galaxy.Galaxy) -> int:
        total = sum(p.num_stars for p in galaxy.quadrants)
        return total

    @staticmethod
    def create_galaxy(
        rand_fact: rf.RandomFactory, cur_quad_factory: CurrentQuadrantFactory
    ) -> galaxy.Galaxy:
        new_galaxy = gal.Galaxy()
        new_galaxy.quadrants = []

        for x in range(gbl.MAX_QUADRANT_SECTOR_XY):
            for y in range(gbl.MAX_QUADRANT_SECTOR_XY):
                new_quadrant = OtherFactories.create_quadrant(coord.Coord(x, y), rand_fact)
                new_galaxy.quadrants.append(new_quadrant)

        starship_quadrant_coord = rand_fact.get_random_coord(gbl.RCT_STARSHIP_QUADRANT)
        starship_sector_coord = rand_fact.get_random_coord(gbl.RCT_STARSHIP_SECTOR)

        ent_quadrant = new_galaxy.get_quadrant(starship_quadrant_coord.x, starship_quadrant_coord.y)

        new_galaxy.current_quadrant = cur_quad_factory.create_current_quadrant(
            ent_quadrant, rand_fact, starship_sector_coord
        )

        ent_quad = new_galaxy.get_quadrant(starship_quadrant_coord.x, starship_quadrant_coord.y)
        ent_quad.has_been_explored = True

        new_galaxy.starship = ent.Starship()
        new_galaxy.mission_time = 0
        new_galaxy.mission_time_deadline = new_galaxy.mission_time + (
            OtherFactories.get_enemies_remaining(new_galaxy) * gbl.MISSION_TIME_PER_ENEMY_RATIO
        )

        return new_galaxy
