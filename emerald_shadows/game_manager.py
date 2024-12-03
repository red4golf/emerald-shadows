"""Game manager module for Emerald Shadows."""
from typing import Dict, Optional, Tuple, Any
from datetime import datetime
import logging
from pathlib import Path
import sys

from .config import (
    SAVE_DIR, LOG_FILE, LOG_FORMAT, INITIAL_GAME_STATE, 
    REQUIRED_ITEMS, REQUIRED_STATES, AUTO_SAVE_INTERVAL,
    BASIC_COMMANDS, COMPLEX_COMMANDS
)
from .location_manager import LocationManager
from .item_manager import ItemManager
from .puzzles import PuzzleManager
from .commands.natural_commands import NaturalCommandHandler
from .utils import SaveLoadManager, print_text, clear_screen
from .game_art import display_title_screen

class GameManager:
    """Main game manager class handling game state and core gameplay loop."""
    
    def __init__(self):
        """Initialize the game manager and all subsystems."""
        # Ensure save directory exists
        Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)
        
        # Initialize managers
        self.init_managers()
        
        # Initialize game state
        self.game_state = INITIAL_GAME_STATE.copy()
        
        # Save/autosave tracking
        self.last_save_time = datetime.now()
        self.auto_save_interval = AUTO_SAVE_INTERVAL
        
        # Configure logging
        self._setup_logging()

    def init_managers(self) -> None:
        """Initialize all game subsystem managers."""
        self.location_manager = LocationManager()
        self.puzzle_manager = PuzzleManager()
        self.item_manager = ItemManager()
        self.command_handler = NaturalCommandHandler()
        self.save_load_manager = SaveLoadManager(SAVE_DIR)

    def _setup_logging(self) -> None:
        """Configure logging system."""
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format=LOG_FORMAT
        )
        logging.info("Game initialized")

    def process_command(self, command: str) -> bool:
        """
        Process a single game command.
        Returns True if game should continue, False if it should end.
        """
        if not command:
            return True
            
        if command == "quit":
            return self.handle_quit()
            
        command_type, args = self.command_handler.understand_command(command)
        
        if command_type not in BASIC_COMMANDS and command_type not in COMPLEX_COMMANDS:
            logging.warning(f"Invalid command type received: {command_type}")
            print_text("I don't understand that command. Type 'help' for available commands.")
            return True
            
        handlers = {
            "go": self._handle_movement,
            "take": self._handle_take_item,
            "examine": self._handle_examine,
            "inventory": self._handle_inventory,
            "save": self._handle_save,
            "load": self._handle_load,
            "solve": self._handle_puzzle,
            "help": self._handle_help
        }
        
        if command_type in handlers:
            handlers[command_type](args)
            
        return True

    def _handle_movement(self, direction: str) -> None:
        """Handle movement commands."""
        self.location_manager.move_to_location(direction, self.game_state)

    def _handle_take_item(self, item: str) -> None:
        """Handle taking items."""
        available_items = self.location_manager.get_available_items()
        if self.item_manager.take_item(item, available_items, self.game_state):
            self.location_manager.remove_item(item)

    def _handle_examine(self, item: str) -> None:
        """Handle examining items."""
        available_items = self.location_manager.get_available_items()
        self.item_manager.examine_item(item, available_items, self.game_state)

    def _handle_inventory(self, _: Any) -> None:
        """Handle inventory command."""
        self.item_manager.show_inventory()

    def _handle_save(self, _: Any) -> None:
        """Handle save command."""
        save_name = input("\nEnter save name (or press Enter for default): ").strip()
        if not save_name:
            save_name = "manual_save"
        if self.save_load_manager.save_game(self, save_name):
            print_text("Game saved successfully!")

    def _handle_load(self, _: Any) -> None:
        """Handle load command."""
        saves = self.save_load_manager.list_saves()
        if not saves:
            print_text("No save files found.")
            return
        
        print_text("\nAvailable saves:")
        for i, save in enumerate(saves):
            print_text(f"{i+1}. {save['name']} - {save['date']}")
        
        choice = input("\nEnter save number to load (or press Enter to cancel): ").strip()
        if choice and choice.isdigit() and 0 < int(choice) <= len(saves):
            save_name = saves[int(choice)-1]['name']
            if self.save_load_manager.load_game(self, save_name):
                print_text("Game loaded successfully!")

    def _handle_puzzle(self, _: Any) -> None:
        """Handle puzzle solving attempts."""
        self.puzzle_manager.handle_puzzle(
            self.location_manager.current_location,
            self.item_manager.get_inventory(),
            self.game_state
        )

    def _handle_help(self, _: Any) -> None:
        """Display help information."""
        self.show_help()

    def handle_quit(self) -> bool:
        """Handle quit command and return False to end game."""
        if input("\nSave before quitting? (y/n) ").lower().startswith('y'):
            self.save_load_manager.save_game(self, "quit_save")
        print_text("\nThanks for playing!")
        return False

    def check_auto_save(self) -> None:
        """Check and perform auto-save if needed."""
        current_time = datetime.now()
        if (current_time - self.last_save_time).seconds >= self.auto_save_interval:
            self.save_load_manager.save_game(self, "autosave")
            self.last_save_time = current_time

    def check_game_progress(self) -> bool:
        """Check if the player has solved the case."""
        return (
            all(item in self.item_manager.get_inventory() for item in REQUIRED_ITEMS) and
            all(self.game_state[state] for state in REQUIRED_STATES)
        )

    def start_game(self) -> None:
        """Main game loop."""
        try:
            display_title_screen()
            
            while True:
                self.check_auto_save()
                
                # Display current location
                print_text("\n" + self.location_manager.get_location_description())
                
                # Get and process command
                command = input("\nWhat would you like to do? ").strip().lower()
                
                if not self.process_command(command):
                    break
                    
                # Check win condition
                if self.check_game_progress():
                    self.show_victory()
                    break
                    
        except KeyboardInterrupt:
            print_text("\nGame interrupted. Saving progress...")
            self.save_load_manager.save_game(self, "interrupt_save")
            print_text("Progress saved. Thanks for playing!")
            
        except Exception as e:
            logging.error(f"Unexpected error in game loop: {e}")
            print_text("\nAn error occurred. The game has been auto-saved.")
            self.save_load_manager.save_game(self, "error_save")
            raise

    def show_help(self) -> None:
        """Display help information."""
        help_text = """
        Available Commands:
        - Movement: 'go <direction>' or just '<direction>'
          Directions: north, south, east, west, up, down
        
        - Items: 
          'take <item>' - Pick up an item
          'examine <item>' - Look at an item closely
          'use <item>' - Use an item you're carrying
          'inventory' or 'i' - Check your inventory
        
        - Puzzles:
          'solve' - Attempt to solve a puzzle in the current location
        
        - Game:
          'save' - Save your progress
          'load' - Load a saved game
          'quit' - Exit the game
          'help' - Show this help message
        
        Tips:
        - Examine everything carefully
        - Take notes of important information
        - Try using items in different locations
        """
        print_text(help_text)

    def show_victory(self) -> None:
        """Display victory message."""
        victory_text = """
        Congratulations! You've solved the case!
        
        Through careful investigation and clever deduction, you've uncovered
        the truth behind the mysterious activities in post-war Seattle.
        
        The evidence you've gathered will ensure justice is served.
        
        Thank you for playing Emerald Shadows!
        """
        print_text(victory_text)

if __name__ == "__main__":
    game = GameManager()
    game.start_game()