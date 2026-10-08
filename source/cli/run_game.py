import sys
from pathlib import Path


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

# These imports follow the path bootstrap so the root launcher works without installation.
from cli.command_line import CommandLine  # noqa: E402
from factories import random_factory  # noqa: E402
from game.game import Game  # noqa: E402

import source.library.factories.other_factories as other_fact  # noqa: E402


class GameRunner:
    def get_game(self) -> Game:
        rand_factory = random_factory.RandomFactory()

        other_factories = other_fact.OtherFactories()
        curr_quad_factory = other_fact.CurrentQuadrantFactory()

        galaxy = other_factories.create_galaxy(rand_factory, curr_quad_factory)
        game = Game(galaxy, rand_factory, curr_quad_factory)

        return game

    def get_command_line(self) -> CommandLine:
        game = self.get_game()
        cl = CommandLine(game)
        return cl


def main() -> None:
    g = GameRunner()
    cl = g.get_command_line()
    print(cl.intro_message())

    game_done = False
    while not game_done:
        try:
            cmd = input("Command : ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if cmd.strip().upper() in {"QUIT", "EXIT"}:
            break

        resp = cl.execute_command_string(cmd)
        print(resp)
        if cl.game_over:
            game_done = True


if __name__ == "__main__":
    main()
