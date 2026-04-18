def test_rover_initial_position():
    # GIVEN
    from rover import Rover

    rover = Rover()

    # WHEN
    position = rover.get_position()

    # THEN
    assert position == (0, 0, "N")
