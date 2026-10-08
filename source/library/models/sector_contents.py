import gbl


class SectorContents:
    def __init__(self, sector_contents: str):
        self.sector_contents = sector_contents

    def has_enemy(self) -> bool:
        return self.sector_contents == gbl.SECTOR_ENEMY

    def has_starship(self) -> bool:
        return self.sector_contents == gbl.SECTOR_STARSHIP

    def has_star(self) -> bool:
        return self.sector_contents == gbl.SECTOR_STAR

    def has_starbase(self) -> bool:
        return self.sector_contents == gbl.SECTOR_STARBASE

    def is_empty(self) -> bool:
        return self.sector_contents == gbl.SECTOR_EMPTY
