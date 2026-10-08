# Deterministic Test Factories

Use the shared helper before creating the galaxy or game:

```python
from source import gbl
from tests.randomFactoryBuilder import RandomFactoryBuilder
from tests.test_cli.gameBuilder import GameBuilder

factory = (
    RandomFactoryBuilder()
    .WithDefaults()
    .SetStarshipQuadrant(0, 0)
    .SetStarshipSector(0, 0)
    .SetEnemyChance(80)
    .SetCoords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
    .SetInteger(gbl.RIT_ENEMY_FIRED_AMOUNT, 20)
    .Build()
)
game = GameBuilder.getGame(factory)
```

`SetInteger(type, value)` and `SetCoord(type, x, y)` repeat the same
response on every request. `SetIntegers(type, *values)` and
`SetCoords(type, *coordinates)` return a finite sequence in order, then
raise an error. Sequences are independent for each request type and each
`Build()` call. Returned coordinates are fresh objects.

`WithDefaults()` resets earlier settings. Call it first, then override
the values relevant to the test. It provides an empty galaxy, Starship
at quadrant/sector (0, 0), Mission Time 0, enemy shields 100, enemy fire 10,
no random device damage or enemy movement, laser hits, and star destruction.
It does not configure enemy/star/starbase placement. When enabling those
objects, supply distinct locations that do not overlap Starship.
Supply enough sequence entries for every quadrant creation the test performs.

Without `WithDefaults()`, configure every required request explicitly.
Missing responses fail immediately; there is no fallback to real randomness.
The helper does not check integer game ranges, allowing deliberate invalid
integer inputs in tests. Coordinates must be valid grid positions.

The convenience setters are `SetEnemyChance`, `SetStarQuantity`,
`SetStarbaseChance`, `SetStarshipQuadrant`, and `SetStarshipSector`.
Use `SetInteger` for the other `gbl.RIT_*` keys and `SetCoord`/`SetCoords`
for other `gbl.RCT_*` keys.

Existing `GameBuilder.getGame()` calls must supply a factory. The builder
preserves the supplied factory for both galaxy generation and gameplay.

Run the helper tests with the root pytest configuration:

```powershell
.\venv2\Scripts\python.exe -m pytest -c pytest.ini -q tests\test_library\test_randomFactoryBuilder.py
```
