"""Puzzle Solver Module

Handles puzzle logic, validation, and solutions.
"""

from typing import Dict, Optional, Any, Tuple
import logging
from .config import PUZZLE_REQUIREMENTS, GAME_MESSAGES

class PuzzleSolver:
    """Manages puzzle mechanics and solutions."""
    
    def __init__(self):
        """Initialize the puzzle solver."""
        self.logger = logging.getLogger(__name__)
        self.solved_puzzles = set()
        
    def check_requirements(self, location: str, inventory: set) -> tuple[bool, str]:
        """Check if player has required items for puzzle."""
        if location not in PUZZLE_REQUIREMENTS:
            return False, GAME_MESSAGES["NO_PUZZLE"]
            
        puzzle_data = PUZZLE_REQUIREMENTS[location]
        for puzzle_type, required_items in puzzle_data.items():
            if puzzle_type == "description":
                continue
            if all(item in inventory for item in required_items):
                return True, puzzle_data["description"]
                
        missing_items = [item for items in puzzle_data.values() 
                        if isinstance(items, list)
                        for item in items 
                        if item not in inventory]
        return False, GAME_MESSAGES["MISSING_ITEMS"].format(items=", ".join(missing_items))
        
    def solve_puzzle(self, location: str, solution: str, inventory: set) -> tuple[bool, str]:
        """Attempt to solve a puzzle."""
        if location in self.solved_puzzles:
            return False, GAME_MESSAGES["ALREADY_SOLVED"]
            
        if not self.check_requirements(location, inventory)[0]:
            return False, GAME_MESSAGES["NO_PUZZLES_AVAILABLE"]
            
        # Get appropriate puzzle handler
        handler = self._get_puzzle_handler(location)
        if not handler:
            return False, GAME_MESSAGES["NO_HANDLER"] + location
            
        # Attempt solution
        success, message = handler(solution)
        if success:
            self.solved_puzzles.add(location)
            
        return success, message
        
    def _get_puzzle_handler(self, location: str):
        """Get the appropriate puzzle handler for the location."""
        handlers = {
            "warehouse_office": self._handle_radio_puzzle,
            "evidence_room": self._handle_cipher_puzzle,
            "underground_tunnels": self._handle_morse_puzzle
        }
        return handlers.get(location)
        
    def _handle_radio_puzzle(self, solution: str) -> tuple[bool, str]:
        """Handle radio frequency puzzle."""
        from .config import PUZZLE_SOLUTIONS
        if solution == PUZZLE_SOLUTIONS["radio_puzzle"]["frequency"]:
            return True, PUZZLE_SOLUTIONS["radio_puzzle"]["success_message"]
        return False, PUZZLE_SOLUTIONS["radio_puzzle"]["fail_message"]
        
    def _handle_cipher_puzzle(self, solution: str) -> tuple[bool, str]:
        """Handle cipher decryption puzzle."""
        from .config import PUZZLE_SOLUTIONS
        if solution.upper() == PUZZLE_SOLUTIONS["cipher_puzzle"]["key"]:
            return True, PUZZLE_SOLUTIONS["cipher_puzzle"]["success_message"]
        return False, PUZZLE_SOLUTIONS["cipher_puzzle"]["fail_message"]
        
    def _handle_morse_puzzle(self, solution: str) -> tuple[bool, str]:
        """Handle Morse code puzzle."""
        from .config import PUZZLE_SOLUTIONS
        if solution.upper() == "WAREHOUSE 22":
            return True, PUZZLE_SOLUTIONS["morse_code"]["success_message"]
        return False, PUZZLE_SOLUTIONS["morse_code"]["fail_message"]