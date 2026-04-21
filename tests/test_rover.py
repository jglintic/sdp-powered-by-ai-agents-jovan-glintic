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
