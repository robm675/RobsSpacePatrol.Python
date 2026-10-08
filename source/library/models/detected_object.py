from models import coord


class DetectedObject:
    def __init__(self, object: str, dist: float, final_coord: coord.Coord, tracking_coords: list):
        self.object = object
        self.dist = dist
        self.tracking_coords = tracking_coords
        self.final_coord = final_coord
