"""High level orchestration for puzzle interactions."""

from __future__ import annotations

from typing import Callable, Dict, Iterable, Optional, Set

from ..utils import print_text
from ..config import GAME_MESSAGES
from .base_puzzle import BasePuzzle
from .radio_puzzle import RadioPuzzle
from .cipher_puzzle import CipherPuzzle
from .morse_puzzle import MorsePuzzle
from .car_puzzle import CarPuzzle

SolutionProvider = Callable[[str], Optional[str]]

# Registry mapping location -> puzzle instance
_PUZZLE_REGISTRY: Dict[str, BasePuzzle] = {
    puzzle.location: puzzle
    for puzzle in [RadioPuzzle(), CipherPuzzle(), MorsePuzzle(), CarPuzzle()]
}

_PROGRESS_MAP: Dict[str, str] = {
    "warehouse_office": "found_warehouse",
    "evidence_room": "decoded_notes",
    "underground_tunnels": "observed_activity",
    "pioneer_square": "identified_vehicle",
}


class PuzzleManager:
    """Manages puzzle state and delegates solving to individual puzzle classes."""

    def __init__(self, solution_provider: Optional[SolutionProvider] = None) -> None:
        self.solved_puzzles: Set[str] = set()
        self.solution_provider = solution_provider or self._prompt_for_solution

    def handle_puzzle(
        self,
        location: str,
        inventory: Iterable[str],
        game_state: dict,
    ) -> bool:
        """Entry point used by ``GameManager`` when the player types ``solve``.

        Returns ``True`` when a puzzle is successfully solved.
        """
        puzzle = _PUZZLE_REGISTRY.get(location)
        if puzzle is None:
            print_text("\n" + GAME_MESSAGES["NO_PUZZLE"])
            return False

        if location in self.solved_puzzles:
            print_text("\n" + GAME_MESSAGES["ALREADY_SOLVED"])
            return False

        inventory_set = set(inventory)
        if not puzzle.check_requirements(inventory_set):
            missing = puzzle.required_items - inventory_set
            print_text("\n" + GAME_MESSAGES["MISSING_ITEMS"].format(items=", ".join(sorted(missing))))
            return False

        print_text("\n" + puzzle.description)
        solution = self.solution_provider(location)
        if not solution:
            print_text("\nNo solution entered.")
            return False

        solved, response = puzzle.attempt(solution)
        print_text("\n" + response)
        if solved:
            self.solved_puzzles.add(location)
            state_flag = _PROGRESS_MAP.get(location)
            if state_flag:
                game_state[state_flag] = True
            game_state["score"] = game_state.get("score", 0) + 25
        return solved

    def should_trigger_on_use(self, item: str, location: str) -> bool:
        """Return True if using this item at this location should activate a puzzle."""
        puzzle = _PUZZLE_REGISTRY.get(location)
        if puzzle is None or location in self.solved_puzzles:
            return False
        return item in puzzle.required_items

    def _prompt_for_solution(self, location: str) -> Optional[str]:
        try:
            return input(f"\nEnter solution for the puzzle at {location}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
