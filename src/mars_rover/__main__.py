import sys

from .domain import Grid, MissionControl
from .input_parser import InputParser


def main():
    try:
        lines = sys.stdin.read().splitlines()
        rover = InputParser.parse_rover(lines[0])
        grid_base = InputParser.parse_grid(lines[1])
        obstacles = (
            InputParser.parse_obstacles(lines[2]) if lines[2].strip() else frozenset()
        )
        grid = Grid(grid_base.width, grid_base.height, obstacles)
        commands = InputParser.parse_commands(lines[3])

        x, y, direction, halted = MissionControl(rover, grid).execute(commands)
        prefix = "O:" if halted else ""
        print(f"{prefix}{x}:{y}:{direction.name}")
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


main()
