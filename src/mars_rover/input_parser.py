from .domain import Command, Direction, Grid, Rover


class InputParser:
    @staticmethod
    def parse_rover(line: str) -> Rover:
        x, y, d = line.split()
        try:
            direction = Direction[d]
        except KeyError:
            raise ValueError(f"Invalid direction: {d}") from None
        return Rover(int(x), int(y), direction)

    @staticmethod
    def parse_grid(line: str) -> Grid:
        w, h = line.split()
        return Grid(int(w), int(h))

    @staticmethod
    def parse_obstacles(line: str) -> frozenset:
        tokens = line.split()
        if len(tokens) % 2 != 0:
            raise ValueError("Obstacle coordinates must be provided in x y pairs")
        return frozenset(
            (int(tokens[i]), int(tokens[i + 1])) for i in range(0, len(tokens), 2)
        )

    @staticmethod
    def validate_position(x: int, y: int, grid: Grid) -> None:
        if not (0 <= x < grid.width and 0 <= y < grid.height):
            raise ValueError(
                f"Starting position ({x}, {y}) is outside grid "
                f"{grid.width}x{grid.height}"
            )

    @staticmethod
    def parse_commands(line: str) -> list:
        result = []
        for c in line:
            try:
                result.append(Command[c])
            except KeyError:
                raise ValueError(f"Invalid command: {c}") from None
        return result
