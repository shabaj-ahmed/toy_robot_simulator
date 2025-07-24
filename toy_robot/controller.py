"""
controller.py

This file defines the RobotController class, which serves as the main interface 
for processing user commands. It delegates robot control (position and direction) 
to the Robot class, and validates movements using the Navigation class.

Responsibilities:
- Parse and validate incoming commands
- Coordinate execution of valid commands
- Enforce safety (e.g., prevent moving off the table)
"""

from toy_robot.robot import Robot
from toy_robot.navigation import Navigation
import logging

# Set of all supported commands
VALID_COMMANDS = {"PLACE", "MOVE", "LEFT", "RIGHT", "REPORT"}

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
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_command(self, command):
        """
        Processes a sequence of string commands in order.

        Parameters:
        - commands: list of strings, e.g., ["PLACE 1,2,EAST", "MOVE", "REPORT"]

        For each command:
        - It is parsed and validated
        - If valid, it's executed based on robot state
        - Commands are ignored if they are invalid or unsafe
        """

        parsed = self.parse_command(command)
        if not parsed:
            # Skip invalid commands
            return

        cmd = parsed[0]

        if cmd == "PLACE":
            # Unpack arguments only if cmd is PLACE
            _ , x, y, direction = parsed

            if not self.navigation.is_valid_position(x, y):
                self.logger.warning(f"PLACE ignored: invalid position ({x},{y},{direction})")
                return
            
            self.robot.place(x, y, direction)

        elif not self.robot.is_placed:
            self.logger.warning(f"Ignoring '{cmd}' as no PLACE command has been issued yet.")
            return

        elif cmd == "MOVE":
            # Ask robot what the next move would be
            new_x, new_y, current_direction = self.robot.propose_move()

            # Check if that move would be valid (on the table)
            if self.navigation.is_valid_position(new_x, new_y):
                self.robot.update_position(new_x, new_y)
            else:
                self.logger.warning(f"Unsafe MOVE ignored: ({new_x},{new_y}{current_direction})")

        elif cmd == "LEFT":
            self.robot.turn_left()

        elif cmd == "RIGHT":
            self.robot.turn_right()

        elif cmd == "REPORT":
            self.robot.report()

    def parse_command(self, command: str):
        """
        Parses and validates a single command string.

        Parameters:
        - command (str): The raw input command

        Returns:
        - tuple representing parsed command:
            - ("PLACE", x, y, direction) if valid PLACE
            - ("MOVE",) or ("LEFT",) or ("RIGHT",) for other commands
            - None if the command is invalid or malformed
        """
        parts = command.strip().split()

        if not parts: # Empty command
            return None

        cmd = parts[0]

        if cmd not in VALID_COMMANDS:
            self.logger.warning(f"Unrecognised command: '{command}'")
            return None

        if cmd == "PLACE":
            # PLACE must have exactly one argument: "X,Y,DIRECTION"
            if len(parts) != 2:
                return None
            try:
                x_str, y_str, direction = parts[1].split(",")
                x, y = int(x_str), int(y_str) # Throws ValueError if not integers
                direction = direction.strip()
                
                if direction not in Robot.GET_CARDINAL_DIRECTIONS:
                    raise ValueError("Invalid direction.")
                    
                return ("PLACE", x, y, direction)
            except (ValueError, IndexError) as e:
                self.logger.error(f"Invalid PLACE command format: {command} - {e}")
                return None # PLACE format is invalid

        # All other commands must be exactly one word
        if len(parts) == 1:
            return (cmd,)

        return None # Invalid command format
