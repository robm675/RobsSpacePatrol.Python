# Deterministic Test Factories

Use the shared helper before creating the galaxy or game:

```python
from source import gbl
from tests.random_factory_builder import RandomFactoryBuilder
from tests.test_cli.game_builder import GameBuilder

factory = (
    RandomFactoryBuilder()
    .with_defaults()
    .set_starship_quadrant(0, 0)
    .set_starship_sector(0, 0)
    .set_enemy_chance(80)
    .set_coords(gbl.RCT_ENEMY_LOCATION, (0, 1), (0, 2), (0, 3))
    .set_integer(gbl.RIT_ENEMY_FIRED_AMOUNT, 20)
    .build()
)
game = GameBuilder.get_game(factory)
```

`set_integer(type, value)` and `set_coord(type, x, y)` repeat the same
response on every request. `set_integers(type, *values)` and
`set_coords(type, *coordinates)` return a finite sequence in order, then
raise an error. Sequences are independent for each request type and each
`build()` call. Returned coordinates are fresh objects.

`with_defaults()` resets earlier settings. Call it first, then override
the values relevant to the test. It provides an empty galaxy, Starship
at quadrant/sector (0, 0), Mission Time 0, enemy shields 100, enemy fire 10,
no random device damage or enemy movement, laser hits, and star destruction.
It does not configure enemy/star/starbase placement. When enabling those
objects, supply distinct locations that do not overlap Starship.
Supply enough sequence entries for every quadrant creation the test performs.

Without `with_defaults()`, configure every required request explicitly.
Missing responses fail immediately; there is no fallback to real randomness.
The helper does not check integer game ranges, allowing deliberate invalid
integer inputs in tests. Coordinates must be valid grid positions.

The convenience setters are `set_enemy_chance`, `set_star_quantity`,
`set_starbase_chance`, `set_starship_quadrant`, and `set_starship_sector`.
Use `set_integer` for the other `gbl.RIT_*` keys and `set_coord`/`set_coords`
for other `gbl.RCT_*` keys.

Existing `GameBuilder.get_game()` calls must supply a factory. The builder
preserves the supplied factory for both galaxy generation and gameplay.

Run the helper tests with the root pytest configuration:

```powershell
.\.venv\Scripts\python.exe -m pytest -c pytest.ini -q tests\test_library\test_random_factory_builder.py
```
