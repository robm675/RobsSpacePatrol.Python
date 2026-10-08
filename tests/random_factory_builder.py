from collections import deque
from typing import Self

from source import gbl
from source.library.factories.random_factory import RandomFactory
from source.library.models.coord import Coord


class _ConfiguredRandomFactory(RandomFactory):
    def __init__(self, integers, coordinates):
        self._integers = {key: deque(values) for key, values in integers.items()}
        self._coordinates = {key: deque(values) for key, values in coordinates.items()}

    @staticmethod
    def _get(responses, random_type):
        if random_type not in responses:
            raise AssertionError(f"No test random response configured for {random_type!r}")
        values = responses[random_type]
        if not values:
            raise AssertionError(f"Test random response sequence exhausted for {random_type!r}")
        # Single-response setters repeat; sequence setters consume a finite sequence.
        if isinstance(values, deque):
            return values.popleft()
        return values[0]

    def get_random_integer(self, random_type: str) -> int:
        return self._get(self._integers, random_type)

    def get_random_coord(self, random_type: str) -> Coord:
        x, y = self._get(self._coordinates, random_type)
        return Coord(x, y)

    def get_random_integer_from_generator(self, min: int, max: int) -> int:
        raise AssertionError("Test factory cannot call the real random generator")


class RandomFactoryBuilder:
    """Build isolated deterministic factories; unconfigured requests fail loudly."""

    def __init__(self):
        self._integers = {}
        self._coordinates = {}
        self._repeat_integers = set()
        self._repeat_coordinates = set()

    def set_integer(self, random_type: str, value: int) -> Self:
        self.set_integers(random_type, value)
        self._repeat_integers.add(random_type)
        return self

    def set_integers(self, random_type: str, *values: int) -> Self:
        if not values:
            raise ValueError("Provide at least one integer response")
        if any(type(value) is not int for value in values):
            raise TypeError("Integer responses must be integers")
        self._integers[random_type] = tuple(values)
        self._repeat_integers.discard(random_type)
        return self

    def set_coord(self, random_type: str, x: int, y: int) -> Self:
        self.set_coords(random_type, (x, y))
        self._repeat_coordinates.add(random_type)
        return self

    def set_coords(self, random_type: str, *values: tuple[int, int]) -> Self:
        if not values:
            raise ValueError("Provide at least one coordinate response")
        coordinates = []
        for x, y in values:
            if any(type(value) is not int for value in (x, y)):
                raise TypeError("Coordinate components must be integers")
            if not (0 <= x < gbl.MAX_QUADRANT_SECTOR_XY and 0 <= y < gbl.MAX_QUADRANT_SECTOR_XY):
                raise ValueError(f"Coordinate ({x}, {y}) is outside the galaxy/sector grid")
            coordinates.append((x, y))
        self._coordinates[random_type] = tuple(coordinates)
        self._repeat_coordinates.discard(random_type)
        return self

    def set_enemy_chance(self, value: int) -> Self:
        return self.set_integer(gbl.RIT_ENEMY_CHANCE, value)

    def set_star_quantity(self, value: int) -> Self:
        return self.set_integer(gbl.RIT_STAR_QUANTITY, value)

    def set_starbase_chance(self, value: int) -> Self:
        return self.set_integer(gbl.RIT_STARBASE_CHANCE, value)

    def set_starship_quadrant(self, x: int, y: int) -> Self:
        return self.set_coord(gbl.RCT_STARSHIP_QUADRANT, x, y)

    def set_starship_sector(self, x: int, y: int) -> Self:
        return self.set_coord(gbl.RCT_STARSHIP_SECTOR, x, y)

    def with_defaults(self) -> Self:
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
        for random_type, value in integers.items():
            self.set_integer(random_type, value)
        self.set_starship_quadrant(0, 0).set_starship_sector(0, 0)
        # Placements are deliberately explicit: repeated coordinates can collide.
        return self

    def build(self) -> RandomFactory:
        factory = _ConfiguredRandomFactory(self._integers, self._coordinates)
        for key in self._repeat_integers:
            factory._integers[key] = self._integers[key]
        for key in self._repeat_coordinates:
            factory._coordinates[key] = self._coordinates[key]
        return factory
