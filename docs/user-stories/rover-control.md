# Rover Control — User Stories

---

## ROVER-STORY-001 · P0 · Execute a command sequence and return final position

**Architecture References**
- Domain: Rover Control, Simulation Orchestration
- Components: `Rover`, `Direction`, `Position`, `Command`, `MissionControl` (§5.2)
- Runtime: Scenario 1 — Successful Command Execution (§6.1, `seq-happy-path.puml`)
- ADR: ADR-001 (Direction as cyclic enum), ADR-003 (Position as immutable record), ADR-004 (three-layer structure)

---

### 1. Original Story

```
AS A mission operator
I WANT to submit a starting position, direction, and command sequence to the rover
SO THAT I receive the rover's final position and direction after all commands are executed
```

---

### 2. Frontend Story — ROVER-FE-001.1

**Focus:** Console I/O — user input and result display

```
AS A mission operator
I WANT to enter rover configuration and commands on the console
SO THAT I can see the final rover state printed to stdout
```

#### SCENARIO 1: Display final position after successful run

**Scenario ID:** ROVER-FE-001.1-S1

**GIVEN**
* the application is running and waiting for input on stdin

**WHEN**
* the user enters starting position `0 0 N`, grid size `5 5`, no obstacles, and commands `MRML`

**THEN**
* stdout prints `1:1:N`
* the process exits with code 0

---

#### SCENARIO 2: Display result for a move-only sequence

**Scenario ID:** ROVER-FE-001.1-S2

**GIVEN**
* the application is running

**WHEN**
* the user enters starting position `2 2 E`, grid size `5 5`, no obstacles, and commands `MM`

**THEN**
* stdout prints `4:2:E`

---

### 3. Backend Story — ROVER-BE-001.1

**Focus:** Domain logic — command dispatch, position update, direction update

```
AS A MissionControl orchestrator
I WANT to iterate over a command sequence and apply each command to the Rover
SO THAT the Rover's position and direction are correctly updated after every step
```

#### SCENARIO 1: Move forward updates position by direction delta

**Scenario ID:** ROVER-BE-001.1-S1

**GIVEN**
* a `Rover` at position `(0, 0)` facing `N`
* a `Grid` of size `5×5` with no obstacles

**WHEN**
* `MissionControl` executes command `M`

**THEN**
* `Rover.position` is `(0, 1)`
* `Rover.direction` remains `N`

---

#### SCENARIO 2: Turn right updates direction without changing position

**Scenario ID:** ROVER-BE-001.1-S2

**GIVEN**
* a `Rover` at position `(2, 2)` facing `N`

**WHEN**
* `MissionControl` executes command `R`

**THEN**
* `Rover.direction` is `E`
* `Rover.position` remains `(2, 2)`

---

#### SCENARIO 3: Full mixed sequence produces correct final state

**Scenario ID:** ROVER-BE-001.1-S3

**GIVEN**
* a `Rover` at position `(0, 0)` facing `N`
* a `Grid` of size `5×5` with no obstacles

**WHEN**
* `MissionControl` executes commands `[M, R, M, L]`

**THEN**
* `Rover.position` is `(1, 1)`
* `Rover.direction` is `N`

---

#### SCENARIO 4: Empty command sequence leaves rover unchanged

**Scenario ID:** ROVER-BE-001.1-S4

**GIVEN**
* a `Rover` at position `(3, 3)` facing `S`

**WHEN**
* `MissionControl` executes an empty command list `[]`

**THEN**
* `Rover.position` is `(3, 3)`
* `Rover.direction` is `S`

---

### 4. Infrastructure Story — ROVER-INFRA-001.1

**Focus:** Docker build, pytest execution, in-memory state, observability

```
AS A developer running the kata
I WANT the rover simulation to build and run inside a Docker container using pytest
SO THAT the system requires no local Python installation and tests are fully reproducible
```

#### SCENARIO 1: Docker image builds successfully

**Scenario ID:** ROVER-INFRA-001.1-S1

**GIVEN**
* a `Dockerfile` at the project root using `python:3.12-slim`
* source files under `src/` and tests under `tests/`

**WHEN**
* the developer runs:
  ```
  docker build -t mars-rover .
  ```

**THEN**
* the image is built without errors
* `pytest` is installed inside the image via `pip install --no-cache-dir pytest`

---

#### SCENARIO 2: pytest runs inside the container and all tests pass

**Scenario ID:** ROVER-INFRA-001.1-S2

**GIVEN**
* the `mars-rover` image has been built
* `tests/test_rover.py` contains tests for `Rover`, `Direction`, `Position`, and `MissionControl`

**WHEN**
* the developer runs:
  ```
  docker run --rm mars-rover pytest tests/
  ```

**THEN**
* pytest discovers and executes all tests
* all tests pass; exit code is `0`
* test results are printed to stdout

---

#### SCENARIO 3: In-memory state is isolated per container run

**Scenario ID:** ROVER-INFRA-001.1-S3

**GIVEN**
* the container is run twice with different inputs

**WHEN**
* each `docker run` invocation executes independently

**THEN**
* each run produces an independent result
* no state persists between runs (no files, no shared volumes)

---

#### Data Model
- `Rover`: holds `position` (tuple or dataclass) and `direction` (enum) — replaced on each successful move
- `Grid`: holds `width`, `height`, `obstacles` (frozenset) — read-only after construction
- `MissionControl`: holds references to `Rover` and `Grid` — scoped to a single execution

#### Execution Model
- Build: `docker build -t mars-rover .`
- Test: `docker run --rm mars-rover pytest tests/`
- Run: `docker run --rm -i mars-rover python -m mars_rover` (reads from stdin)
- All state is in-memory; no files, databases, or network calls

#### Observability
- Normal result → `stdout`
- Errors → `stderr`
- pytest output provides per-test pass/fail visibility

---

## ROVER-STORY-002 · P0 · Halt and report when an obstacle is encountered

**Architecture References**
- Domain: Rover Control
- Components: `Rover`, `Grid`, `Position`, `MissionControl`, `OutputFormatter` (§5.2)
- Runtime: Scenario 2 — Obstacle Encountered (§6.2, `seq-obstacle.puml`)
- ADR: ADR-002 (obstacle detection via `ObstacleException`), ADR-003 (Position immutability — state never partially updated)
- Quality Scenario 2: rover at `(0,0,N)` + `MM` with obstacle at `(0,1)` → output `O:0:0:N` (§10.2)
- Cross-cutting: error handling — `ObstacleException` caught by `MissionControl`; `O:` prefix convention (§8.2)

---

### 1. Original Story

```
AS A mission operator
I WANT the rover to stop immediately and report its current position when it would enter an obstacle cell
SO THAT I know where the rover halted and can identify the blocked path
```

---

### 2. Frontend Story — ROVER-FE-002.1

**Focus:** Console output shows `O:` prefix and halted position

```
AS A mission operator
I WANT to see an obstacle-prefixed position string on stdout when the rover is blocked
SO THAT I can distinguish a halted run from a successful one
```

#### SCENARIO 1: Obstacle on first move — output prefixed with O:

**Scenario ID:** ROVER-FE-002.1-S1

**GIVEN**
* the application is running
* grid size is `5 5`, obstacle at `0 1`

**WHEN**
* the user enters starting position `0 0 N`, commands `MM`

**THEN**
* stdout prints `O:0:0:N`
* the process exits with code 0 (obstacle is not a system error)

---

#### SCENARIO 2: Obstacle mid-sequence — partial progress reported

**Scenario ID:** ROVER-FE-002.1-S2

**GIVEN**
* the application is running
* grid size is `5 5`, obstacle at `1 1`

**WHEN**
* the user enters starting position `0 0 N`, commands `MRMM`

**THEN**
* stdout prints `O:1:0:E`
* commands after the blocked move are not executed

---

### 3. Backend Story — ROVER-BE-002.1

**Focus:** `Grid.isObstacle` check before move; `ObstacleException` thrown and caught; rover state unchanged on block

```
AS A Rover
I WANT to check the next position against the obstacle set before committing a move
SO THAT my state is never partially updated and execution halts cleanly at the blocked step
```

#### SCENARIO 1: Move into obstacle throws ObstacleException

**Scenario ID:** ROVER-BE-002.1-S1

**GIVEN**
* a `Rover` at `Position(0, 0)` facing `N`
* a `Grid` with obstacle at `Position(0, 1)`

**WHEN**
* `Rover` executes command `M`

**THEN**
* `Grid.isObstacle(Position(0, 1))` returns `true`
* `Rover` throws `ObstacleException`
* `Rover.position` remains `Position(0, 0)` — no partial update

---

#### SCENARIO 2: MissionControl catches ObstacleException and returns halted state

**Scenario ID:** ROVER-BE-002.1-S2

**GIVEN**
* `MissionControl` is iterating commands `[M, M]`
* first `M` throws `ObstacleException` at `Position(0, 1)`

**WHEN**
* `MissionControl` catches `ObstacleException`

**THEN**
* command iteration stops immediately
* `MissionControl` returns the rover's current state `(0, 0, N)` with an obstacle flag
* second `M` is never executed

---

#### SCENARIO 3: Move to non-obstacle cell succeeds normally

**Scenario ID:** ROVER-BE-002.1-S3

**GIVEN**
* a `Rover` at `Position(0, 0)` facing `N`
* a `Grid` with obstacle at `Position(0, 2)` only

**WHEN**
* `Rover` executes command `M`

**THEN**
* `Grid.isObstacle(Position(0, 1))` returns `false`
* `Rover.position` updates to `Position(0, 1)`
* no exception is thrown

---

#### SCENARIO 4: Rover state is never partially updated on a blocked move

**Scenario ID:** ROVER-BE-002.1-S4

**GIVEN**
* a `Rover` at `Position(3, 3)` facing `E`
* a `Grid` with obstacle at `Position(4, 3)`

**WHEN**
* `Rover` executes command `M` and `Grid.isObstacle` returns `true`

**THEN**
* `Rover.position` is still `Position(3, 3)`
* `Rover.direction` is still `E`
* `ObstacleException` is thrown before any field assignment

---

### 4. Infrastructure Story — ROVER-INFRA-002.1

**Focus:** Obstacle set as `Set<Position>` for O(1) lookup; `O:` prefix formatting; no persistence

```
AS A developer
I WANT obstacles stored in a Set<Position> and the halted result formatted with an O: prefix
SO THAT obstacle detection is efficient and the output convention is consistently applied
```

#### SCENARIO 1: Obstacle set provides O(1) lookup

**Scenario ID:** ROVER-INFRA-002.1-S1

**GIVEN**
* `Grid` is constructed with a `Set<Position>` of obstacles

**WHEN**
* `Grid.isObstacle(position)` is called on every `M` command

**THEN**
* lookup is O(1) via `Set.contains`
* `Position.equals` and `hashCode` (provided by Java `record`) are used for set membership

---

#### SCENARIO 2: OutputFormatter applies O: prefix for obstacle result

**Scenario ID:** ROVER-INFRA-002.1-S2

**GIVEN**
* `MissionControl` returns a result flagged as obstacle-halted with rover state `(0, 0, N)`

**WHEN**
* `OutputFormatter.format(result)` is called

**THEN**
* the returned string is `"O:0:0:N"`
* the same formatter handles both normal (`"x:y:DIR"`) and halted (`"O:x:y:DIR"`) results

---

#### SCENARIO 3: Obstacle input is parsed into Set<Position> at startup

**Scenario ID:** ROVER-INFRA-002.1-S3

**GIVEN**
* the user provides obstacle coordinates `0 1` and `2 3` on stdin

**WHEN**
* `InputParser` processes the obstacle line

**THEN**
* a `Set<Position>` containing `Position(0,1)` and `Position(2,3)` is passed to `Grid`
* no obstacle data is stored outside the JVM process

---

#### Data Model
- `Grid.obstacles`: `Set<Position>` — populated once at construction from parsed input, read-only thereafter
- `ObstacleException`: unchecked exception carrying the rover's current `Position` and `Direction` at the moment of halt

#### Execution Model
- Obstacle check occurs inside `Rover.execute(M, grid)` before any state mutation
- `MissionControl` wraps the command loop in a try/catch for `ObstacleException`; on catch, returns immediately

#### Observability
- Obstacle halt is visible in stdout via `O:` prefix — no additional logging needed
- Unit tests assert both the thrown exception and the unchanged rover state post-block

---

## ROVER-STORY-003 · P1 · Rotate rover left and right

**Architecture References**
- Domain: Rover Control
- Components: `Direction`, `Rover` (§5.2)
- Solution Strategy: cyclic index arithmetic `(index ± 1) % 4`; no conditionals (§4.3)
- ADR: ADR-001 (Direction as cyclic enum `[N, E, S, W]`)
- Quality Scenario 3: `LLLL` from `N` returns to `N` (§10.2)

---

### 1. Original Story

```
AS A mission operator
I WANT the rover to turn left or right by 90° without changing its position
SO THAT I can reorient the rover before issuing move commands
```

---

### 2. Frontend Story — ROVER-FE-003.1

**Focus:** Console output reflects direction change after rotation commands

```
AS A mission operator
I WANT the final direction in the output string to reflect all rotation commands applied
SO THAT I can verify the rover is facing the expected direction
```

#### SCENARIO 1: Four left turns return to original direction

**Scenario ID:** ROVER-FE-003.1-S1

**GIVEN**
* the application is running, grid `5 5`, no obstacles

**WHEN**
* the user enters starting position `0 0 N` and commands `LLLL`

**THEN**
* stdout prints `0:0:N`

---

#### SCENARIO 2: Single right turn changes direction

**Scenario ID:** ROVER-FE-003.1-S2

**GIVEN**
* the application is running, grid `5 5`, no obstacles

**WHEN**
* the user enters starting position `2 2 N` and commands `R`

**THEN**
* stdout prints `2:2:E`

---

### 3. Backend Story — ROVER-BE-003.1

**Focus:** `Direction` cyclic rotation via index arithmetic; position unchanged

```
AS A Direction enum
I WANT to compute the next direction by shifting one step in the cyclic order [N, E, S, W]
SO THAT rotation is branch-free and correct for all starting directions
```

#### SCENARIO 1: Turn right advances one step clockwise

**Scenario ID:** ROVER-BE-003.1-S1

**GIVEN**
* cyclic order `[N=0, E=1, S=2, W=3]`

**WHEN**
* `Direction.N.rotate(R)` is called

**THEN**
* returns `Direction.E` — formula: `(0 + 1) % 4 = 1`

---

#### SCENARIO 2: Turn left retreats one step counter-clockwise

**Scenario ID:** ROVER-BE-003.1-S2

**GIVEN**
* cyclic order `[N=0, E=1, S=2, W=3]`

**WHEN**
* `Direction.N.rotate(L)` is called

**THEN**
* returns `Direction.W` — formula: `(0 - 1 + 4) % 4 = 3`

---

#### SCENARIO 3: Full clockwise rotation returns to origin

**Scenario ID:** ROVER-BE-003.1-S3

**GIVEN**
* a `Rover` at `(0, 0)` facing `N`

**WHEN**
* commands `[R, R, R, R]` are executed

**THEN**
* `Rover.direction` is `N`
* `Rover.position` is unchanged at `(0, 0)`

---

#### SCENARIO 4: Full counter-clockwise rotation returns to origin

**Scenario ID:** ROVER-BE-003.1-S4

**GIVEN**
* a `Rover` at `(0, 0)` facing `N`

**WHEN**
* commands `[L, L, L, L]` are executed

**THEN**
* `Rover.direction` is `N`
* `Rover.position` is unchanged at `(0, 0)`

---

#### SCENARIO 5: Rotation from W right wraps to N

**Scenario ID:** ROVER-BE-003.1-S5

**GIVEN**
* a `Rover` facing `W` (index 3)

**WHEN**
* `Direction.W.rotate(R)` is called

**THEN**
* returns `Direction.N` — formula: `(3 + 1) % 4 = 0`

---

### 4. Infrastructure Story — ROVER-INFRA-003.1

**Focus:** Rotation is a pure enum method; no state, no I/O, no infrastructure concerns

```
AS A developer
I WANT direction rotation to be a pure method on the Direction enum
SO THAT it is testable in isolation with no setup and has zero infrastructure dependencies
```

#### SCENARIO 1: Direction.rotate is a pure function with no side effects

**Scenario ID:** ROVER-INFRA-003.1-S1

**GIVEN**
* `Direction` is a Java enum with a `rotate(Command)` method

**WHEN**
* `rotate` is called with `L` or `R`

**THEN**
* returns a new `Direction` value
* no fields are mutated; `Rover` replaces its `direction` reference with the returned value

---

#### Data Model
- `Direction`: enum constants `N, E, S, W` at indices `0, 1, 2, 3`
- `rotate(Command c)`: `(ordinal() + (c == R ? 1 : -1) + 4) % 4` → `Direction.values()[result]`

#### Execution Model
- Called inside `Rover.execute(L|R, grid)` — no grid interaction needed for rotation
- Pure computation; no allocation beyond the returned enum constant reference

#### Observability
- Rotation correctness verified entirely through unit tests on `Direction.rotate`
- No runtime logging needed; incorrect rotation produces a wrong direction in stdout output

---

## ROVER-STORY-004 · P2 · Support extensible command set (add new command)

**Architecture References**
- Domain: Rover Control
- Components: `Command`, `Rover`, `InputParser` (§5.2)
- Solution Strategy: commands modeled as enum or strategy; adding a command requires no changes to `MissionControl` or the core loop (§4.1)
- Quality Scenario 4: adding `B` (move backward) touches only `Command` enum and `Rover` handler (§10.2)
- ADR: ADR-001 (Direction owns dx/dy — backward is just opposite delta, no new direction logic needed)

---

### 1. Original Story

```
AS A developer
I WANT to add a new command by extending the Command enum and its handler in Rover
SO THAT MissionControl, Grid, InputParser's command loop, and OutputFormatter require no changes
```

---

### 2. Frontend Story — ROVER-FE-004.1

**Focus:** New command character accepted on stdin and reflected in output without any I/O layer changes

```
AS A mission operator
I WANT to use a new command character (e.g. B for move backward) in my command string
SO THAT the simulation executes it without requiring changes to how I provide input
```

#### SCENARIO 1: New command B moves rover backward and output reflects result

**Scenario ID:** ROVER-FE-004.1-S1

**GIVEN**
* `B` has been added as a valid command
* the application is running, grid `5 5`, no obstacles

**WHEN**
* the user enters starting position `2 2 N` and commands `B`

**THEN**
* stdout prints `2:1:N` (moved one step in the opposite of N, i.e. south)

---

### 3. Backend Story — ROVER-BE-004.1

**Focus:** Adding `B` requires only a new `Command` constant and a handler branch in `Rover`; no other class changes

```
AS A developer
I WANT to add command B by adding one enum constant and one handler case in Rover
SO THAT the open/closed principle is respected and no existing logic is modified
```

#### SCENARIO 1: Adding B constant to Command enum requires no changes elsewhere in the loop

**Scenario ID:** ROVER-BE-004.1-S1

**GIVEN**
* `Command` enum has constants `L`, `R`, `M`

**WHEN**
* constant `B` is added to `Command`

**THEN**
* `MissionControl`'s command iteration loop requires no modification
* `InputParser`'s character-to-command mapping requires only one new entry for `'B'`
* `OutputFormatter` requires no modification

---

#### SCENARIO 2: B moves rover one step opposite to current direction

**Scenario ID:** ROVER-BE-004.1-S2

**GIVEN**
* a `Rover` at `Position(2, 2)` facing `N`
* `Grid` 5×5, no obstacles

**WHEN**
* `Rover` executes command `B`

**THEN**
* `nextPosition` is computed using the opposite delta: `direction.opposite().delta()`
* `Rover.position` becomes `Position(2, 1)`
* `Rover.direction` remains `N`

---

#### SCENARIO 3: B respects obstacle detection before moving

**Scenario ID:** ROVER-BE-004.1-S3

**GIVEN**
* a `Rover` at `Position(2, 2)` facing `N`
* obstacle at `Position(2, 1)`

**WHEN**
* `Rover` executes command `B`

**THEN**
* `Grid.isObstacle(Position(2, 1))` returns `true`
* `ObstacleException` is thrown
* `Rover.position` remains `Position(2, 2)`

---

#### SCENARIO 4: B respects toroidal wrap at grid edge

**Scenario ID:** ROVER-BE-004.1-S4

**GIVEN**
* a `Rover` at `Position(0, 0)` facing `N`
* `Grid` 5×5, no obstacles

**WHEN**
* `Rover` executes command `B`

**THEN**
* `Rover.position` becomes `Position(0, 4)` (wraps south edge)

---

### 4. Infrastructure Story — ROVER-INFRA-004.1

**Focus:** Extensibility is a design property, not a runtime concern; verified by change-impact analysis

```
AS A developer
I WANT the change required to add a new command to be confined to Command and Rover
SO THAT I can verify extensibility by inspecting which files change, not by adding infrastructure
```

#### SCENARIO 1: Change impact for adding command B is limited to two touch points

**Scenario ID:** ROVER-INFRA-004.1-S1

**GIVEN**
* the codebase implements `L`, `R`, `M`

**WHEN**
* command `B` is added

**THEN**
* files modified: `Command.java` (new constant), `Rover.java` (new handler case)
* files unmodified: `MissionControl.java`, `Grid.java`, `Direction.java`, `OutputFormatter.java`
* `InputParser.java` requires one new character mapping entry — acceptable as it is the I/O boundary

---

#### Data Model
- No new data structures; `B` reuses `Direction.opposite()` (inverse index: `(ordinal() + 2) % 4`) to get the backward delta
- `Direction.opposite()` can be a one-line helper on the existing enum

#### Execution Model
- Same command loop in `MissionControl`; `B` is dispatched identically to `M`
- Obstacle check and wrap apply automatically — no special casing

#### Observability
- Extensibility verified through unit tests on the new `B` handler in `Rover`
- No infrastructure changes; no new logging or I/O paths
