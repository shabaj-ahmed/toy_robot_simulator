"""
toy_robot/interface.py

This file defines interfaces for the Robot and Navigation classes to ensure
consistent method signatures and promote modularity.

Responsibilities:
- Define abstract base classes for Robot and Navigation
- Enforce method signatures for key functionalities
- Facilitate easier testing and mocking
- Promote adherence to SOLID principles, enhancing code modularity
"""

from abc import ABC, abstractmethod
from typing import Tuple

class RobotInterface(ABC):
    """
    The RobotInterface defines the essential methods that any Robot class must implement.
    """
    @abstractmethod
    def place(self, x: int, y: int, direction: str) -> None: ...
    @abstractmethod
    def propose_move(self) -> Tuple[int, int, str]: ...
    @abstractmethod
    def update_position(self, new_x: int, new_y: int) -> None: ...
    @abstractmethod
    def turn_left(self) -> None: ...
    @abstractmethod
    def turn_right(self) -> None: ...
    @abstractmethod
    def report(self) -> Tuple[int, int, str]: ...

class NavigationInterface(ABC):
    """
    The NavigationInterface defines the essential methods that any Navigation class must implement.
    """
    @abstractmethod
    def is_valid_position(self, x: int, y: int) -> bool: ...
