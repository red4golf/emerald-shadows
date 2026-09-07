"""Morse puzzle — underground_tunnels.

Someone is tapping on a pipe down here. The signal is real Morse; the chart is
in the radio manual the player is carrying. Decoding it by hand is the puzzle —
three characters, short enough to be a pleasure and long enough to be work.
"""

from typing import Dict, Set, Tuple

from ..codes import from_morse, to_morse
from .base_puzzle import BasePuzzle, Interaction

# What the pipe is saying: W22. The hub designation, tapped by someone who
# can't risk saying it out loud.
SIGNAL = to_morse("W22")

_CORRECT = "W22"
_ALT_ANSWERS = {
    "W-22", "W 22", "WAREHOUSE 22", "WAREHOUSE22", "WAREHOUSE-22",
    "WAREHOUSE TWENTY TWO", "22",
}


class MorsePuzzle(BasePuzzle):
    """Player must decode a tapped signal to identify the smugglers' hub."""

    def __init__(self) -> None:
        super().__init__(
            location="underground_tunnels",
            required_items={"flashlight", "radio_manual"},
            description="A repeating signal, tapped on a pipe somewhere ahead in the dark.",
        )

    def briefing(self, game_state: Dict) -> str:
        game_state["heard_signal"] = True
        return (
            "You kill the light and stand still.\n\n"
            "It comes again — metal on metal, somewhere ahead where the tunnel bends. "
            "Not settling. Not water. Someone down here is tapping on a pipe, patiently, "
            "the same short phrase over and over, the way you signal when you can't "
            "afford to be heard saying it.\n\n"
            f"   {SIGNAL}\n\n"
            "The chart's in the radio manual in your coat. Three characters. "
            "You've got a flashlight, a pencil, and as long as it takes.\n\n"
            "  listen        - hear the signal again\n"
            "  tap <answer>  - tap it back, and call the wagons in behind it"
        )

    def verbs(self) -> Set[str]:
        return {"listen", "tap"}

    def interact(self, verb: str, argument: str, game_state: Dict) -> Interaction:
        if verb == "listen":
            game_state["heard_signal"] = True
            return False, (
                "You hold still and let it come around again.\n\n"
                f"   {SIGNAL}\n\n"
                "Same phrase. Whoever's tapping has been at it a while."
            )

        if verb == "tap":
            if not argument.strip():
                return False, "Tap what? You'd want to be sure before you answer."
            return self.attempt(argument)

        return None

    def attempt(self, solution: str) -> Tuple[bool, str]:
        normalised = " ".join((solution or "").strip().upper().split())
        if normalised == _CORRECT or normalised in _ALT_ANSWERS:
            return True, (
                f"You tap it back against the brick — {SIGNAL} — and the pipe goes quiet, "
                "and then answers once. Acknowledged.\n\n"
                "Warehouse 22. Not a name in a file. A building with a number on it, four "
                "blocks from where you're standing, that somebody has been feeding for "
                "eighteen months.\n\n"
                "You tap the pre-arranged signal for the wagons and start counting the "
                "minutes until they come."
            )
        decoded = from_morse(SIGNAL)
        if normalised and normalised in decoded:
            return False, "Close. Read the whole phrase — every character, in order."
        return False, (
            "You tap out your answer. Nothing comes back.\n\n"
            "Either you read it wrong or the man on the other end just decided you're "
            "not who he was waiting for. Check the chart again."
        )
