"""Main entry point for Emerald Shadows."""

import logging
import sys
from .game_manager import GameManager
from .config import LOG_FILE, LOG_FORMAT

def setup_logging():
    """Configure logging for the game."""
    logging.basicConfig(
        filename=LOG_FILE,
        format=LOG_FORMAT,
        level=logging.INFO
    )

def main():
    """Main entry point for the game."""
    try:
        setup_logging()
        game = GameManager()
        game.start_game()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print("An unexpected error occurred. Check the log file for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()