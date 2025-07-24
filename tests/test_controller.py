import pytest
from toy_robot.controller import RobotController

def test_ignore_invalid_commands(caplog):
    controller = RobotController()
    for cmd in ["JUMP", "FLY", "PLACE2,3,EAST"]:
        controller.process_command(cmd)
    assert "Unrecognised command" in caplog.text

def test_invalid_place_command_format(caplog):
    controller = RobotController()
    for cmd in ["PLACE 1,A,EAST", "RIGHT", "MOVE"]:
        controller.process_command(cmd)
    assert "Invalid PLACE command format: PLACE 1,A,EAST - invalid literal for int() with base 10: 'A'" in caplog.text

def test_case_insensitive_command_is_ignored():
    controller = RobotController()
    controller.process_command("place 0,0,NORTH")
    assert not controller.robot.is_placed

def test_case_insensitive_direction_is_ignored():
    controller = RobotController()
    controller.process_command("PLACE 0,0,north")
    assert not controller.robot.is_placed

def test_valid_place_command(caplog):
    controller = RobotController()
    controller.process_command("PLACE 5,6,EAST")
    assert "PLACE ignored: invalid position (5,6,EAST)" in caplog.text

def test_place_and_report(monkeypatch, capsys):
    controller = RobotController()
    for cmd in ["PLACE 1,2,EAST", "REPORT"]:
        controller.process_command(cmd)
    captured = capsys.readouterr()
    assert "1,2,EAST" in captured.out

def test_prevent_move_off_table(caplog):
    controller = RobotController()
    for cmd in ["PLACE 0,0,SOUTH", "MOVE"]:
        controller.process_command(cmd)
    assert "Unsafe MOVE ignored" in caplog.text

def test_ignore_move_before_place(caplog):
    controller = RobotController()
    controller.process_command("MOVE")
    assert "Ignoring 'MOVE' as no PLACE command has been issued yet." in caplog.text
