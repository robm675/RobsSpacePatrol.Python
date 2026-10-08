from pathlib import Path
import sys


def _ensure_project_paths() -> None:
    project_root = Path(__file__).resolve().parents[2]
    entries = [
        project_root,
        project_root / "source",
        project_root / "source" / "library",
        project_root / "source" / "library" / "factories",
    ]
    for entry in reversed(entries):
        entry_str = str(entry)
        if entry_str not in sys.path:
            sys.path.insert(0, entry_str)


_ensure_project_paths()

from cli.commandLine import CommandLine
from factories import randomFactory
from game.game import Game
import source.library.factories.otherFactories as otherFact


class runGame:
    def getGame(self) -> Game:
        randFactory = randomFactory.RandomFactory()

        otherFactories = otherFact.otherFactories()
        currQuadFactory = otherFact.CurrentQuadrantFactory()

        galaxy = otherFactories.createGalaxy(randFactory, currQuadFactory)
        game = Game(galaxy, randFactory, currQuadFactory)

        return game

    def getCommandLine(self) -> CommandLine:
        game = self.getGame()
        cl = CommandLine(game)
        return cl


def main() -> None:
    g = runGame()
    cl = g.getCommandLine()
    print(cl.introMessage())

    gameDone = False
    while not gameDone:
        try:
            cmd = input("Command : ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if cmd.strip().upper() in {"QUIT", "EXIT"}:
            break

        resp = cl.executeCommandString(cmd)
        print(resp)
        if cl.GameOver:
            gameDone = True


if __name__ == "__main__":
    main()
