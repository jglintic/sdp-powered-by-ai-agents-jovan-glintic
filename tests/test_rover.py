from mars_rover.domain import Command, Direction, Grid, Rover


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
