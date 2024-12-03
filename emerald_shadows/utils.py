import os
import sys
import time
import logging
import json
import shutil
import textwrap
from typing import Tuple, Optional, Dict, Any, List
from functools import wraps
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Configure root logger
logging.basicConfig(
    filename='emerald_shadows.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class DisplayManager:
    """Handles all display-related functionality in a centralized way."""
    
    MIN_TERMINAL_WIDTH = 60
    MAX_TERMINAL_WIDTH = 120
    DEFAULT_TERMINAL_WIDTH = 80
    DEFAULT_TERMINAL_HEIGHT = 24
    
    @staticmethod
    def get_terminal_size() -> tuple[int, int]:
        """Get current terminal size with fallback values."""
        try:
            width, height = shutil.get_terminal_size()
            width = max(DisplayManager.MIN_TERMINAL_WIDTH, 
                       min(width, DisplayManager.MAX_TERMINAL_WIDTH))
            return width, height
        except Exception:
            return DisplayManager.DEFAULT_TERMINAL_WIDTH, DisplayManager.DEFAULT_TERMINAL_HEIGHT
    
    @staticmethod
    def wrap_text(text: str, width: Optional[int] = None, indent: int = 0) -> str:
        """Wrap text to fit terminal width with proper indentation."""
        if width is None:
            width, _ = DisplayManager.get_terminal_size()
        
        # Adjust width for indent
        effective_width = width - indent
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.strip().split('\n\n')]
        wrapped_paragraphs = []
        
        for paragraph in paragraphs:
            # Normalize spaces
            paragraph = ' '.join(paragraph.split())
            
            # Wrap the paragraph
            wrapped = textwrap.fill(
                paragraph,
                width=effective_width,
                expand_tabs=True,
                replace_whitespace=True,
                break_long_words=False,
                break_on_hyphens=True,
                initial_indent=' ' * indent,
                subsequent_indent=' ' * indent
            )
            
            wrapped_paragraphs.append(wrapped)
        
        return '\n\n'.join(wrapped_paragraphs)
    
    @staticmethod
    def print_text(text: str, delay: Optional[float] = None, 
                  indent: int = 0, wrap: bool = True) -> None:
        """
        Print text with optional wrapping and slow printing effect.
        
        Args:
            text: Text to display
            delay: Delay between characters for slow printing
            indent: Number of spaces to indent text
            wrap: Whether to wrap text to terminal width
        """
        try:
            # Prepare the text
            display_text = DisplayManager.wrap_text(text, indent=indent) if wrap else text
            
            # Print with or without delay
            if delay:
                for char in display_text:
                    sys.stdout.write(char)
                    sys.stdout.flush()
                    time.sleep(delay)
                print()  # Add final newline
            else:
                print(display_text)
                
        except KeyboardInterrupt:
            print("\nDisplay interrupted.")
        except Exception as e:
            logging.error(f"Error displaying text: {e}")
            print("\nError displaying text.")
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        try:
            # Check if running in IDLE
            if 'idlelib.run' in sys.modules:
                print("\n" * 100)
                return
            
            # Use appropriate clear command based on OS
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            logging.error(f"Error clearing screen: {e}")
            print("\n" * 100)  # Fallback
    
    @staticmethod
    def format_location_description(description: str, 
                                  exits: list[str], 
                                  items: list[str]) -> str:
        """Format a location description with exits and items."""
        try:
            if not description:
                raise ValueError("Invalid description")
            
            formatted = description.strip()
            
            if exits:
                formatted += f"\n\nExits: {', '.join(exits)}"
            
            if items:
                formatted += f"\n\nYou can see: {', '.join(items)}"
            
            return formatted
            
        except Exception as e:
            logging.error(f"Error formatting location description: {e}")
            return description  # Return original description on error

# Convenience functions that use DisplayManager
def clear_screen() -> None:
    """Clear the terminal screen."""
    DisplayManager.clear_screen()

def print_text(text: str, delay: Optional[float] = None, 
              indent: int = 0, wrap: bool = True) -> None:
    """Print text using DisplayManager."""
    DisplayManager.print_text(text, delay, indent, wrap)

@dataclass
class SaveGameData:
    """Data structure for saved game state"""
    save_name: str
    save_date: str
    game_state: Dict[str, Any]
    location_states: Dict[str, Dict[str, Any]]
    version: str = "1.0.0"

    def __post_init__(self):
        """Initialize optional fields if they're None"""
        if self.location_states is None:
            self.location_states = {}

class SaveLoadManager:
    def __init__(self, save_dir: str):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save_game(self, game_instance: Any, save_name: Optional[str] = None) -> bool:
        """Save the current game state to a file."""
        try:
            if not save_name:
                save_name = f"autosave_{int(time.time())}"
            
            save_data = {
                'save_name': save_name,
                'save_date': datetime.now().isoformat(),
                'version': "1.0.0",
                'game_state': game_instance.game_state,
                'current_location': game_instance.current_location,
                'location_states': game_instance.location_manager.get_location_states(),
                'inventory_state': game_instance.item_manager.get_inventory_state()
            }
            
            file_path = self.save_dir / f"{save_name}.json"
            
            with open(file_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            self.logger.info(f"Game saved successfully to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving game: {e}")
            return False

    def load_game(self, game_instance: Any, save_name: str) -> bool:
        """Load a saved game state."""
        try:
            file_path = self.save_dir / f"{save_name}.json"
            if not file_path.exists():
                print(f"\nSave file not found: {save_name}")
                return False

            with open(file_path, 'r') as f:
                save_data = json.load(f)

            # Verify save data structure
            required_keys = {'game_state', 'current_location', 'location_states', 'inventory_state'}
            if not all(key in save_data for key in required_keys):
                raise ValueError("Save file is missing required data")

            # Restore game state
            game_instance.game_state = save_data['game_state']
            game_instance.current_location = save_data['current_location']
            
            # Restore location states
            game_instance.location_manager.current_location = save_data['current_location']
            game_instance.location_manager.restore_location_states(save_data['location_states'])
            
            # Restore inventory
            game_instance.item_manager.restore_inventory_state(save_data['inventory_state'])
            
            self.logger.info(f"Game loaded successfully from {file_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error loading game: {str(e)}")
            return False

    def list_saves(self) -> List[Dict[str, Any]]:
        """List all available save files with metadata."""
        saves = []
        for save_file in self.save_dir.glob("*.json"):
            try:
                with open(save_file, 'r') as f:
                    save_data = json.load(f)
                saves.append({
                    'name': save_data['save_name'],
                    'date': save_data['save_date'],
                    'location': save_data['current_location'],
                    'file_path': str(save_file)
                })
            except Exception as e:
                self.logger.warning(f"Error reading save file {save_file}: {e}")
                continue
        
        return sorted(saves, key=lambda x: x['date'], reverse=True)

    def delete_save(self, save_name: str) -> bool:
        """Delete a save file."""
        try:
            file_path = self.save_dir / f"{save_name}.json"
            if file_path.exists():
                file_path.unlink()
                self.logger.info(f"Deleted save file: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting save file: {e}")
            return False

class ErrorHandler:
    """Handles error management and logging."""
    
    @staticmethod
    def handle_game_error(error: Exception, context: str = "") -> None:
        """Handle game errors with proper logging and user feedback."""
        error_msg = f"Error in {context}: {str(error)}"
        logger.error(error_msg)
        print(f"\nAn error occurred: {str(error)}")
        print("The game has been auto-saved. Type 'quit' to exit or press Enter to continue.")

    @staticmethod
    def safe_exit() -> None:
        """Safely exit the game with cleanup."""
        try:
            logger.info("Game terminated safely")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error during safe exit: {e}")
            sys.exit(1)

def validate_input(func):
    """Decorator for input validation."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Validate string arguments
            for arg in args:
                if isinstance(arg, str) and not arg.strip():
                    logger.warning("Empty input provided")
                    return True
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return True
    return wrapper