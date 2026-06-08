"""
Configuration settings for Emerald Shadows.

This module contains all configuration constants and game settings.
Settings are organized by category and include validation.
"""

from pathlib import Path
from typing import Dict, Set, Any, Final
from dataclasses import dataclass
import os

# Version Information
GAME_VERSION: Final[str] = "1.0.0"
SAVE_FILE_VERSION: Final[str] = "1.0"

# File System Settings
SAVE_DIR: Final[Path] = Path("saves")
LOG_DIR: Final[Path] = Path("logs")
LOG_FILE: Final[Path] = LOG_DIR / "emerald_shadows.log"
LOG_FORMAT: Final[str] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# File System Constraints
MAX_SAVE_DIR_SIZE_MB: Final[int] = 100
MAX_SAVE_FILES: Final[int] = 50
MAX_LOG_SIZE_MB: Final[int] = 10

# Game State Initialization
INITIAL_GAME_STATE: Final[Dict[str, Any]] = {
    # Progress tracking
    "morse_attempts": 0,
    "has_badge": False,
    "examined_cipher": False,
    "discovered_suspect": False,

    # Major plot points
    "decoded_notes": False,
    "found_emergency_frequency": False,
    "observed_activity": False,
    "surveilled_docks": False,
    "found_warehouse": False,
    "found_all_notes": False,
    "identified_organization": False,
    "identified_suspect": False,
    "identified_vehicle": False,

    # Darkness / grue tracking
    "flashlight_lit": False,
    "dark_turns": 0,

    # Darkness / grue tracking (continued)
    "ches_tip": False,

    # Scoring
    "score": 0,
}

# Required Items for Game Completion
REQUIRED_ITEMS: Final[Set[str]] = frozenset({
    "cipher_wheel",
    "notebook",
    "badge",
    "binoculars",
    "radio_manual",
    "photo",
    "meeting_minutes",
    "manifest",
})

# Required Game States for Completion
REQUIRED_STATES: Final[Set[str]] = frozenset({
    "decoded_notes",
    "found_emergency_frequency",
    "observed_activity",
    "surveilled_docks",
    "found_warehouse",
    "identified_organization",
    "identified_suspect",
    "identified_vehicle",
    "ches_tip",
})

# Game Settings
STARTING_LOCATION: Final[str] = "police_station"
AUTO_SAVE_INTERVAL: Final[int] = 300  # 5 minutes in seconds
INVENTORY_LIMIT: Final[int] = 10

# Terminal Display Settings
@dataclass(frozen=True)
class TerminalSettings:
    """Terminal display configuration."""
    min_width: int = 60
    max_width: int = 120
    default_width: int = 80
    default_height: int = 24
    
    def __post_init__(self) -> None:
        """Validate terminal settings."""
        if not (self.min_width <= self.default_width <= self.max_width):
            raise ValueError("Invalid terminal width configuration")
        if self.default_height < 10:
            raise ValueError("Terminal height must be at least 10 lines")

# Initialize terminal settings
TERMINAL: Final[TerminalSettings] = TerminalSettings()

# Command Sets
BASIC_COMMANDS: Final[Set[str]] = frozenset({
    # Navigation
    "look", "north", "south", "east", "west", "up", "down",

    # Inventory
    "inventory", "i",

    # Game Control
    "help", "quit", "save", "load", "score"
})

COMPLEX_COMMANDS: Final[Set[str]] = frozenset({
    # Action Commands
    "go", "take", "examine", "use", "combine", "solve", "drop"
})

# Validate command sets
if BASIC_COMMANDS & COMPLEX_COMMANDS:
    raise ValueError("Command sets must not overlap")

# Game Text Settings
TEXT_SCROLL_SPEED: Final[float] = 0.03  # seconds per character
ENABLE_TEXT_EFFECTS: Final[bool] = True
MAX_MESSAGE_LENGTH: Final[int] = 1000

# Puzzle Settings
MAX_PUZZLE_ATTEMPTS: Final[int] = 3
PUZZLE_TIMEOUT: Final[int] = 300  # seconds

PUZZLE_SOLUTIONS: Final[Dict[str, Dict[str, str]]] = {
    "radio_puzzle": {
        "frequency": "415.6",
        "success_message": "You lock onto 415.6 MHz—smugglers chatter floods your headphones.",
        "fail_message": "Static sputters. That frequency is dead tonight.",
    },
    "cipher_puzzle": {
        "key": "ANGELS",
        "success_message": "The cipher wheel clicks—'ANGELS' unlocks the entire memo.",
        "fail_message": "The letters refuse to line up; that key isn't right.",
    },
    "morse_code": {
        "success_message": "Your Morse reply sends a patrol to Warehouse 22 immediately.",
        "fail_message": "You mis-tap the code and only echoes answer back.",
    },
}

GAME_MESSAGES: Final[Dict[str, str]] = {
    "NO_PUZZLE": "Nothing here calls for that kind of attention. Keep moving.",
    "MISSING_ITEMS": "You're not ready for this yet. You still need: {items}.",
    "ALREADY_SOLVED": "You've already worked that one. Don't second-guess yourself.",
    "NO_PUZZLES_AVAILABLE": "You don't have what you need. Diamond doesn't bluff.",
    "NO_HANDLER": "No handler registered for puzzle at ",
}

def validate_config() -> None:
    """Validate configuration constants for internal consistency."""
    for state in REQUIRED_STATES:
        if state not in INITIAL_GAME_STATE:
            raise ValueError(f"Required state '{state}' not found in initial game state")
    if AUTO_SAVE_INTERVAL < 60:
        raise ValueError("Auto-save interval must be at least 60 seconds")
    if MAX_SAVE_DIR_SIZE_MB < 1:
        raise ValueError("Maximum save directory size must be at least 1 MB")


def check_filesystem() -> None:
    """Check that save and log directories are writable. Call at startup, not import."""
    if not os.access(SAVE_DIR.parent, os.W_OK):
        raise PermissionError(f"Cannot write to save directory: {SAVE_DIR}")
    if not os.access(LOG_DIR.parent, os.W_OK):
        raise PermissionError(f"Cannot write to log directory: {LOG_DIR}")


# Validate constants at import time (pure logic checks only — no I/O)
validate_config()