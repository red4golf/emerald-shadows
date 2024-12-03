from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import logging
from .utils import print_text

INITIAL_GAME_STATE = {
    "notes_found": 0,
    "has_key": False,
    "has_badge": False
}

ITEM_DESCRIPTIONS = {
    "badge": {
        "basic": "A detective's badge, worn but well-maintained.",
        "detailed": "Your detective's badge shows signs of wear but remains a symbol of authority. The metal is cool to the touch.",
        "use_effects": {
            "smith_tower": "You show your badge to gain access to the restricted areas.",
            "police_station": "The desk sergeant nods as you flash your badge."
        },
        "use_locations": ["smith_tower", "police_station", "warehouse"],
        "consumable": False
    },
    "binoculars": {
        "basic": "A pair of high-quality binoculars.",
        "detailed": "These binoculars are military surplus, perfect for surveillance work.",
        "use_effects": {
            "observation_deck": "You use the binoculars to observe the city below, noting suspicious movements.",
            "waterfront": "The binoculars help you track ship movements in the harbor."
        },
        "use_locations": ["observation_deck", "waterfront", "pioneer_square"],
        "consumable": False
    },
    "cipher_wheel": {
        "basic": "A peculiar device with rotating rings of letters.",
        "detailed": "This cipher wheel appears to be custom-made. The outer ring shows the standard alphabet, while the inner ring can be rotated to create different letter substitutions.",
        "use_effects": {
            "all": "You could use this to decode encrypted messages."
        },
        "use_locations": ["evidence_room", "office", "warehouse"],
        "consumable": False
    }
}

ITEM_COMBINATIONS = {
    frozenset(["notebook", "cipher_wheel"]): {
        "description": "You use the cipher wheel to decode the cryptic notes in the notebook.",
        "result": "decoded_notes",
        "removes_items": False
    },
    frozenset(["badge", "photo"]): {
        "description": "You notice some details in the photo that correspond to your department records.",
        "result": "identified_suspect",
        "removes_items": False
    }
}

class ItemManager:
    def __init__(self):
        self.inventory: List[str] = []
        self.notes_found: int = INITIAL_GAME_STATE.get("notes_found", 0)
        self.discovered_combinations: Set[str] = set()
        self.removed_items: Set[str] = set()
           
    def take_item(self, item: str, location_items: List[str], game_state: Dict) -> bool:
        """Pick up an item from the current location."""
        try:
            if item not in location_items:
                print_text(f"There is no {item} here.")
                return False
        
            self.inventory.append(item)
            self.removed_items.add(item)  # Track that this item has been removed
        
            # Handle special items first
            if item == "badge":
                game_state["has_badge"] = True
                print_text("You clip the badge to your belt. Its familiar weight is reassuring.")
                logging.info("Badge taken and has_badge state set to True")
                return True
            
            # Handle finding notes
            if item.startswith("note_"):
                self.notes_found += 1
                print_text(f"You've found clue {self.notes_found}.")
                if self.notes_found == 5:
                    game_state["found_all_notes"] = True
                    print_text("\nYou've collected all the scattered notes!")
                    self.show_compiled_notes()
                return True
            
            # Generic message for all other items
            print_text(f"You take the {item}.")
            return True
        
        except Exception as e:
            logging.error(f"Error taking item {item}: {e}")
            print_text("There was a problem picking up the item.")
            return False
       
    def examine_item(self, item: str, location_items: List[str], game_state: Dict) -> None:
        """Examine an item in inventory or in the current location."""
        try:
            if item in self.inventory:
                if item in ITEM_DESCRIPTIONS:
                    print_text("\n" + ITEM_DESCRIPTIONS[item]["detailed"])
                    if item == "photo" and not game_state.get("discovered_suspect", False):
                        game_state["discovered_suspect"] = True
                        print_text("\nThe person in the photo looks familiar...")
                    elif item == "cipher_wheel" and not game_state.get("examined_cipher", False):
                        game_state["examined_cipher"] = True
                        print_text("\nThe cipher wheel looks like it could decode encrypted messages...")
                else:
                    print_text(f"You examine the {item} closely but find nothing unusual.")
            elif item in location_items:
                print_text(f"You'll need to take the {item} first to examine it closely.")
            else:
                print_text(f"You don't see any {item} here.")
            
        except Exception as e:
            logging.error(f"Error examining item {item}: {e}")
            print_text("There was a problem examining the item.")

    def use_item(self, item: str, current_location: str, game_state: Dict) -> None:
        """Use an item from the inventory."""
        try:
            if item not in self.inventory:
                print_text("You don't have that item.")
                return
           
            item_data = ITEM_DESCRIPTIONS.get(item, {})
            use_effects = item_data.get("use_effects", {})
            valid_locations = item_data.get("use_locations", [])
       
            if current_location in use_effects or ("all" in use_effects and current_location in valid_locations):
                effect = use_effects.get(current_location, use_effects.get("all"))
                print_text("\n" + effect)
           
                if item_data.get("consumable", False):
                    self.inventory.remove(item)
                    print_text(f"You no longer have the {item}.")
           
                self._handle_special_item_effects(item, current_location, game_state)
            else:
                print_text(f"You can't use the {item} here effectively.")
           
        except Exception as e:
            logging.error(f"Error using item {item}: {e}")
            print_text("There was a problem using the item.")

    def _handle_special_item_effects(self, item: str, location: str, game_state: Dict) -> None:
        """Handle special effects when using certain items in specific locations."""
        try:
            special_effects = {
                ("badge", "smith_tower"): lambda: game_state.update({"has_badge_shown": True}),
                ("binoculars", "observation_deck"): lambda: game_state.update({"observed_activity": True}),
                ("cipher_wheel", "evidence_room"): lambda: game_state.update({"started_decoding": True})
            }
       
            effect = special_effects.get((item, location))
            if effect:
                effect()
           
        except Exception as e:
            logging.error(f"Error handling special effect for {item} at {location}: {e}")

    def combine_items(self, item1: str, item2: str, game_state: Dict) -> bool:
        """Attempt to combine two items from the inventory."""
        try:
            if item1 not in self.inventory or item2 not in self.inventory:
                print_text("You need both items in your inventory to combine them.")
                return False
           
            combo = frozenset([item1, item2])
            if combo in ITEM_COMBINATIONS and combo not in self.discovered_combinations:
                result = ITEM_COMBINATIONS[combo]
                print_text("\n" + result['description'])
           
                if result['removes_items']:
                    for item in result['removes_items']:
                        if item in self.inventory:
                            self.inventory.remove(item)
           
                game_state[result['result']] = True
                self.discovered_combinations.add(combo)
                return True
            elif combo in self.discovered_combinations:
                print_text("You've already discovered what these items reveal together.")
                return False
            else:
                print_text("These items can't be combined in any meaningful way.")
                return False
           
        except Exception as e:
            logging.error(f"Error combining items {item1} and {item2}: {e}")
            print_text("There was a problem combining the items.")
            return False

    def show_inventory(self) -> None:
        """Display the current inventory contents with basic descriptions."""
        try:
            if not self.inventory:
                print_text("Your inventory is empty.")
                return
           
            print_text("\nInventory:")
            for item in self.inventory:
                basic_desc = ITEM_DESCRIPTIONS.get(item, {}).get("basic", "No description available.")
                print_text(f"- {item}: {basic_desc}")
            print_text("\nTip: Use 'examine <item>' for a closer look.")
       
        except Exception as e:
            logging.error(f"Error showing inventory: {e}")
            print_text("There was a problem displaying the inventory.")

    def show_compiled_notes(self) -> None:
        """Display the complete compiled notes once all are collected."""
        notes = """
        Collected Intelligence Notes:
        
        1. Multiple reports of suspicious activity around the harbor district.
        2. Pattern of unexplained equipment movements in the dead of night.
        3. Several witnesses mention seeing the same blue sedan.
        4. Possible connection to recent thefts from medical warehouses.
        5. Key suspect believed to be operating from Smith Tower vicinity.
        
        These notes paint a picture of organized criminal activity...
        """
        print_text("\nAs you organize all the collected notes, patterns emerge...")
        print_text(notes)
        print_text("\nThis could be the breakthrough you needed in the case.")

    def get_inventory(self) -> List[str]:
        """Get the current inventory contents."""
        return self.inventory.copy()

    def has_item(self, item: str) -> bool:
        """Check if an item is in the inventory."""
        return item in self.inventory
    
    def get_inventory_state(self) -> Dict[str, any]:
        """Get the complete inventory state."""
        return {
            "inventory": self.inventory.copy(),
            "notes_found": self.notes_found,
            "discovered_combinations": list(self.discovered_combinations),
            "removed_items": list(self.removed_items)
        }
    
    def restore_inventory_state(self, state: Dict[str, any]) -> None:
        """Restore inventory from saved state."""
        self.inventory = state.get("inventory", []).copy()
        self.notes_found = state.get("notes_found", 0)
        self.discovered_combinations = set(state.get("discovered_combinations", []))
        self.removed_items = set(state.get("removed_items", []))