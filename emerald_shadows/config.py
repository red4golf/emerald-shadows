# config.py

from pathlib import Path
from typing import Dict, Any

# File System Settings
SAVE_DIR = Path("saves")
LOG_FILE = "emerald_shadows.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Game Settings
AUTO_SAVE_INTERVAL = 300  # seconds (5 minutes)
MAX_SAVE_FILES = 5
MAX_AUTO_SAVES = 3
MAX_SAVE_DIR_SIZE_MB = 50.0

# Display Settings
TEXT_DELAY = 0.03  # seconds between characters for slow text
MIN_TERMINAL_WIDTH = 40
MAX_TERMINAL_WIDTH = 120
DEFAULT_TERMINAL_WIDTH = 80
DEFAULT_TERMINAL_HEIGHT = 24

# Game State Constants
REQUIRED_ITEMS = {
    "torn_letter",
    "dock_schedule",
    "wallet",
    "smuggling_plans",
    "coded_message"
}

REQUIRED_STATES = {
    "spoke_to_witness",
    "discovered_clue",
    "solved_cipher",
    "solved_radio_puzzle",
    "found_secret_room",
    "tracked_car",
    "evidence_connection",
    "decoded_message",
    "mapped_route"
}

# Command Settings
BASIC_COMMANDS = {
    'quit', 'help', 'look', 'inventory', 'talk',
    'history', 'solve', 'save', 'load', 'saves'
}

COMPLEX_COMMANDS = {
    'take', 'go', 'examine', 'use', 'combine'
}

# Initial Game State
INITIAL_GAME_STATE: Dict[str, Any] = {
    "cipher_attempts": 3,
    "inventory": [],
    "current_location": 'start',
    "morse_attempts": 0,
    "car_tracking_attempts": 0,
    "has_badge": False,
    "has_badge_shown": False,
    "found_wallet": False,
    "spoke_to_witness": False,
    "discovered_clue": False,
    "solved_cipher": False,
    "found_secret_room": False,
    "tracked_car": False,
    "solved_radio_puzzle": False,
    "completed_smith_tower": False,
    "found_all_newspaper_pieces": False,
    "warehouse_unlocked": False,
    "understood_radio": False,
    "observed_suspicious_activity": False,
    "case_insights": False,
    "evidence_connection": False,
    "decoded_message": False,
    "radio_frequency": False,
    "mapped_route": False
}

# Game Messages
GAME_MESSAGES = {
    "NO_PUZZLE": "There are no puzzles to solve here.",
    "NO_PUZZLES_AVAILABLE": "No puzzles are available here right now.",
    "ALREADY_SOLVED": "You've already solved the puzzle here.",
    "PUZZLE_ERROR": "Something went wrong with the puzzle. Try again later.",
    "NO_HANDLER": "No handler found for puzzle:",
    "MISSING_ITEMS": "You need {items} to solve this puzzle."
}

# Locations
LOCATIONS = {
    "police_station": {
        "description": "You're in the Seattle Police Department headquarters, housed in the Public Safety Building on 4th Avenue. Built in 1909, this fortress-like building has seen its share of cases. The wooden walls are lined with wanted posters, and the smell of coffee fills the air. Your desk is covered with case files.",
        "exits": {"outside": "pike_place", "office": "captain_office", "basement": "evidence_room"},
        "items": ["badge", "case_file", "coffee"],
        "first_visit": True,
        "historical_note": "The Seattle Police Department played a crucial role during WWII, coordinating with the Coast Guard to protect the vital shipyards."
    },
    "pike_place": {
        "description": "The bustling Pike Place Market stretches before you. Even in the post-war era, it's a hive of activity. Fishmongers call out their daily catches, and the aroma of fresh produce fills the air. The historic clock reads 10:45.",
        "exits": {"north": "police_station", "south": "pioneer_square", "east": "trolley_stop", "west": "waterfront"},
        "items": ["newspaper_piece_1", "apple"],
        "first_visit": True,
        "historical_note": "Pike Place Market, opened in 1907, served as a crucial connection between local farmers and urban customers during the war years."
    },
    "smith_tower": {
        "description": "The famous Smith Tower rises above you, its white terra cotta gleaming. Once the tallest building west of the Mississippi, it still commands respect. The elegant lobby features intricate bronze and marble work.",
        "exits": {"west": "pioneer_square", "elevator": "observation_deck"},
        "items": ["building_directory"],
        "first_visit": True,
        "historical_note": "Completed in 1914, the Smith Tower remained the tallest building on the West Coast until the Space Needle was built in 1962.",
        "requires": "has_badge"
    }
}

# Item Descriptions
ITEM_DESCRIPTIONS = {
    "badge": {
        "basic": "Your detective's badge, recently polished. Number 738.",
        "detailed": "A Seattle Police Department detective's badge, its silver surface showing slight wear. The design dates from the 1930s reform era, featuring the city seal and your number: 738. It carries the weight of responsibility and authority in post-war Seattle.",
        "use_locations": ["smith_tower", "warehouse_district", "suspicious_warehouse"],
        "use_effects": {"smith_tower": "The security guard examines your badge and nods respectfully, granting you access."}
    },
    "radio_manual": {
        "basic": "A technical manual for police radio equipment.",
        "detailed": "A well-worn technical manual dated 1945. Pages of frequency tables and operation codes, some marked with recent pencil annotations. The cover bears the seal of the War Department.",
        "use_locations": ["police_station", "warehouse_office"],
        "use_effects": {"warehouse_office": "You reference the manual's frequency tables while examining the radio equipment."}
    }
}

# Trolley Routes
TROLLEY_ROUTES = {
    0: {"description": "Downtown Stop", "exits": {"off": "pike_place"}},
    1: {"description": "Pioneer Square Stop", "exits": {"off": "pioneer_square"}},
    2: {"description": "Waterfront Stop", "exits": {"off": "waterfront"}},
    3: {"description": "Smith Tower Stop", "exits": {"off": "smith_tower"}}
}

# Puzzle Solutions
PUZZLE_SOLUTIONS = {
    "radio_puzzle": {
        "frequency": "147.85",
        "success_message": "The radio crackles to life, revealing a conversation about tonight's shipment.",
        "fail_message": "You hear only static on this frequency."
    },
    "cipher_puzzle": {
        "key": "EMERALD",
        "success_message": "The message becomes clear as you align the correct letters.",
        "fail_message": "The text remains encrypted. This isn't the right key."
    },
    "morse_code": {
        "message": ".-- .- .-. . .... --- ..- ... . / ..--- ..---",  # "WAREHOUSE 22"
        "success_message": "You successfully decode the tapping: 'WAREHOUSE 22'",
        "fail_message": "The tapping pattern eludes your understanding."
    }
}

# Version Information
GAME_VERSION = "1.0.0"
SAVE_FILE_VERSION = "1.0.0"