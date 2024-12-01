"""Trolley System Module

Handles the historic trolley transportation system.
"""

from typing import Dict, Optional
import logging
from .config import TROLLEY_ROUTES

class TrolleySystem:
    """Manages the trolley transportation system."""
    
    def __init__(self):
        """Initialize the trolley system."""
        self.current_stop = 0
        self.on_trolley = False
        self.logger = logging.getLogger(__name__)
        
    def board_trolley(self) -> bool:
        """Board the trolley at current stop."""
        if self.on_trolley:
            return False
            
        self.on_trolley = True
        self.logger.info(f"Boarded trolley at stop {self.current_stop}")
        return True
        
    def exit_trolley(self) -> Optional[str]:
        """Exit the trolley at current stop."""
        if not self.on_trolley:
            return None
            
        current_route = TROLLEY_ROUTES.get(self.current_stop)
        if not current_route:
            return None
            
        self.on_trolley = False
        self.logger.info(f"Exited trolley at stop {self.current_stop}")
        return current_route["exits"].get("off")
        
    def next_stop(self) -> bool:
        """Move to next trolley stop."""
        if not self.on_trolley:
            return False
            
        next_stop = (self.current_stop + 1) % len(TROLLEY_ROUTES)
        self.current_stop = next_stop
        self.logger.info(f"Moved to trolley stop {self.current_stop}")
        return True