import uuid

from models import coord


class Quadrant:
    def __init__(self, coord: coord.Coord, numEnemies: int, numStars: int):
        self.id = uuid.uuid4()
        self.Coord = coord
        self.NumEnemies = numEnemies
        self.NumStars = numStars
        self.HasBeenExplored = False
        self.HasStarBase = False
