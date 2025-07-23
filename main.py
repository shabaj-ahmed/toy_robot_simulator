"""
main.py

This is the entry point of the Toy Robot Simulator. It passes a list of commands to the controller.
"""

from controller import RobotController
from logging_config import setup_logger

setup_logger()

if __name__ == "__main__":
    commands = [
        "PLACE 1,2,EAST",
        "MOVE",
        "MOVE",
        "LEFT",
        "MOVE",
        "REPORT"
    ]
    controller = RobotController()
    controller.process_commands(commands)
