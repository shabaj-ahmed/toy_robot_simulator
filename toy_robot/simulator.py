"""
simulator.py

This file defines the Simulator class, which reads commands from a file
and feeds them to the RobotController one line at a time.

Responsibilities:
- Load a default command file
- Stream each command to the controller
- Gracefully handle missing or unreadable files
"""

import logging
from toy_robot.controller import RobotController

class Simulator:
    """
    The Simulator reads command input from a file and delegates
    execution to the provided RobotController instance.
    """

    def __init__(self, controller: RobotController) -> None:
        """
        Initialise the Simulator with a RobotController instance.

        Parameters:
        - controller: an instance of RobotController that processes each command
        """
        self.controller = controller
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_from_default_file(self) -> None:
        """
        Reads commands from the default file ('data/commands.txt') line by line.
        Each non-empty line is sent to the controller for processing.

        If the file is missing, an error is logged.
        """
        filename = "data/commands.txt"
        try:
            with open(filename, "r") as file:
                for line in file:
                    command = line.strip()
                    if command:
                        self.controller.process_command(command)
        except FileNotFoundError:
            self.logger.error(f"File not found: {filename}")
