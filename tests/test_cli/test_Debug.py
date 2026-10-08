# region imports
import sys

from cli import CLI_Messages, commandLine

from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")

# endregion

def test_Debug_CheckOK():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    resp = cl.executeCommandString("DEBUG CHECK")

    assert resp == CLI_Messages.DebugCommandOK

def test_Debug_CheckLowerCaseOK():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    resp = cl.executeCommandString("debug check")

    assert resp == CLI_Messages.DebugCommandOK

def test_Debug_SetGet_SectorContents():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    contents = "STARSHIP"

    resp = cl.executeCommandString(f"DEBUG SET CURRENTQUADRANT SECTOR 0 0 {contents}")
    data = cl.executeCommandString("DEBUG GET CURRENTQUADRANT SECTOR 0 0")

    assert resp is not None
    assert data == contents

def test_Debug_SetGet_SectorEnemy():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    shieldLevel = "1000"

    resp = cl.executeCommandString(f"DEBUG SET CURRENTQUADRANT ENEMY 0 0 {shieldLevel}")
    data = cl.executeCommandString("DEBUG GET CURRENTQUADRANT ENEMY 0 0")

    assert resp is not None
    assert data == "ENEMY:" + shieldLevel

def test_Debug_SetGet_QuadrantNumEnemies():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    numEnemies = "3"

    resp = cl.executeCommandString(f"DEBUG SET QUADRANT 0 0 NUMENEMIES {numEnemies}")
    data = cl.executeCommandString("DEBUG GET QUADRANT 0 0 NUMENEMIES")

    assert resp is not None
    assert data == numEnemies

def test_Debug_SetGet_QuadrantNumStars():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = "5"

    resp = cl.executeCommandString(f"DEBUG SET QUADRANT 0 0 NUMSTARS {value}")
    data = cl.executeCommandString("DEBUG GET QUADRANT 0 0 NUMSTARS")

    assert resp is not None
    assert data == value

def test_Debug_SetGet_QuadrantStarbase():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = "1"

    resp = cl.executeCommandString(f"DEBUG SET QUADRANT 0 0 STARBASE {value}")
    data = cl.executeCommandString("DEBUG GET QUADRANT 0 0 STARBASE")

    assert resp is not None
    assert data == value

def test_Debug_SetGet_QuadrantExplored():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = "1"

    resp = cl.executeCommandString(f"DEBUG SET QUADRANT 0 0 EXPLORED {value}")
    data = cl.executeCommandString("DEBUG GET QUADRANT 0 0 EXPLORED")

    assert resp is not None
    assert data == value

def test_Debug_SetGet_StarshipEnergy():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = 2000

    resp = cl.executeCommandString(f"DEBUG SET STARSHIP ENERGY {value}")
    data = cl.executeCommandString("DEBUG GET STARSHIP ENERGY")

    assert resp is not None
    assert data == str(value)

def test_Debug_SetGet_StarshipShield():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = 2000

    resp = cl.executeCommandString(f"DEBUG SET STARSHIP SHIELD {value}")
    data = cl.executeCommandString("DEBUG GET STARSHIP SHIELD")

    assert resp is not None
    assert data == str(value)

def test_Debug_SetGet_StarshipTorp():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = 2000
    #srsData2 = cl.game.srs()
    #print(srsData2, file=sys.stderr)


    #srsData = cl.executeCommandString("SRS")
    #print(srsData, file=sys.stderr)

    resp = cl.executeCommandString(f"DEBUG SET STARSHIP TORP {value}")
    data = cl.executeCommandString("DEBUG GET STARSHIP TORP")

    assert resp is not None
    assert data == str(value)

def test_Debug_SetGet_StarshipDeviceDamage():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    deviceName = "TOR"
    damageAmt = "-3.0"

    resp = cl.executeCommandString(f"DEBUG SET STARSHIP DEVICE {deviceName} {damageAmt}")
    data = cl.executeCommandString(f"DEBUG GET STARSHIP DEVICE {deviceName}")

    assert resp is not None
    assert data == damageAmt

def test_Debug_SetGet_StarshipSector():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    x = "1"
    y = "2"

    resp = cl.executeCommandString(f"DEBUG SET STARSHIP SECTOR {x} {y}")
    data = cl.executeCommandString("DEBUG GET STARSHIP SECTOR")

    assert resp is not None
    assert data == f"{x}.{y}"

def test_Debug_SetGet_StarshipQuadrant():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    x = "2"
    y = "3"

    resp = cl.executeCommandString(f"DEBUG SET STARSHIP QUADRANT {x} {y}")
    data = cl.executeCommandString("DEBUG GET STARSHIP QUADRANT")

    assert resp is not None
    assert data == f"{x}.{y}"

def test_Debug_SetGet_GalaxyMissionTime():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = "1234.0"

    resp = cl.executeCommandString(f"DEBUG SET GALAXY MISSION_TIME {value}")
    data = cl.executeCommandString("DEBUG GET GALAXY MISSION_TIME")

    assert resp is not None
    assert data == value

def test_Debug_SetGet_GalaxyMissionTimeDeadline():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    value = "1234.0"

    resp = cl.executeCommandString(f"DEBUG SET GALAXY MISSIONTIMEDEADLINE {value}")
    data = cl.executeCommandString("DEBUG GET GALAXY MISSIONTIMEDEADLINE")

    assert resp is not None
    assert data == value

def test_Debug_SetClearSector_ALL():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")

    # if it doesn't get an error, then we're good

def test_Debug_SetClearSector_NotALL():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ")

    # if it doesn't get an error, then we're good

