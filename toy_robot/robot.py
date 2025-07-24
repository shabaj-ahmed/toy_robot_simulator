"""
robot.py

This file defines the Robot class, which maintains the robot's position, direction, 
and implements logic for movement and rotation.

It delegates safety validation (e.g., table boundaries) to the Navigation class 
and only updates its internal state when the update methods are explicitly called.

Responsibilities:
- Store the robot’s current position and direction
- Update position and direction based on commands
- Generate movement proposals without executing moves
- Prints a formatted report of the robot’s position and direction
"""

class Robot:
    """
    The Robot class stores the robot's current position (x, y) and direction.

    It provides methods to:
    - Place the robot on the grid
    - Rotate left or right
    - Propose a move without updating position and direction
    - Executes a move when requested to update position
    - Prints a report to the console of the current position and direction
    """

    # Constants for cardinal directions
    GET_CARDINAL_DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]
    GET_DIRECTION_DELTAS = {
        "NORTH": (0, 1),
        "EAST": (1, 0),
        "SOUTH": (0, -1),
        "WEST": (-1, 0)
    }

    def __init__(self):
        """
        Initialise the robot. The robot is not placed on the table initially.
        """
        self.current_x = None
        self.current_y = None
        self.current_direction = None
        self.is_placed = False

    def place(self, x, y, direction):
        """
        Place the robot on the grid at a specific location and orientation.

        Parameters:
        - x (int): X-coordinate
        - y (int): Y-coordinate
        - direction (str): One of 'NORTH', 'EAST', 'SOUTH', 'WEST'
        """
        self.current_x = x
        self.current_y = y
        self.current_direction = direction
        self.is_placed = True

    def propose_move(self):
        """
        Propose the next position based on the current direction without changing state.

        Returns:
        - tuple: (new_x, new_y, direction) representing the proposed move
        """
        dx, dy = self.GET_DIRECTION_DELTAS[self.current_direction]
        return self.current_x + dx, self.current_y + dy, self.current_direction
    
    def update_position(self, new_x, new_y):
        """
        Update the robot’s position.

        Parameters:
        - new_x (int): New X-coordinate
        - new_y (int): New Y-coordinate
        """
        self.current_x = new_x
        self.current_y = new_y

    def turn_left(self):
        """
        Rotate the robot 90° counter-clockwise.
        """
        idx = self.GET_CARDINAL_DIRECTIONS.index(self.current_direction)
        self.current_direction = self.GET_CARDINAL_DIRECTIONS[(idx - 1) % 4]

    def turn_right(self):
        """
        Rotate the robot 90 degrees clockwise.
        """
        idx = self.GET_CARDINAL_DIRECTIONS.index(self.current_direction)
        self.current_direction = self.GET_CARDINAL_DIRECTIONS[(idx + 1) % 4]

    def report(self):
        """
        Print the robot's current position and direction in the format: X,Y,DIRECTION
        """
        print(f"{self.current_x},{self.current_y},{self.current_direction}")
