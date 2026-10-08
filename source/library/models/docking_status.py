from dataclasses import dataclass


@dataclass
class DockingStatus:
    previous_status: bool
    current_status: bool
