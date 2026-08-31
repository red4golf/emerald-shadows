"""Dialogue content for Emerald Shadows.

Pure data. Topics are *global knowledge* — once Diamond learns that there's a
blue sedan worth asking about, he can raise it with anyone. Each person answers
only for the topics they actually have something on, which is what makes going
back around the city with a new question worth doing.

A topic entry may carry:
    text      - what they say
    unlocks   - topic keys this conversation opens up
    sets      - game_state flag set True
    score     - points awarded the first time
    fragment  - licence-plate fragment key (see puzzles.car_puzzle)
    gives     - item dropped into the player's current location
    requires  - game_state flag that must be True before they'll answer
    locked    - what they say when `requires` isn't met
    once      - True if the full answer only lands the first time
"""

from typing import Dict, List

# Topics Diamond can raise. `label` is what the casebook and topic lists show.
TOPICS: Dict[str, Dict] = {
    "case": {"label": "the case", "aliases": ["it", "the case", "everything"]},
    "supplies": {"label": "the missing medical supplies",
                 "aliases": ["medical supplies", "morphine", "penicillin", "cargo", "shipment"]},
    "harbormaster": {"label": "the Harbormaster", "aliases": ["the harbormaster"]},
    "sullivan": {"label": "Sullivan", "aliases": []},
    "voss": {"label": "Captain Voss", "aliases": ["harlan voss", "captain voss"]},
    "mathers": {"label": "Walt Mathers", "aliases": ["walt", "badge 447", "447"]},
    "sedan": {"label": "the blue sedan", "aliases": ["blue sedan", "the car", "car", "plate"]},
    "warehouse": {"label": "Warehouse 22", "aliases": ["warehouse 22", "w22"]},
    "angels": {"label": "the word 'angels'", "aliases": ["angels", "password"]},
    "eagles": {"label": "the Eagles hall", "aliases": ["eagles", "the eagles", "lodge"]},
    "frequency": {"label": "the radio frequency", "aliases": ["radio", "415.6", "frequency"]},
    "pier": {"label": "Pier 7", "aliases": ["pier 7", "pier seven", "the pier"]},
}

# What Diamond knows to ask about before anyone tells him anything.
STARTING_TOPICS: List[str] = ["case", "supplies"]


NPCS: Dict[str, Dict] = {
    # ------------------------------------------------------------------
    "ches": {
        "name": "Ches",
        "title": "the barman at the Anchor",
        "location": "anchor_tavern",
        "aliases": ["barman", "bartender"],
        "greeting": (
            "Ches is wiping a glass that was dry ten minutes ago. He does that when he's "
            "deciding about somebody. Behind you, the two men in the corner booth have "
            "stopped talking.\n\n"
            "'Detective,' he says, to the glass. 'You want something, or you want something.'"
        ),
        "deflection": (
            "Ches shakes his head slowly. 'Not my end of the bar. I hear what comes in "
            "the door and nothing that doesn't.'"
        ),
        "topics": {
            "case": {
                "text": (
                    "'Everybody's got a case.' He sets the glass down. 'Mine's that half "
                    "the longshoremen on this waterfront have been drinking on somebody "
                    "else's money since spring and none of them will say whose. You want "
                    "to ask me something, ask me something narrow.'"
                ),
                "unlocks": ["harbormaster"],
            },
            "supplies": {
                "text": (
                    "'Army morphine.' He says it flat, like a price. 'It comes off the "
                    "boats at night and it doesn't go to the veterans' hospital, which is "
                    "four miles that way and has men in it who came back from Leyte "
                    "without legs.'\n\n"
                    "He looks at the booth in the corner and lowers his voice.\n\n"
                    "'There's a ship sitting out in the roads three nights running. Not "
                    "docked. Waiting. That's not how honest cargo behaves.'"
                ),
                "unlocks": ["harbormaster", "pier"],
                "score": 10,
            },
            "harbormaster": {
                "text": (
                    "The wiping stops.\n\n"
                    "'That's a word I hear and don't repeat. Nobody's met him. Everybody's "
                    "been paid by him.' He glances past you. 'A man came through here in "
                    "June, drunk enough to be honest, and he said the Harbormaster wasn't "
                    "a man at all — it's whoever's holding the schedule that week.'\n\n"
                    "He shrugs. 'I think he was wrong. I think it's a man. I think his "
                    "name is Sullivan and I'd thank you to forget you got that here.'"
                ),
                "unlocks": ["sullivan"],
                "sets": "heard_harbormaster",
                "score": 15,
            },
            "sullivan": {
                "text": (
                    "'Comes in maybe twice a month. Sits where you're standing. Drinks "
                    "one thing, slowly, and pays in bills that have never been folded.'\n\n"
                    "Ches finally puts the glass on the shelf.\n\n"
                    "'He's not frightening in the way you'd want him to be. He's polite. "
                    "He asks after your family. That's worse.'"
                ),
                "unlocks": ["sedan"],
            },
            "sedan": {
                "text": (
                    "'The blue one.' He nods slowly. 'Parks up on Railroad where the light "
                    "doesn't reach. I've closed up and watched it sit there.'\n\n"
                    "He thinks about it properly, which not many people bother to do.\n\n"
                    "'Plate ended in a one. I remember because it didn't — the frame's bent "
                    "and it reads like a seven until you're close. One. I'd put money on it.'"
                ),
                "fragment": "ches",
                "score": 10,
            },
            "pier": {
                "text": (
                    "'Pier seven.' He says it like it tastes wrong. 'A launch went out from "
                    "there last night around three and came back light. Whatever it was "
                    "going for, it didn't get it yet.'"
                ),
                "sets": "knows_pier",
            },
            "mathers": {
                "text": (
                    "Ches looks at you for a long moment, and there's something close to "
                    "pity in it.\n\n"
                    "'Third District fella. Comes in Tuesdays.' A pause. 'Detective, he "
                    "drinks here on a patrolman's salary and he tips like a man who's "
                    "embarrassed about something. That's all I'll say and I've said it to "
                    "you and not to anybody.'"
                ),
            },
        },
    },
    # ------------------------------------------------------------------
    "harold": {
        "name": "Harold",
        "title": "the Smith Tower elevator operator",
        "location": "smith_tower",
        "aliases": ["operator", "elevator operator"],
        "greeting": (
            "Harold has the brass gate half-open and his cap squared. Pacific, you'd guess "
            "— he has the way of standing that men brought back from it.\n\n"
            "'Detective. Floor?' A beat. 'Or not a floor.'"
        ),
        "deflection": (
            "'Couldn't tell you.' Harold adjusts the gate. 'I see the building. That's the "
            "whole of my expertise.'"
        ),
        "topics": {
            "case": {
                "text": (
                    "'I run a box up and down a shaft forty-two floors, twelve hours a day. "
                    "You'd be amazed what rides in it.' He almost smiles. 'Ask me about "
                    "something that's been in my elevator.'"
                ),
            },
            "supplies": {
                "text": (
                    "'Crates came through the freight side in the spring. Stencilled US ARMY "
                    "and painted over, badly.' He shrugs. 'Freight's not my car. I mention "
                    "it because you asked and because I was in the Pacific and I know what "
                    "those crates are for.'"
                ),
                "score": 5,
            },
            "sedan": {
                "text": (
                    "'Blue sedan. Pulls up at the Yesler door, never the front.' Harold "
                    "looks out through the revolving door at the wet street, remembering "
                    "properly.\n\n"
                    "'Third figure on the plate was a seven. I'd swear to that in a "
                    "courtroom. The first two I never had the angle on, and the last one "
                    "the frame ate.'"
                ),
                "fragment": "harold",
                "score": 10,
            },
            "voss": {
                "text": (
                    "'Captain Voss. Port Authority.' Harold's face does nothing at all, "
                    "which is itself an answer. 'Rides up to thirty-five. Not an office up "
                    "there — the Chinese Room. Meets a man who doesn't sign the book.'\n\n"
                    "He closes the gate a careful inch.\n\n"
                    "'And he wears a pin. Little eagle, three chapters. I only mention it "
                    "because he takes it off in the elevator, every time, before the doors "
                    "open. A man doesn't do that by accident.'"
                ),
                "unlocks": ["eagles"],
                "sets": "voss_observed",
                "score": 15,
            },
            "eagles": {
                "text": (
                    "'Third Chapter, over on the west side.' Harold nods once. 'Respectable "
                    "enough. Half the department's in it. That's either a comfort or it "
                    "isn't, depending what you're asking me.'"
                ),
            },
            "harbormaster": {
                "text": (
                    "'Heard it. Twice, in my car, from men who stopped talking when they "
                    "remembered I was standing there.' Harold shrugs. 'People forget the "
                    "operator. I've built a whole life on it.'"
                ),
            },
        },
    },
    # ------------------------------------------------------------------
    "roy": {
        "name": "the motorman",
        "title": "on the waterfront line",
        "location": "trolley",
        "aliases": ["motorman", "driver", "conductor", "hendricks"],
        "greeting": (
            "The motorman has one hand on the controller and hasn't looked at you since "
            "you boarded. Grey at the temples, pension in sight, the particular stillness "
            "of a man who has decided something and is waiting for the nerve.\n\n"
            "'Ride's a nickel,' he says. 'Whatever else you want is more than that.'"
        ),
        "deflection": (
            "'I drive the car,' he says, watching the wire. 'I don't drive it anywhere "
            "interesting.'"
        ),
        "topics": {
            "case": {
                "text": (
                    "He works the controller a notch. The car groans down Yesler.\n\n"
                    "'I've been on this line nineteen years. You see the same faces at the "
                    "same hours and you learn the shape of a week.' He glances at you for "
                    "the first time. 'This spring the shape changed. That's all I've got "
                    "that's mine to give.'"
                ),
                "unlocks": ["supplies"],
            },
            "supplies": {
                "text": (
                    "'Trucks,' he says. 'Tuesdays and Fridays, after midnight, down "
                    "Railroad Avenue where my line runs empty. Three of them. Waved "
                    "through at the gate by a man in uniform who ought to be stopping "
                    "them.'\n\n"
                    "His jaw sets.\n\n"
                    "'My brother came back from Anzio and waited eleven weeks for morphine "
                    "that the Army said it had already destroyed. He waited in a bed in "
                    "Bremerton. So no, Detective, I'm not being brave. I'm being angry, "
                    "and it took me until now to tell the difference.'"
                ),
                "unlocks": ["mathers", "frequency"],
                "sets": "roy_talking",
                "score": 15,
            },
            "frequency": {
                "text": (
                    "He is quiet for a full block. Then he takes one hand off the "
                    "controller, digs in his coat, and holds out a folded scrap of paper "
                    "without looking at you.\n\n"
                    "'They talk on the radio. Nightly, two in the morning. I wrote it down "
                    "off a set in the barn where they park the trucks.'\n\n"
                    "The car sways. He puts the hand back on the controller.\n\n"
                    "'Don't use the telephone. Don't come and find me again. I've got "
                    "eight months to a pension and a wife who thinks I drive a streetcar.'"
                ),
                "gives": "informant_note",
                "sets": "roy_gave_note",
                "score": 20,
                "once": True,
            },
            "mathers": {
                "text": (
                    "'Didn't get a name. Got a badge number off his coat when he turned "
                    "under the light.' He says it carefully, the way you hand somebody "
                    "something breakable. 'Four four seven.'\n\n"
                    "He watches the wire.\n\n"
                    "'I'm told you people don't much like it when it's one of yours. "
                    "I'd rather find that out now than later.'"
                ),
                "sets": "knows_mathers",
                "unlocks": ["sedan"],
                "score": 15,
            },
            "harbormaster": {
                "text": (
                    "'That's a word off the piers, not off my line.' He shakes his head. "
                    "'Ask a man who drinks with longshoremen. I don't drink.'"
                ),
            },
            "sedan": {
                "text": (
                    "'Blue one follows the trucks down.' He shrugs. 'I'm forty feet up a "
                    "wire in the dark, Detective. I see shapes and headlights. You'll want "
                    "somebody who saw it standing still.'"
                ),
            },
        },
    },
    # ------------------------------------------------------------------
    "porter": {
        "name": "the night porter",
        "title": "at the Eagles hall",
        "location": "eagles_hall",
        "aliases": ["night porter", "caretaker"],
        "greeting": (
            "The porter is a grey man in a grey cardigan who has materialised from a side "
            "corridor without any of the floorboards mentioning it.\n\n"
            "'Members only after nine,' he says, entirely without hostility. He has already "
            "looked at where your badge would be if you were showing it."
        ),
        "deflection": (
            "'I couldn't say, sir.' The porter folds his hands. 'I lock up and I put the "
            "chairs straight.'"
        ),
        "requires": "has_badge",
        "locked": (
            "The porter looks at you the way a good porter looks at anybody: politely, and "
            "as though you have already left. 'Members only after nine, sir.'\n\n"
            "There's a shield in your coat pocket that would change this conversation."
        ),
        "topics": {
            "eagles": {
                "text": (
                    "'Third Chapter, eleven forty-four. Founded 1904.' He recites it the "
                    "way you'd recite a hymn you stopped believing years ago. 'Two hundred "
                    "and six members in good standing. Rather fewer in attendance.'\n\n"
                    "'The back room is spoken for on Thursdays. It has been spoken for on "
                    "Thursdays since the war ended, by gentlemen who do not sign the book.'"
                ),
                "unlocks": ["voss"],
                "score": 10,
            },
            "voss": {
                "text": (
                    "A very long pause. The porter looks at the corridor he came out of.\n\n"
                    "'Captain Voss is a member, sir. He chairs the Thursday room.' He "
                    "chooses the next words like a man stepping between mines. 'The "
                    "minutes of the Thursday room are kept, because the minutes of every "
                    "room are kept. That is the rule and I did not write it.'\n\n"
                    "He steps aside from the corridor. It is not quite an invitation and "
                    "it is not quite anything else.\n\n"
                    "'They are in the lounge. I have been asked not to see who reads them.'"
                ),
                "sets": "porter_relented",
                "score": 15,
            },
            "harbormaster": {
                "text": (
                    "'Not a term used in this building, sir.' The smallest hesitation. "
                    "'Not upstairs, at any rate.'"
                ),
            },
            "supplies": {
                "text": (
                    "'I wouldn't know what comes through the loading door, sir. It isn't "
                    "my door.' He almost sighs. 'It is, however, a very busy door for a "
                    "fraternal society.'"
                ),
            },
        },
    },
    # ------------------------------------------------------------------
    "mathers": {
        "name": "Mathers",
        "title": "Badge 447, Third District",
        "location": "police_station",
        "aliases": ["walt", "walt mathers", "badge 447"],
        "requires_act": 2,
        "greeting": (
            "Walt Mathers is sitting on the edge of your desk with his hat in his hands, "
            "which is not where he sits and not what he does with his hat.\n\n"
            "You came up together in '39. He was better than you at the written exam and "
            "worse than you at everything after it.\n\n"
            "'Johnny,' he says. 'You've been asking people about Tuesdays.'"
        ),
        "deflection": (
            "'Don't,' Mathers says quietly. 'Whatever that one is. Don't.'"
        ),
        "topics": {
            "mathers": {
                "text": (
                    "He turns the hat around once.\n\n"
                    "'It was waving trucks through a gate. That's all it ever was, the "
                    "first time — a man asks you to look at the water for ninety seconds "
                    "and hands you more than you make in a month.' He looks up. 'And then "
                    "it's not the first time, and there's no version of the second one "
                    "where you're a man who did it once.'\n\n"
                    "'My wife thinks the money's from her father. Her father's been dead "
                    "two years, Johnny. She just needs it to be from somewhere.'"
                ),
                "sets": "mathers_confessed",
                "unlocks": ["voss", "warehouse"],
                "score": 20,
            },
            "supplies": {
                "text": (
                    "'Morphine, plasma, penicillin. Crates that were supposed to go in a "
                    "furnace under the demobilisation order.' He says the inventory like a "
                    "man who has said it to himself at three in the morning. 'I know what "
                    "it was. I knew in April.'"
                ),
            },
            "warehouse": {
                "text": (
                    "'Twenty-two. Down past the grain terminal.' He rubs his face. 'It "
                    "goes in there and it comes out with a different bill of lading and "
                    "it's legal by the time it's on a boat. That's the whole trick. "
                    "There's no clever part.'"
                ),
                "sets": "mathers_named_warehouse",
                "score": 10,
            },
            "voss": {
                "text": (
                    "'Voss has the contracts and the uniform and the lodge, and none of "
                    "it touches him.' Bitterly: 'I'm the one who stood in the rain. He's "
                    "the one who signed. Guess which of us they'll hang it on.'"
                ),
                "unlocks": ["sullivan"],
            },
            "harbormaster": {
                "text": (
                    "'Never met him. Never wanted to.' Mathers stands up, finally. "
                    "'Sullivan runs the water. Voss runs the paper. I ran a gate. "
                    "That's the whole org chart and I'm the bottom of it.'"
                ),
                "unlocks": ["sullivan"],
            },
            "case": {
                "text": (
                    "'You're going to finish it,' he says. Not a question. 'I know you. "
                    "You'll file it complete and you'll put my number in it and you'll be "
                    "right to.'\n\n"
                    "He puts his hat on.\n\n"
                    "'Do me the one courtesy. Don't come to the house.'"
                ),
            },
        },
    },
}


def npc_at(location: str, act: int) -> List[str]:
    """Keys of the people available at a location in the current act."""
    return [
        key for key, npc in NPCS.items()
        if npc["location"] == location and act >= npc.get("requires_act", 1)
    ]


def resolve_npc(word: str) -> str:
    """Match player input to an NPC key by name or alias. Returns '' on no match."""
    word = (word or "").strip().lower()
    if not word:
        return ""
    if word in NPCS:
        return word
    for key, npc in NPCS.items():
        if word == npc["name"].lower() or word in npc.get("aliases", []):
            return key
        if word in npc["name"].lower().split():
            return key
    return ""


def resolve_topic(word: str) -> str:
    """Match player input to a topic key by name or alias. Returns '' on no match."""
    word = (word or "").strip().lower()
    if not word:
        return ""
    for prefix in ("the ", "a "):
        if word.startswith(prefix):
            word = word[len(prefix):]
    if word in TOPICS:
        return word
    for key, topic in TOPICS.items():
        if word == topic["label"].lower() or word in topic.get("aliases", []):
            return key
        if word in key:
            return key
    return ""
