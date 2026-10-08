import gbl
from models.sector import Sector

import source.library.models.current_quadrant as cq
import source.library.models.quadrant as q
import source.library.models.starship as ent
from source.library.models import coord


class Galaxy:
    starship: ent.Starship
    current_quadrant: cq.CurrentQuadrant
    mission_time: float
    mission_time_deadline: float
    quadrants: list[q.Quadrant]

    def __init__(self):
        self.quadrants = []
        self.starship = ent.Starship()
        self.mission_time = 0
        self.mission_time_deadline = 0

    def get_quadrant(self, x: int, y: int) -> q.Quadrant:
        data = [s for s in self.quadrants if s.coord.x == x and s.coord.y == y]
        return data[0]

    def get_quadrant_by_coord(self, coord: coord.Coord) -> q.Quadrant:
        data = [s for s in self.quadrants if s.coord.x == coord.x and s.coord.y == coord.y]
        return data[0]

    def get_explored_quadrant(self) -> list[q.Quadrant]:
        data = [s for s in self.quadrants if s.has_been_explored]
        return data

    def get_starbases_remaining(self) -> int:
        sbs = [s for s in self.quadrants if s.has_star_base]
        return len(sbs)

    def get_starship_sector(self) -> Sector:
        data = [
            s
            for s in self.current_quadrant.sectors
            if s.sector_contents.sector_contents == gbl.SECTOR_STARSHIP
        ]
        if len(data) == 0:
            raise RuntimeError("starship not found in galaxy.getstarshipsector")
        return data[0]

    def get_starship_quadrant(self) -> q.Quadrant:
        return self.get_quadrant(self.current_quadrant.coord.x, self.current_quadrant.coord.y)
