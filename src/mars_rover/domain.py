from enum import Enum


class Direction(Enum):
    N = (0, 1)
    E = (1, 0)
    S = (0, -1)
    W = (-1, 0)

    @property
    def dx(self):
        return self.value[0]

    @property
    def dy(self):
        return self.value[1]

    def rotate(self, command: "Command") -> "Direction":
        directions = list(Direction)
        delta = 1 if command == Command.R else -1
        return directions[(directions.index(self) + delta) % 4]


class Command(Enum):
    M = "M"
    L = "L"
    R = "R"


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Rover:
    def __init__(self, x: int, y: int, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction

    def execute(self, command: Command, grid: Grid):
        if command == Command.M:
            self.x = (self.x + self.direction.dx) % grid.width
            self.y = (self.y + self.direction.dy) % grid.height
        elif command in (Command.L, Command.R):
            self.direction = self.direction.rotate(command)


class MissionControl:
    def __init__(self, rover: Rover, grid: Grid):
        self.rover = rover
        self.grid = grid

    def execute(self, commands: list[Command]):
        for command in commands:
            self.rover.execute(command, self.grid)
