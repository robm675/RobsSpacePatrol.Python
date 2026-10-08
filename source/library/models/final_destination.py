from models import coord


class FinalDestination:
    def __init__(
        self,
        final_quadrant: coord.Coord,
        final_sector: coord.Coord,
        outside_galaxy: bool,
        object_hit: bool,
    ):
        self.final_quadrant = final_quadrant
        self.final_sector = final_sector
        self.out_side_galaxy = outside_galaxy
        self.object_hit = object_hit
