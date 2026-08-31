"""Act structure for Emerald Shadows.

The case used to end when a checklist filled up. Noir doesn't work that way —
it works by getting worse. Three acts: you ask questions, the questions get
noticed, and then you go down to the water and finish it.

Acts are computed from game state rather than stored, so a loaded save always
lands in the right one.
"""

from __future__ import annotations

from typing import Dict, List, Optional

# Flags that must all be True to stand in each act.
ACT_REQUIREMENTS: Dict[int, List[str]] = {
    1: [],
    2: ["decoded_notes", "identified_organization"],
    3: ["found_warehouse", "observed_activity", "identified_suspect", "identified_vehicle"],
}

ACT_NAMES: Dict[int, str] = {
    1: "Legwork",
    2: "Heat",
    3: "Pier Seven",
}

ACT_OPENINGS: Dict[int, str] = {
    2: (
        "                    * * *\n\n"
        "                ACT TWO — HEAT\n\n"
        "You decode a memo in a locked room at eleven at night and by morning the city "
        "knows. That's not a figure of speech. Somebody in this building told somebody "
        "in that building, and the machinery you've been poking at has turned over once "
        "and looked at you.\n\n"
        "The desk sergeant doesn't meet your eye. There's a car at the end of Third that "
        "was there when you went in and is there when you come out, and the man in it is "
        "reading a newspaper in the rain, which nobody does.\n\n"
        "You have what you have. From here, everything you learn costs somebody something."
    ),
    3: (
        "                    * * *\n\n"
        "             ACT THREE — PIER SEVEN\n\n"
        "It closes the way these things close: all at once, and then not at all.\n\n"
        "The warehouse. The plate. The frequency and the hour and the word that opens "
        "the gate. A Port Authority captain who takes his lodge pin off in an elevator, "
        "and a friend from the academy who waved three trucks through a gate on Tuesdays "
        "because a man asked him to look at the water.\n\n"
        "The radio said tonight. The memo said pier seven, after midnight, ask only for "
        "the Harbormaster.\n\n"
        "It's a quarter past eleven. The waterfront is twenty minutes on the trolley and "
        "you have exactly as much as you're going to have.\n\n"
        "[Pier 7 is open to you now — south from the docks. Go and finish it.]"
    ),
}

# What the arrest actually needs in the coat pocket. Evidence, not trophies.
FINALE_ITEMS: Dict[str, str] = {
    "badge": "your shield — without it this is a mugging",
    "notebook": "the notebook, with the plate and the decoded memo in it",
    "meeting_minutes": "the Thursday minutes, with Voss's signature on them",
    "manifest": "the manifest off the Pioneer Square board",
}


def current_act(game_state: Dict) -> int:
    """The highest act whose requirements are all satisfied."""
    act = 1
    for number in sorted(ACT_REQUIREMENTS):
        if all(game_state.get(flag, False) for flag in ACT_REQUIREMENTS[number]):
            act = number
    return act


def check_advance(game_state: Dict) -> Optional[int]:
    """Detect an act change since last check. Returns the new act, or None.

    The last-seen act is kept in game state so it survives save and load.
    """
    act = current_act(game_state)
    seen = game_state.get("act_seen", 1)
    if act > seen:
        game_state["act_seen"] = act
        return act
    # Never walk backwards, even if a flag is somehow cleared.
    game_state["act_seen"] = max(seen, act)
    return None


def opening_text(act: int) -> Optional[str]:
    return ACT_OPENINGS.get(act)


def act_label(game_state: Dict) -> str:
    act = current_act(game_state)
    return f"Act {act} — {ACT_NAMES.get(act, '?')}"


def missing_for_next_act(game_state: Dict) -> List[str]:
    """Flags still outstanding before the next act opens. Empty in act 3."""
    act = current_act(game_state)
    nxt = act + 1
    if nxt not in ACT_REQUIREMENTS:
        return []
    return [f for f in ACT_REQUIREMENTS[nxt] if not game_state.get(f, False)]


def missing_finale_items(inventory: List[str]) -> List[str]:
    """Evidence the player still needs before the arrest will stick."""
    return [item for item in FINALE_ITEMS if item not in inventory]
