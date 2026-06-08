"""Car licence plate puzzle — pioneer_square (reserved for future expansion)."""

from typing import Tuple
from .base_puzzle import BasePuzzle

_CORRECT_PLATE = "WA-4471"
_LOCATION = "pioneer_square"


class CarPuzzle(BasePuzzle):
    """Player must identify the smugglers' vehicle from witness descriptions."""

    def __init__(self) -> None:
        super().__init__(
            location=_LOCATION,
            required_items={"notebook"},
            description="Your notes describe a blue sedan seen near three crime scenes. Can you pin down the plate number?",
        )

    def attempt(self, solution: str) -> Tuple[bool, str]:
        if solution.strip().upper().replace(" ", "-") == _CORRECT_PLATE:
            return (
                True,
                "WA-4471 — registered to a shell company. That's your blue sedan.",
            )
        return False, "That plate doesn't match the witness descriptions."
