"""
robot.py

This file defines the Robot class, which maintains the robot's position, direction, and logic 
for movement and rotation. It does not validate moves — that responsibility lies with Navigation.
"""

class Robot:
    """
    The Robot class stores the robot's current position (x, y) and facing direction.
    It can propose moves, turn left/right, update its position, and report its state.
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
        Place the robot on the table at the given position and direction.
        """
        self.current_x = x
        self.current_y = y
        self.current_direction = direction
        self.is_placed = True

    def propose_move(self):
        """
        Calculate the next position based on current direction without updating state.
        Returns: (new_x, new_y)
        """
        dx, dy = self.GET_DIRECTION_DELTAS[self.current_direction]
        return self.current_x + dx, self.current_y + dy
    
    def update_position(self, new_x, new_y):
        """
        Update the robot's internal position.
        """
        self.current_x = new_x
        self.current_y = new_y

    def turn_left(self):
        """
        Rotate the robot 90 degrees counter-clockwise.
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
        Print the robot's current position and facing direction.
        """
        print(f"{self.current_x},{self.current_y},{self.current_direction}")
