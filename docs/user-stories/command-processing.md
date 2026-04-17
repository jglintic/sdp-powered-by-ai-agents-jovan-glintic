# Command Processing & Output — User Stories

---

## CMD-STORY-001 · P1 · Parse raw console input into domain objects

**Architecture References**
- Domain: Command Processing, Output
- Components: `InputParser`, `Main` (§5.2)
- Cross-cutting: Input Validation — direction, commands, grid dimensions, starting position (§8.4)
- Constraints: no external libraries; pure Java; stdin as sole input channel (§2.1, §3.2)
- ADR: ADR-004 (infrastructure layer owns I/O; domain has zero I/O dependencies)

---

### 1. Original Story

```
AS A mission operator
I WANT my console input to be parsed into a rover, a grid, and a command list
SO THAT the simulation can execute without any domain component knowing about raw strings
```

---

### 2. Frontend Story — CMD-FE-001.1

**Focus:** User provides structured input on stdin; errors appear on stderr

```
AS A mission operator
I WANT to enter rover configuration and commands in a defined format on stdin
SO THAT the application accepts my input and starts the simulation
```

#### SCENARIO 1: Valid input is accepted and simulation runs

**Scenario ID:** CMD-FE-001.1-S1

**GIVEN**
* the application is running and waiting on stdin

**WHEN**
* the user enters:
  ```
  0 0 N
  5 5
  0 1 2 3
  MRML
  ```

**THEN**
* the simulation runs and stdout prints the final result
* no error appears on stderr

---

#### SCENARIO 2: Invalid direction prints error to stderr

**Scenario ID:** CMD-FE-001.1-S2

**GIVEN**
* the application is running

**WHEN**
* the user enters starting position `0 0 X` (unknown direction)

**THEN**
* stderr prints a descriptive error message (e.g. `"Invalid direction: X"`)
* stdout remains empty
* the process exits with a non-zero code

---

### 3. Backend Story — CMD-BE-001.1

**Focus:** `InputParser` tokenises each input line and constructs domain objects; rejects invalid tokens

```
AS A InputParser
I WANT to convert each line of stdin into the corresponding domain type
SO THAT MissionControl receives fully-typed, validated objects with no raw strings
```

#### SCENARIO 1: Parse starting position and direction

**Scenario ID:** CMD-BE-001.1-S1

**GIVEN**
* input line `"0 0 N"`

**WHEN**
* `InputParser` parses the position/direction line

**THEN**
* returns a `Rover` with `Position(0, 0)` and `Direction.N`

---

#### SCENARIO 2: Parse grid dimensions

**Scenario ID:** CMD-BE-001.1-S2

**GIVEN**
* input line `"5 5"`

**WHEN**
* `InputParser` parses the grid line

**THEN**
* returns a `Grid` with `width=5`, `height=5`, and an empty obstacle set

---

#### SCENARIO 3: Parse obstacle list into Set<Position>

**Scenario ID:** CMD-BE-001.1-S3

**GIVEN**
* input line `"0 1 2 3"` (pairs of coordinates)

**WHEN**
* `InputParser` parses the obstacle line

**THEN**
* returns `Set<Position>` containing `Position(0,1)` and `Position(2,3)`

---

#### SCENARIO 4: Parse command string into Command list

**Scenario ID:** CMD-BE-001.1-S4

**GIVEN**
* input line `"MRML"`

**WHEN**
* `InputParser` parses the command line

**THEN**
* returns `[Command.M, Command.R, Command.M, Command.L]`

---

#### SCENARIO 5: Unknown command character throws IllegalArgumentException

**Scenario ID:** CMD-BE-001.1-S5

**GIVEN**
* input line `"MXL"` (unknown character `X`)

**WHEN**
* `InputParser` parses the command line

**THEN**
* throws `IllegalArgumentException` with message `"Invalid command: X"`

---

### 4. Infrastructure Story — CMD-INFRA-001.1

**Focus:** stdin as input channel; `Main` wires parser and catches parse errors to stderr

```
AS A developer
I WANT InputParser to read from stdin and Main to catch parse errors and write them to stderr
SO THAT the infrastructure boundary is clear and the domain is never exposed to raw I/O
```

#### SCENARIO 1: Main reads all input lines from stdin before constructing domain objects

**Scenario ID:** CMD-INFRA-001.1-S1

**GIVEN**
* the JVM process is started

**WHEN**
* `Main` runs

**THEN**
* all input is read from `System.in` via `InputParser`
* `InputParser` produces `Rover`, `Grid`, and `List<Command>` — no raw strings leave the infrastructure layer

---

#### SCENARIO 2: Parse exception is caught by Main and written to stderr

**Scenario ID:** CMD-INFRA-001.1-S2

**GIVEN**
* `InputParser` throws `IllegalArgumentException` during parsing

**WHEN**
* `Main` catches the exception

**THEN**
* the exception message is written to `System.err`
* `System.exit` is called with a non-zero code
* `MissionControl` is never invoked

---

#### Data Model
- `InputParser` produces: `Rover` (position + direction), `Grid` (dimensions + obstacle set), `List<Command>`
- All produced objects are domain types; no raw strings cross the infrastructure boundary

#### Execution Model
- Input is read line-by-line from `System.in`
- Parsing is synchronous and completes before `MissionControl` is invoked

#### Observability
- Parse errors → `stderr` with a descriptive message identifying the invalid token
- Successful parse produces no output (silent pass-through to simulation)

---

## CMD-STORY-002 · P1 · Format final rover state as output string

**Architecture References**
- Domain: Output
- Components: `OutputFormatter`, `Main` (§5.2)
- Cross-cutting: `O:` prefix convention for obstacle-halted results (§8.2)
- Constraints: output is a single string to stdout; no files or structured formats (§2.2, §3.2)
- ADR: ADR-004 (infrastructure layer owns formatting; domain returns state, not strings)

---

### 1. Original Story

```
AS A mission operator
I WANT the rover's final state printed as a formatted string on stdout
SO THAT I can read the result in a consistent, predictable format
```

---

### 2. Frontend Story — CMD-FE-002.1

**Focus:** stdout output format for both successful and obstacle-halted runs

```
AS A mission operator
I WANT to see either "x:y:DIR" or "O:x:y:DIR" on stdout after the simulation ends
SO THAT I can immediately distinguish a completed run from a halted one
```

#### SCENARIO 1: Successful run prints x:y:DIR

**Scenario ID:** CMD-FE-002.1-S1

**GIVEN**
* the simulation completes without hitting an obstacle
* final rover state is position `(1, 2)`, direction `E`

**WHEN**
* `OutputFormatter` formats the result

**THEN**
* stdout prints `1:2:E`

---

#### SCENARIO 2: Obstacle-halted run prints O:x:y:DIR

**Scenario ID:** CMD-FE-002.1-S2

**GIVEN**
* the simulation halted due to an obstacle
* rover state at halt is position `(0, 0)`, direction `N`

**WHEN**
* `OutputFormatter` formats the result

**THEN**
* stdout prints `O:0:0:N`

---

### 3. Backend Story — CMD-BE-002.1

**Focus:** `OutputFormatter` composes the result string from rover state and an obstacle flag

```
AS A OutputFormatter
I WANT to receive the rover's position, direction, and a halted flag
SO THAT I produce the correct string without any formatting logic leaking into the domain
```

#### SCENARIO 1: Normal result — format is "x:y:DIR"

**Scenario ID:** CMD-BE-002.1-S1

**GIVEN**
* rover position `(3, 4)`, direction `S`, obstacle flag `false`

**WHEN**
* `OutputFormatter.format(position, direction, halted=false)` is called

**THEN**
* returns `"3:4:S"`

---

#### SCENARIO 2: Halted result — format is "O:x:y:DIR"

**Scenario ID:** CMD-BE-002.1-S2

**GIVEN**
* rover position `(2, 1)`, direction `W`, obstacle flag `true`

**WHEN**
* `OutputFormatter.format(position, direction, halted=true)` is called

**THEN**
* returns `"O:2:1:W"`

---

#### SCENARIO 3: All four directions are formatted correctly

**Scenario ID:** CMD-BE-002.1-S3

**GIVEN**
* four rover states: `(0,0,N)`, `(0,0,E)`, `(0,0,S)`, `(0,0,W)`, all non-halted

**WHEN**
* `OutputFormatter.format` is called for each

**THEN**
* returns `"0:0:N"`, `"0:0:E"`, `"0:0:S"`, `"0:0:W"` respectively

---

### 4. Infrastructure Story — CMD-INFRA-002.1

**Focus:** stdout as output channel; `Main` calls formatter and prints result

```
AS A developer
I WANT Main to pass the simulation result to OutputFormatter and print to stdout
SO THAT all I/O is confined to the infrastructure layer
```

#### SCENARIO 1: Main prints formatter output to stdout

**Scenario ID:** CMD-INFRA-002.1-S1

**GIVEN**
* `MissionControl` returns a result (position, direction, halted flag)

**WHEN**
* `Main` calls `OutputFormatter.format(result)` and prints the return value

**THEN**
* the string is written to `System.out`
* `OutputFormatter` has no reference to `System.out` — it only returns a `String`

---

#### Data Model
- `OutputFormatter` is stateless; takes rover state + halted flag, returns a `String`
- No intermediate representation; format is assembled directly: `(halted ? "O:" : "") + x + ":" + y + ":" + direction`

#### Execution Model
- Called once per run, after `MissionControl` completes or catches `ObstacleException`
- Synchronous; result printed immediately to `System.out` by `Main`

#### Observability
- The printed string is the sole observable output of a successful run
- No additional logging; the format itself encodes the run outcome

---

## CMD-STORY-003 · P2 · Reject invalid commands and directions at input

**Architecture References**
- Domain: Command Processing
- Components: `InputParser`, `Main` (§5.2)
- Cross-cutting: Input Validation — direction one of `N,E,S,W`; commands only `L,R,M`; grid dimensions positive integers (§8.4)
- ADR: ADR-004 (infrastructure layer rejects bad input before domain is touched)

---

### 1. Original Story

```
AS A mission operator
I WANT the system to reject unrecognised directions, commands, and non-positive grid dimensions
SO THAT the simulation never starts with malformed input
```

---

### 2. Frontend Story — CMD-FE-003.1

**Focus:** stderr message identifies the specific invalid token; stdout stays empty

```
AS A mission operator
I WANT a clear stderr message naming the invalid token when my input is malformed
SO THAT I can correct exactly the right part of my input
```

#### SCENARIO 1: Unknown direction character produces named error

**Scenario ID:** CMD-FE-003.1-S1

**GIVEN**
* the application is running

**WHEN**
* the user enters starting position `0 0 X`

**THEN**
* stderr prints `"Invalid direction: X"`
* stdout is empty; process exits non-zero

---

#### SCENARIO 2: Unknown command character produces named error

**Scenario ID:** CMD-FE-003.1-S2

**GIVEN**
* the application is running

**WHEN**
* the user enters commands `"MXL"`

**THEN**
* stderr prints `"Invalid command: X"`
* stdout is empty; process exits non-zero

---

#### SCENARIO 3: Non-positive grid dimension produces named error

**Scenario ID:** CMD-FE-003.1-S3

**GIVEN**
* the application is running

**WHEN**
* the user enters grid size `0 5`

**THEN**
* stderr prints `"Invalid grid dimension: 0"`
* stdout is empty; process exits non-zero

---

### 3. Backend Story — CMD-BE-003.1

**Focus:** `InputParser` validates each token against its allowed set before constructing domain objects

```
AS A InputParser
I WANT to validate direction, command, and grid dimension tokens individually
SO THAT each IllegalArgumentException names the exact invalid value
```

#### SCENARIO 1: Direction not in {N,E,S,W} throws with token name

**Scenario ID:** CMD-BE-003.1-S1

**GIVEN**
* direction token `"X"`

**WHEN**
* `InputParser` parses the direction

**THEN**
* throws `IllegalArgumentException("Invalid direction: X")`

---

#### SCENARIO 2: Command character not in {L,R,M} throws with token name

**Scenario ID:** CMD-BE-003.1-S2

**GIVEN**
* command string `"MXL"`

**WHEN**
* `InputParser` iterates characters

**THEN**
* throws `IllegalArgumentException("Invalid command: X")` on the first unknown character
* remaining characters are not processed

---

#### SCENARIO 3: Grid dimension ≤ 0 throws with value

**Scenario ID:** CMD-BE-003.1-S3

**GIVEN**
* grid input `"0 5"`

**WHEN**
* `InputParser` parses grid dimensions

**THEN**
* throws `IllegalArgumentException("Invalid grid dimension: 0")`

---

#### SCENARIO 4: All-valid input passes without exception

**Scenario ID:** CMD-BE-003.1-S4

**GIVEN**
* direction `"N"`, commands `"LRM"`, grid `"5 5"`

**WHEN**
* `InputParser` validates all tokens

**THEN**
* no exception is thrown; domain objects are returned normally

---

### 4. Infrastructure Story — CMD-INFRA-003.1

**Focus:** Single catch in `Main` handles all `IllegalArgumentException` from `InputParser`; no duplicate error paths

```
AS A developer
I WANT all input validation errors to propagate as IllegalArgumentException to the single catch in Main
SO THAT error handling is centralised and consistent
```

#### SCENARIO 1: Single catch in Main handles all parse errors uniformly

**Scenario ID:** CMD-INFRA-003.1-S1

**GIVEN**
* `InputParser` throws `IllegalArgumentException` for any invalid token (direction, command, or dimension)

**WHEN**
* `Main` catches the exception

**THEN**
* the exception message is written to `System.err`
* `System.exit` is called with a non-zero code
* no separate catch blocks are needed per error type

---

#### Data Model
- No new structures; validation is guard clauses in `InputParser` using `switch`/`valueOf` with explicit fallthrough for unknowns

#### Execution Model
- Fail-fast: first invalid token throws immediately; subsequent tokens are not evaluated
- All validation completes before any domain object is constructed

#### Observability
- Error message on `stderr` names the invalid token — sufficient for the operator to identify and fix the input
