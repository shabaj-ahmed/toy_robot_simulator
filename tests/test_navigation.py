import pytest
from navigation import Navigation

def test_valid_position_within_bounds():
    nav = Navigation(grid_size=5)
    assert nav.is_valid_position(0, 0)
    assert nav.is_valid_position(4, 4)

def test_invalid_position_out_of_bounds():
    nav = Navigation(grid_size=5)
    assert not nav.is_valid_position(-1, 0)
    assert not nav.is_valid_position(0, 5)
    assert not nav.is_valid_position(5, 5)
