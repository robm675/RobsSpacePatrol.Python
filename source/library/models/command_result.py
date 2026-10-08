from enum import Enum


class CommandResult(Enum):
    OK = 0
    DAMAGED = 1
    TOR_MISSED = 2
    CPU_STB_NO_STARBASE_PRESENT = 3
    NO_ENEMIES_PRESENT = 4
    INSUFFICIENT_INVENTORY = 5
    ERROR = 6
    EMPTY = 7
