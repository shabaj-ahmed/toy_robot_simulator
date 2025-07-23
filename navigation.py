"""
navigation.py

This file defines the Navigation class, responsible for validating whether a position is
within the bounds of the tabletop grid.
"""

class Navigation:
    """
    Navigation checks if a given position (x, y) is valid based on the grid size.
    """

    def __init__(self, grid_size=5):
        """
        Initialise with a square grid of the given size.
        """
        self.grid_size = grid_size

    def is_valid_position(self, x, y):
        """
        Returns True if (x, y) is within the bounds of the grid.
        """
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size
