# Chapter 7: Deployment View

## 7.1 Overview

The Mars Rover system is a single JVM process executed from the command line. There is no network, no container runtime, and no external infrastructure.

## 7.2 Deployment Topology

| Node | Description |
|------|-------------|
| Developer workstation | Any OS with JDK 17+ installed |
| JVM process | Single process; launched via `java -jar` or `mvn exec:java` |
| stdin / stdout | Sole I/O channels; no files, sockets, or databases |

See [`diagrams/deployment.svg`](diagrams/deployment.svg).

## 7.3 Build and Run

```bash
# Build
mvn package

# Run
java -jar target/mars-rover.jar

# Test
mvn test
```

## 7.4 Deployment Constraints

- JDK 17 or higher required (records, enhanced switch)
- No environment variables, config files, or external dependencies at runtime
- The application is stateless between runs; each execution is independent
