# Rob's Space Patrol

A command-line space game written in Python. Explore an 8-by-8 galaxy,
manage your ship's energy and shields, and destroy the remaining enemies
before the mission deadline.

This is a personal learning and portfolio project. I independently wrote
the original implementation in C# and subsequently ported my own
implementation to Python.

I created this project to apply what I learned in a Python class,
while porting the game and writing unit tests.

## Prerequisites

- Python 3.11 or newer. Development and tests have been verified locally
  with Python 3.14 on Windows; other versions and operating systems have
  not yet been verified.
- A terminal. The examples below use Windows PowerShell.
- Git, if you want to clone the repository.

IntelliJ IDEA and VS Code are optional. The game runs from the command line.
The game uses Python's standard library; the packages in
`requirements-dev.txt` are for running the tests and checking code style.

## Setup

```powershell
git clone https://github.com/robm675/RobsSpacePatrol.Python.git
cd RobsSpacePatrol.Python
```

If you already have the project locally, open PowerShell in its root folder
instead. Run all commands below from that folder.

Create a virtual environment and install the test dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

These commands call the environment's Python directly, so activating the
environment is not required. If you already use an environment named
`venv2`, substitute `venv2` for `.venv` in the commands below.

## Run

```powershell
.\.venv\Scripts\python.exe run_game.py
```

Enter commands at the `Command :` prompt. Commands are case-insensitive.
Type `QUIT` or `EXIT` to leave the game, or press Ctrl+C.

## Controls

Coordinates are zero-based; quadrant and sector coordinates range from
0 through 7. Mission Time starts at zero and advances as actions are taken.

| Command | Description and example |
| --- | --- |
| `NAV <direction> <distance>` | Moves the starship in the specified direction and distance.  Enter without parameters to view the direction guide. |
| `SRS` | Displays a text grid of the sectors in the current quadrant. |
| `LRS` | Displays a text grid summarizing neighboring quadrants. |
| `SHE <amount>` | Sets shields to a nonnegative integer level, transferring energy between shields and the ship's energy reserve. Use `SHE 0` to lower shields. |
| `LAS <amount>` | Fires lasers using a positive integer energy amount, divided among enemies in the current quadrant. Hits weaken with distance. Example: `LAS 100`. |
| `TOR <direction>` | Fires a torpedo in the given direction. Enter `TOR` without parameters for the direction guide. |
| `COM REC` | Displays the galaxy as a text grid. Contents of unexplored quadrants are hidden. |
| `COM STA` | Displays the current status |
| `COM TOR` | Calculates the directions to each of the enemies in the current quadrant |
| `COM STB` | Calculates the direction and distance to the starbase in the current quadrant |
| `COM NAV <quadrant-x> <quadrant-y> <sector-x> <sector-y>` | Calculates the direction and distance from your position to the given quadrant and sector coordinates |
| `DAM` | Displays damaged devices and their remaining repair time in Mission Time units. |
| `QUIT` / `EXIT` | Exit the game. |

The direction guide uses `1` for east, `3` for north, `5` for west, and `7`
for south, with intermediate directions between them. Navigation distance
is measured in quadrants; one quadrant spans eight sectors. For example,
`NAV 1 0.5` moves east by half a quadrant if the route is clear. The maximum
distance range is 0.1 to 8; a damaged navigation system limits travel to 0.2.

Moving next to a starbase with shields lowered docks the ship during routine
maintenance. Starbases replenish energy and torpedoes. If devices are damaged,
you can authorize repairs when prompted; these repairs advance Mission Time.

Destroy all enemies before the Mission Time deadline to win. Losing your ship,
running out of usable energy, or exceeding the deadline ends the mission.

Developer/debug commands are also available. Enter `DEBUG` without parameters
to view them; they can change game state and bypass normal gameplay.

## Tests

Run the suite using the root pytest configuration:

```powershell
.\.venv\Scripts\python.exe -m pytest -c pytest.ini -q
```

Show each test's name and result, plus a summary of failures:

```powershell
.\.venv\Scripts\python.exe -m pytest -c pytest.ini -v -ra
```

Show and save the output to a separate file for each run:

```powershell
$testLog = "pytest-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
.\.venv\Scripts\python.exe -m pytest -c pytest.ini -v -ra 2>&1 |
    Tee-Object -FilePath $testLog
```

Add `-s` to include debug `print()` output. Add `-x` to stop at the first
failure. Run a single file by adding its path, for example
`tests\test_library\test_routine_maint.py`.

The suite exercises game calculations, command handling, combat,
maintenance, and factory behavior. Tests use configurable deterministic
factories for repeatable scenarios; normal gameplay uses the real random
factory.

## Project Layout

- `run_game.py`: command-line entry point.
- `source/cli/`: command parsing and terminal output.
- `source/library/`: game logic, models, factories, and calculation utilities.
- `source/gbl.py`: shared constants and configuration values.
- `tests/`: CLI and game-library tests, plus deterministic factory helpers.
- `requirements-dev.txt`: pinned test and code-style dependencies.
- `pyproject.toml`: Ruff formatting and lint configuration.

## Code Style

Modules, functions, methods, and variables use `snake_case`; classes use
`PascalCase`; constants and enum members use `UPPER_SNAKE_CASE`. Game commands
such as `NAV`, `LAS`, and `COM STA` are unchanged.

Check formatting and lint without changing source files:

```powershell
.\.venv\Scripts\python.exe -m ruff format --check source tests run_game.py
.\.venv\Scripts\python.exe -m ruff check source tests run_game.py
```

To apply formatting:

```powershell
.\.venv\Scripts\python.exe -m ruff format source tests run_game.py
```

Then review the diff and run the tests. See
[the test factory examples](tests/random_factory_builder.md) for the helper API.

## Current Limitations

- This is a text-only learning project, not a finished commercial game.
- Only local Windows execution has been verified so far.

## Inspiration and Authorship

Inspired by classic text-based space games. I independently wrote the
original game in C#, then ported my own implementation to Python. I did
not copy code from the inspiration project.

In particular, I acknowledge Mike Mayfield's classic text-based *Star Trek*
game as an inspiration. A historical listing crediting Mayfield and Centerline
Engineering is preserved in the
[Computer History Museum's archive](https://archive.computerhistory.org/resources/access/text/2017/09/102661095/102661095-05-v4-n4-acc.pdf).
This project is not affiliated with or endorsed by the Star Trek rights holders.

## License

Copyright (c) 2026 Rob. This project's original code is licensed under the
[MIT License](LICENSE). You may use, modify, and redistribute it, including
commercially, subject to the license's terms. The software is provided without
warranty.

Development dependencies are listed in `requirements-dev.txt`; their own licenses
remain applicable to those packages.
