"""
test_integration.py

This file contains end-to-end integration tests for the RobotController class,
verifying the robot's behavior across multiple commands and interactions.

Tests cover:
- Valid command sequences
- Ignoring commands before valid placement
- Behavior at table boundaries
- Command overrides (e.g., re-placing the robot)
- Redundant commands and output validation
"""

import pytest
from toy_robot.controller import RobotController
from toy_robot.robot import Robot
from toy_robot.navigation import Navigation

class TestCommandSequences:
    def setup_method(self):
        self.controller = RobotController(robot=Robot(), navigation=Navigation())

    def test_standard_command_sequence(self, capsys):
        """
        Test a normal sequence of commands resulting in a valid final position.
        """
        for cmd in ["PLACE 1,2,EAST", "MOVE", "MOVE", "LEFT", "MOVE", "REPORT"]:
            self.controller.process_command(cmd)
        captured = capsys.readouterr()
        assert "3,3,NORTH" in captured.out

    def test_move_before_place_ignored(self, caplog):
        """
        Test that commands issued before a valid PLACE are ignored.
        """
        for cmd in ["MOVE", "PLACE 1,2,EAST", "MOVE", "MOVE", "LEFT", "MOVE", "REPORT"]:
            self.controller.process_command(cmd)
        assert "Ignoring 'MOVE' as no PLACE command has been issued yet." in caplog.text

    def test_invalid_then_valid_place_command(self, capsys):
        """
        Test that an invalid PLACE is ignored and a valid one overrides it.
        """
        for cmd in ["PLACE 5,5,EAST", "PLACE 0,0,NORTH", "MOVE", "REPORT"]:
            self.controller.process_command(cmd)
        captured = capsys.readouterr()
        assert "0,1,NORTH" in captured.out

    @pytest.mark.parametrize("place, expected", [
        ("PLACE 0,0,SOUTH", "0,0,SOUTH"),
        ("PLACE 4,4,NORTH", "4,4,NORTH"),
        ("PLACE 0,0,WEST",  "0,0,WEST"),
        ("PLACE 4,4,EAST",  "4,4,EAST"),
    ])
    def test_boundary_place_and_move_ignored(self, place, expected, capsys):
        """
        Test that a MOVE at the edge of the grid is ignored and the robot remains in place.
        """
        for cmd in [place, "MOVE", "REPORT"]:
            self.controller.process_command(cmd)
        captured = capsys.readouterr()
        assert expected in captured.out

    def test_multiple_place_resets_position(self, capsys):
        """
        Test that a second PLACE command overrides the initial position and direction.
        """
        for cmd in ["PLACE 1,1,NORTH", "MOVE", "PLACE 2,2,SOUTH", "MOVE", "REPORT"]:
            self.controller.process_command(cmd)
        captured = capsys.readouterr()
        assert "2,1,SOUTH" in captured.out

    def test_move_without_place_ignored(self, capsys):
        """
        Test that all commands are ignored if PLACE hasn't been called.
        """
        for cmd in ["MOVE", "LEFT", "RIGHT", "REPORT"]:
            self.controller.process_command(cmd)
        captured = capsys.readouterr()
        assert "" in captured.out

    def test_redundant_turns(self, capsys):
        """
        Test that unnecessary LEFT and RIGHT commands don't affect position if robot stays in place.
        """
        for cmd in ["PLACE 0,0,SOUTH", "LEFT", "RIGHT", "REPORT"]:
            self.controller.process_command(cmd)
        captured = capsys.readouterr()
        assert "0,0,SOUTH" in captured.out
