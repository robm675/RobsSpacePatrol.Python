import sys
sys.path.append("/pythontrek/source/library/")
sys.path.append("/pythontrek/source/")
from enum import Enum
import source.library.models.coord as coord
import source.library.models.starship as ent
import random
import gbl as gbl

class RandomFactory:
    def GetRandomCoord(self, randomType: str) -> coord.Coord:
        match randomType:
            case gbl.RCT_ENEMY_LOCATION:
                x = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x,y)
            case gbl.RCT_STAR_LOCATION:
                x = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x,y)
            case gbl.RCT_STARSHIP_SECTOR:
                x = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x,y)
            case gbl.RCT_STARSHIP_QUADRANT:
                x = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x,y)
            case gbl.RCT_STARBASE_LOCATION:
                x = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                y = self.GetRandomIntegerFromGenerator(0, gbl.MAX_QUADRANT_SECTOR_XY - 1)
                return coord.Coord(x,y)            
        raise Exception(f"Unknown: {randomType}")

    def GetRandomInteger(self, randomType: str) -> int:
        match randomType:
            case gbl.RIT_STARTING_MISSION_TIME:
                return 0
            case gbl.RIT_DAMAGE_DEVICE:
                totalDevices = len(ent.eDevice)
                return self.GetRandomIntegerFromGenerator(1, totalDevices)
            case gbl.RIT_DAMAGE_DEVICE_AMOUNT:
                return self.GetRandomIntegerFromGenerator(0, gbl.MAX_DAMAGE_MISSION_TIME_AMOUNT)
            case gbl.RIT_DAMAGE_DEVICE_CHANCE:
                return self.GetRandomIntegerFromGenerator(0, 100)
            case gbl.RIT_ENEMY_CHANCE:
                return self.GetRandomIntegerFromGenerator(0, 100)
            case gbl.RIT_STAR_QUANTITY:
                return self.GetRandomIntegerFromGenerator(0, gbl.MAX_STARSPERQUADRANT)
            case gbl.RIT_STARBASE_CHANCE:
                return self.GetRandomIntegerFromGenerator(0, 100)
            case gbl.RIT_ENEMY_SHIELD_LEVEL:
                return self.GetRandomIntegerFromGenerator(100, 200)
            case gbl.RIT_ENEMY_FIRED_AMOUNT:
                return self.GetRandomIntegerFromGenerator(10, 50)
            case gbl.RIT_ENEMY_MOVE_CHANCE:
                return self.GetRandomIntegerFromGenerator(0, 100)
            case gbl.RIT_STAR_DESTROYED_CHANCE:
                return self.GetRandomIntegerFromGenerator(0, 100)
            case gbl.RIT_LASER_MISS_CHANCE:
                return self.GetRandomIntegerFromGenerator(0, 100)
        raise Exception(f"Unknown: {randomType}")

    def GetRandomIntegerFromGenerator(self, min: int, max:int) -> int:
        return random.randint(min, max)
