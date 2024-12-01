"""Item Manager Module

Handles inventory management and item interactions.
"""

from typing import Dict, List, Set, Optional
import logging
from .config import ITEM_DESCRIPTIONS, ITEM_COMBINATIONS

class ItemManager:
    """Manages game items and inventory system."""
    
    def __init__(self):
        """Initialize the item manager."""
        self.inventory: Set[str] = set()
        self.logger = logging.getLogger(__name__)
        
    def add_item(self, item_id: str) -> bool:
        """Add an item to inventory."""
        if item_id not in ITEM_DESCRIPTIONS:
            self.logger.error(f"Attempted to add invalid item: {item_id}")
            return False
            
        self.inventory.add(item_id)
        self.logger.info(f"Added item to inventory: {item_id}")
        return True
        
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from inventory."""
        if item_id not in self.inventory:
            return False
            
        self.inventory.remove(item_id)
        self.logger.info(f"Removed item from inventory: {item_id}")
        return True