"""Location management system for Emerald Shadows."""
from typing import Dict, Optional, List, Tuple, Any
import json
import logging
from copy import deepcopy
from dataclasses import dataclass
from .config import STARTING_LOCATION
from .config_locations import LOCATIONS
from .trolley_system import TrolleySystem, TrolleyState
from .utils import print_text

@dataclass
class Location:
    """Data structure for location information."""
    name: str
    description: str
    exits: Dict[str, str]
    items: List[str]
    first_visit: bool = True
    requires: Optional[str] = None
    historical_note: Optional[str] = None

class LocationError(Exception):
    """Custom exception for location-related errors."""
    pass

class LocationManager:
    """Manages game locations and movement between them."""
    
    def __init__(self) -> None:
        """Initialize the LocationManager with all game locations and routes."""
        self._initialize_locations()
        self.trolley = TrolleySystem()
        self.last_command: Optional[str] = None

    def _initialize_locations(self) -> None:
        """Initialize location data structures."""
        try:
            self.current_location: str = STARTING_LOCATION
            self.locations: Dict[str, Location] = {}
            self.original_items: Dict[str, List[str]] = {}
            
            for name, data in LOCATIONS.items():
                # Convert dictionary data to Location objects
                location = Location(
                    name=name,
                    description=data["description"],
                    exits=data["exits"].copy(),
                    items=data.get("items", []).copy(),
                    first_visit=True,
                    requires=data.get("requires"),
                    historical_note=data.get("historical_note")
                )
                self.locations[name] = location
                self.original_items[name] = data.get("items", []).copy()
                
            logging.info("Locations initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize locations: {e}")
            raise LocationError("Could not initialize game locations")

    def get_location_description(self) -> str:
        """Get the description of the current location with available exits and items."""
        try:
            location = self.locations[self.current_location]
            description_parts = [location.description]

            # Add available exits
            if location.exits:
                exit_list = ", ".join(location.exits.keys())
                description_parts.append(f"\nExits: {exit_list}")
        
            # List items in the room
            if location.items:
                item_list = ", ".join(location.items)
                description_parts.append(f"\nYou can see: {item_list}")
        
            return "\n".join(description_parts)
            
        except KeyError:
            logging.error(f"Invalid location reference: {self.current_location}")
            return "Error: Location not found."
        except Exception as e:
            logging.error(f"Error getting location description: {e}")
            return "Error: Could not get location description."
    
    def move_to_location(self, direction: str, game_state: Dict) -> bool:
        """
        Attempt to move in the specified direction.
        
        Args:
            direction: The direction to move in
            game_state: Current game state for checking requirements
            
        Returns:
            bool: True if movement was successful, False otherwise
        """
        try:
            self._validate_current_location()
            current_location = self.locations[self.current_location]
            
            if direction not in current_location.exits:
                print_text("You can't go that way.")
                return False

            new_location_name = current_location.exits[direction]

            # Handle trolley as special case
            if new_location_name == "trolley":
                return self._handle_trolley_movement()
            
            # Check requirements for new location
            if not self._check_location_requirements(new_location_name, game_state):
                return False
            
            # Perform the movement
            self.current_location = new_location_name
            new_location = self.locations[new_location_name]
            
            # Handle first visit
            if new_location.first_visit:
                new_location.first_visit = False
                if new_location.historical_note:
                    print_text(f"\nHistorical Note: {new_location.historical_note}")
            
            return True
            
        except LocationError as e:
            logging.error(f"Location error during movement: {e}")
            print_text(str(e))
            return False
        except Exception as e:
            logging.error(f"Unexpected error during movement: {e}")
            print_text("There was a problem moving to that location.")
            return False

    def _validate_current_location(self) -> None:
        """Validate that current_location is valid."""
        if self.current_location not in self.locations:
            raise LocationError(f"Invalid current location: {self.current_location}")

    def _check_location_requirements(self, location_name: str, game_state: Dict) -> bool:
        """Check if requirements are met for entering a location."""
        try:
            if location_name not in self.locations:
                return False
                
            location = self.locations[location_name]
            if location.requires:
                if not game_state.get(location.requires, False):
                    print_text(f"You can't access this area yet. You need to {location.requires.replace('_', ' ')} first.")
                    return False
            return True
            
        except Exception as e:
            logging.error(f"Error checking location requirements: {e}")
            return False

    def _handle_trolley_movement(self) -> bool:
        """Handle special case of trolley movement."""
        try:
            self.current_location = "trolley"
            trolley_location = self.locations["trolley"]
            
            # First boarding
            if trolley_location.first_visit:
                trolley_location.first_visit = False
                print_text(self.trolley.board_trolley())
                initial_exits = {"next": "trolley", "off": self.trolley.routes[0]["exits"]["off"]}
                trolley_location.exits = initial_exits
                return True
            
            return True
            
        except Exception as e:
            logging.error(f"Error handling trolley movement: {e}")
            print_text("There was a problem with the trolley system.")
            return False
    
    def handle_trolley_command(self, command: str) -> None:
        """Handle trolley-specific commands."""
        try:
            if self.current_location != "trolley":
                return

            command = command.lower().strip()
            self.last_command = command
            
            if command == "status":
                print_text(self.trolley.get_status())
            elif command == "history":
                print_text(self.trolley.get_history())
            elif command == "look":
                print_text(self.trolley.get_status())
            elif command in ["next", "off"]:
                message, exits = self.trolley.handle_movement()
                print_text(message)
                self.locations["trolley"].exits = exits
            else:
                print_text("Invalid trolley command. Use: next, off, status, history, or look")
            
        except Exception as e:
            logging.error(f"Error handling trolley command: {e}")
            print_text("There was a problem with the trolley system.")

    def show_historical_note(self, location: str) -> None:
        """Display historical information about the specified location."""
        try:
            if location in self.locations and self.locations[location].historical_note:
                print_text(f"\nHistorical Note: {self.locations[location].historical_note}")
            else:
                print_text("No historical information available for this location.")
           
        except Exception as e:
            logging.error(f"Error showing historical note for {location}: {e}")
            print_text("There was a problem accessing the historical information.")

    def get_available_items(self) -> List[str]:
        """Get list of items in current location."""
        try:
            return self.locations[self.current_location].items.copy()
        except KeyError:
            logging.error(f"Failed to get items - invalid location: {self.current_location}")
            return []
        except Exception as e:
            logging.error(f"Error getting available items: {e}")
            return []

    def remove_item(self, item: str) -> None:
        """Remove an item from the current location."""
        try:
            location = self.locations[self.current_location]
            if item in location.items:
                location.items.remove(item)
                logging.info(f"Removed {item} from {self.current_location}")
        except Exception as e:
            logging.error(f"Error removing item {item} from {self.current_location}: {e}")

    def get_location_states(self) -> Dict[str, Dict[str, Any]]:
        """Get the current state of all locations."""
        try:
            return {
                name: {
                    "items": location.items.copy(),
                    "first_visit": location.first_visit
                }
                for name, location in self.locations.items()
            }
        except Exception as e:
            logging.error(f"Error getting location states: {e}")
            return {}

    def restore_location_states(self, location_states: Dict[str, Dict[str, Any]]) -> None:
        """Restore location states from saved data."""
        try:
            for location_name, state in location_states.items():
                if location_name in self.locations:
                    location = self.locations[location_name]
                    location.items = state.get("items", []).copy()
                    location.first_visit = state.get("first_visit", True)
            logging.info("Location states restored successfully")
        except Exception as e:
            logging.error(f"Error restoring location states: {e}")
            raise LocationError("Failed to restore location states")

    def get_valid_exits(self) -> List[str]:
        """Get list of valid exits from current location."""
        try:
            return list(self.locations[self.current_location].exits.keys())
        except KeyError:
            logging.error(f"Failed to get exits - invalid location: {self.current_location}")
            return []
        except Exception as e:
            logging.error(f"Error getting valid exits: {e}")
            return []

    def get_requirements(self, location: str) -> Optional[str]:
        """Get requirements for accessing a location."""
        try:
            return self.locations[location].requires if location in self.locations else None
        except Exception as e:
            logging.error(f"Error getting requirements for {location}: {e}")
            return None

    def reset_location(self, location: str) -> None:
        """Reset a location to its original state."""
        try:
            if location in self.locations and location in self.original_items:
                self.locations[location].items = self.original_items[location].copy()
                self.locations[location].first_visit = True
                logging.info(f"Reset location {location} to original state")
        except Exception as e:
            logging.error(f"Error resetting location {location}: {e}")
            raise LocationError(f"Failed to reset location: {location}")

    def get_state(self) -> Dict[str, Any]:
        """Get complete state for saving."""
        return {
            'current_location': self.current_location,
            'locations': self.get_location_states(),
            'trolley': self.trolley.get_state()
        }

    def restore_state(self, state: Dict[str, Any]) -> None:
        """Restore complete state from save data."""
        try:
            if not isinstance(state, dict) or 'current_location' not in state:
                raise ValueError("Invalid state format")
                
            self.current_location = state['current_location']
            self.restore_location_states(state['locations'])
            
            if 'trolley' in state:
                self.trolley.restore_state(state['trolley'])
                
            logging.info("Location manager state restored successfully")
        except Exception as e:
            logging.error(f"Error restoring location manager state: {e}")
            raise LocationError("Failed to restore location manager state")