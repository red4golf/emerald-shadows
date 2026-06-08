"""Radio frequency puzzle — warehouse_office."""

from typing import Tuple
from .base_puzzle import BasePuzzle
from ..config import PUZZLE_SOLUTIONS


class RadioPuzzle(BasePuzzle):
    """Player must tune a salvaged radio to the smugglers' emergency frequency."""

    def __init__(self) -> None:
        super().__init__(
            location="warehouse_office",
            required_items={"radio_manual"},
            description="You unfold the seized radio equipment and tune its broken dials.",
        )
        self._solution = PUZZLE_SOLUTIONS["radio_puzzle"]["frequency"]

    def attempt(self, solution: str) -> Tuple[bool, str]:
        if solution.strip() == self._solution:
            return True, PUZZLE_SOLUTIONS["radio_puzzle"]["success_message"]
        return False, PUZZLE_SOLUTIONS["radio_puzzle"]["fail_message"]
