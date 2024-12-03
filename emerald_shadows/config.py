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
    "found_warehouse": False,
    "found_all_notes": False,
    "identified_organization": False
}

# Required Items for Game Completion
REQUIRED_ITEMS: Final[Set[str]] = frozenset({
    "cipher_wheel",
    "notebook",
    "badge",
    "binoculars",
    "radio_manual"
})

# Required Game States for Completion
REQUIRED_STATES: Final[Set[str]] = frozenset({
    "decoded_notes",
    "found_emergency_frequency",
    "observed_activity",
    "found_warehouse",
    "identified_organization"
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
    "help", "quit", "save", "load"
})

COMPLEX_COMMANDS: Final[Set[str]] = frozenset({
    # Action Commands
    "go", "take", "examine", "use", "combine", "solve"
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

def validate_config() -> None:
    """Validate configuration settings."""
    # Validate game states
    for state in REQUIRED_STATES:
        if state not in INITIAL_GAME_STATE:
            raise ValueError(f"Required state '{state}' not found in initial game state")
    
    # Validate paths
    if not os.access(SAVE_DIR.parent, os.W_OK):
        raise PermissionError(f"Cannot write to save directory: {SAVE_DIR}")
    if not os.access(LOG_DIR.parent, os.W_OK):
        raise PermissionError(f"Cannot write to log directory: {LOG_DIR}")
    
    # Validate intervals
    if AUTO_SAVE_INTERVAL < 60:
        raise ValueError("Auto-save interval must be at least 60 seconds")
    if MAX_SAVE_DIR_SIZE_MB < 1:
        raise ValueError("Maximum save directory size must be at least 1 MB")

# Run validation on module import
validate_config()