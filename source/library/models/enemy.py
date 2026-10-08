import uuid


class Enemy:
    def __init__(self, shieldLevel: int):
        id = uuid.uuid4
        self.shieldLevel = shieldLevel
