"""High level orchestration for puzzle interactions."""

from __future__ import annotations

from typing import Callable, Iterable, Optional

from ..puzzle_solver import PuzzleSolver
from ..utils import print_text
from ..config import GAME_MESSAGES

SolutionProvider = Callable[[str], Optional[str]]


class PuzzleManager:
    """Bridge between the game loop and the low level puzzle solver."""

    def __init__(self, solution_provider: Optional[SolutionProvider] = None) -> None:
        self.solver = PuzzleSolver()
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

        inventory_set = set(inventory)
        has_requirements, message = self.solver.check_requirements(location, inventory_set)
        print_text("\n" + message)

        if not has_requirements:
            return False

        solution = self.solution_provider(location)
        if not solution:
            print_text("\nNo solution entered.")
            return False

        solved, response = self.solver.solve_puzzle(location, solution, inventory_set)
        print_text("\n" + response)
        if solved:
            self._mark_progress(location, game_state)
        return solved

    def _prompt_for_solution(self, location: str) -> Optional[str]:
        try:
            return input(f"\nEnter solution for the puzzle at {location}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

    def _mark_progress(self, location: str, game_state: dict) -> None:
        progress_map = {
            "warehouse_office": "found_warehouse",
            "evidence_room": "decoded_notes",
            "underground_tunnels": "observed_activity",
        }
        state_flag = progress_map.get(location)
        if state_flag:
            game_state[state_flag] = True
        else:
            # Provide a default acknowledgement when no specific state mapping exists
            print_text("\n" + GAME_MESSAGES.get("NO_PUZZLE", "Puzzle solved."))
