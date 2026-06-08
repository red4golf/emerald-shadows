"""Abstract base class for all puzzles in Emerald Shadows."""

from abc import ABC, abstractmethod
from typing import Set, Tuple


class BasePuzzle(ABC):
    """Base class that all puzzle implementations must inherit from."""

    def __init__(self, location: str, required_items: Set[str], description: str) -> None:
        self.location = location
        self.required_items = required_items
        self.description = description

    def check_requirements(self, inventory: Set[str]) -> bool:
        """Return True if the player has all items needed for this puzzle."""
        return self.required_items.issubset(inventory)

    @abstractmethod
    def attempt(self, solution: str) -> Tuple[bool, str]:
        """
        Evaluate a player's solution attempt.

        Returns:
            (True, success_message) on correct solution
            (False, failure_message) on incorrect solution
        """
