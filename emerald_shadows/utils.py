"""Utility functions for Emerald Shadows.

Provides common functionality used across the game.
"""

import time
import json
from pathlib import Path
from typing import Any, Dict, Optional
import logging
from .config import TEXT_DELAY, SAVE_DIR

def slow_print(text: str, delay: float = TEXT_DELAY):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def save_game_state(state: Dict[str, Any], filename: str) -> bool:
    """Save game state to file."""
    try:
        save_path = SAVE_DIR / f"{filename}.save"
        SAVE_DIR.mkdir(exist_ok=True)
        
        with save_path.open('w') as f:
            json.dump(state, f)
        return True
    except Exception as e:
        logging.error(f"Failed to save game: {e}")
        return False

def load_game_state(filename: str) -> Optional[Dict[str, Any]]:
    """Load game state from file."""
    try:
        save_path = SAVE_DIR / f"{filename}.save"
        if not save_path.exists():
            return None
            
        with save_path.open('r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load game: {e}")
        return None