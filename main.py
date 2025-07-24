"""
main.py

This is the entry point of the Toy Robot Simulator. It passes a list of commands to the controller.
"""

from toy_robot.controller import RobotController
from toy_robot.simulator import Simulator
from logging_config import setup_logger

setup_logger()

if __name__ == "__main__":
    controller = RobotController()
    simulator = Simulator(controller)
    simulator.run_from_default_file()

