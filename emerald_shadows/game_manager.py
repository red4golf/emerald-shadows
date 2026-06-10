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
from .media import present

TROLLEY_COMMANDS = {"next", "off", "status", "history"}

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

        # Brief mode: track last displayed location so description only shows on move
        self._last_location: Optional[str] = None

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

        if not command_type:
            # A bare named exit ("outside", "upstairs", "tavern", "o") is movement.
            words = command.split()
            if len(words) == 1 and self.location_manager.resolve_exit(words[0]):
                self._handle_movement(words[0])
                return True
            print_text("Diamond considered that, then decided it wasn't productive. (Type 'help' for commands.)")
            return True
        
        if command_type in TROLLEY_COMMANDS:
            self._handle_trolley_command(command_type)
            return True
        
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
            "help": self._handle_help,
            "look": self._handle_look,
            "use": self._handle_use_item,
            "combine": self._handle_combine_items,
            "drop": self._handle_drop_item,
            "score": self._handle_score,
            "exits": self._handle_exits,
        }
        
        if command_type in handlers:
            handlers[command_type](args)
            
        return True

    def _handle_movement(self, direction: str) -> None:
        """Handle movement commands."""
        self.location_manager.move_to_location(direction, self.game_state)

    def _handle_take_item(self, item: str) -> None:
        """Handle taking items, including 'take all'."""
        if not item:
            print_text("Take what?")
            return
        available_items = self.location_manager.get_available_items()
        if item in ("all", "everything"):
            if not available_items:
                print_text("There's nothing here worth taking.")
                return
            for thing in list(available_items):
                if self.item_manager.take_item(thing, available_items, self.game_state):
                    self.location_manager.remove_item(thing)
            return
        if self.item_manager.take_item(item, available_items, self.game_state):
            self.location_manager.remove_item(item)

    def _handle_examine(self, item: str) -> None:
        """Handle examining items."""
        if not item:
            print_text("Examine what?")
            return
        available_items = self.location_manager.get_available_items()
        self.item_manager.examine_item(item, available_items, self.game_state)

    def _handle_look(self, _: Any) -> None:
        """Describe the current location, respecting darkness."""
        if self.location_manager.is_dark() and not self.game_state.get("flashlight_lit", False):
            print_text(
                "\nIt is pitch dark. Something moves in the dark nearby — patient, "
                "unhurried. It has done this before. Use your flashlight, Diamond."
            )
            return
        description = self.location_manager.get_location_description()
        print_text("\n" + description)

    def _handle_inventory(self, _: Any) -> None:
        """Handle inventory command."""
        self.item_manager.show_inventory(self.game_state)

    def _handle_use_item(self, item: str) -> None:
        """Handle using an inventory item. Triggers a puzzle if the item activates one here."""
        if not item:
            print_text("Use what?")
            return
        location = self.location_manager.current_location
        self.item_manager.use_item(item, location, self.game_state)
        if self.puzzle_manager.should_trigger_on_use(item, location):
            self.puzzle_manager.handle_puzzle(location, self.item_manager.get_inventory(), self.game_state)

    def _handle_drop_item(self, item: str) -> None:
        """Handle dropping an inventory item into the current location."""
        if not item:
            print_text("Drop what?")
            return
        if self.item_manager.drop_item(item):
            self.location_manager.add_item(item)

    def _handle_combine_items(self, items: str) -> None:
        """Handle combining inventory items."""
        item1, item2 = self._parse_combine_args(items)
        if not item1 or not item2:
            print_text("Combine which items? Try 'combine notebook with cipher wheel'.")
            return
        self.item_manager.combine_items(item1, item2, self.game_state)

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
                # Force the location description to redisplay after load
                self._last_location = None

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

    def _handle_trolley_command(self, command: str) -> None:
        """Route trolley-specific commands to the location manager."""
        self.location_manager.handle_trolley_command(command)

    def _handle_score(self, _: Any) -> None:
        """Display the current score."""
        score = self.game_state.get("score", 0)
        print_text(f"\nCase progress: {score} points.")

    def _handle_exits(self, _: Any) -> None:
        """List the ways out of the current location."""
        exits = self.location_manager.get_valid_exits()
        if exits:
            print_text("\nWays out: " + ", ".join(exits))
        else:
            print_text("\nNo obvious way out. That's rarely a good sign.")

    def _check_darkness(self) -> bool:
        """
        Check whether the player is in a dark location without light.
        Returns True if the player has been eaten by a grue (game over).
        """
        if not self.location_manager.is_dark():
            self.game_state["dark_turns"] = 0
            return False
        if self.game_state.get("flashlight_lit", False):
            return False

        self.game_state["dark_turns"] = self.game_state.get("dark_turns", 0) + 1
        if self.game_state["dark_turns"] == 1:
            print_text(
                "\nIt is pitch dark. Something moves in the dark nearby — patient, "
                "unhurried. It has done this before. Use your flashlight, Diamond."
            )
            return False
        return self._handle_grue_death()

    def _handle_grue_death(self) -> bool:
        """Handle death by grue. Offers to restore the most recent save."""
        present("grue_death")
        print_text(
            "\n*** YOU HAVE BEEN EATEN BY A GRUE ***\n\n"
            "It was dark. It was always going to be dark. Something materialized from "
            "the blackness with the efficiency of a thing that has done this many times. "
            "Diamond did not survive the Pacific to be eaten in a tunnel beneath Pioneer "
            "Square, but the grue had other ideas.\n\n"
            "Diamond's expense account will go unfiled.\n"
            "The city will not miss him. It never does."
        )
        saves = self.save_load_manager.list_saves()
        if saves:
            choice = input("\nRestore last save? (y/n) ").strip().lower()
            if choice.startswith("y"):
                # list_saves() is sorted newest-first
                save_name = saves[0]["name"]
                if self.save_load_manager.load_game(self, save_name):
                    print_text("\nRestored. The grue slinks back into the dark.")
                    return False
        return True

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
            self._last_location = None

            while True:
                self.check_auto_save()

                # Show location description only when location changes
                current_location = self.location_manager.current_location
                if current_location != self._last_location:
                    print_text("\n" + self.location_manager.get_location_description())
                    self._last_location = current_location

                # Get and process command
                command = input("\n> ").strip().lower()

                if not self.process_command(command):
                    break

                # Check darkness / grue
                if self._check_darkness():
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

    def _parse_combine_args(self, items: str) -> Tuple[str, str]:
        """Parse user input for the combine command."""
        if not items:
            return "", ""
        lowered = items.lower()
        for separator in (" with ", " and "):
            if separator in lowered:
                left, right = lowered.split(separator, 1)
                return left.strip(), right.strip()
        parts = lowered.split()
        if len(parts) >= 2:
            return parts[0], " ".join(parts[1:]).strip()
        return "", ""

    def show_help(self) -> None:
        """Display help information."""
        help_text = (
            "DIAMOND'S CASEBOOK\n"
            "==================\n\n"
            "You are a detective. You know how to get around.\n\n"
            "MOVEMENT\n"
            "  north / south / east / west / up / down  (or: go north, n, etc.)\n"
            "  Named exits work too — type the exit as you see it: 'outside',\n"
            "  'upstairs', 'tavern', 'trolley'. Or 'o' for outside. \n"
            "  exits — list the ways out of wherever you're standing\n"
            "  Compass directions work. So does common sense.\n\n"
            "INVESTIGATION\n"
            "  look                  — take in your surroundings\n"
            "  look at <item>        — examine something without picking it up\n"
            "  examine <item>        — look closely at something you're carrying\n"
            "  read <item>           — same as examine\n"
            "  take <item>           — pocket an item ('take all' grabs everything)\n"
            "  drop <item>           — set something down\n"
            "  use <item>            — put an item to work; may reveal a puzzle\n"
            "  combine <x> with <y>  — two clues are sometimes one clue\n"
            "  inventory (or i)      — check what you're carrying\n"
            "  score                 — check your case progress\n\n"
            "HOUSEKEEPING\n"
            "  save / load   — the city will still be here when you come back\n"
            "  quit          — end the session\n\n"
            "A NOTE ON DARKNESS\n"
            "  Seattle has places where the lights don't reach.\n"
            "  In such places, it is pitch dark.\n"
            "  You are likely to be eaten by a grue.\n"
            "  This is not a metaphor. Carry a light source.\n\n"
            "  (The foregoing is in tribute to a certain text adventure from 1980\n"
            "   whose Great Underground Empire bears a passing resemblance to this city.)"
        )
        print_text(help_text)

    def show_victory(self) -> None:
        """Display victory message."""
        victory_text = (
            "EXPENSE ACCOUNT MEMO\n"
            "The Matter of the Northwest Maritime Imports\n"
            "Filed: October 1947, Seattle, Washington\n"
            "Investigator: J. Diamond\n"
            "============================================\n\n"
            "Expense account item one: Cab fare, police headquarters to the waterfront "
            "docks. One dollar and fifteen cents. The driver didn't ask where I'd been. "
            "Smart man.\n\n"
            "Expense account item two: One pair of shoe leather, worn through the "
            "underground tunnels beneath Pioneer Square. Three dollars even. I'll need "
            "new ones before the next case.\n\n"
            "Expense account item three: One copy of the Seattle Post-Intelligencer. "
            "Five cents. The headline the following morning read: PORT AUTHORITY CAPTAIN "
            "RESIGNS. The story ran below the fold. These things always do.\n\n"
            "Expense account item four: Six hours of sleep, not taken. I'll put them "
            "on the next bill.\n\n"
            "Total expenses to date: four dollars and twenty cents.\n\n"
            "Sullivan — the man they called the Harbormaster — was taken at Pier 7 at "
            "twenty past three in the morning, along with six of his crew and two tons "
            "of stolen Army medical supplies. Northwest Maritime Imports dissolved before "
            "the ink dried on the warrant. The shell company behind it had the same "
            "registered agent as four others. All investigated. None prosecuted. "
            "Until now.\n\n"
            "Voss — Captain Harlan Voss, Port Authority liaison, Eagles Third Chapter "
            "No. 1144 — resigned his commission before the arraignment. The department "
            "accepted it without comment. The Eagles chapter voted to expunge his "
            "membership record three days later. The minutes of that vote are not "
            "available for general circulation. That's how these things go.\n\n"
            "Mathers — Badge 447, Third District — submitted his papers the morning of "
            "the arrest. Beat me to the paperwork by two hours. Last I heard, "
            "he moved to Spokane. I hope it rains there.\n\n"
            "R. — Roy Hendricks, motorman on the waterfront line, who had the presence "
            "of mind to write down a frequency and the courage to pass it to a stranger "
            "— collected his pension the following spring and moved to Olympia. "
            "I never learned his last name until it was over. That's how it goes "
            "with the ones who actually help you.\n\n"
            "I filed my report, poured two fingers of rye, and listened to the radio. "
            "Richard Diamond was on. He was having a worse night than I was. "
            "I found that comforting.\n\n"
            "The city would have more cases.\n"
            "It always does.\n\n"
            "Yours truly,\n"
            "Johnny Diamond\n\n"
            "                    * * *\n\n"
            "               EMERALD SHADOWS\n"
            "         A noir detective adventure for one\n"
            "           Seattle, Washington. October 1947.\n\n"
            "   In tribute to Yours Truly, Johnny Dollar\n"
            "   and Richard Diamond, Private Detective —\n"
            "   the detectives who lived inside the radio.\n\n"
            "   And to Infocom, whose Great Underground Empire\n"
            "   taught a generation that stories could live inside machines."
        )
        print_text(victory_text)

if __name__ == "__main__":
    game = GameManager()
    game.start_game()