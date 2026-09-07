"""Licence plate puzzle — pioneer_square.

No cipher here, and no trick. This is the legwork puzzle: nobody saw the whole
plate, so you assemble it out of three people's partial memories. The work is
in having gone and asked.
"""

from typing import Dict, List, Set, Tuple

from .base_puzzle import BasePuzzle, Interaction

_CORRECT_PLATE = "WA-4471"
_LOCATION = "pioneer_square"

# Each source fills in the digits it can. Positions are 0-3 of the numeric block.
FRAGMENTS: Dict[str, Dict] = {
    "photo": {
        "digits": {0: "4", 1: "4"},
        "source": "the surveillance photograph — first two figures, the rest lost to grain",
    },
    "harold": {
        "digits": {2: "7"},
        "source": "Harold at the Smith Tower — 'third one was a seven, I'd swear to it'",
    },
    "ches": {
        "digits": {3: "1"},
        "source": "Ches at the Anchor — 'ended in a one. I remember because it didn't'",
    },
}


def known_digits(game_state: Dict) -> Dict[int, str]:
    """Merge every plate fragment the player has collected."""
    digits: Dict[int, str] = {}
    for key in game_state.get("plate_fragments", []):
        fragment = FRAGMENTS.get(key)
        if fragment:
            digits.update(fragment["digits"])
    return digits


def render_plate(game_state: Dict) -> str:
    """The plate as currently reconstructed: 'WA-44??'."""
    digits = known_digits(game_state)
    return "WA-" + "".join(digits.get(i, "?") for i in range(4))


class CarPuzzle(BasePuzzle):
    """Player must reconstruct the smugglers' plate from three partial accounts."""

    def __init__(self) -> None:
        super().__init__(
            location=_LOCATION,
            required_items={"notebook"},
            description="Three people saw the blue sedan. No two of them saw the same thing.",
        )

    def briefing(self, game_state: Dict) -> str:
        collected: List[str] = game_state.get("plate_fragments", [])
        lines = [
            "You put your back against the pergola and open the notebook to the page "
            "where you've been keeping the sedan.",
            "",
            "A blue sedan, seen near three separate scenes by three people who each "
            "caught a different piece of it. Nobody got the whole plate. Between them, "
            "they might have.",
            "",
            f"   {render_plate(game_state)}",
            "",
        ]
        if collected:
            lines.append("What you have, and who gave it to you:")
            for key in collected:
                fragment = FRAGMENTS.get(key)
                if fragment:
                    lines.append(f"  - {fragment['source']}")
        else:
            lines.append(
                "You have nothing yet. Somebody in this city looked at that car long "
                "enough to remember it. Go and find out who."
            )

        missing = 4 - len(known_digits(game_state))
        if missing:
            lines += [
                "",
                f"{missing} figure{'s' if missing != 1 else ''} still missing. "
                "Ask around — the ones who help you are rarely the ones you'd expect.",
            ]
        else:
            lines += ["", "That's the whole plate. Write it down: 'solve' and give it to me."]
        return "\n".join(lines)

    def interact(self, verb: str, argument: str, game_state: Dict) -> Interaction:
        return None

    def attempt(self, solution: str) -> Tuple[bool, str]:
        normalised = (solution or "").strip().upper().replace(" ", "").replace("-", "")
        target = _CORRECT_PLATE.replace("-", "")
        if normalised == target:
            return True, (
                "WA-4471.\n\n"
                "You run it through the licensing office in the morning. The registration "
                "comes back to Northwest Maritime Imports, which is an address on Railroad "
                "Avenue, which is a door in an alley with no company behind it — a shell "
                "with the same registered agent as four others.\n\n"
                "A car that doesn't belong to anybody, parked at three scenes it had no "
                "business being at. That's not a coincidence. That's a motor pool."
            )
        if normalised and normalised.isdigit():
            return False, (
                "That's a number, not a plate. Washington plates run 'WA-' and four figures."
            )
        return False, "That doesn't match what the three of them told you. Check your notes."
