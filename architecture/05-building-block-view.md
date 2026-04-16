# Chapter 5: Building Block View

## 5.1 Level 1 — Container View

The system is a single Java process. There are no separate containers (no server, no database).

See [`diagrams/c4-container.svg`](diagrams/c4-container.svg).

## 5.2 Level 2 — Component View

The single container is decomposed into three packages:

### `infrastructure`
| Component | Responsibility |
|-----------|----------------|
| `Main` | Entry point; wires components and starts the app |
| `InputParser` | Parses console input into domain objects |
| `OutputFormatter` | Formats the result string for console output |

### `application`
| Component | Responsibility |
|-----------|----------------|
| `MissionControl` | Iterates commands; delegates to `Rover`; returns result |

### `domain`
| Component | Responsibility |
|-----------|----------------|
| `Rover` | Holds position + direction; applies `Command` |
| `Grid` | Holds dimensions and obstacle set; validates moves |
| `Position` | Value object: `(x, y)` with wrapping logic |
| `Direction` | Enum: `N, E, S, W`; knows `(dx, dy)` and rotation |
| `Command` | Enum: `L, R, M` |

See [`diagrams/c4-component.svg`](diagrams/c4-component.svg).

## 5.3 Key Relationships

- `MissionControl` owns a `Rover` and a `Grid`
- `Rover` delegates move validation to `Grid` before updating its `Position`
- `Direction` encapsulates all rotation and delta logic — no direction-related conditionals elsewhere
- `InputParser` and `OutputFormatter` depend only on domain types; they are unaware of `MissionControl`
