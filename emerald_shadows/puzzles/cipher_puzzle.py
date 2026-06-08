"""Cipher wheel puzzle — evidence_room."""

from typing import Tuple
from .base_puzzle import BasePuzzle
from ..config import PUZZLE_SOLUTIONS


class CipherPuzzle(BasePuzzle):
    """Player must find the correct cipher key to decode the smugglers' memo."""

    def __init__(self) -> None:
        super().__init__(
            location="evidence_room",
            required_items={"cipher_wheel", "notebook"},
            description="The cipher wheel and coded notes beg to be decoded.",
        )
        self._solution = PUZZLE_SOLUTIONS["cipher_puzzle"]["key"].upper()

    def attempt(self, solution: str) -> Tuple[bool, str]:
        if solution.strip().upper() == self._solution:
            return True, PUZZLE_SOLUTIONS["cipher_puzzle"]["success_message"]
        return False, PUZZLE_SOLUTIONS["cipher_puzzle"]["fail_message"]
