"""Morse code puzzle — underground_tunnels."""

from typing import Tuple
from .base_puzzle import BasePuzzle
from ..config import PUZZLE_SOLUTIONS

_CORRECT_ANSWER = "WAREHOUSE 22"
_ALT_ANSWERS = {"W-22", "W 22", "WAREHOUSE22"}


class MorsePuzzle(BasePuzzle):
    """Player must decode a Morse transmission to identify the smugglers' base."""

    def __init__(self) -> None:
        super().__init__(
            location="underground_tunnels",
            required_items={"flashlight"},
            description=(
                "With something else in the dark behind you, you tap out Morse "
                "to your contacts — the pre-arranged signal, the one that means "
                "you found it and you need backup at the warehouse. "
                "Make it fast. Make it right."
            ),
        )

    def attempt(self, solution: str) -> Tuple[bool, str]:
        normalised = solution.strip().upper()
        if normalised == _CORRECT_ANSWER or normalised in _ALT_ANSWERS:
            return True, PUZZLE_SOLUTIONS["morse_code"]["success_message"]
        return False, PUZZLE_SOLUTIONS["morse_code"]["fail_message"]
