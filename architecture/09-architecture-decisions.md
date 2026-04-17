# Chapter 9: Architecture Decisions

## ADR-001: Direction as a Cyclic Enum

**Status:** Accepted

**Context:**
The rover must turn left and right from any of four cardinal directions. A naive implementation uses nested `if/switch` statements, which are error-prone and hard to extend.

**Decision:**
Model `Direction` as an enum with a fixed cyclic order `[N, E, S, W]`. Rotation is `(index ± 1) % 4`.

**Rationale:**
Eliminates all direction-related branching. Adding a new direction (e.g. diagonal) requires only adding an enum constant and a delta — no changes to rotation logic.

**Consequences:**
- (+) Zero conditional logic for rotation
- (+) Each direction owns its `(dx, dy)` delta — movement logic is also branch-free
- (-) Cyclic order must be maintained correctly in the enum declaration

---

## ADR-002: Obstacle Detection via Exception

**Status:** Accepted

**Context:**
When a move is blocked by an obstacle, execution must halt and the current state must be reported. Options: return a result type (e.g. `Optional`, sealed result), use a boolean flag, or throw an exception.

**Decision:**
`Rover` throws an unchecked `ObstacleException` when a move is blocked. `MissionControl` catches it and returns the current rover state.

**Rationale:**
Keeps the `Rover.execute()` API simple (void return). The obstacle case is genuinely exceptional within the command loop. A result type would require every call site to unwrap it.

**Consequences:**
- (+) Clean `Rover` API; no return type pollution
- (+) Halts the command loop naturally without extra control flow
- (-) Uses exceptions for flow control, which is a mild anti-pattern; acceptable at kata scale

---

## ADR-003: Position as an Immutable Record

**Status:** Accepted

**Context:**
Position `(x, y)` is a value that changes with each move. It can be modeled as a mutable field pair on `Rover`, a mutable class, or an immutable value object.

**Decision:**
Model `Position` as a Java `record` with wrapping applied in a factory/constructor. `Rover` replaces its `Position` reference on each successful move.

**Rationale:**
Immutability makes it safe to pass `Position` to `Grid` for obstacle checking without defensive copying. Records provide `equals`/`hashCode` for free, which is required for `Set<Position>` obstacle lookup.

**Consequences:**
- (+) Safe to use as `Set` key without custom `equals`/`hashCode`
- (+) No risk of `Grid` mutating a position it receives
- (-) A new object is allocated per move; negligible at kata scale

---

## ADR-004: Three-Layer Package Structure

**Status:** Accepted

**Context:**
The system needs separation between I/O concerns and domain logic to keep the domain unit-testable without console setup.

**Decision:**
Split into three packages: `domain` (pure logic), `application` (orchestration), `infrastructure` (I/O and wiring).

**Rationale:**
Domain classes have zero I/O dependencies and can be tested with plain JUnit. `MissionControl` can also be tested without touching `Main`. The boundary is enforced by package structure, not a framework.

**Consequences:**
- (+) Domain and application layers are fully unit-testable in isolation
- (+) `InputParser` and `OutputFormatter` can be changed without touching domain logic
- (-) Slight overhead of three packages for a small kata; justified by testability goal
