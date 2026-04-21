import pytest

from mars_rover.domain import (
    Command,
    Direction,
    Grid,
    MissionControl,
    ObstacleError,
    Rover,
)


def test_rover_be_001_1_s1_move_forward_updates_position_to_0_1():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=0, y=0, direction=Direction.N)

    # WHEN
    rover.execute(Command.M, grid)

    # THEN
    assert rover.x == 0
    assert rover.y == 1
    assert rover.direction == Direction.N


def test_rover_be_003_1_s1_rotate_right_from_n_returns_e():
    # GIVEN / WHEN / THEN
    assert Direction.N.rotate(Command.R) == Direction.E


def test_rover_be_003_1_s2_rotate_left_from_n_returns_w():
    # GIVEN / WHEN / THEN
    assert Direction.N.rotate(Command.L) == Direction.W


def test_rover_be_001_1_s2_turn_right_leaves_position_unchanged():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=2, y=2, direction=Direction.N)

    # WHEN
    rover.execute(Command.R, grid)

    # THEN
    assert rover.direction == Direction.E
    assert rover.x == 2
    assert rover.y == 2


def test_rover_be_001_1_s3_full_sequence_mrml_from_0_0_n_returns_1_1_n():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=0, y=0, direction=Direction.N)
    mission = MissionControl(rover, grid)

    # WHEN
    mission.execute([Command.M, Command.R, Command.M, Command.L])

    # THEN
    assert rover.x == 1
    assert rover.y == 1
    assert rover.direction == Direction.N


def test_rover_be_001_1_s4_empty_command_list_leaves_rover_unchanged():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=3, y=3, direction=Direction.S)
    mission = MissionControl(rover, grid)

    # WHEN
    mission.execute([])

    # THEN
    assert rover.x == 3
    assert rover.y == 3
    assert rover.direction == Direction.S


def test_rover_be_002_1_s1_move_into_obstacle_raises_exception_and_position_unchanged():
    # GIVEN
    grid = Grid(5, 5, obstacles=frozenset({(0, 1)}))
    rover = Rover(x=0, y=0, direction=Direction.N)

    # WHEN / THEN
    with pytest.raises(ObstacleError):
        rover.execute(Command.M, grid)

    assert rover.x == 0
    assert rover.y == 0


def test_rover_be_002_1_s2_mission_control_stops_on_obstacle_and_returns_halted_state():
    # GIVEN
    grid = Grid(5, 5, obstacles=frozenset({(0, 1)}))
    rover = Rover(x=0, y=0, direction=Direction.N)
    mission = MissionControl(rover, grid)

    # WHEN
    result = mission.execute([Command.M, Command.M])

    # THEN
    assert result == (0, 0, Direction.N, True)
    assert rover.x == 0
    assert rover.y == 0


def test_rover_be_002_1_s3_move_to_non_obstacle_cell_succeeds():
    # GIVEN
    grid = Grid(5, 5, obstacles=frozenset({(0, 2)}))
    rover = Rover(x=0, y=0, direction=Direction.N)

    # WHEN
    rover.execute(Command.M, grid)

    # THEN
    assert rover.x == 0
    assert rover.y == 1


def test_rover_be_002_1_s4_rover_state_never_partially_updated_on_blocked_move():
    # GIVEN
    grid = Grid(5, 5, obstacles=frozenset({(4, 3)}))
    rover = Rover(x=3, y=3, direction=Direction.E)

    # WHEN / THEN
    with pytest.raises(ObstacleError):
        rover.execute(Command.M, grid)

    assert rover.x == 3
    assert rover.y == 3
    assert rover.direction == Direction.E


def test_grid_001_1_s1_move_south_from_y0_wraps_to_y4():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=0, y=0, direction=Direction.S)
    # WHEN
    rover.execute(Command.M, grid)
    # THEN
    assert rover.x == 0
    assert rover.y == 4


def test_grid_001_1_s2_move_east_from_x4_wraps_to_x0():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=4, y=2, direction=Direction.E)
    # WHEN
    rover.execute(Command.M, grid)
    # THEN
    assert rover.x == 0
    assert rover.y == 2


def test_grid_001_1_s3_move_north_from_y4_wraps_to_y0():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=2, y=4, direction=Direction.N)
    # WHEN
    rover.execute(Command.M, grid)
    # THEN
    assert rover.x == 2
    assert rover.y == 0


def test_grid_001_1_s4_move_west_from_x0_wraps_to_x4():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=0, y=3, direction=Direction.W)
    # WHEN
    rover.execute(Command.M, grid)
    # THEN
    assert rover.x == 4
    assert rover.y == 3


def test_grid_001_1_s5_move_within_bounds_no_wrap():
    # GIVEN
    grid = Grid(5, 5)
    rover = Rover(x=2, y=2, direction=Direction.N)
    # WHEN
    rover.execute(Command.M, grid)
    # THEN
    assert rover.x == 2
    assert rover.y == 3
