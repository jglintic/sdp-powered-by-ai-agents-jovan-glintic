# Chapter 8: Cross-cutting Concepts

## 8.1 Authentication & Authorization

Not applicable. The system is a local console application with no users, sessions, or access control.

## 8.2 Error Handling

Two categories of error are handled:

| Error | Handling Strategy |
|-------|-------------------|
| Obstacle encountered | `Rover` throws `ObstacleException` (unchecked); `MissionControl` catches it, halts execution, returns current state with `O:` prefix |
| Invalid input | `InputParser` throws `IllegalArgumentException` with a descriptive message; `Main` catches and prints to stderr |

**Principles:**
- Domain errors (obstacle) are modeled as exceptions, not return codes — keeps `Rover` API clean
- No silent failures; every error produces visible output
- `Rover` state is never partially updated — position only changes after a successful obstacle check

## 8.3 Logging

No logging framework is used. This is a kata, not a production system.

- Normal output → `stdout`
- Error output → `stderr`
- No log files, no log levels, no structured logging

## 8.4 Input Validation

`InputParser` validates:
- Direction is one of `N, E, S, W`
- Commands contain only `L`, `R`, `M`
- Grid dimensions are positive integers
- Starting position is within grid bounds

Invalid input causes immediate termination with an error message on `stderr`.

## 8.5 Domain Model Integrity

- `Position` is an immutable value object (Java `record`); wrapping is applied at construction time
- `Direction` is an enum; invalid directions are impossible by construction
- `Command` is an enum; unknown characters are rejected by `InputParser` before reaching the domain
