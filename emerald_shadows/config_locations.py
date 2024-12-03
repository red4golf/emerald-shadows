# Location configurations for Emerald Shadows
LOCATIONS = {
    "police_station": {
        "description": "The police station buzzes with activity even at this late hour. Your desk sits in the corner of the detective's bullpen, files neatly arranged. The window offers a view of Smith Tower in the distance.",
        "exits": {"outside": "street", "upstairs": "evidence_room"},
        "items": ["badge", "case_file"],
        "first_visit": True,
        "historical_note": "Seattle's central police station has stood here since the early 1900s, watching over the growing city."
    },
    "evidence_room": {
        "description": "Metal shelves line the walls of the evidence room, filled with tagged items and files. A work table in the center provides space for examining materials.",
        "exits": {"downstairs": "police_station"},
        "items": ["cipher_wheel", "radio_manual"],
        "first_visit": True,
        "historical_note": "The evidence room's organization system was modernized after several items went missing in 1946."
    },
    "street": {
        "description": "The rain-slicked streets reflect the neon signs of nearby establishments. Steam rises from manhole covers, and the distant sound of the harbor carries through the night air.",
        "exits": {
            "station": "police_station",
            "north": "smith_tower",
            "east": "warehouse_district",
            "south": "docks"
        },
        "items": ["newspaper"],
        "first_visit": True,
        "historical_note": "These streets have seen Seattle transform from a frontier town to a modern city."
    },
    "smith_tower": {
        "description": "At 42 stories, the Smith Tower remains Seattle's tallest building. The ornate lobby features bronze fittings and marble floors. The elevator operator tips his hat as you enter.",
        "exits": {"outside": "street", "elevator": "observation_deck"},
        "items": ["note_1"],
        "first_visit": True,
        "historical_note": "Completed in 1914, the Smith Tower has a hidden Chinese Room at the top, popular with sailors during WWII."
    },
    "observation_deck": {
        "description": "The observation deck offers a panoramic view of Seattle's harbor. Through binoculars, you can see the bustling waterfront below - trucks moving between warehouses, and the maze of streets that make up the heart of the city.",
        "exits": {"down": "smith_tower"},
        "items": ["binoculars", "note_2"],
        "first_visit": True,
        "historical_note": "The Smith Tower observation deck served as an aircraft spotting station during WWII."
    },
    "warehouse_district": {
        "description": "Rows of identical warehouses stretch into the darkness. The sound of distant machinery and the smell of the sea fill the air. Most buildings are dark, but a few show signs of activity.",
        "exits": {
            "west": "street",
            "south": "docks",
            "enter": "warehouse_three"
        },
        "items": ["note_3"],
        "first_visit": True,
        "historical_note": "The warehouse district expanded rapidly during the war years to handle increased shipping traffic."
    },
    "warehouse_three": {
        "description": "The interior of Warehouse Three is dimly lit by overhead lights. Crates and shipping containers are stacked in neat rows. A small office occupies one corner.",
        "exits": {
            "outside": "warehouse_district",
            "office": "warehouse_office"
        },
        "items": ["note_4"],
        "first_visit": True,
        "historical_note": "Built in 1943, Warehouse Three was originally used for military supplies."
    },
    "warehouse_office": {
        "description": "A cramped office with a desk covered in paperwork. Filing cabinets line one wall, and a radio set sits in the corner. The window overlooks the warehouse floor.",
        "exits": {"door": "warehouse_three"},
        "items": ["notebook", "note_5"],
        "first_visit": True,
        "historical_note": "The office was added during renovations in 1946."
    },
    "docks": {
        "description": "The docks stretch along the waterfront, various vessels moored in their berths. Cranes loom overhead, and the smell of salt water and diesel fuel mingles in the air.",
        "exits": {
            "north": "street",
            "east": "warehouse_district"
        },
        "items": [],
        "first_visit": True,
        "historical_note": "Seattle's docks have been crucial to the city's growth since its founding."
    }
}