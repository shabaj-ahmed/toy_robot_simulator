import pytest
from toy_robot.controller import RobotController

def test_standard_command_sequence(capsys):
    controller = RobotController()
    controller.process_commands([
        "PLACE 1,2,EAST",
        "MOVE",
        "MOVE",
        "LEFT",
        "MOVE",
        "REPORT"
    ])
    captured = capsys.readouterr()
    assert "3,3,NORTH" in captured.out

def test_move_before_place_ignored(caplog):
    controller = RobotController()
    controller.process_commands([
        "MOVE",
        "PLACE 1,2,EAST",
        "MOVE",
        "MOVE",
        "LEFT",
        "MOVE",
        "REPORT"
    ])
    assert "Ignoring 'MOVE' as no PLACE command has been issued yet." in caplog.text

def test_invalid_then_valid_place_command(capsys):
    controller = RobotController()
    controller.process_commands([
        "PLACE 5,5,EAST",   # Invalid
        "PLACE 0,0,NORTH",  # Valid
        "MOVE",
        "REPORT"
    ])
    captured = capsys.readouterr()
    assert "0,1,NORTH" in captured.out

@pytest.mark.parametrize("x, y, direction, expected", [
    (0, 0, "SOUTH", "0,0,SOUTH"),
    (4, 4, "NORTH", "4,4,NORTH"),
    (0, 0, "WEST",  "0,0,WEST"),
    (4, 4, "EAST",  "4,4,EAST"),
])
def test_boundary_place_and_move_ignored(x, y, direction, expected, capsys):
    controller = RobotController()
    controller.process_commands([
        f"PLACE {x},{y},{direction}",
        "MOVE",
        "REPORT"
    ])
    captured = capsys.readouterr()
    assert expected in captured.out

def test_multiple_place_resets_position(capsys):
    controller = RobotController()
    controller.process_commands([
        "PLACE 1,1,NORTH",
        "MOVE",
        "PLACE 2,2,SOUTH",  # Re-position
        "MOVE",
        "REPORT"
    ])
    captured = capsys.readouterr()
    assert "2,1,SOUTH" in captured.out

def test_move_without_place_ignored(capsys):
    controller = RobotController()
    controller.process_commands([
        "MOVE",
        "LEFT",
        "RIGHT",
        "REPORT"
    ])
    captured = capsys.readouterr()
    assert "" in captured.out

def test_redundant_turns(capsys):
    controller = RobotController()
    controller.process_commands([
        "PLACE 0,0,NORTH",
        "LEFT",
        "LEFT",
        "REPORT"
    ])
    captured = capsys.readouterr()
    assert "0,0,SOUTH" in captured.out
