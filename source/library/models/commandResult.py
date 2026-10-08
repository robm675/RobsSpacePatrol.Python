from enum import Enum


class CommandResult(Enum):
    OK = 0
    Damaged = 1
    TOR_Missed = 2
    CPU_STB_No_Starbase_Present = 3
    No_Enemies_Present = 4
    InsufficientInventory = 5
    Error = 6
    Empty = 7