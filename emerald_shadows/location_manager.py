"""Location Manager Module

Handles location management, movement, and location-specific interactions.
"""

from typing import Dict, List, Optional
import logging
from .config import LOCATIONS

class LocationManager:
    """Manages game locations and player movement."""
    
    def __init__(self):
        """Initialize the location manager."""
        self.current_location = "police_station"
        self.logger = logging.getLogger(__name__)
        self.visited_locations = set()
        
    def get_location_description(self, location_id: str) -> str:
        """Get the description for a location."""
        if location_id not in LOCATIONS:
            self.logger.error(f"Invalid location requested: {location_id}")
            return "Location not found."
            
        location = LOCATIONS[location_id]
        is_first_visit = location_id not in self.visited_locations
        
        if is_first_visit:
            self.visited_locations.add(location_id)
            
        return location["description"]
        
    def get_available_exits(self) -> Dict[str, str]:
        """Get available exits from current location."""
        if self.current_location not in LOCATIONS:
            return {}
        return LOCATIONS[self.current_location]["exits"]
        
    def move_to_location(self, direction: str) -> bool:
        """Attempt to move in the specified direction."""
        exits = self.get_available_exits()
        if direction not in exits:
            return False
            
        new_location = exits[direction]
        if self._check_location_requirements(new_location):
            self.current_location = new_location
            self.logger.info(f"Moved to location: {new_location}")
            return True
        return False