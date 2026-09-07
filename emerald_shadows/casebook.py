"""The casebook — Diamond's running summary of the investigation.

Replaces a bare score with the thing a detective would actually keep: what's
established, who's named, and what's still open. Every line is gated on a state
flag, so the casebook can never claim more than the player has earned.
"""

from __future__ import annotations

from typing import Dict, List

from .acts import ACT_NAMES, current_act
from .puzzles.car_puzzle import render_plate

# Established facts. Shown once the flag is set.
FACTS: List[Dict[str, str]] = [
    {"flag": "decoded_notes",
     "text": "The seized memo decodes. Password 'angels', Pier 7, after midnight."},
    {"flag": "identified_organization",
     "text": "Northwest Maritime Imports is the front — a shell with four siblings and "
             "one registered agent."},
    {"flag": "found_emergency_frequency",
     "text": "They broadcast nightly at 2 AM on 415.6 MHz."},
    {"flag": "tuned_frequency",
     "text": "Heard on the air: the count was short, and the Harbormaster wants it moved "
             "tonight. Pier seven."},
    {"flag": "found_warehouse",
     "text": "Warehouse 22 is the hub. Everything is relabelled there and legal by the "
             "time it floats."},
    {"flag": "observed_activity",
     "text": "Confirmed by signal in the tunnels beneath Pioneer Square."},
    {"flag": "identified_vehicle",
     "text": "Blue sedan, WA-4471, registered to the shell. Seen at three scenes."},
    {"flag": "surveilled_docks",
     "text": "Night movement on the docks observed and logged from above."},
    {"flag": "ches_tip",
     "text": "A ship has been sitting in the roads three nights, waiting. Launches out "
             "of Pier 7 at three in the morning."},
    {"flag": "found_all_notes",
     "text": "All five scattered notes recovered and compiled."},
]

# People, and what you've got on them.
PEOPLE: List[Dict[str, str]] = [
    {"flag": "heard_harbormaster", "name": "The Harbormaster",
     "text": "A name nobody has met and everybody has been paid by. Ches puts it on "
             "a man called Sullivan."},
    {"flag": "identified_suspect", "name": "Sullivan",
     "text": "Runs the water. Polite, which is worse. Photograph matched."},
    {"flag": "voss_observed", "name": "Capt. Harlan Voss",
     "text": "Port Authority liaison. Rides to the 35th floor and takes his lodge pin "
             "off in the elevator first."},
    {"flag": "porter_relented", "name": "Capt. Harlan Voss",
     "text": "Chairs the Thursday room at Eagles Third Chapter No. 1144. The minutes "
             "are kept."},
    {"flag": "knows_mathers", "name": "Badge 447",
     "text": "A patrolman waved the trucks through. Third District. Number taken off "
             "his coat under a light."},
    {"flag": "mathers_confessed", "name": "Walt Mathers",
     "text": "Badge 447. Came up with you in '39. Confessed on the edge of your desk "
             "with his hat in his hands."},
]

# Open threads. Shown while the flag is still unset.
OPEN: List[Dict[str, str]] = [
    {"flag": "decoded_notes",
     "text": "The memo in your notebook is still in cipher. You have a wheel for that."},
    {"flag": "identified_organization",
     "text": "You don't have a name for the company behind it."},
    {"flag": "found_emergency_frequency",
     "text": "They talk to each other somehow. You don't know how."},
    {"flag": "identified_vehicle",
     "text": "A blue sedan keeps turning up. Nobody saw the whole plate."},
    {"flag": "found_warehouse",
     "text": "The cargo goes somewhere between the dock and the boat. Where?"},
    {"flag": "identified_suspect",
     "text": "You have a face in a photograph and no name to put on it."},
    {"flag": "surveilled_docks",
     "text": "You've never actually watched the docks work at night."},
    {"flag": "observed_activity",
     "text": "Something is going on under Pioneer Square and you haven't been down."},
    {"flag": "ches_tip",
     "text": "The waterfront talks to bartenders before it talks to detectives."},
]


def _rule(title: str) -> str:
    return f"\n{title}\n{'-' * len(title)}"


def render(game_state: Dict, inventory: List[str], dialogue_state: Dict) -> str:
    """Build the casebook text for the current state of the investigation."""
    act = current_act(game_state)
    score = game_state.get("score", 0)

    lines: List[str] = [
        "DIAMOND'S CASEBOOK",
        "==================",
        f"Act {act} — {ACT_NAMES.get(act, '?')}        Case progress: {score} points",
    ]

    established = [f["text"] for f in FACTS if game_state.get(f["flag"], False)]
    if established:
        lines.append(_rule("ESTABLISHED"))
        lines += [f"  - {text}" for text in established]

    people = [f"  {p['name']}: {p['text']}" for p in PEOPLE if game_state.get(p["flag"], False)]
    if people:
        lines.append(_rule("PEOPLE"))
        lines += people

    plate = render_plate(game_state)
    if "?" in plate and game_state.get("plate_fragments"):
        lines.append(_rule("THE SEDAN"))
        lines.append(f"  Plate so far: {plate}")

    open_threads = [o["text"] for o in OPEN if not game_state.get(o["flag"], False)]
    if open_threads:
        lines.append(_rule("OPEN"))
        lines += [f"  - {text}" for text in open_threads]

    known = dialogue_state.get("known_topics", [])
    if known:
        lines.append(_rule("QUESTIONS YOU CAN ASK"))
        lines.append("  'topics' lists them. 'ask <person> about <topic>' puts them to work.")

    if act == 3:
        lines.append(_rule("TONIGHT"))
        lines.append("  Pier 7, after midnight. South from the docks.")

    return "\n".join(lines)
