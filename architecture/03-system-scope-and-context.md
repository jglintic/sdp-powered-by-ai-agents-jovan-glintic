# Chapter 3: System Scope and Context

## 3.1 Business Context

The Mars Rover system is a self-contained console application. The user provides an initial rover configuration and a command string; the system returns the final state.

| Neighbour | Description |
|-----------|-------------|
| User (operator) | Provides starting position, direction, grid size, obstacle list, and command sequence via console input |
| Console Output | Receives the final position + direction, or an obstacle-encountered report |

There are no external systems, databases, or network interfaces.

## 3.2 Technical Context

All input is read from `stdin` and all output is written to `stdout`. The entire computation is in-memory within a single JVM process.

## 3.3 C4 System Context Diagram

See [`diagrams/c4-context.svg`](diagrams/c4-context.svg).
