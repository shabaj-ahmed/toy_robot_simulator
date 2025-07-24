"""
navigation.py

This file defines the Navigation class, which is responsible for validating whether 
a given (x, y) position is within the bounds of the tabletop grid.

Responsibilities:
- Enforce grid boundaries
- Prevent unsafe movement off the table
- Log any out-of-bounds validation attempts
"""

import logging

class Navigation:
    """
    The Navigation class provides utility methods to check whether a position is 
    within the boundaries of the tabletop grid.
    """

    def __init__(self, grid_size: int = 5) -> None:
        """
        Initialise the navigation system with a square grid of the specified size.

        Parameters:
        - grid_size (int): The dimension of the square grid (default: 5)
        """
        self.grid_size: int = grid_size
        self.logger = logging.getLogger(self.__class__.__name__)

    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check whether the given position (x, y) lies within the grid boundaries.

        Parameters:
        - x (int): X-coordinate on the grid
        - y (int): Y-coordinate on the grid

        Returns:
        - bool: True if the position is valid, False otherwise
        """
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return True
        else:
            self.logger.warning(f"Invalid position check: ({x},{y}) is out of bounds.")
            return False

