"""Abstract base class for all puzzles in Emerald Shadows."""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Set, Tuple

# A puzzle interaction either goes unhandled (None) or reports whether it
# solved the puzzle along with the text to show the player.
Interaction = Optional[Tuple[bool, str]]


class BasePuzzle(ABC):
    """Base class that all puzzle implementations must inherit from.

    A puzzle is a *worked* thing, not a password prompt. Subclasses expose the
    verbs the player uses to operate it (turn the wheel, tune the dial, tap a
    reply) via :meth:`verbs` and :meth:`interact`; ``attempt`` remains the final
    commit step for puzzles that take a typed answer.
    """

    def __init__(self, location: str, required_items: Set[str], description: str) -> None:
        self.location = location
        self.required_items = required_items
        self.description = description

    def check_requirements(self, inventory: Set[str]) -> bool:
        """Return True if the player has all items needed for this puzzle."""
        return self.required_items.issubset(inventory)

    def briefing(self, game_state: Dict) -> str:
        """The working materials shown when the player engages the puzzle.

        This is what they have in front of them — the ciphertext, the dial, the
        tapping on the pipe — plus how to operate it. Defaults to the puzzle's
        static description.
        """
        return self.description

    def verbs(self) -> Set[str]:
        """Extra command verbs this puzzle responds to at its location."""
        return set()

    def interact(self, verb: str, argument: str, game_state: Dict) -> Interaction:
        """Handle one of this puzzle's verbs.

        Returns None when the verb isn't handled, otherwise (solved, message).
        """
        return None

    @abstractmethod
    def attempt(self, solution: str) -> Tuple[bool, str]:
        """
        Evaluate a player's typed solution.

        Returns:
            (True, success_message) on correct solution
            (False, failure_message) on incorrect solution
        """
