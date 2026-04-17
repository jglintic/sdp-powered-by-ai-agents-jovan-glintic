# Chapter 10: Quality Requirements

## 10.1 Quality Tree

| Quality Goal | Scenario | Measure |
|--------------|----------|---------|
| Correctness | All command sequences produce the expected position and direction | All unit tests pass; edge cases covered (wrap-around, obstacle halt) |
| Testability | Domain logic can be tested without I/O setup | `Rover`, `Grid`, `Direction`, `Position` have no I/O dependencies; tested with plain JUnit |
| Extensibility | A new command (e.g. `B` for move backward) can be added | Add enum constant + handler; no changes to `MissionControl` or `Rover` core loop |
| Simplicity | Codebase is understandable in one reading | No frameworks, no DI, no abstractions beyond what the problem requires |

## 10.2 Quality Scenarios

### Scenario 1 — Wrap-around correctness
- **Stimulus:** Rover at `(0, 0, S)` receives command `M` on a 5×5 grid
- **Expected:** Rover moves to `(0, 4)` (wraps to opposite edge)
- **Measure:** Unit test asserts final position `(0, 4, S)`

### Scenario 2 — Obstacle halt
- **Stimulus:** Rover at `(0, 0, N)` receives `MM` with obstacle at `(0, 1)`
- **Expected:** Rover halts at `(0, 0, N)`; output prefixed with `O:`
- **Measure:** Unit test asserts output `"O:0:0:N"`

### Scenario 3 — Rotation correctness
- **Stimulus:** Rover at `(0, 0, N)` receives `LLLL`
- **Expected:** Rover ends at `(0, 0, N)` (full rotation)
- **Measure:** Unit test asserts direction unchanged

### Scenario 4 — Extensibility
- **Stimulus:** Developer adds command `B` (move backward)
- **Expected:** Only `Command` enum and `Rover` command handler require changes
- **Measure:** No modifications to `MissionControl`, `Grid`, or `InputParser` command loop
