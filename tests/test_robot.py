import pytest
from robot import Robot

def test_place_sets_position_and_direction():
    robot = Robot()
    robot.place(2, 3, "EAST")
    assert robot.current_x == 2
    assert robot.current_y == 3
    assert robot.current_direction == "EAST"
    assert robot.is_placed

def test_propose_move_returns_correct_position():
    robot = Robot()
    robot.place(0, 0, "NORTH")
    new_x, new_y, direction = robot.propose_move()
    assert (new_x, new_y, direction) == (0, 1, "NORTH")

def test_turn_left_changes_direction_counterclockwise():
    robot = Robot()
    robot.place(0, 0, "NORTH")
    robot.turn_left()
    assert robot.current_direction == "WEST"

def test_turn_right_changes_direction_clockwise():
    robot = Robot()
    robot.place(0, 0, "NORTH")
    robot.turn_right()
    assert robot.current_direction == "EAST"

def test_turn_left_full_circle():
    robot = Robot()
    robot.place(0, 0, "NORTH")
    for _ in range(4):
        robot.turn_left()
    assert robot.current_direction == "NORTH"

def test_turn_right_full_circle():
    robot = Robot()
    robot.place(0, 0, "NORTH")
    for _ in range(4):
        robot.turn_right()
    assert robot.current_direction == "NORTH"

def test_update_position_changes_coordinates():
    robot = Robot()
    robot.place(0, 0, "NORTH")
    robot.update_position(1, 1)
    assert robot.current_x == 1
    assert robot.current_y == 1
    assert robot.current_direction == "NORTH"

def test_report_returns_correct_format(capfd):
    robot = Robot()
    robot.place(1, 2, "EAST")
    robot.report()

    out, err = capfd.readouterr()
    assert out.strip() == "1,2,EAST"
