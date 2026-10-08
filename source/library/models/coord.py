import uuid


class Coord:
    id = uuid.uuid4()
    x = 0
    y = 0

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def to_string(self) -> str:
        return f"({self.x},{self.y})"
