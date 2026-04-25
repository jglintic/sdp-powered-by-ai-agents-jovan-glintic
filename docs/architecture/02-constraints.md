# Chapter 2: Architecture Constraints

## 2.1 Technical Constraints

| Constraint | Rationale |
|------------|-----------|
| Java (console application) | Kata requirement; no framework needed |
| In-memory data model only | No persistence required; keeps the solution focused |
| No external dependencies | Pure Java; no libraries beyond the JDK and a test framework |
| JUnit for unit testing | Standard Java testing tool; validates core logic in isolation |

## 2.2 Organizational Constraints

| Constraint | Rationale |
|------------|-----------|
| Single deployable unit | Console app run from the command line; no server or container needed |
| No UI beyond console output | Output is a string representing final position/direction or obstacle report |

## 2.3 Conventions

| Convention | Rationale |
|------------|-----------|
| Object-oriented design | Commands, directions, and grid modeled as types, not primitives |
| No static state | All state held in object instances for testability |
| Grid wrapping is toroidal | Standard kata rule: moving off one edge reappears on the opposite edge |
