"""Main entry point for Emerald Shadows."""

import logging
import sys
from pathlib import Path
from typing import Optional
from .game_manager import GameManager
from .config import LOG_FILE, LOG_FORMAT, SAVE_DIR

def setup_logging() -> logging.Handler:
    """
    Configure logging for the game.
    Returns the logging handler for cleanup.
    """
    # Ensure log directory exists
    log_path = Path(LOG_FILE).parent
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
    
    return handler

def cleanup_logging(handler: Optional[logging.Handler]) -> None:
    """Clean up logging handlers."""
    if handler:
        handler.close()
        logging.getLogger().removeHandler(handler)
    logging.shutdown()

def ensure_directories() -> None:
    """Ensure required directories exist."""
    # Create save directory if it doesn't exist
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)

def main() -> None:
    """Main entry point for the game."""
    handler = None
    try:
        # Setup
        ensure_directories()
        handler = setup_logging()
        logging.info("Starting Emerald Shadows")
        
        # Initialize and start game
        game = GameManager()
        game.start_game()
        
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
        logging.info("Game terminated by user")
        
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)
        print("\nAn unexpected error occurred. Check the log file for details.")
        
    finally:
        # Cleanup
        cleanup_logging(handler)
        sys.exit(0)

if __name__ == "__main__":
    main()