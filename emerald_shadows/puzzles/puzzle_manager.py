"""High level orchestration for puzzle interactions."""

from __future__ import annotations

from typing import Callable, Dict, Iterable, Optional, Set, Tuple

from ..config import GAME_MESSAGES
from ..utils import print_block, print_text
from .base_puzzle import BasePuzzle
from .car_puzzle import CarPuzzle
from .cipher_puzzle import CipherPuzzle
from .morse_puzzle import MorsePuzzle
from .radio_puzzle import RadioPuzzle

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

PUZZLE_SCORE = 25


class PuzzleManager:
    """Manages puzzle state and delegates the work to individual puzzle classes."""

    def __init__(self, solution_provider: Optional[SolutionProvider] = None) -> None:
        self.solved_puzzles: Set[str] = set()
        self.solution_provider = solution_provider or self._prompt_for_solution

    # ------------------------------------------------------------------
    # Engagement
    # ------------------------------------------------------------------
    def handle_puzzle(
        self,
        location: str,
        inventory: Iterable[str],
        game_state: dict,
    ) -> bool:
        """Entry point when the player types ``solve``.

        Lays out the working materials. Puzzles that are *operated* (a wheel to
        turn, a dial to sweep) then wait for the player to work them; puzzles
        that take a typed answer ask for one straight away.
        """
        puzzle = self._available(location, inventory, game_state)
        if puzzle is None:
            return False

        print_block("\n" + puzzle.briefing(game_state))

        if puzzle.verbs():
            # The player operates this one themselves.
            return False

        solution = self.solution_provider(location)
        if not solution:
            print_text("\nYou let it lie for now.")
            return False

        solved, response = puzzle.attempt(solution)
        print_block("\n" + response)
        if solved:
            self._record(location, game_state)
        return solved

    def interact(
        self,
        location: str,
        verb: str,
        argument: str,
        inventory: Iterable[str],
        game_state: dict,
    ) -> bool:
        """Route an operating verb (turn/tune/tap/listen) to the puzzle here.

        Returns True if the verb was consumed by a puzzle.
        """
        puzzle = _PUZZLE_REGISTRY.get(location)
        if puzzle is None or verb not in puzzle.verbs():
            return False

        if location in self.solved_puzzles:
            print_text("\n" + GAME_MESSAGES["ALREADY_SOLVED"])
            return True

        if not self._has_requirements(puzzle, inventory):
            self._report_missing(puzzle, inventory)
            return True

        result = puzzle.interact(verb, argument, game_state)
        if result is None:
            return False

        solved, message = result
        if message:
            print_block("\n" + message)
        if solved:
            self._record(location, game_state)
        return True

    def verbs_at(self, location: str) -> Set[str]:
        """Operating verbs the puzzle at this location responds to."""
        puzzle = _PUZZLE_REGISTRY.get(location)
        return puzzle.verbs() if puzzle else set()

    def should_trigger_on_use(self, item: str, location: str) -> bool:
        """Return True if using this item here should bring the puzzle up."""
        puzzle = _PUZZLE_REGISTRY.get(location)
        if puzzle is None or location in self.solved_puzzles:
            return False
        return item in puzzle.required_items

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _available(
        self, location: str, inventory: Iterable[str], game_state: dict
    ) -> Optional[BasePuzzle]:
        """The puzzle here, if there is one the player can currently work."""
        puzzle = _PUZZLE_REGISTRY.get(location)
        if puzzle is None:
            print_text("\n" + GAME_MESSAGES["NO_PUZZLE"])
            return None
        if location in self.solved_puzzles:
            print_text("\n" + GAME_MESSAGES["ALREADY_SOLVED"])
            return None
        if not self._has_requirements(puzzle, inventory):
            self._report_missing(puzzle, inventory)
            return None
        return puzzle

    @staticmethod
    def _has_requirements(puzzle: BasePuzzle, inventory: Iterable[str]) -> bool:
        return puzzle.check_requirements(set(inventory))

    @staticmethod
    def _report_missing(puzzle: BasePuzzle, inventory: Iterable[str]) -> None:
        missing = puzzle.required_items - set(inventory)
        print_text(
            "\n" + GAME_MESSAGES["MISSING_ITEMS"].format(items=", ".join(sorted(missing)))
        )

    def _record(self, location: str, game_state: dict) -> None:
        """Mark a puzzle solved and pay out its progress."""
        self.solved_puzzles.add(location)
        flag = _PROGRESS_MAP.get(location)
        if flag:
            game_state[flag] = True
        game_state["score"] = game_state.get("score", 0) + PUZZLE_SCORE

    def _prompt_for_solution(self, location: str) -> Optional[str]:
        try:
            return input("\nWhat have you got? ").strip()
        except (EOFError, KeyboardInterrupt):
            return None

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def get_state(self) -> dict:
        """Get puzzle progress for saving."""
        return {"solved_puzzles": sorted(self.solved_puzzles)}

    def restore_state(self, state: Optional[dict]) -> None:
        """Restore puzzle progress from save data. Older saves that predate
        puzzle persistence have no entry; they restore to nothing solved."""
        state = state or {}
        self.solved_puzzles = set(state.get("solved_puzzles", []))
