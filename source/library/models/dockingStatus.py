from dataclasses import dataclass


@dataclass
class DockingStatus:
    PreviousStatus:bool
    CurrentStatus:bool
