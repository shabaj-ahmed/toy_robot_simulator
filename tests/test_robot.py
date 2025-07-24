"""
test_robot.py

Unit tests for the Robot class, which manages placement, direction, movement, and reporting.
"""

import pytest
from toy_robot.robot import Robot

class TestPlacement:
    def test_place_sets_position_and_direction(self):
        """
        Test that placing the robot updates its position and direction correctly.
        """
        robot = Robot()
        robot.place(2, 3, "EAST")
        assert (robot.current_x, robot.current_y, robot.current_direction) == (2, 3, "EAST")
        assert robot.is_placed

class TestMovement:
    def test_propose_move_returns_correct_position(self):
        """
        Test that proposing a move returns the expected new position without changing state.
        """
        robot = Robot()
        robot.place(0, 0, "NORTH")
        assert robot.propose_move() == (0, 1, "NORTH")

    def test_update_position_changes_coordinates(self):
        """
        Test that updating the robot's position changes its coordinates correctly.
        """
        robot = Robot()
        robot.place(0, 0, "NORTH")
        robot.update_position(1, 2)
        assert (robot.current_x, robot.current_y) == (1, 2)

class TestTurning:
    @pytest.mark.parametrize("turn_method, expected", [
        ("turn_left", "WEST"),
        ("turn_right", "EAST"),
    ])
    def test_turn_once_changes_direction(self, turn_method, expected):
        """
        Test that turning left or right changes the robot's direction as expected.
        """
        robot = Robot()
        robot.place(0, 0, "NORTH")
        getattr(robot, turn_method)()
        assert robot.current_direction == expected

    @pytest.mark.parametrize("turn_method", ["turn_left", "turn_right"])
    def test_turn_full_circle_returns_to_original_direction(self, turn_method):
        """
        Test that turning left or right four times returns the robot to its original direction.
        """
        robot = Robot()
        robot.place(0, 0, "NORTH")
        for _ in range(4):
            getattr(robot, turn_method)()
        assert robot.current_direction == "NORTH"

class TestReporting:
    def test_report_returns_correct_format(self, capfd):
        """
        Test that reporting the robot's position outputs the correct format.
        """
        robot = Robot()
        robot.place(1, 2, "EAST")
        robot.report()
        out, _ = capfd.readouterr()
        assert out.strip() == "1,2,EAST"
