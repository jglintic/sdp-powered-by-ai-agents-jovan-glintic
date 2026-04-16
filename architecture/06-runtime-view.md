# Chapter 6: Runtime View

## 6.1 Scenario 1 — Successful Command Execution

The rover receives a command sequence with no obstacles in the path. All moves succeed and the final position is returned.

See [`diagrams/seq-happy-path.svg`](diagrams/seq-happy-path.svg).

## 6.2 Scenario 2 — Obstacle Encountered

The rover moves until it would enter a cell occupied by an obstacle. Execution halts immediately and the current position is reported with an `O:` prefix.

See [`diagrams/seq-obstacle.svg`](diagrams/seq-obstacle.svg).
