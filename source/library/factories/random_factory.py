import random

import gbl as gbl

import source.library.models.coord as coord
import source.library.models.starship as ent


class RandomFactory:
    def get_random_coord(self, random_type: str) -> coord.Coord:
        match random_type:
            case gbl.RCT_ENEMY_LOCATION:
                x = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x, y)
            case gbl.RCT_STAR_LOCATION:
                x = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x, y)
            case gbl.RCT_STARSHIP_SECTOR:
                x = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x, y)
            case gbl.RCT_STARSHIP_QUADRANT:
                x = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x, y)
            case gbl.RCT_STARBASE_LOCATION:
                x = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.get_random_integer_from_generator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x, y)
        raise Exception(f"Unknown: {random_type}")

    def get_random_integer(self, random_type: str) -> int:
        match random_type:
            case gbl.RIT_STARTING_MISSION_TIME:
                return 0
            case gbl.RIT_DAMAGE_DEVICE:
                total_devices = len(ent.DeviceType)
                return self.get_random_integer_from_generator(1, total_devices)
            case gbl.RIT_DAMAGE_DEVICE_AMOUNT:
                return self.get_random_integer_from_generator(0, gbl.MAX_DAMAGE_MISSION_TIME_AMOUNT)
            case gbl.RIT_DAMAGE_DEVICE_CHANCE:
                return self.get_random_integer_from_generator(0, 100)
            case gbl.RIT_ENEMY_CHANCE:
                return self.get_random_integer_from_generator(0, 100)
            case gbl.RIT_STAR_QUANTITY:
                return self.get_random_integer_from_generator(0, gbl.MAX_STARSPERQUADRANT)
            case gbl.RIT_STARBASE_CHANCE:
                return self.get_random_integer_from_generator(0, 100)
            case gbl.RIT_ENEMY_SHIELD_LEVEL:
                return self.get_random_integer_from_generator(100, 200)
            case gbl.RIT_ENEMY_FIRED_AMOUNT:
                return self.get_random_integer_from_generator(10, 50)
            case gbl.RIT_ENEMY_MOVE_CHANCE:
                return self.get_random_integer_from_generator(0, 100)
            case gbl.RIT_STAR_DESTROYED_CHANCE:
                return self.get_random_integer_from_generator(0, 100)
            case gbl.RIT_LASER_MISS_CHANCE:
                return self.get_random_integer_from_generator(0, 100)
        raise Exception(f"Unknown: {random_type}")

    def get_random_integer_from_generator(self, min: int, max: int) -> int:
        return random.randint(min, max)
