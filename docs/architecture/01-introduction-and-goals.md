# Chapter 1: Introduction and Goals

## 1.1 Requirements Overview

The Mars Rover kata simulates a rover navigating a bounded grid on Mars. The system accepts a sequence of commands and returns the rover's final state.

**Core capabilities:**

- Place a rover at a starting position `(x, y)` with an initial direction `(N, E, S, W)`
- Accept a command string composed of:
  - `L` — turn left (90°)
  - `R` — turn right (90°)
  - `M` — move one step forward in the current direction
- Wrap around grid edges (toroidal grid)
- Detect obstacles before moving; halt and report if one is encountered
- Return the final position and direction, or an obstacle report

## 1.2 Quality Goals

| Priority | Quality Goal     | Motivation                                                                 |
|----------|------------------|----------------------------------------------------------------------------|
| 1        | Correctness      | Commands must produce accurate position and direction changes              |
| 2        | Testability      | Core logic must be unit-testable in isolation                              |
| 3        | Extensibility    | New commands or grid behaviors should be easy to add                       |
| 4        | Simplicity       | Console application with no persistence; avoid overengineering             |

## 1.3 Stakeholders

| Role         | Expectation                                                        |
|--------------|--------------------------------------------------------------------|
| Developer    | Clean, readable code that is easy to extend and test               |
| Kata Reviewer| Correct behavior for all command sequences, including edge cases   |
