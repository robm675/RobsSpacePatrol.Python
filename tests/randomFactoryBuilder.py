from collections import deque
from typing import Self

from source import gbl
from source.library.factories.randomFactory import RandomFactory
from source.library.models.coord import Coord


class _ConfiguredRandomFactory(RandomFactory):
    def __init__(self, integers, coordinates):
        self._integers = {key: deque(values) for key, values in integers.items()}
        self._coordinates = {key: deque(values) for key, values in coordinates.items()}

    @staticmethod
    def _get(responses, randomType):
        if randomType not in responses:
            raise AssertionError(f"No test random response configured for {randomType!r}")
        values = responses[randomType]
        if not values:
            raise AssertionError(f"Test random response sequence exhausted for {randomType!r}")
        # SetInteger/SetCoord repeat; SetIntegers/SetCoords consume a finite sequence.
        if isinstance(values, deque):
            return values.popleft()
        return values[0]

    def GetRandomInteger(self, randomType: str) -> int:
        return self._get(self._integers, randomType)

    def GetRandomCoord(self, randomType: str) -> Coord:
        x, y = self._get(self._coordinates, randomType)
        return Coord(x, y)

    def GetRandomIntegerFromGenerator(self, min: int, max: int) -> int:
        raise AssertionError("Test factory cannot call the real random generator")


class RandomFactoryBuilder:
    """Build isolated deterministic factories; unconfigured requests fail loudly."""

    def __init__(self):
        self._integers = {}
        self._coordinates = {}
        self._repeat_integers = set()
        self._repeat_coordinates = set()

    def SetInteger(self, randomType: str, value: int) -> Self:
        self.SetIntegers(randomType, value)
        self._repeat_integers.add(randomType)
        return self

    def SetIntegers(self, randomType: str, *values: int) -> Self:
        if not values:
            raise ValueError("Provide at least one integer response")
        if any(type(value) is not int for value in values):
            raise TypeError("Integer responses must be integers")
        self._integers[randomType] = tuple(values)
        self._repeat_integers.discard(randomType)
        return self

    def SetCoord(self, randomType: str, x: int, y: int) -> Self:
        self.SetCoords(randomType, (x, y))
        self._repeat_coordinates.add(randomType)
        return self

    def SetCoords(self, randomType: str, *values: tuple[int, int]) -> Self:
        if not values:
            raise ValueError("Provide at least one coordinate response")
        coordinates = []
        for x, y in values:
            if any(type(value) is not int for value in (x, y)):
                raise TypeError("Coordinate components must be integers")
            if not (0 <= x < gbl.MAX_QUADRANT_SECTOR_XY and
                    0 <= y < gbl.MAX_QUADRANT_SECTOR_XY):
                raise ValueError(f"Coordinate ({x}, {y}) is outside the galaxy/sector grid")
            coordinates.append((x, y))
        self._coordinates[randomType] = tuple(coordinates)
        self._repeat_coordinates.discard(randomType)
        return self

    def SetEnemyChance(self, value: int) -> Self:
        return self.SetInteger(gbl.RIT_ENEMY_CHANCE, value)

    def SetStarQuantity(self, value: int) -> Self:
        return self.SetInteger(gbl.RIT_STAR_QUANTITY, value)

    def SetStarbaseChance(self, value: int) -> Self:
        return self.SetInteger(gbl.RIT_STARBASE_CHANCE, value)

    def SetStarshipQuadrant(self, x: int, y: int) -> Self:
        return self.SetCoord(gbl.RCT_STARSHIP_QUADRANT, x, y)

    def SetStarshipSector(self, x: int, y: int) -> Self:
        return self.SetCoord(gbl.RCT_STARSHIP_SECTOR, x, y)

    def WithDefaults(self) -> Self:
        """Reset to an empty galaxy, predictable combat, and no device damage/movement."""
        self._integers.clear()
        self._coordinates.clear()
        self._repeat_integers.clear()
        self._repeat_coordinates.clear()
        integers = {
            gbl.RIT_STARTING_MISSION_TIME: 0,
            gbl.RIT_STAR_QUANTITY: 0,
            gbl.RIT_ENEMY_CHANCE: 0,
            gbl.RIT_STARBASE_CHANCE: 0,
            gbl.RIT_ENEMY_SHIELD_LEVEL: 100,
            gbl.RIT_ENEMY_FIRED_AMOUNT: 10,
            gbl.RIT_DAMAGE_DEVICE_CHANCE: 0,
            gbl.RIT_DAMAGE_DEVICE: 1,
            gbl.RIT_DAMAGE_DEVICE_AMOUNT: 1,
            gbl.RIT_ENEMY_MOVE_CHANCE: 0,
            gbl.RIT_STAR_DESTROYED_CHANCE: 100,
            gbl.RIT_LASER_MISS_CHANCE: 0,
        }
        for randomType, value in integers.items():
            self.SetInteger(randomType, value)
        self.SetStarshipQuadrant(0, 0).SetStarshipSector(0, 0)
        # Placements are deliberately explicit: repeated coordinates can collide.
        return self

    def Build(self) -> RandomFactory:
        factory = _ConfiguredRandomFactory(self._integers, self._coordinates)
        for key in self._repeat_integers:
            factory._integers[key] = self._integers[key]
        for key in self._repeat_coordinates:
            factory._coordinates[key] = self._coordinates[key]
        return factory
