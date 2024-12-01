# config.py - Continued

# Trolley Routes
TROLLEY_ROUTES = {
    0: {"description": "Downtown Stop", "exits": {"off": "pike_place"}},
    1: {"description": "Pioneer Square Stop", "exits": {"off": "pioneer_square"}},
    2: {"description": "Waterfront Stop", "exits": {"off": "waterfront"}},
    3: {"description": "Smith Tower Stop", "exits": {"off": "smith_tower"}}
}

# Additional Locations
LOCATIONS.update({
    "smith_tower": {
        "description": "The famous Smith Tower rises above you, its white terra cotta gleaming. Once the tallest building west of the Mississippi, it still commands respect. The elegant lobby features intricate bronze and marble work.",
        "exits": {"west": "pioneer_square", "elevator": "observation_deck"},
        "items": ["building_directory"],
        "first_visit": True,
        "historical_note": "Completed in 1914, the Smith Tower remained the tallest building on the West Coast until the Space Needle was built in 1962.",
        "requires": "has_badge"
    },
    "underground_tunnels": {
        "description": "The infamous Seattle Underground stretches before you. Brick-lined passages and remnants of old storefronts tell the story of the city's resurrection after the Great Fire. The air is cool and damp.",
        "exits": {"up": "pioneer_square", "north": "secret_warehouse"},
        "items": ["newspaper_piece_4", "old_key"],
        "first_visit": True,
        "historical_note": "These tunnels were created when Seattle raised its streets one to two stories after the Great Fire of 1889."
    },
    "warehouse_district": {
        "description": "Rows of industrial warehouses line the street. The smell of salt water mingles with diesel fuel. Workers move cargo between buildings and the nearby docks.",
        "exits": {"south": "waterfront", "north": "suspicious_warehouse"},
        "items": ["newspaper_piece_5", "shipping_manifest"],
        "first_visit": True,
        "historical_note": "The warehouse district expanded rapidly during WWII to handle increased military shipping."
    }
})

# Additional Items
ITEM_DESCRIPTIONS.update({
    "radio_manual": {
        "basic": "A technical manual for police radio equipment.",
        "detailed": "A well-worn technical manual dated 1945. Pages of frequency tables and operation codes, some marked with recent pencil annotations. The cover bears the seal of the War Department.",
        "use_locations": ["police_station", "warehouse_office"],
        "use_effects": {"warehouse_office": "You reference the manual's frequency tables while examining the radio equipment."}
    },
    "cipher_wheel": {
        "basic": "A brass cipher wheel with rotating disks.",
        "detailed": "A sophisticated decoding device with multiple brass disks that rotate to align different letters and numbers. The craftsmanship suggests military origin.",
        "use_locations": ["evidence_room", "warehouse_office"],
        "use_effects": {"evidence_room": "You begin working on decoding the message using the cipher wheel."}
    }
})

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