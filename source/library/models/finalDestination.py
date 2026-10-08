from models import coord


class FinalDestination:
    def __init__(self, finalQuadrant: coord.Coord, finalSector: coord.Coord, outsideGalaxy: bool, objectHit: bool):
        self.FinalQuadrant = finalQuadrant
        self.FinalSector = finalSector
        self.OutSideGalaxy = outsideGalaxy
        self.ObjectHit = objectHit
