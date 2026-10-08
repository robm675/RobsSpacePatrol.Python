import sys
import uuid

sys.path.append("/pythontrek/source/library/")
sys.path.append("/pythontrek/source/")
import gbl


class SectorContents:
    def __init__(self, sectorContents: str):
        id = uuid.uuid4
        self.sectorContents = sectorContents
        
    def hasEnemy(self) -> bool:
        return self.sectorContents == gbl.SECTOR_ENEMY
    
    def hasStarship(self) -> bool:
        return self.sectorContents == gbl.SECTOR_STARSHIP
    
    def hasStar(self) -> bool:
        return self.sectorContents == gbl.SECTOR_STAR
    
    def hasStarbase(self) -> bool:
        return self.sectorContents == gbl.SECTOR_STARBASE

    def isEmpty(self) -> bool:
        return self.sectorContents == gbl.SECTOR_EMPTY
    
