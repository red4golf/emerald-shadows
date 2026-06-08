# Location configurations for Emerald Shadows
LOCATIONS = {
    "police_station": {
        "description": (
            "The bullpen never really sleeps. Typewriters clatter on the night shift, "
            "somebody's percolator is burning the bottom of the pot, and the fluorescent "
            "light above your desk flickers like it can't make up its mind. Your name is "
            "on the door: J. DIAMOND, DETECTIVE. The files on your desk are neat. Everything "
            "else about this case is not. Through the window, the top of Smith Tower catches "
            "the last of the evening light."
        ),
        "exits": {"outside": "street", "upstairs": "evidence_room"},
        "items": ["badge", "case_file"],
        "first_visit": True,
        "historical_note": (
            "Seattle's police headquarters on Third Avenue has seen its share of scandal. "
            "The department's reputation took a beating during Prohibition and never fully "
            "recovered. Half the city knows which sergeant you pay to look the other way "
            "at the docks."
        )
    },
    "evidence_room": {
        "description": (
            "The evidence room smells of old paper, gun oil, and bad decisions. Steel shelves "
            "run floor to ceiling, each item tagged and catalogued by someone who believed "
            "in order. A work table in the center is scarred from years of use. Whatever "
            "went missing in '46 left gaps on those shelves that nobody talks about. You "
            "notice the gaps immediately."
        ),
        "exits": {"downstairs": "police_station"},
        "items": ["cipher_wheel", "radio_manual", "photo"],
        "first_visit": True,
        "historical_note": (
            "Three evidence packages disappeared from this room in the spring of 1946. "
            "The official report called it a clerical error. The unofficial version involves "
            "two officers who transferred to Tacoma shortly afterward and a captain who "
            "bought a boat."
        )
    },
    "street": {
        "description": (
            "Second Avenue at night. The rain comes down the way it always does in October "
            "in Seattle — not hard, just permanent, like it intends to stay. Neon from the "
            "taverns bleeds across the wet pavement. Steam rises from the manhole covers "
            "at your feet, carrying the smell of the city's underside. Somewhere downhill, "
            "beyond the rooftops, Elliott Bay is black and cold."
        ),
        "exits": {
            "station": "police_station",
            "north": "smith_tower",
            "east": "warehouse_district",
            "south": "docks",
            "west": "eagles_hall"
        },
        "items": ["newspaper"],
        "first_visit": True,
        "historical_note": (
            "Before the Great Fire of 1889, this block sat twenty feet lower. The city "
            "rebuilt upward, burying its mistakes below street level. In Seattle, the past "
            "is not behind you. It is underneath you."
        )
    },
    "smith_tower": {
        "description": (
            "Forty-two stories of white terracotta and ambition, the Smith Tower still "
            "commands the Seattle skyline in 1947 — the tallest building west of the "
            "Mississippi, and don't let anyone tell you different. The lobby is all "
            "Italian marble and brass elevator gates. The operator is a Pacific war vet "
            "named Harold who sees everything and says nothing. He tips his hat. "
            "You tip yours back. Through the revolving door, the Waterfront Electric "
            "tram stop at Second and Yesler is visible across the street."
        ),
        "exits": {"outside": "street", "elevator": "observation_deck", "trolley": "trolley"},
        "items": ["note_1"],
        "first_visit": True,
        "historical_note": (
            "L.C. Smith built this tower in 1914 to prove Seattle had arrived. On the "
            "35th floor sits the Chinese Room, given to the city by the Empress of China "
            "herself, with a wishing well at its center. During the war, sailors climbed "
            "all the way up here to make wishes. Most of those wishes didn't come back "
            "with them."
        )
    },
    "observation_deck": {
        "description": (
            "The wind off Puget Sound cuts through your coat up here. Below, the city "
            "spreads out like a map someone drew while drinking — the steep hills, the "
            "dark grid of the warehouse district, the black ribbon of Elliott Bay. To "
            "the west, the Olympic Mountains are a dark wall against the sky. You can "
            "see the waterfront clearly from here, and one of the ships at anchor is "
            "running no lights. That is worth remembering."
        ),
        "exits": {"down": "smith_tower"},
        "items": ["binoculars", "note_2"],
        "first_visit": True,
        "historical_note": (
            "During the war, civilian volunteers stood watch up here around the clock, "
            "scanning the horizon for Japanese aircraft that never came. They had "
            "binoculars, notepads, and thermos bottles full of bad coffee. "
            "The binoculars are still here."
        )
    },
    "warehouse_district": {
        "description": (
            "The warehouse district stretches east from the waterfront in long identical "
            "rows, built fast and cheap during the war years to handle military cargo. "
            "Most are dark now, padlocked, the government stencils on their sides fading "
            "in the salt air. But not all of them. A few windows show light where light "
            "has no business being at this hour. Somewhere a chain-link gate creaks "
            "on its hinges."
        ),
        "exits": {
            "west": "street",
            "south": "docks",
            "enter": "warehouse_three"
        },
        "items": ["note_3"],
        "first_visit": True,
        "historical_note": (
            "The Port of Seattle handled more tonnage during 1942 to 1945 than in the "
            "previous two decades combined. When the contracts dried up after V-J Day, "
            "half these buildings went dark overnight. Empty warehouses, in Diamond's "
            "experience, are never actually empty."
        )
    },
    "warehouse_three": {
        "description": (
            "The interior of Warehouse Three smells of machine oil and something else — "
            "something chemical and faintly sweet that doesn't belong with maritime cargo. "
            "Bare bulbs on a wire overhead push back just enough of the dark to see by. "
            "The crates are stacked in rows too neat for legitimate dock work. Someone "
            "is running an orderly operation here. A small office is partitioned off "
            "in the corner. A military-surplus flashlight sits on a crate near the door, "
            "left by whoever came through here last."
        ),
        "exits": {
            "outside": "warehouse_district",
            "office": "warehouse_office"
        },
        "items": ["note_4", "flashlight"],
        "first_visit": True,
        "historical_note": (
            "Built in 1943 to store Army medical supplies bound for the Pacific theater. "
            "The army surplus disposal contracts after the war were awarded without "
            "competitive bidding. Several of those contracts went to a company that "
            "didn't exist six months earlier."
        )
    },
    "warehouse_office": {
        "description": (
            "The office is small enough that two men would be uncomfortable in it. "
            "A metal desk, a swivel chair with a cracked leather seat, filing cabinets "
            "that somebody locked in a hurry — you can see where the drawer was forced. "
            "In the corner, a military surplus radio transceiver sits on a crate, "
            "its dials hand-labeled in grease pencil. Someone has been using this "
            "equipment recently. The ashtray is full."
        ),
        "exits": {"door": "warehouse_three"},
        "items": ["notebook", "note_5"],
        "first_visit": True,
        "historical_note": (
            "The office was thrown up in 1946 when the new tenants took the lease. "
            "The building inspector who signed off on it retired to Bainbridge Island "
            "three months later. Nice place out there, people say. "
            "Waterfront property."
        )
    },
    "docks": {
        "description": (
            "The working docks of Elliott Bay stretch in both directions, timber pilings "
            "black with creosote, the water below them the color of old iron. A Norwegian "
            "freighter rides at the far berth, unloading something that isn't listed on "
            "the manifest posted at the harbormaster's shack. The longshoremen on the "
            "night crew keep their eyes down and their mouths shut. That's a learned "
            "behavior. At the end of the pier, the Waterfront Electric tram stop sits "
            "under a bare bulb, rain ticking against the iron roof."
        ),
        "exits": {
            "north": "street",
            "east": "warehouse_district",
            "underground": "underground_tunnels",
            "trolley": "trolley",
            "shack": "harbormaster_shack"
        },
        "items": [],
        "first_visit": True,
        "historical_note": (
            "Seattle's docks have handled gold rush freight, wartime munitions, and "
            "everything in between. The International Longshoremen's and Warehousemen's "
            "Union has had a stranglehold on waterfront labor since the 1934 strike. "
            "The men who work these docks know every crate that moves — and know "
            "better than to talk about it."
        )
    },
    "underground_tunnels": {
        "description": (
            "It is pitch dark. You are likely to be eaten by a grue.\n\n"
            "That is, if grues have made it to Seattle — and given what you have already "
            "found in this city, you would not rule it out. The brick tunnels beneath "
            "Pioneer Square are close, cold, and absolutely lightless. Water seeps "
            "through the mortar. The air smells of tide and old timber and decades of "
            "secrets. Somewhere in the dark ahead, something drips with terrible "
            "patience. You brought a flashlight. Use it."
        ),
        "exits": {
            "up": "docks"
        },
        "items": [],
        "first_visit": True,
        "dark": True,
        "requires": "found_warehouse",
        "historical_note": (
            "After the Great Fire of 1889, the city regraded its streets two stories "
            "higher, leaving the original ground floor of every building entombed below. "
            "For a while, people still used the underground storefronts. Then the rats "
            "moved in and the people moved out. Rumrunners rediscovered these tunnels "
            "in the twenties. The current tenants are worse."
        )
    },
    "trolley": {
        "description": (
            "You are aboard the Waterfront Electric, one of three private tram lines "
            "still running along Seattle's waterfront in 1947 — the public streetcar "
            "system folded in '41, but the dock companies kept their own rolling stock "
            "for moving workers between the piers. The wooden seats are worn smooth "
            "by ten thousand longshoremen. Brass fittings, salt air, the smell of "
            "motor grease and rain. The motorman doesn't look at you. Nobody on "
            "these cars looks at anybody."
        ),
        "exits": {
            "next": "trolley",
            "off": "pike_place"
        },
        "items": [],
        "first_visit": True,
        "historical_note": (
            "Seattle's public streetcar system — once one of the finest in the Pacific "
            "Northwest — ran its last car down the Madison Street line in April of 1941. "
            "The city sold the rails for scrap to feed the war effort. What remains now "
            "are a handful of private industrial lines the port companies own outright. "
            "They will be gone within the decade."
        )
    },
    "pike_place": {
        "description": (
            "Pike Place Market clings to the hillside above Elliott Bay like it's "
            "afraid to let go — which, right now, it is. The developers want it "
            "flattened for a parking garage. The fishmongers and flower sellers and "
            "farmers who've worked these stalls since 1907 are fighting back, but "
            "nobody's taking bets on who wins. Even at this hour, a few stalls are "
            "still lit. A man in a grey coat stands near the flower stalls with his "
            "hands in his pockets, watching the water. He has been there a while."
        ),
        "exits": {
            "east": "street",
            "trolley": "trolley"
        },
        "items": ["informant_note"],
        "first_visit": True,
        "historical_note": (
            "Pike Place Market opened August 17, 1907, after city council member Thomas "
            "Revelle stood on a street corner and shouted for farmers to bring their "
            "wagons directly to the public. Ten thousand people showed up the first day. "
            "The market has survived the Depression, the war, and every developer who's "
            "tried to kill it. So far."
        )
    },
    "anchor_tavern": {
        "description": (
            "The Anchor has been serving longshoremen since before the first war — low "
            "ceiling, oil lamps, the smell of beer and salt air soaked so deep into the "
            "wood it will never come out. The clientele are men who work for a living and "
            "don't talk about it. A booth in the back holds two of them, shoulders turned "
            "inward, conversation stopped the moment you pushed through the door. Behind "
            "the bar, a man with two fingers missing on his left hand wipes down a glass "
            "that was already clean. He watches you the way a man watches weather — not "
            "afraid of it, just reading it. Use your badge if you want him to read you right."
        ),
        "exits": {
            "outside": "waterfront"
        },
        "items": [],
        "first_visit": True,
        "historical_note": (
            "Seattle's waterfront taverns in 1947 occupied a particular niche in the "
            "city's social geography — neither respectable enough for city hall, nor rough "
            "enough for the vice squad. They were the natural habitat of men who moved "
            "things between ships and warehouses and preferred not to discuss the details "
            "over anything stronger than beer. Three of the seven waterfront taverns "
            "operating that year were used as informal labor exchanges. No questions asked "
            "on either side."
        )
    },
    "pioneer_square": {
        "description": (
            "Pioneer Square: Seattle's first neighborhood, rebuilt in brick after the "
            "Great Fire, and somehow both grander and seedier for it. The iron pergola "
            "at the center of the plaza once sheltered passengers waiting for the "
            "underground streetcar terminal beneath it. Now it shelters pigeons and "
            "men who have nowhere else to be. This is where Yesler's mill sat in 1852, "
            "where logs were skidded down to the waterfront on what they called "
            "the Skid Road. The expression survived the road. A bulletin board near "
            "the saloon door has something pinned to it."
        ),
        "exits": {
            "north": "street",
            "trolley": "trolley"
        },
        "items": ["bulletin_notice"],
        "first_visit": True,
        "historical_note": (
            "The totem pole at the center of Pioneer Square was stolen from a Tlingit "
            "village at Fort Tongass, Alaska, in 1899 by a group of prominent Seattle "
            "businessmen on a sightseeing cruise. When the original pole burned in 1938, "
            "the city wrote to the Tlingit nation to ask for a replacement. The tribe "
            "sent a bill for the first one."
        )
    },
    "eagles_hall": {
        "description": (
            "The Fraternal Order of Eagles hall at Seventh and Union occupies a building "
            "that can't decide if it's a civic institution or a gentleman's club — so it's "
            "settled on being both. Dark wood paneling, portrait photographs of past officers "
            "in gilded frames, a trophy case with a loving cup and a ceremonial gavel behind "
            "glass. The hall smells of wood polish, cigar smoke, and the accumulated "
            "self-regard of forty years of civic leadership. A leather-bound membership "
            "register sits open on a lectern near the door. A corridor at the back leads "
            "to a private lounge that doesn't appear in the public directory."
        ),
        "exits": {
            "east": "street",
            "back": "eagles_lounge"
        },
        "items": ["membership_register"],
        "first_visit": True,
        "historical_note": (
            "The Fraternal Order of Eagles was founded in Seattle in 1898 by six theater "
            "owners who wanted a civic organization that working men — not just the wealthy "
            "— could join. By 1947 it had grown into one of the most politically connected "
            "fraternal organizations in the country, lobbying successfully for the five-day "
            "work week and Social Security. In a city where the port authority, the police "
            "department, and organized labor all drank from the same well, the Eagles "
            "provided the cup."
        )
    },
    "eagles_lounge": {
        "description": (
            "The back room of the Eagles hall — private, paneled in darker wood than the "
            "main room, with leather armchairs that cost more than a beat cop's monthly "
            "salary. A roll-top desk sits against the far wall, its surface unusually clear "
            "for a room that sees this much use. A thick folder of documents sits on the "
            "side table, the Eagles crest embossed on the cover. The ashtray holds three "
            "cold stubs — someone was here recently, in conference, for a long time. "
            "The folder is labeled COMMITTEE MINUTES — NOT FOR GENERAL CIRCULATION."
        ),
        "exits": {
            "hall": "eagles_hall"
        },
        "items": ["meeting_minutes"],
        "first_visit": True,
        "historical_note": (
            "Civic organizations in mid-century American cities operated on a principle "
            "best described as selective transparency — their public activities were highly "
            "visible; their private deliberations were conducted in rooms exactly like this "
            "one. The minutes of those private sessions, when they have survived, have "
            "occasionally told historians things the participants would have preferred "
            "to keep among themselves."
        )
    },
    "harbormaster_shack": {
        "description": (
            "The harbormaster's shack at the end of Pier Three is barely large enough to "
            "turn around in — tar-papered walls, a single window facing the water, a plank "
            "desk with a logbook chained to it. A corkboard covers most of one wall: "
            "manifests, schedules, tide tables, cargo declarations, all pinned in overlapping "
            "layers going back three years. Everything in here is official, documented, filed "
            "in triplicate. Which means that whatever isn't in here is being moved very "
            "carefully indeed. One of the manifests near the center of the board is for "
            "Pier 7. Its declared weight doesn't match its declared cargo — and someone "
            "with a pen and authority signed off on that discrepancy."
        ),
        "exits": {
            "outside": "docks"
        },
        "items": ["manifest"],
        "first_visit": True,
        "historical_note": (
            "The Port of Seattle's cargo documentation in 1947 was a paper-based operation "
            "run by men who learned their trade before the war and adapted minimally since. "
            "Customs declarations, bills of lading, cargo manifests — typed on standard "
            "forms, filed in triplicate, copies going to the port authority, the customs "
            "house, and the shipping company. A system with that many copies should have "
            "been impossible to corrupt. In postwar Seattle, the word 'impossible' was "
            "doing a lot of work it wasn't qualified to do."
        )
    },
    "waterfront": {
        "description": (
            "The waterfront at the foot of the hills. Elliott Bay runs black to the "
            "west, and across the water the Olympic Peninsula is a dark mass against "
            "the clouds. On a clear night you can see the mountains. Tonight is not "
            "a clear night. The Kalakala — the silver streamlined ferry they call the "
            "Flying Clam — sits at her berth further up the dock, waiting for the "
            "morning run to Bremerton. Anchored out in the roads, well away from the "
            "pier lights, a cargo vessel rides the swell with no running lights and "
            "no name visible on her hull."
        ),
        "exits": {
            "east": "docks",
            "trolley": "trolley",
            "tavern": "anchor_tavern"
        },
        "items": [],
        "first_visit": True,
        "historical_note": (
            "Puget Sound ferries have connected Seattle to the Kitsap Peninsula since "
            "the Mosquito Fleet of the 1880s. The Kalakala, launched in 1935, became "
            "the most photographed vessel in the Pacific Northwest — a streamlined, "
            "art deco marvel that looks like it belongs in the future. She carries "
            "commuters, workers from the Bremerton naval shipyard, and, if the rumors "
            "are right, the occasional shipment that doesn't appear on any manifest."
        )
    }
}
