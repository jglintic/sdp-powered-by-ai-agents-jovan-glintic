# Grid / Map — User Stories

---

## GRID-STORY-001 · P0 · Wrap rover position at grid edges (toroidal grid)

**Architecture References**
- Domain: Grid / Map
- Components: `Position` (wrap logic), `Grid` (dimensions), `Direction` (dx/dy delta) (§5.2)
- Solution Strategy: toroidal wrap via modulo on grid dimensions (§4.3)
- ADR: ADR-003 (Position as immutable record — wrapping applied at construction)
- Quality Scenario 1: wrap-around correctness — rover at `(0,0,S)` + `M` → `(0,4)` on 5×5 grid (§10.2)

---

### 1. Original Story

```
AS A mission operator
I WANT the rover to wrap around to the opposite edge when it moves off the grid boundary
SO THAT the rover can navigate a toroidal surface without hitting hard boundaries
```

---

### 2. Frontend Story — GRID-FE-001.1

**Focus:** Console output reflects wrapped position correctly

```
AS A mission operator
I WANT the final position printed to stdout to reflect the wrapped coordinate
SO THAT I can confirm the rover correctly traversed the grid edge
```

#### SCENARIO 1: Wrap from south edge to north edge

**Scenario ID:** GRID-FE-001.1-S1

**GIVEN**
* the application is running
* grid size is `5 5`

**WHEN**
* the user enters starting position `0 0 S`, no obstacles, and command `M`

**THEN**
* stdout prints `0:4:S`

---

#### SCENARIO 2: Wrap from east edge to west edge

**Scenario ID:** GRID-FE-001.1-S2

**GIVEN**
* the application is running
* grid size is `5 5`

**WHEN**
* the user enters starting position `4 2 E`, no obstacles, and command `M`

**THEN**
* stdout prints `0:2:E`

---

### 3. Backend Story — GRID-BE-001.1

**Focus:** `Position` wrapping logic via modulo; `Grid` supplies dimensions

```
AS A Position value object
I WANT to apply modulo arithmetic on x and y using the grid dimensions
SO THAT any coordinate that exceeds the boundary wraps to the opposite edge
```

#### SCENARIO 1: Moving south from y=0 wraps to y=(height-1)

**Scenario ID:** GRID-BE-001.1-S1

**GIVEN**
* a `Grid` of width `5`, height `5`
* a `Rover` at `Position(0, 0)` facing `S` (dy = -1)

**WHEN**
* `Rover` computes `nextPosition = position.translate(direction, grid)`

**THEN**
* `nextPosition` is `Position(0, 4)`
* formula: `y = (0 + (-1) + 5) % 5 = 4`

---

#### SCENARIO 2: Moving east from x=(width-1) wraps to x=0

**Scenario ID:** GRID-BE-001.1-S2

**GIVEN**
* a `Grid` of width `5`, height `5`
* a `Rover` at `Position(4, 2)` facing `E` (dx = +1)

**WHEN**
* `Rover` computes `nextPosition`

**THEN**
* `nextPosition` is `Position(0, 2)`
* formula: `x = (4 + 1) % 5 = 0`

---

#### SCENARIO 3: Moving north from y=(height-1) wraps to y=0

**Scenario ID:** GRID-BE-001.1-S3

**GIVEN**
* a `Grid` of width `5`, height `5`
* a `Rover` at `Position(2, 4)` facing `N` (dy = +1)

**WHEN**
* `Rover` computes `nextPosition`

**THEN**
* `nextPosition` is `Position(2, 0)`
* formula: `y = (4 + 1) % 5 = 0`

---

#### SCENARIO 4: Moving west from x=0 wraps to x=(width-1)

**Scenario ID:** GRID-BE-001.1-S4

**GIVEN**
* a `Grid` of width `5`, height `5`
* a `Rover` at `Position(0, 3)` facing `W` (dx = -1)

**WHEN**
* `Rover` computes `nextPosition`

**THEN**
* `nextPosition` is `Position(4, 3)`
* formula: `x = (0 + (-1) + 5) % 5 = 4`

---

#### SCENARIO 5: Position within bounds is unchanged by wrap logic

**Scenario ID:** GRID-BE-001.1-S5

**GIVEN**
* a `Grid` of width `5`, height `5`
* a `Rover` at `Position(2, 2)` facing `N`

**WHEN**
* `Rover` computes `nextPosition`

**THEN**
* `nextPosition` is `Position(2, 3)`
* no wrapping occurs; modulo has no effect

---

### 4. Infrastructure Story — GRID-INFRA-001.1

**Focus:** In-memory grid dimensions, wrap computation at construction, no persistence

```
AS A developer
I WANT the grid dimensions to be held in memory and the wrap logic to be applied inside Position construction
SO THAT wrapping is automatic, side-effect-free, and requires no runtime infrastructure
```

#### SCENARIO 1: Grid dimensions are immutable after construction

**Scenario ID:** GRID-INFRA-001.1-S1

**GIVEN**
* `Grid` is constructed with `width=5`, `height=5`

**WHEN**
* `MissionControl` passes the `Grid` to `Rover` for move validation

**THEN**
* `Grid.width` and `Grid.height` are read-only for the duration of the run
* no external storage is consulted

---

#### SCENARIO 2: Wrap is applied at Position construction, not at call sites

**Scenario ID:** GRID-INFRA-001.1-S2

**GIVEN**
* `Position` is a Java `record` with wrapping in its canonical constructor

**WHEN**
* any component creates a `Position` with out-of-bounds coordinates

**THEN**
* the stored `x` and `y` are always within `[0, width)` and `[0, height)`
* no call site needs to apply modulo manually

---

#### Data Model
- `Grid`: `int width`, `int height` — set once at construction, read-only thereafter
- `Position`: Java `record(int x, int y)` — wrap applied via `Math.floorMod(x, width)` at construction to handle negative deltas correctly

#### Execution Model
- Pure in-memory computation; no I/O involved in wrap logic
- Wrap is exercised on every `M` command that crosses a boundary

#### Observability
- Wrap events are implicitly observable via unit tests asserting pre/post `Position` values
- No dedicated logging; incorrect wrap produces a wrong final coordinate visible in stdout output

---

## GRID-STORY-002 · P1 · Validate starting position is within grid bounds

**Architecture References**
- Domain: Grid / Map
- Components: `InputParser`, `Grid`, `Position` (§5.2)
- Cross-cutting: Input Validation — starting position must be within grid bounds (§8.4)
- Constraints: invalid input causes immediate termination with stderr message (§8.2)
- ADR: ADR-004 (infrastructure layer owns validation of raw input before domain objects are constructed)

---

### 1. Original Story

```
AS A mission operator
I WANT the system to reject a starting position that falls outside the grid
SO THAT the simulation never runs with an invalid initial state
```

---

### 2. Frontend Story — GRID-FE-002.1

**Focus:** stderr error when starting position is out of bounds; no simulation output

```
AS A mission operator
I WANT to see a clear error message on stderr when my starting position is outside the grid
SO THAT I know to correct my input before rerunning
```

#### SCENARIO 1: Starting position outside grid prints error to stderr

**Scenario ID:** GRID-FE-002.1-S1

**GIVEN**
* the application is running
* grid size is `5 5`

**WHEN**
* the user enters starting position `6 3 N` (x=6 exceeds width-1=4)

**THEN**
* stderr prints a descriptive error (e.g. `"Starting position (6, 3) is outside grid 5x5"`)
* stdout remains empty
* the process exits with a non-zero code

---

#### SCENARIO 2: Starting position on the boundary is accepted

**Scenario ID:** GRID-FE-002.1-S2

**GIVEN**
* the application is running
* grid size is `5 5`

**WHEN**
* the user enters starting position `4 4 N` (maximum valid coordinate) and commands `L`

**THEN**
* stdout prints `4:4:W`
* no error is produced

---

### 3. Backend Story — GRID-BE-002.1

**Focus:** `InputParser` checks `0 ≤ x < width` and `0 ≤ y < height` after parsing grid and position

```
AS A InputParser
I WANT to verify the starting position is within grid bounds after both are parsed
SO THAT an IllegalArgumentException is thrown before any domain object is handed to MissionControl
```

#### SCENARIO 1: x coordinate exceeds width throws IllegalArgumentException

**Scenario ID:** GRID-BE-002.1-S1

**GIVEN**
* grid `width=5`, `height=5`
* parsed starting position `x=6`, `y=0`

**WHEN**
* `InputParser` validates the starting position against the grid

**THEN**
* throws `IllegalArgumentException` with a message identifying the invalid coordinate

---

#### SCENARIO 2: y coordinate exceeds height throws IllegalArgumentException

**Scenario ID:** GRID-BE-002.1-S2

**GIVEN**
* grid `width=5`, `height=5`
* parsed starting position `x=0`, `y=7`

**WHEN**
* `InputParser` validates the starting position

**THEN**
* throws `IllegalArgumentException` with a message identifying the invalid coordinate

---

#### SCENARIO 3: Negative coordinate throws IllegalArgumentException

**Scenario ID:** GRID-BE-002.1-S3

**GIVEN**
* grid `width=5`, `height=5`
* parsed starting position `x=-1`, `y=2`

**WHEN**
* `InputParser` validates the starting position

**THEN**
* throws `IllegalArgumentException`

---

#### SCENARIO 4: Position exactly at max boundary is valid

**Scenario ID:** GRID-BE-002.1-S4

**GIVEN**
* grid `width=5`, `height=5`
* parsed starting position `x=4`, `y=4`

**WHEN**
* `InputParser` validates the starting position

**THEN**
* no exception is thrown
* `Rover` is constructed with `Position(4, 4)`

---

### 4. Infrastructure Story — GRID-INFRA-002.1

**Focus:** Validation occurs in `InputParser` before domain construction; error surfaced by `Main` to stderr

```
AS A developer
I WANT bounds validation to happen inside InputParser, not inside Grid or Rover
SO THAT domain objects are always constructed in a valid state
```

#### SCENARIO 1: Validation runs after both grid and position lines are parsed

**Scenario ID:** GRID-INFRA-002.1-S1

**GIVEN**
* `InputParser` has parsed the grid dimensions and the starting position

**WHEN**
* bounds check `0 ≤ x < width && 0 ≤ y < height` is evaluated

**THEN**
* if invalid, `IllegalArgumentException` is thrown before `Rover` or `Grid` are returned
* `Main` catches it and writes to `stderr` (same path as CMD-INFRA-001.1-S2)

---

#### Data Model
- No new data structures; validation is a guard clause in `InputParser` using already-parsed `int` values
- Valid range: `x ∈ [0, width)`, `y ∈ [0, height)`

#### Execution Model
- Synchronous check inside `InputParser.parse()`, after grid dimensions and position are both available
- Fails fast: exception thrown immediately, `MissionControl` never reached

#### Observability
- Error message on `stderr` names the invalid coordinate and the grid size
- No logging framework needed; the exception message is the observable signal

---

## GRID-STORY-003 · P2 · Support multiple obstacles on the grid

**Architecture References**
- Domain: Grid / Map
- Components: `Grid`, `Position`, `InputParser` (§5.2)
- Solution Strategy: `Set<Position>` for obstacles — O(1) lookup regardless of count (§4.3)
- ADR: ADR-003 (Position as immutable record — `equals`/`hashCode` from `record` enables correct `Set` membership)
- Cross-cutting: obstacle list parsed from a single input line as coordinate pairs (§8.4)

---

### 1. Original Story

```
AS A mission operator
I WANT to place multiple obstacles on the grid
SO THAT I can simulate realistic terrain where the rover may be blocked from several directions
```

---

### 2. Frontend Story — GRID-FE-003.1

**Focus:** Multiple obstacle coordinates accepted on stdin; rover halts at the first one it would enter

```
AS A mission operator
I WANT to specify multiple obstacle positions on a single input line
SO THAT the rover correctly avoids all of them during the simulation
```

#### SCENARIO 1: Rover halts at first obstacle in a multi-obstacle grid

**Scenario ID:** GRID-FE-003.1-S1

**GIVEN**
* the application is running, grid `5 5`
* obstacles at `0 1` and `2 2`

**WHEN**
* the user enters starting position `0 0 N` and commands `MMM`

**THEN**
* stdout prints `O:0:0:N` (blocked at `(0,1)` on first move)

---

#### SCENARIO 2: Rover navigates past one obstacle and halts at another

**Scenario ID:** GRID-FE-003.1-S2

**GIVEN**
* the application is running, grid `5 5`
* obstacles at `3 0` and `1 1`

**WHEN**
* the user enters starting position `0 0 N` and commands `MRM`

**THEN**
* stdout prints `O:0:1:E` (moved north to `(0,1)`, turned east, blocked at `(1,1)`)

---

#### SCENARIO 3: Empty obstacle list runs without error

**Scenario ID:** GRID-FE-003.1-S3

**GIVEN**
* the application is running, grid `5 5`
* obstacle line is empty

**WHEN**
* the user enters starting position `0 0 N` and commands `M`

**THEN**
* stdout prints `0:1:N` — no obstacles, move succeeds

---

### 3. Backend Story — GRID-BE-003.1

**Focus:** `Grid` holds all obstacles in a `Set<Position>`; each `M` command checks the full set in O(1)

```
AS A Grid
I WANT to store any number of obstacle positions in a Set<Position>
SO THAT isObstacle() is O(1) regardless of how many obstacles exist
```

#### SCENARIO 1: Grid constructed with multiple obstacles detects each one

**Scenario ID:** GRID-BE-003.1-S1

**GIVEN**
* `Grid` constructed with obstacles `{Position(0,1), Position(2,2), Position(4,3)}`

**WHEN**
* `Grid.isObstacle` is called for each position

**THEN**
* returns `true` for `Position(0,1)`, `Position(2,2)`, `Position(4,3)`
* returns `false` for any other position

---

#### SCENARIO 2: Rover halts at the first obstacle encountered in sequence

**Scenario ID:** GRID-BE-003.1-S2

**GIVEN**
* a `Rover` at `Position(0,0)` facing `N`
* obstacles at `Position(0,1)` and `Position(0,2)`

**WHEN**
* `MissionControl` executes commands `[M, M, M]`

**THEN**
* first `M` triggers `ObstacleException` at `Position(0,1)`
* `Position(0,2)` is never checked
* rover halts at `Position(0,0)`

---

#### SCENARIO 3: Grid with zero obstacles never blocks the rover

**Scenario ID:** GRID-BE-003.1-S3

**GIVEN**
* `Grid` constructed with an empty obstacle set

**WHEN**
* `Grid.isObstacle` is called for any position

**THEN**
* always returns `false`

---

### 4. Infrastructure Story — GRID-INFRA-003.1

**Focus:** Obstacle list parsed as coordinate pairs into `Set<Position>`; set is immutable after construction

```
AS A developer
I WANT InputParser to parse any number of obstacle coordinate pairs into a Set<Position>
SO THAT Grid receives a complete, immutable obstacle set before the simulation starts
```

#### SCENARIO 1: Even number of tokens parsed into Set<Position>

**Scenario ID:** GRID-INFRA-003.1-S1

**GIVEN**
* obstacle input line `"0 1 2 2 4 3"` (three pairs)

**WHEN**
* `InputParser` parses the obstacle line

**THEN**
* returns `Set<Position>` containing `Position(0,1)`, `Position(2,2)`, `Position(4,3)`
* set size is 3

---

#### SCENARIO 2: Odd number of obstacle tokens throws IllegalArgumentException

**Scenario ID:** GRID-INFRA-003.1-S2

**GIVEN**
* obstacle input line `"0 1 2"` (incomplete pair)

**WHEN**
* `InputParser` parses the obstacle line

**THEN**
* throws `IllegalArgumentException("Obstacle coordinates must be provided in x y pairs")`

---

#### SCENARIO 3: Duplicate obstacle coordinates are silently deduplicated by Set

**Scenario ID:** GRID-INFRA-003.1-S3

**GIVEN**
* obstacle input line `"0 1 0 1"` (same position twice)

**WHEN**
* `InputParser` parses the obstacle line

**THEN**
* `Set<Position>` contains one entry: `Position(0,1)`
* no error is thrown

---

#### Data Model
- `Grid.obstacles`: `Set<Position>` — `HashSet` populated at construction; `Position` record provides correct `equals`/`hashCode`
- Passed as an unmodifiable view (`Collections.unmodifiableSet`) to prevent mutation after construction

#### Execution Model
- Obstacle set built once during `InputParser.parse()`; read-only for the entire simulation run
- `Set.contains` called on every `M` command — O(1) per call

#### Observability
- Obstacle count visible implicitly: each blocked move produces an `O:` prefixed output
- Unit tests assert set contents after parsing and correct halt position during simulation
