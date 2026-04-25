# Chapter 12: Glossary

| Term | Definition |
|------|------------|
| **Rover** | The simulated vehicle navigating the grid. Holds a position and direction. |
| **Position** | An immutable `(x, y)` coordinate on the grid. Wrapping is applied at construction. |
| **Direction** | One of four cardinal directions: `N` (North), `E` (East), `S` (South), `W` (West). |
| **Command** | A single instruction: `L` (turn left 90°), `R` (turn right 90°), `M` (move forward one step). |
| **Grid** | The bounded surface the rover moves on. Defined by width and height; holds the obstacle set. |
| **Obstacle** | A cell on the grid the rover cannot enter. Stored as a `Set<Position>`. |
| **Toroidal grid** | A grid where moving off one edge reappears on the opposite edge (wrap-around). |
| **MissionControl** | The application component that iterates commands and orchestrates rover execution. |
| **ObstacleException** | Unchecked exception thrown by `Rover` when a move is blocked by an obstacle. |
| **InputParser** | Infrastructure component that parses raw console input into domain objects. |
| **OutputFormatter** | Infrastructure component that formats the rover's final state as a result string. |
| **O: prefix** | Output convention indicating the rover was halted by an obstacle (e.g. `O:0:0:N`). |
| **ADR** | Architecture Decision Record — a document capturing a significant design choice and its rationale. |
| **C4 model** | A hierarchical diagramming approach: Context → Container → Component → Code. |
