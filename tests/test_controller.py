"""
test_controller.py

Unit tests for the RobotController class, which parses and validates user commands,
coordinates robot actions, and ensures safety logic is enforced (e.g., ignoring invalid or unsafe commands).
"""

import pytest
from toy_robot.controller import RobotController
from toy_robot.robot import Robot
from toy_robot.navigation import Navigation

class TestCommandValidation:
    def test_ignores_completely_invalid_commands(self, caplog):
        """
        Commands that are unrecognised or malformed should be ignored and logged as warnings.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        invalid_cmds = ["JUMP", "FLY", "PLACE2,3,EAST"]
        for cmd in invalid_cmds:
            controller.process_command(cmd)
        assert "Unrecognised command" in caplog.text

    def test_rejects_invalid_place_format_and_logs_error(self, caplog):
        """
        PLACE commands with invalid format (e.g., non-integer or missing fields) should trigger errors.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("PLACE 1,A,EAST")
        assert "Invalid PLACE command format: PLACE 1,A,EAST - invalid literal for int() with base 10: 'A'" in caplog.text

    def test_rejects_case_insensitive_command_keyword(self):
        """
        Commands must be uppercase — lowercase or mixed case commands are ignored.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("place 0,0,NORTH")
        assert not controller.robot.is_placed

    def test_rejects_case_insensitive_direction(self):
        """
        PLACE commands with lowercase direction are considered invalid.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("PLACE 0,0,north")
        assert not controller.robot.is_placed

    def test_ignores_place_command_out_of_bounds(self, caplog):
        """
        PLACE commands with out-of-bound coordinates are ignored and logged.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("PLACE 5,6,EAST")
        assert "PLACE ignored: invalid position (5,6,EAST)" in caplog.text

class TestCommandExecution:
    def test_place_and_report_outputs_position(self, capsys):
        """
        After a valid PLACE command, REPORT should output the correct position and direction.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("PLACE 1,2,EAST")
        controller.process_command("REPORT")
        out = capsys.readouterr().out
        assert out.strip() == "Output: 1,2,EAST"

    def test_move_is_blocked_if_unsafe(self, caplog):
        """
        A MOVE that would push the robot off the grid should be ignored and logged.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("PLACE 0,0,SOUTH")
        controller.process_command("MOVE")
        assert "Unsafe MOVE ignored" in caplog.text

    def test_move_is_ignored_before_valid_place(self, caplog):
        """
        A MOVE command issued before any valid PLACE should be ignored and logged.
        """
        controller = RobotController(robot=Robot(), navigation=Navigation())
        controller.process_command("MOVE")
        assert "Ignoring 'MOVE' as no PLACE command has been issued yet." in caplog.text