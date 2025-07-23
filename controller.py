"""
controller.py

This file defines the RobotController, which processes incoming commands, 
delegates state updates to the Robot, and uses Navigation to validate movement.
"""

from robot import Robot
from navigation import Navigation

class RobotController:
    """
    The RobotController orchestrates command parsing and execution. It ensures that:
    - PLACE is the first valid command
    - MOVE only happens after validation
    - LEFT/RIGHT/REPORT are ignored until robot is placed
    """

    def __init__(self):
        self.robot = Robot()
        self.navigation = Navigation()

    def process_commands(self, commands):
        """
        Process a list of string commands and apply them in order.
        Commands: PLACE, MOVE, LEFT, RIGHT, REPORT
        """

        for command in commands:
            command = command.strip()
            parts = command.split()

            if parts[0] == "PLACE" and len(parts) == 2:
                x_str, y_str, direction = parts[1].split(",")
                x, y = int(x_str), int(y_str)
                direction = direction.strip().upper()
                if self.navigation.is_valid_position(x, y) and direction in Robot.GET_CARDINAL_DIRECTIONS:
                    self.robot.place(x, y, direction)

            elif not self.robot.is_placed:
                continue # Ignore commands until robot is placed

            elif command == "MOVE":
                new_x, new_y = self.robot.propose_move()
                if self.navigation.is_valid_position(new_x, new_y):
                    self.robot.update_position(new_x, new_y)

            elif command == "LEFT":
                self.robot.turn_left()

            elif command == "RIGHT":
                self.robot.turn_right()

            elif command == "REPORT":
                self.robot.report()

    def is_valid_command(self, command):
        pass