# region imports
import sys

from cli import CLI_Messages, commandLine

import gbl
from tests.test_cli import gameBuilder
from tests.randomFactoryBuilder import RandomFactoryBuilder

sys.path.append("/pythontrek/source/library/")


# endregion

def test_RoutineMaint_EnemyFiredCoords():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetEnemyChance(80)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.executeCommandString("SRS")

    print(res, file=sys.stderr)

    assert "0,5" in res

def test_RoutineMaint_EnemyDestroyed_NoWarningMessage():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 0")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")

    res = cl.executeCommandString("SRS")

    print(f"[{res}]")
    assert CLI_Messages.WarningMessageShieldDownInCombatArea not in res

def test_RoutineMaint_ThreeEnemiesFired():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetEnemyChance(80)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.executeCommandString("SRS")

    print(f"[{res}]")

    assert "0,5" in res
    assert "0,6" in res
    assert "0,7" in res

def test_RoutineMaint_ProtectedByStarbase():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetEnemyChance(80)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))        
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    # print(game.getCurrentQuadrantFormatted())

    res = cl.executeCommandString("SRS")

    # print(f"[{res}]")

    assert CLI_Messages.MAINT_StarbaseShieldsProtected in res

def test_RoutineMaint_ProtectedByStarbase_Repeatedly():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetEnemyChance(80)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))          
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 1 STARBASE ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE OFF")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = ""
    res += cl.executeCommandString("SRS")
    res += cl.executeCommandString("SRS")
    res += cl.executeCommandString("SRS")
    res += cl.executeCommandString("SRS")

    assert CLI_Messages.MAINT_StarbaseShieldsProtected in res
    assert res.count(CLI_Messages.MAINT_StarbaseShieldsProtected) == 12

def test_RoutineMaint_DeviceRepaired():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetEnemyChance(80)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))            
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")
    cl.executeCommandString("DEBUG SET STARSHIP DEVICE TOR -.1")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")


    res = cl.executeCommandString("SRS")


    assert CLI_Messages.MAINT_RepairsComplete in res

def test_RoutineMaint_DeviceRepaired_NotRepeated():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")
    cl.executeCommandString("DEBUG SET STARSHIP DEVICE TOR -.1")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")

    print(game.getCurrentQuadrantFormatted())

    res = cl.executeCommandString("SRS")
    res = cl.executeCommandString("SRS")


    assert CLI_Messages.MAINT_RepairsComplete not in res

def test_RoutineMaint_EnemiesMoved():
    randomFactory = (
        RandomFactoryBuilder()
        .WithDefaults()
        .SetEnemyChance(80)
        .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 1), (1, 2))           
        .Build()
    )
    game = gameBuilder.GameBuilder.getGame(randomFactory)
    cl = commandLine.CommandLine(game)

    cl.executeCommandString("DEBUG SET CLEARCQ ALL")
    cl.executeCommandString("DEBUG SET STARSHIP SHIELD 1000")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT SECTOR 0 0 STARSHIP ")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 7 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 6 100")
    cl.executeCommandString("DEBUG SET CURRENTQUADRANT ENEMY 0 5 100")
    cl.executeCommandString("DEBUG SET ENEMYMOVE FORCE")
    cl.executeCommandString("DEBUG SET PREVENTENEMYFIRE ON")
    cl.executeCommandString("DEBUG SET GALAXY MISSIONTIMEDEADLINE 2600")

    res = cl.executeCommandString("SRS")

    assert "Enemy moved!" in res
    assert CLI_Messages.MAINT_TechWaiting not in res
