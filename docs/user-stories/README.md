# Mars Rover — User Story Inventory

## Domains (Bounded Contexts)

| Domain | Package | Core Components |
|--------|---------|-----------------|
| **Rover Control** | `domain` | `Rover`, `Direction`, `Position` |
| **Command Processing** | `domain` + `application` | `Command`, `MissionControl` |
| **Grid / Map** | `domain` | `Grid`, `Position` (wrap logic) |
| **Simulation Orchestration** | `application` | `MissionControl` |
| **Output** | `infrastructure` | `InputParser`, `OutputFormatter`, `Main` |

---

## Pareto Analysis — 20% Core Stories → 80% System Value

The system has **10 stories** total. The **P0 core (3 stories = 30%)** covers the complete end-to-end execution path and delivers ~80% of observable system value.

| # | Story ID | Title | Domain | Priority | Status |
|---|----------|-------|--------|----------|--------|
| 1 | `ROVER-STORY-001` | Execute a command sequence and return final position | Rover Control + Simulation Orchestration | **P0** | ✅ Done |
| 2 | `GRID-STORY-001` | Wrap rover position at grid edges (toroidal grid) | Grid / Map | **P0** | ✅ Done |
| 3 | `ROVER-STORY-002` | Halt and report when an obstacle is encountered | Rover Control | **P0** | ✅ Done |
| 4 | `CMD-STORY-001` | Parse raw console input into domain objects | Command Processing + Output | **P1** | ✅ Done |
| 5 | `CMD-STORY-002` | Format final rover state as output string | Output | **P1** | ✅ Done |
| 6 | `ROVER-STORY-003` | Rotate rover left and right | Rover Control | **P1** | ✅ Done |
| 7 | `GRID-STORY-002` | Validate starting position is within grid bounds | Grid / Map | **P1** | ✅ Done |
| 8 | `CMD-STORY-003` | Reject invalid commands and directions at input | Command Processing | **P2** | ✅ Done |
| 9 | `ROVER-STORY-004` | Support extensible command set (add new command) | Rover Control | **P2** | ✅ Done |
| 10 | `GRID-STORY-003` | Support multiple obstacles on the grid | Grid / Map | **P2** | ✅ Done |

---

## Pareto Progress

```
P0 Core (3 stories — ~80% value)
[x] ROVER-STORY-001   Execute command sequence → final position
[x] GRID-STORY-001    Toroidal wrap-around
[x] ROVER-STORY-002   Obstacle halt + report

P1 Correctness (4 stories)
[x] CMD-STORY-001     Parse console input
[x] CMD-STORY-002     Format output string
[x] ROVER-STORY-003   Rotate left / right
[x] GRID-STORY-002    Validate starting position

P2 Enhancements (3 stories)
[x] CMD-STORY-003     Reject invalid input
[x] ROVER-STORY-004   Extensible command set
[x] GRID-STORY-003    Multiple obstacles
```

**Completed: 10 / 10 ✅ ALL STORIES DONE**

---

## Story Files

| File | Domain | Stories |
|------|--------|---------|
| [`rover-control.md`](rover-control.md) | Rover Control | ROVER-STORY-001, 002, 003, 004 |
| [`grid-map.md`](grid-map.md) | Grid / Map | GRID-STORY-001, 002, 003 |
| [`command-processing.md`](command-processing.md) | Command Processing + Output | CMD-STORY-001, 002, 003 |
