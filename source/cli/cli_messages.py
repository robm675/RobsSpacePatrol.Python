from typing import Final

ERROR_MESSAGE: Final[str] = "**ERROR**"
INTERNAL_ERROR_MESSAGE: Final[str] = "**Internal Error Has Occurred**"

UNKNOWN_COMMAND: Final[str] = "Unknown Command: "

DEBUG_COMMAND_OK: Final[str] = "OK"
DEBUG_UNKNOWN_COMMAND: Final[str] = "Unknown debug command"
DEBUG_ERROR_IN_COMMAND: Final[str] = "There was an error in the debug command"
DEBUG_INVALID_COMMAND: Final[str] = "Invalid debug command or parameter"

WARNING_MESSAGE_SHIELD_DOWN_IN_COMBAT_AREA: Final[str] = (
    "Warning! Shields dangerously low in a combat area!"
)

DAM_DAMAGE_REPORT: Final[str] = "Damage report:"
DAM_DAMAGE_REPORT_NO_DAMAGES: Final[str] = "No damages - All devices functional"

SRS_DAMAGED: Final[str] = "Short range sensors damaged"

LRS_DAMAGED: Final[str] = "Long range sensors damaged"

SHE_MISSING_AMOUNT: Final[str] = "Invalid shield command - missing amount"
SHE_INVALID_AMOUNT: Final[str] = "Invalid SHE amount: "
SHE_CHANGED: Final[str] = "Shield level changed to: "
SHE_DAMAGED: Final[str] = "Shield control damaged"

LAS_MISSING_AMOUNT: Final[str] = "Invalid LAS command - missing amount"
LAS_INVALID_AMOUNT: Final[str] = "Invalid LAS amount: "
LAS_FIRED: Final[str] = "Lasers fired "
LAS_HIT: Final[str] = " hit on enemy in sector["
LAS_ENEMY_DESTROYED: Final[str] = "] Enemy destroyed!"
LAS_SENSORS_INDICATE: Final[str] = "] (Sensors indicate "
LAS_REMAINING: Final[str] = " remaining)"
LAS_DAMAGED: Final[str] = "Laser control damaged"
LAS_INSUFFICIENT_ENERGY: Final[str] = "Insufficient energy"
LAS_NO_ENEMIES: Final[str] = "No enemies in quadrant"

TOR_MISSING_DIRECTION: Final[str] = "Invalid TOR command - missing direction"
TOR_INVALID_DIRECTION: Final[str] = "Invalid TOR direction: "
TOR_FIRED: Final[str] = "Torpedo fired! "
TOR_ENEMY_AT_SECTOR: Final[str] = "Enemy at sector ["
TOR_DESTROYED: Final[str] = "] destroyed!"
TOR_DAMAGED: Final[str] = "Torpedo control damaged"
TOR_EXPENDED: Final[str] = "All torpedos expended"
TOR_MISSED: Final[str] = "Torpedo missed!"
TOR_NO_ENEMIES: Final[str] = "No enemies found in quadrant"
TOR_STAR_DESTROYED: Final[str] = "Star destroyed! "
TOR_STAR_ABSORBED_TORP: Final[str] = "Star absorbed torpedo! "
TOR_STARBASE_DESTROYED: Final[str] = "Starbase destroyed!"

CPU_DAMAGED: Final[str] = "Computer damaged"
CPU_NAV_INVALID: Final[str] = "Invalid CPU NAV command"
CPU_NAV_INVALID_QX: Final[str] = "Invalid CPU NAV quadrant x:"
CPU_NAV_INVALID_QY: Final[str] = "Invalid CPU NAV quadrant y:"
CPU_NAV_INVALID_SX: Final[str] = "Invalid CPU NAV sector x:"
CPU_NAV_INVALID_SY: Final[str] = "Invalid CPU NAV sector y:"
CPU_NAV_INVALID_COORD: Final[str] = "Invalid target coordinates"
CPU_NAV_DIR: Final[str] = "Direction: "
CPU_NAV_DIST: Final[str] = " Distance: "
CPU_TOR_ENEMY_AT_SECTOR: Final[str] = "Enemy at sector ["
CPU_TOR_IS_BEARING: Final[str] = "] is bearing "
CPU_TOR_NO_ENEMIES: Final[str] = "No enemies in sector."
CPU_STB_NO_STARBASES: Final[str] = "No starbases in quadrant."
CPU_STB_STARBASE_FOUND_IN_SECTOR: Final[str] = "Starbase found in sector ["
CPU_STB_DIR: Final[str] = "Direction: "
CPU_STB_DIST: Final[str] = " Distance: "
CPU_INVALID_COMMAND: Final[str] = "Invalid CPU command"
CPU_STA_MISSION_TIME: Final[str] = "Mission Time: \t\t"
CPU_STA_QUADRANT: Final[str] = "Quadrant: \t\t"
CPU_STA_SECTOR: Final[str] = "Sector: \t\t"
CPU_STA_DEVICE_STATUS: Final[str] = "Device status:"
CPU_STA_ENEMIES_REMAINING: Final[str] = "Enemies remaining: \t"
CPU_STA_STARBASES_REMAINING: Final[str] = "Starbase remaining: \t"
CPU_STA_ENERGY_REMAINING: Final[str] = "Energy:\t\t\t"
CPU_STA_SHIELD_LEVEL: Final[str] = "Shields:\t\t"
CPU_STA_TORP_REMAINING: Final[str] = "Torpedos:\t\t"
CPU_STA_DOCKED: Final[str] = "Docked status:\t\t"
CPU_STA_MISSION_TIME_REMAINING: Final[str] = "Time remaining:\t\t"

NAV_INVALID_COMMAND: Final[str] = "Invalid NAV command"
NAV_INVALID_DIR_VALUE: Final[str] = "Invalid NAV DIR value: "
NAV_INVALID_DIST_VALUE: Final[str] = "Invalid NAV DIST value: "
NAV_OUTSIDE_GALAXY: Final[str] = (
    "Warp drive cancelled - Navigation outside the galaxy is not permitted."
)
NAV_WARP_DRIVE_DAMAGED: Final[str] = "Warp drives damaged - Maximum speed is 0.2"
NAV_INVALID_DIR: Final[str] = "Invalid NAV Direction: "
NAV_INVALID_DIST: Final[str] = "Invalid NAV Distance: "
NAV_IMPULSE_ENGAGED: Final[str] = "Impulse engaged"
NAV_WARP_ENGAGED: Final[str] = "Warp drive engaged"
NAV_IMPULSE_ENGINE_SHUT_DOWN: Final[str] = "Impulse engines shut down at sector [ "
NAV_BAD_NAVIGATION: Final[str] = "] due to bad navigation"
NAV_NOT_ENOUGH_ENERGY_SHIELD_ENERGY_AVAIL: Final[str] = (
    "Insufficient energy to make the trip, but there is shield energy available"
)

MAINT_DOCKED: Final[str] = "The Starship is docked with the starbase."
MAINT_TECH_WAITING: Final[str] = "Technicians are waiting to repair damages."
MAINT_IT_WILL_TAKE: Final[str] = "It will take "
MAINT_MISSION_TIME: Final[str] = " mission time units."
MAINT_REPLY_YES: Final[str] = "Reply 'YES' to make the repairs."
MAINT_REPAIRS_MADE: Final[str] = "Repairs complete."
MAINT_REPAIRS_COMPLETE: Final[str] = "Repairs are complete on "
MAINT_ENEMY_FIRED_SHIELD_HIT: Final[str] = (
    "Enemy fired! {0} hit from enemy in sector [{1}].  Shield level now {2}."
)
MAINT_ENEMY_FIRED_PROTECTED: Final[str] = "Enemy fired! {0} hit from enemy in sector [{1}]."
MAINT_STARBASE_SHIELDS_PROTECTED: Final[str] = "Starbase shields are protecting the Starship."
MAINT_DEVICE_DAMAGED: Final[str] = " has been damaged. "
MAINT_ENEMY_FIRED_STARSHIP_DESTROYED: Final[str] = (
    "Enemy fired!  {0} hit from enemy in sector [{1}].  Starship was destroyed!!!"
)
MAINT_MISSION_TIME_TO_REPAIR: Final[str] = " mission time units to repair."
MAINT_NEW_QUADRANT_ENEMIES_RED_ALERT: Final[str] = "Enemies in this quadrant, RED ALERT!"
MAINT_ENEMY_MOVED: Final[str] = "Enemy moved!  Enemy at sector [{0}] moved to sector [{1}]"

END_MISSION_FAILED_STARSHIP_DESTROYED: Final[str] = (
    "Mission failed: Starship was destroyed!  Space Command will be conquered."
)
END_MISSION_FAILED_RAN_OUT_OF_ENERGY: Final[str] = (
    "Mission failed: Starship ran out of energy, and is left stranded.  Space Command will be conquered."
)
END_MISSION_FAILED_RAN_OUT_OF_TIME: Final[str] = (
    "Mission failed: You ran out of time, Space Command will be conquered."
)
END_MISSION_FAILED_QUIT: Final[str] = (
    "Mission failed: You abandoned your post, Space Command will be conquered."
)
END_MISSION_ACCOMPLISHED: Final[str] = "Mission accomplished!  All enemy ships were destroyed!"
END_ENERGY_GONE_SHIELD_ENERGY_AVAIL: Final[str] = (
    "Insufficient energy, but can be transferred from shield control."
)
