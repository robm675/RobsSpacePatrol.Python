import uuid

from models import coord


class Quadrant:
    def __init__(self, coord: coord.Coord, num_enemies: int, num_stars: int):
        self.id = uuid.uuid4()
        self.coord = coord
        self.num_enemies = num_enemies
        self.num_stars = num_stars
        self.has_been_explored = False
        self.has_star_base = False
