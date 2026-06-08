from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import logging
from .utils import print_text

ITEM_DESCRIPTIONS = {
    "informant_note": {
        "basic": "A folded note, left where you'd find it.",
        "detailed": (
            "The handwriting is cramped and hurried, like someone who knew they weren't "
            "safe standing still long enough to write slowly. It reads: 'Emergency "
            "frequency 415.6 MHz — they broadcast shipment times nightly at 2 AM. "
            "Don't use the phone. —R.' Somebody out there is taking a risk for you. "
            "Don't waste it."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "bulletin_notice": {
        "basic": "A notice from the Pioneer Square bulletin board.",
        "detailed": (
            "A shipping manifest, typed on company letterhead. The name at the top stops "
            "you cold: NORTHWEST MARITIME IMPORTS. You've seen that name before — in the "
            "evidence room, in the warehouse files, in the margin of the radio manual. "
            "It's always in the margin. Never the headline. Until now. "
            "You have your organization."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "flashlight": {
        "basic": "A military-surplus flashlight, heavy and reliable.",
        "detailed": (
            "Olive drab casing, Army-issue, the kind that came back from the Pacific in "
            "somebody's kit bag. It works. In certain parts of this city, that makes it "
            "more valuable than your badge. You recall reading once about creatures that "
            "live in absolute darkness — grues, they were called. You've always assumed "
            "that was fiction. You're less sure now."
        ),
        "use_effects": {
            "underground_tunnels": (
                "You click on the flashlight. The beam cuts through the dark — "
                "brick, timber, old iron. You move forward and then stop.\n\n"
                "Somewhere ahead, water drips from the mortar. Then something shifts. "
                "One of those sounds is the building settling. "
                "The other one isn't.\n\n"
                "You note the exits, take your bearings, and keep moving. "
                "Whoever else is in these tunnels with you hasn't acted yet. "
                "You plan to be finished before they decide to."
            )
        },
        "use_locations": ["underground_tunnels"],
        "consumable": False
    },
    "badge": {
        "basic": "Your detective's shield. It's seen better days. So have you.",
        "detailed": (
            "Gold-toned, dented on one corner from a disagreement in '44 that you came "
            "out of better than the other party. Your name and number are stamped on the "
            "back. DIAMOND, J. — No. 7714. In this city, the badge opens some doors and "
            "closes others. Knowing which is which is the job."
        ),
        "use_effects": {
            "smith_tower": (
                "You hold the badge where Harold the elevator operator can see it. "
                "He nods once and takes you up to the restricted floor without being asked."
            ),
            "police_station": (
                "The desk sergeant glances at the shield and goes back to his paperwork. "
                "That's acknowledgment enough on the night shift."
            ),
            "eagles_hall": (
                "You show the badge to the night porter — a grey man in a grey cardigan "
                "who materializes from a side corridor. He studies it with the careful "
                "attention of someone who has learned that things are not always what they "
                "appear. Then he steps aside without a word and gestures toward the back "
                "room. He has decided that the badge is more interesting than whatever "
                "he was paid not to see tonight."
            ),
            "anchor_tavern": (
                "You set the badge on the bar. Ches looks at it for a long moment — "
                "not afraid of it, just reading it — then sets down the glass he's "
                "been wiping.\n\n"
                "'The ship in the roads.' His voice is low enough that the men in the "
                "booth can't hear. 'Sitting out there three nights running. Waiting. "
                "A launch went out from Pier 7 last night, around three. Came back light. "
                "Whatever it was going for, it didn't get it yet.'\n\n"
                "He picks up the badge with two fingers and slides it back across the bar.\n\n"
                "'I didn't say that. You didn't hear it. Understood?'\n\n"
                "You pocket the badge and leave him to his glass."
            )
        },
        "use_locations": ["smith_tower", "police_station", "warehouse", "eagles_hall", "anchor_tavern"],
        "consumable": False
    },
    "binoculars": {
        "basic": "Military binoculars, 7x50, from the war.",
        "detailed": (
            "Zeiss glass in a Navy-issue housing — the kind a ship's officer would carry. "
            "Someone brought these back from the Pacific and left them on the observation "
            "deck of the Smith Tower, which tells you either they forgot them or they "
            "wanted to forget what they'd seen through them. Either way, they're yours now."
        ),
        "use_effects": {
            "observation_deck": (
                "Through the Zeiss glass, the warehouse district sharpens into focus. "
                "Trucks moving after midnight. No dock authority vehicles. One of the "
                "ships at anchor has a boarding ladder down, which means someone is "
                "expected. You make a note."
            ),
            "waterfront": (
                "The cargo vessel offshore comes into sharp relief. No name on the hull "
                "that you can read. The boarding ladder is down and a small launch is "
                "making for it through the dark water. You make another note."
            )
        },
        "use_locations": ["observation_deck", "waterfront"],
        "consumable": False
    },
    "cipher_wheel": {
        "basic": "A handmade cipher device — two rotating rings of letters.",
        "detailed": (
            "Custom work, not military issue. The outer ring is the standard alphabet; "
            "the inner ring rotates to create substitutions. Someone built this carefully "
            "and used it regularly — the brass is worn smooth at the grip points. "
            "A cipher wheel without a key is just a puzzle. "
            "You need to find the key."
        ),
        "use_effects": {
            "all": "You turn the cipher wheel in your hands. It's waiting for a key word."
        },
        "use_locations": ["evidence_room", "office", "warehouse"],
        "consumable": False
    },
    "notebook": {
        "basic": "Your case notebook — half full, all business.",
        "detailed": (
            "Your own handwriting across fifty pages: times, names, addresses, license "
            "plates, things people said when they thought nobody was listening. The "
            "entries get tighter and more urgent as you get closer to the warehouse "
            "district. The last page ends mid-sentence. You wrote it in a hurry. "
            "The coded notes from the evidence room are in here too, waiting."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "radio_manual": {
        "basic": "A restricted military radio operations manual.",
        "detailed": (
            "Stamped RESTRICTED — WAR DEPARTMENT in red on the cover, though the war "
            "is over and the department is busy becoming the Defense Department. Inside: "
            "frequency allocation tables, tuning procedures, band charts. Someone has "
            "pencilled a note in the margin next to the emergency frequencies section: "
            "'415.6 — check nightly.' The pencil is recent. The war surplus radio in "
            "the warehouse office was built for exactly this frequency range."
        ),
        "use_effects": {
            "warehouse_office": (
                "You lay the manual open on the desk beside the radio set and work "
                "through the tuning procedure step by step. The dial clicks under "
                "your fingers. The frequency is in here. You just have to find it."
            )
        },
        "use_locations": ["warehouse_office"],
        "consumable": False
    },
    "case_file": {
        "basic": "Your open case file — thick and getting thicker.",
        "detailed": (
            "The manila folder is stamped ACTIVE in blue ink that someone pressed hard "
            "enough to dent the cardboard. Inside: three witness statements that don't "
            "quite line up, two incident reports from the port authority that were "
            "filed and then quietly unfiled, a hand-drawn map of the warehouse district "
            "with three buildings circled in red grease pencil. "
            "And a note from your captain: 'Keep this quiet, Diamond.'\n\n"
            "You kept it quiet for three weeks — until you found out where the morphine "
            "sulfate was going instead of veterans' hospitals, and who was being paid to "
            "wave the trucks through. Closing this case will cost you the badge, yours "
            "or someone else's. You made your decision the night you read that ledger page. "
            "You're done being quiet."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "newspaper": {
        "basic": "This morning's Seattle Post-Intelligencer, rain-damp.",
        "detailed": (
            "The P-I, October 1947. The headline above the fold: PORT AUTHORITY DENIES "
            "SMUGGLING CLAIMS. Below the fold, smaller: THIRD WATERFRONT BREAK-IN THIS "
            "MONTH — POLICE CITE NO LEADS. You are a lead. You are, at this moment, "
            "the only lead. You fold the paper under your arm and keep moving."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "photo": {
        "basic": "A surveillance photograph, slightly out of focus.",
        "detailed": (
            "Two men in overcoats unloading crates from a panel truck backed up to a "
            "warehouse door. Night shot, grainy — whoever took this was working fast "
            "and didn't have good light. The shorter man's face is turned away. "
            "The taller one is half-visible, and something about the set of his "
            "shoulders is familiar in the way that makes your jaw tighten. "
            "You've seen this man before. You'll know him when you find him.\n\n"
            "The rear plate of the panel truck is just visible at the frame's edge: "
            "WA-4471. Washington registration. You write it down."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "note_1": {
        "basic": "A torn scrap of paper, found in the Smith Tower lobby.",
        "detailed": (
            "Pencil on the back of a matchbook cover, written fast: "
            "'Tues + Fri, after midnight. Three trucks. No. 447 waves them through.' "
            "Badge 447 is Walt Mathers. Third District. "
            "He came up through the academy with you in '39. "
            "You stood up at his wedding. "
            "Your first solid lead, and it points somewhere you've been trying "
            "not to look for three weeks."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "note_2": {
        "basic": "A ledger page, torn out and folded small.",
        "detailed": (
            "Inventory columns, neatly typed — but the goods listed don't match any "
            "legitimate shipping manifest you've ever seen. Morphine sulfate. Penicillin. "
            "Whole blood plasma. Army medical supplies, quantities that should have been "
            "destroyed under the 1946 demobilization orders. Instead they went somewhere "
            "else. This page tells you how much. Other pages will tell you where."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "note_3": {
        "basic": "A water-stained note — the ink has run but the message hasn't.",
        "detailed": (
            "'Warehouse 22 is the hub. Everything moves through there. Do not go alone.' "
            "The handwriting belongs to someone who was frightened when they wrote it. "
            "The warning is sound. You're going alone anyway. "
            "That's the job."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "note_4": {
        "basic": "A typed internal memo, one corner burned away.",
        "detailed": (
            "Company letterhead, the name burned off with the corner. The text "
            "references 'Project Emerald' and a man referred to only as the Harbormaster "
            "— no name, no title, no address. The memo authorizes 'continued operations "
            "through Q4.' Whatever was signed at the bottom is ash. "
            "The project name is not lost on you."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "membership_register": {
        "basic": "The Eagles' 1946 membership roster — alphabetical, annotated.",
        "detailed": (
            "The register is open to the 1946 annual roster. Under V: Voss, H.R. — "
            "No. 1144 — Port Authority Liaison, Third Chapter. His co-sponsorships are "
            "listed: three new members inducted in March of that year. One of the names "
            "makes you very still. Sullivan, E.D. Another makes you stiller. "
            "You write down Voss's member number. 1144. You have a feeling you'll need it."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "meeting_minutes": {
        "basic": "Eagles Third Chapter committee minutes, marked NOT FOR GENERAL CIRCULATION.",
        "detailed": (
            "You go straight to the March 1946 session. Under new business: a motion to "
            "authorize the Eagles Third Chapter's 'civic improvement partnership' with "
            "Northwest Maritime Imports — moved by Voss, seconded by a name that's been "
            "whited out, carried unanimously. The attached agreement shows quarterly "
            "payments into a fund described only as 'waterfront development.' "
            "Voss's signature is at the bottom, full and clear, no ambiguity. "
            "You fold the minutes carefully and put them in your inside pocket next to "
            "the photo. The two of them belong together."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "manifest": {
        "basic": "The Pier 7 cargo declaration — the numbers don't add up.",
        "detailed": (
            "Cargo: Army surplus medical supplies, lot 44-F, fifteen hundred units. "
            "Declared weight: 3,200 pounds. You stand there doing arithmetic. Fifteen "
            "hundred units of packaged morphine sulfate and penicillin would weigh "
            "approximately 850 pounds. Something weighing 3,200 pounds is not just "
            "medical supplies. There is a second load underneath the first, and someone "
            "in the Port Authority signed off on the discrepancy. "
            "You have his name. You have his signature on the Eagles minutes "
            "in your other pocket. Now you have the weight of what he signed."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    },
    "note_5": {
        "basic": "A business card with a handwritten note on the back.",
        "detailed": (
            "Northwest Maritime Imports — printed front, engraved stock, the kind of "
            "card a company uses when it wants to look legitimate. On the back, in the "
            "same hand as the margin note in the radio manual: "
            "'Ask for Sullivan. Tell him the angels sent you.' "
            "You turn the card over. You turn it back. "
            "Something about that word won't let go of you."
        ),
        "use_effects": {},
        "use_locations": [],
        "consumable": False
    }
}

ITEM_COMBINATIONS = {
    frozenset(["notebook", "cipher_wheel"]): {
        "description": (
            "You set the cipher wheel against the coded entries in your notebook and "
            "rotate the inner ring through the alphabet, one letter at a time, until "
            "the text resolves into plain English. It's slower than radio. "
            "It's more reliable than most people."
        ),
        "result": "decoded_notes",
        "removes_items": False
    },
    frozenset(["badge", "photo"]): {
        "description": (
            "You hold the photograph next to your badge and look at both. "
            "The taller man in the photo — the set of his jaw, the way he stands. "
            "You've seen that man sign off on interdepartmental memos. "
            "You've shaken that hand.\n\n"
            "Captain Harlan Voss. Port Authority liaison to the department. "
            "Badge on the thirty-second floor. His name is on three of those "
            "interdepartmental memos, and his signature is on the building inspector's "
            "sign-off for the warehouse office. "
            "That's your Harbormaster.\n\n"
            "You put the photo in your inside pocket. You won't need to look at it again."
        ),
        "result": "identified_suspect",
        "removes_items": False
    }
}

class ItemManager:
    def __init__(self):
        self.inventory: List[str] = []
        self.notes_found: int = 0
        self.discovered_combinations: Set[str] = set()
        self.removed_items: Set[str] = set()
           
    _SCORED_ITEMS = {
        "badge", "cipher_wheel", "notebook", "binoculars", "radio_manual",
        "membership_register", "meeting_minutes", "manifest",
    }

    def take_item(self, item: str, location_items: List[str], game_state: Dict) -> bool:
        """Pick up an item from the current location."""
        try:
            if item not in location_items:
                print_text(f"There is no {item} here.")
                return False

            self.inventory.append(item)
            self.removed_items.add(item)

            if item == "badge":
                game_state["has_badge"] = True
                game_state["score"] = game_state.get("score", 0) + 10
                print_text("You clip the badge to your belt. Its familiar weight is reassuring.")
                logging.info("Badge taken and has_badge state set to True")
                return True

            if item.startswith("note_"):
                self.notes_found += 1
                game_state["score"] = game_state.get("score", 0) + 5
                print_text(f"You've found clue {self.notes_found}.")
                if self.notes_found == 5:
                    game_state["found_all_notes"] = True
                    game_state["score"] = game_state.get("score", 0) + 10
                    print_text("\nYou've collected all the scattered notes!")
                    self.show_compiled_notes()
                return True

            if item in self._SCORED_ITEMS:
                game_state["score"] = game_state.get("score", 0) + 10

            if item == "informant_note":
                print_text(
                    "You take the note. Something in the handwriting stops you — "
                    "it was written in a hurry by someone who knew the risk. "
                    "Read it carefully."
                )
                return True

            if item == "bulletin_notice":
                print_text(
                    "You pull the notice from the board. Whatever's on it, "
                    "someone went to the trouble of posting it where you'd find it. "
                    "Examine it when you get a moment."
                )
                return True

            if item == "membership_register":
                print_text(
                    "You tear out the 1946 roster page and fold it into your pocket. "
                    "The night porter is going to have questions in the morning. "
                    "You'll be somewhere else by then."
                )
                return True

            if item == "meeting_minutes":
                print_text(
                    "You take the folder. It's heavy — months of meetings, agreements, "
                    "money moving between names that shouldn't be in the same room. "
                    "Examine it when you're ready to see exactly what Voss signed."
                )
                return True

            if item == "manifest":
                print_text(
                    "You pull the manifest from the board. Someone will notice it's "
                    "missing when they come to cover their tracks. "
                    "You intend to be finished before that happens."
                )
                return True

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
                    elif item == "informant_note" and not game_state.get("found_emergency_frequency", False):
                        game_state["found_emergency_frequency"] = True
                        game_state["score"] = game_state.get("score", 0) + 10
                        print_text("\nYou have the emergency frequency. They'll be broadcasting tonight.")
                    elif item == "bulletin_notice" and not game_state.get("identified_organization", False):
                        game_state["identified_organization"] = True
                        game_state["score"] = game_state.get("score", 0) + 10
                        print_text("\nNorthwest Maritime Imports — that's the front. You have your organization.")
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
            def _award(flag: str, pts: int):
                def _inner():
                    if not game_state.get(flag, False):
                        game_state[flag] = True
                        game_state["score"] = game_state.get("score", 0) + pts
                return _inner

            special_effects = {
                ("binoculars", "observation_deck"): _award("surveilled_docks", 10),
                ("binoculars", "waterfront"): _award("surveilled_docks", 10),
                ("flashlight", "underground_tunnels"): lambda: game_state.update({"flashlight_lit": True, "dark_turns": 0}),
                ("badge", "anchor_tavern"): _award("ches_tip", 15),
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
           
                if isinstance(result['removes_items'], (list, tuple)):
                    for item in result['removes_items']:
                        if item in self.inventory:
                            self.inventory.remove(item)
           
                game_state[result['result']] = True
                game_state["score"] = game_state.get("score", 0) + 15
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

    def show_inventory(self, game_state: Optional[Dict] = None) -> None:
        """Display the current inventory contents with basic descriptions."""
        try:
            if not self.inventory:
                print_text("Your inventory is empty.")
            else:
                print_text("\nInventory:")
                for item in self.inventory:
                    basic_desc = ITEM_DESCRIPTIONS.get(item, {}).get("basic", "No description available.")
                    print_text(f"- {item}: {basic_desc}")
                print_text("\nTip: Use 'examine <item>' for a closer look.")

            if game_state is not None:
                score = game_state.get("score", 0)
                print_text(f"\nCase progress: {score} points.")

        except Exception as e:
            logging.error(f"Error showing inventory: {e}")
            print_text("There was a problem displaying the inventory.")

    def show_compiled_notes(self) -> None:
        """Display the complete compiled notes once all are collected."""
        print_text(
            "\nFive pieces of paper. You spread them out on the desk and look at them "
            "the way you'd look at a map of a city you've never been to — trying to "
            "find the through road.\n\n"
            "Note one: Badge 447. Walt Mathers. We came up together in '39. "
            "Tuesdays and Fridays, after midnight. Three trucks, waved through. "
            "I didn't want it to be him. It's him.\n\n"
            "Note two: The cargo. Morphine sulfate. Penicillin. Whole blood plasma. "
            "Army medical supplies that were supposed to be destroyed under the '46 "
            "demobilization orders. Not destroyed. Redirected. Someone had the "
            "contracts to do the redirecting, and someone was paid to look away.\n\n"
            "Note three: The hub. Warehouse 22. Everything moves through there. "
            "Don't go alone, the writer warned. You filed that under noted and went anyway.\n\n"
            "Note four: Project Emerald. The Harbormaster — no name, no face. "
            "Operations continuing through Q4. Whatever Q4 was supposed to mean, "
            "it means right now.\n\n"
            "Note five: Northwest Maritime Imports. Sullivan. "
            "The password is 'angels.'\n\n"
            "You close your notebook. The picture isn't pretty — "
            "stolen medical supplies meant for veterans' hospitals, "
            "a friend from the academy who looked the other way, "
            "a Harbormaster with no face yet, "
            "and a shell company that exists only to move things that shouldn't be moved. "
            "But it's finally a picture. "
            "Diamond doesn't go to court with less."
        )

    def drop_item(self, item: str) -> bool:
        """Remove an item from inventory (caller adds it to the location)."""
        try:
            if item not in self.inventory:
                print_text(f"You're not carrying a {item}.")
                return False
            self.inventory.remove(item)
            print_text(f"You set down the {item}.")
            return True
        except Exception as e:
            logging.error(f"Error dropping item {item}: {e}")
            print_text("There was a problem dropping the item.")
            return False

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
            "discovered_combinations": [sorted(combo) for combo in self.discovered_combinations],
            "removed_items": list(self.removed_items)
        }

    def restore_inventory_state(self, state: Dict[str, any]) -> None:
        """Restore inventory from saved state."""
        self.inventory = state.get("inventory", []).copy()
        self.notes_found = state.get("notes_found", 0)
        self.discovered_combinations = {
            frozenset(combo) for combo in state.get("discovered_combinations", [])
        }
        self.removed_items = set(state.get("removed_items", []))