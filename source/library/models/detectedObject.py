from models import coord


class detectedObject:
    def __init__(self, object: str, dist: float, finalCoord: coord.Coord, trackingCoords: list):
        self.object = object
        self.dist = dist
        self.trackingCoords = trackingCoords
        self.finalCoord = finalCoord