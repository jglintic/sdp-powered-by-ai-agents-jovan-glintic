# Chapter 4: Solution Strategy

## 4.1 Key Decisions

| Goal | Strategy |
|------|----------|
| Correctness | Model direction as an ordered enum; rotation is index arithmetic, not conditionals |
| Testability | Pure domain logic with no I/O dependencies; `Rover` and `Grid` are plain Java objects |
| Extensibility | Commands modeled as an enum or strategy; adding a new command requires no changes to existing classes |
| Simplicity | No frameworks, no DI container; `Main` wires everything together manually |

## 4.2 Decomposition Strategy

The system is split into three responsibilities:

- **Domain** — `Rover`, `Position`, `Direction`, `Grid`, `Command`; pure logic, no I/O
- **Application** — `MissionControl`; orchestrates command execution against the rover and grid
- **Infrastructure** — `Main`, `InputParser`, `OutputFormatter`; handles console I/O and wiring

## 4.3 Key Algorithmic Choices

**Direction rotation** — `Direction` is an enum with a fixed cyclic order `[N, E, S, W]`. Turning left/right is `(index ± 1) % 4`, eliminating branching.

**Movement** — Each `Direction` knows its own `(dx, dy)` delta. Moving forward applies the delta and wraps via modulo on grid dimensions.

**Obstacle detection** — Before applying a move, the next position is computed and checked against the obstacle set. If blocked, execution halts and reports the current position with an `O:` prefix.

## 4.4 Technology Choices

| Concern | Choice | Reason |
|---------|--------|--------|
| Language | Java | Kata requirement |
| Testing | JUnit 5 | Standard; no extra setup |
| Build | Maven or plain `javac` | No framework dependencies to manage |
| Data structures | `Set<Position>` for obstacles | O(1) lookup |
