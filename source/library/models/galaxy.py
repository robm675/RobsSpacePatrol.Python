import gbl
from models.sector import Sector

import source.library.models.currentQuadrant as cq
import source.library.models.starship as ent
import source.library.models.quadrant as q
from source.library.models import coord


class Galaxy:
    Starship: ent.Starship
    CurrentQuadrant: cq.CurrentQuadrant
    MissionTime: float
    MissionTimeDeadline: float
    Quadrants: list[q.Quadrant]

    def __init__(self):
        self.Quadrants = []
        self.Starship = ent.Starship()
        self.MissionTime = 0
        self.MissionTimeDeadline = 0

    def GetQuadrant(self, x:int, y:int) -> q.Quadrant:
        #print(f"quadrants: {self.Quadrants}", file=sys.stderr)
        data = [s for s in self.Quadrants if s.Coord.x == x and s.Coord.y == y]
        #print(f"data={data}", file=sys.stderr)
        return data[0]

    def GetQuadrantByCoord(self, coord: coord.Coord) -> q.Quadrant:
        data = [s for s in self.Quadrants if s.Coord.x == coord.x and s.Coord.y == coord.y]
        return data[0]

    def GetExploredQuadrant(self) -> list[q.Quadrant]:
        data = [s for s in self.Quadrants if s.HasBeenExplored]
        return data

    def GetStarbasesRemaining(self) -> int:
        sbs = [s for s in self.Quadrants if s.HasStarBase]
        return len(sbs)

    def GetStarshipSector(self) -> Sector:
        data = [s for s in self.CurrentQuadrant.sectors if s.sectorContents.sectorContents == gbl.SECTOR_STARSHIP]
        # print(f"numsectors: {len(self.CurrentQuadrant.sectors)}")
        if len(data) == 0:
            raise RuntimeError("starship not found in galaxy.getstarshipsector")
        return data[0]

    def GetStarshipQuadrant(self) -> q.Quadrant:
        return self.GetQuadrant(self.CurrentQuadrant.coord.x, self.CurrentQuadrant.coord.y)
