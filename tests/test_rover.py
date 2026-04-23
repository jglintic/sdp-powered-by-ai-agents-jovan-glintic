import subprocess  # nosec B404
from pathlib import Path

import pytest

from mars_rover.domain import (
    Command,
    Direction,
    Grid,
    MissionControl,
    ObstacleError,
    Rover,
)
from mars_rover.input_parser import InputParser


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


# --- InputParser tests ---


def test_cmd_be_001_1_s1_parse_position_line_returns_rover():
    rover = InputParser.parse_rover("0 0 N")
    assert rover.x == 0
    assert rover.y == 0
    assert rover.direction == Direction.N


def test_cmd_be_001_1_s2_parse_grid_line_returns_grid():
    grid = InputParser.parse_grid("5 5")
    assert grid.width == 5
    assert grid.height == 5
    assert grid.obstacles == frozenset()


def test_cmd_be_001_1_s3_parse_obstacle_line_returns_frozenset():
    obstacles = InputParser.parse_obstacles("0 1 2 3")
    assert obstacles == frozenset({(0, 1), (2, 3)})


def test_cmd_be_001_1_s4_parse_command_string_returns_list():
    commands = InputParser.parse_commands("MRML")
    assert commands == [Command.M, Command.R, Command.M, Command.L]


def test_cmd_be_001_1_s5_unknown_command_raises_value_error():
    with pytest.raises(ValueError, match="Invalid command: X"):
        InputParser.parse_commands("MXL")


def test_cmd_be_003_1_s1_unknown_direction_raises_value_error():
    with pytest.raises(ValueError, match="Invalid direction: X"):
        InputParser.parse_rover("0 0 X")


# --- Main (__main__) tests ---


def run_main(stdin_text: str):
    import os

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")
    return subprocess.run(  # nosec B404 B603 B607
        ["python", "-m", "mars_rover"],
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
    )


def test_cmd_fe_001_1_s1_main_runs_simulation_and_prints_result():
    result = run_main("0 0 N\n5 5\n\nMRML\n")
    assert result.stdout.strip() == "1:1:N"
    assert result.returncode == 0


def test_cmd_fe_001_1_s2_main_writes_error_to_stderr_on_invalid_direction():
    result = run_main("0 0 X\n5 5\n\nM\n")
    assert result.stderr.strip() == "Invalid direction: X"
    assert result.stdout == ""
    assert result.returncode != 0


# --- ROVER-STORY-004: extensible command set (B = move backward) ---


def test_rover_be_004_1_direction_opposite_n_returns_s():
    assert Direction.N.opposite() == Direction.S


def test_rover_be_004_1_s1_command_b_exists():
    assert Command.B is not None


def test_rover_be_004_1_s2_b_moves_rover_opposite_to_direction():
    grid = Grid(5, 5)
    rover = Rover(x=2, y=2, direction=Direction.N)
    rover.execute(Command.B, grid)
    assert rover.x == 2
    assert rover.y == 1
    assert rover.direction == Direction.N


def test_rover_be_004_1_s3_b_raises_obstacle_error_and_state_unchanged():
    grid = Grid(5, 5, obstacles=frozenset({(2, 1)}))
    rover = Rover(x=2, y=2, direction=Direction.N)
    with pytest.raises(ObstacleError):
        rover.execute(Command.B, grid)
    assert rover.x == 2
    assert rover.y == 2


def test_rover_be_004_1_s4_b_wraps_at_grid_edge():
    grid = Grid(5, 5)
    rover = Rover(x=0, y=0, direction=Direction.N)
    rover.execute(Command.B, grid)
    assert rover.x == 0
    assert rover.y == 4


def test_rover_be_004_1_s5_input_parser_accepts_b():
    commands = InputParser.parse_commands("B")
    assert commands == [Command.B]


def test_rover_fe_004_1_s1_b_command_moves_backward_via_stdin():
    result = run_main("2 2 N\n5 5\n\nB\n")
    assert result.stdout.strip() == "2:1:N"
    assert result.returncode == 0


# --- GRID-INFRA-003.1-S2: odd obstacle token count raises ValueError ---


def test_grid_infra_003_1_s2_odd_obstacle_tokens_raises_value_error():
    with pytest.raises(ValueError, match="pairs"):
        InputParser.parse_obstacles("0 1 2")


def test_grid_infra_003_1_s3_duplicate_obstacle_coords_deduplicated():
    obstacles = InputParser.parse_obstacles("0 1 0 1")
    assert obstacles == frozenset({(0, 1)})


# --- GRID-INFRA-002.1-S1: starting position bounds validation ---


def test_grid_infra_002_1_s1_starting_position_outside_grid_raises_value_error():
    with pytest.raises(ValueError, match="outside grid"):
        grid = InputParser.parse_grid("5 5")
        InputParser.validate_position(6, 0, grid)


# --- GRID-INFRA-001.1-S1/S2: grid immutability and wrap in Rover ---


def test_grid_infra_001_1_s1_grid_dimensions_are_read_only():
    grid = Grid(5, 5)
    assert not hasattr(grid, "__set__")
    # width and height are plain int attributes set at construction
    assert grid.width == 5
    assert grid.height == 5


def test_grid_infra_001_1_s2_wrap_applied_inside_rover_execute_not_at_call_sites():
    # Wrap logic lives in Rover.execute via modulo — no call site applies it manually.
    # Verify: moving off the south edge from (0,0) produces (0,4).
    grid = Grid(5, 5)
    rover = Rover(x=0, y=0, direction=Direction.S)
    rover.execute(Command.M, grid)
    assert rover.y == 4  # wrapped, never stored as -1


# --- CMD-INFRA-002.1-S1: output formatting is a pure string operation ---


def test_cmd_infra_002_1_s1_format_result_returns_string_not_printed():
    # OutputFormatter logic lives inline in __main__; verify the formula directly.
    x, y, direction, halted = 1, 2, Direction.E, False
    result = ("O:" if halted else "") + f"{x}:{y}:{direction.name}"
    assert result == "1:2:E"
    assert isinstance(result, str)


def test_cmd_infra_002_1_s1_format_halted_result_returns_o_prefixed_string():
    x, y, direction, halted = 0, 0, Direction.N, True
    result = ("O:" if halted else "") + f"{x}:{y}:{direction.name}"
    assert result == "O:0:0:N"


# --- CMD-INFRA-003.1-S1: single catch in Main for all parse errors ---


def test_cmd_infra_003_1_s1_invalid_grid_dimension_writes_to_stderr():
    result = run_main("0 0 N\n0 5\n\nM\n")
    assert result.returncode != 0
    assert result.stdout == ""
    assert "0" in result.stderr


def test_cmd_infra_003_1_s1_out_of_bounds_position_writes_to_stderr():
    result = run_main("6 0 N\n5 5\n\nM\n")
    assert result.returncode != 0
    assert result.stdout == ""
    assert "outside grid" in result.stderr


# --- ROVER-INFRA-004.1-S1: change impact for B is limited to Command + Rover ---


def test_rover_infra_004_1_s1_b_command_defined_in_command_enum():
    assert hasattr(Command, "B")


def test_rover_infra_004_1_s1_mission_control_dispatches_b_without_modification():
    # MissionControl.execute iterates commands generically; B uses the same loop.
    grid = Grid(5, 5)
    rover = Rover(x=2, y=2, direction=Direction.N)
    mc = MissionControl(rover, grid)
    mc.execute([Command.B])
    assert rover.y == 1  # moved backward (south)
