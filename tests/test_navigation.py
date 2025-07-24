"""
test_navigation.py

This file contains unit tests for the Navigation class, which validates whether a given
(x, y) position is within the bounds of a 5x5 tabletop grid.
"""

from toy_robot.navigation import Navigation

def test_valid_position_at_origin():
    """
    Test that the origin (0, 0) is a valid position on the grid.
    """
    nav = Navigation(grid_size=5)
    assert nav.is_valid_position(0, 0)

def test_valid_position_at_upper_right_corner():
    """
    Test that the upper right corner (4, 4) is a valid position on the grid.
    """
    nav = Navigation(grid_size=5)
    assert nav.is_valid_position(4, 4)

def test_invalid_position_negative_coordinates():
    """
    Test that negative coordinates are invalid positions on the grid.
    """
    nav = Navigation(grid_size=5)
    assert not nav.is_valid_position(-1, 0)
    assert not nav.is_valid_position(0, -1)
    assert not nav.is_valid_position(-1, -1)

def test_invalid_position_outside_upper_bounds():
    """
    Test that coordinates greater than or equal to the grid size are invalid positions.
    """
    nav = Navigation(grid_size=5)
    assert not nav.is_valid_position(5, 0)
    assert not nav.is_valid_position(0, 5)
    assert not nav.is_valid_position(5, 5)
