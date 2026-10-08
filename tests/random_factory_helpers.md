# Per-File Factory Helpers

Each file that used `mock_random_int` or `mock_random_coord` now has a
`create_random_factory()` helper. It uses `RandomFactoryBuilder` and returns
a built factory, ready for galaxy creation and gameplay. Tests use these
helpers or configure `RandomFactoryBuilder` directly.

In a test in the same file, replace its factory setup and method overrides
with:

```python
test_factory = create_random_factory()
```

Keep passing that same object to `create_galaxy()` and `Game()`. Do not add
the old `get_random_integer = MagicMock()` / `get_random_coord = MagicMock()`
assignments afterward: those replace the configured responses.

| File | Scenario options |
| --- | --- |
| `test_galaxy_factory.py` | Original quadrant (2, 3), sector (4, 5), one enemy and a starbase |
| `test_current_quadrant_builder.py` | Original object locations for explicit quadrant construction |
| `test_quadrant_factory.py` | Three stars, one enemy, and a starbase |
| `test_calculation_utils.py` | Starship-sector lookup returns (1, 2) |
| `test_com_nav.py` | Default empty galaxy; `no_enemies=True` selects the old two-star variant |
| `test_com_sta.py` | Three enemies, two stars, starbase at (4, 6) |
| `test_com_stb.py` | `no_starbase=True` |
| `test_com_tor.py` | `no_enemies=True` |
| `test_dam.py` | `no_enemies=True` |
| `test_lrs.py` | `corner=True` selects quadrant (0, 0) |
| `test_nav.py` | `bottom_right=True` or `object_in_way=True` |
| `test_las.py` | `no_enemies=True`, `laser_miss=True`, `star_survives=True` |
| `test_she.py` | `no_enemies=True` |
| `test_tor.py` | `no_enemies=True`, `hit_star=True`, `hit_starbase=True`, `star_survives=True` |
| `tests/test_library/test_routine_maint.py` | `with_enemies=True` or `enemies_moving=True` |

Examples:

```python
test_factory = create_random_factory(no_enemies=True)
test_factory = create_random_factory(hit_star=True, star_survives=True)
test_factory = create_random_factory(bottom_right=True)
```

Only use options supported by the helper in that file. All helpers that
generate a multi-object galaxy also accept `quadrant_visits=1`. Increase
this for tests that enter or regenerate additional quadrants:

```python
test_factory = create_random_factory(quadrant_visits=2)
```

Coordinate sequences are finite. Each visit receives distinct star/enemy
locations. Exhaustion indicates that the scenario needs more responses.
The repeating starbase location represents one starbase per new quadrant;
it does not provide an alternative when that location is occupied.
If the test changes Starship's entry sector to one of the supplied object
locations, edit the helper's positions or provide extra candidate locations.

The helpers retain the original scenario's counts and important target
coordinates while adding distinct locations for objects that previously
overwrote each other. Unspecified integer requests use explicit builder
defaults, not the old `-1` fallback. Laser helpers give enemies positive
shields; maintenance helpers provide valid device values 1 through 7 in
order, with independent state for every factory. Movement scenarios provide
three additional empty destinations after initial placement. Extend these
finite responses when testing more movement or damage events.

Run the new verification tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -c pytest.ini -q tests\test_random_factory_helpers.py tests\test_library\test_random_factory_builder.py
```
