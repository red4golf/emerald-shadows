"""Radio puzzle — warehouse_office.

The informant's note gave up its last digit to the rain. What's left is a band
to sweep, and a dial that tells you — through the static — when you're close.
"""

from typing import Dict, Set, Tuple

from .base_puzzle import BasePuzzle, Interaction

TARGET = 415.6
BAND_LOW = 415.0
BAND_HIGH = 415.9


class RadioPuzzle(BasePuzzle):
    """Player must sweep a band to find the smugglers' emergency frequency."""

    def __init__(self) -> None:
        super().__init__(
            location="warehouse_office",
            required_items={"radio_manual", "informant_note"},
            description="A seized Army set, and a frequency the rain got to first.",
        )

    def briefing(self, game_state: Dict) -> str:
        return (
            "You clear the desk and get the seized set warmed up. The manual says these "
            "Army units hold a band clean enough to eavesdrop on, if you know where to sit.\n\n"
            "The informant's note is in your other hand, and the rain has had it:\n\n"
            "   'Emergency frequency 415.? MHz — they broadcast shipment times nightly "
            "at 2 AM.'\n\n"
            "One digit. Ten places it could be. The set's dial reads to a tenth and the "
            "static will tell you when you're warm.\n\n"
            "  tune <frequency>  - e.g. 'tune 415.3'"
        )

    def verbs(self) -> Set[str]:
        return {"tune"}

    def interact(self, verb: str, argument: str, game_state: Dict) -> Interaction:
        if verb != "tune":
            return None

        text = (argument or "").strip().lower()
        for junk in ("radio", "set", "dial", "to "):
            if text.startswith(junk):
                text = text[len(junk):].strip()
        text = text.replace("mhz", "").strip()

        if not text:
            return False, "Tune to what? The note says 415-point-something."

        try:
            frequency = float(text)
        except ValueError:
            return False, (
                "That's not a frequency. The dial takes numbers — 'tune 415.3'."
            )

        game_state["frequencies_tried"] = sorted(
            set(game_state.get("frequencies_tried", [])) | {round(frequency, 1)}
        )
        return self._response(frequency, game_state)

    def _response(self, frequency: float, game_state: Dict) -> Tuple[bool, str]:
        distance = abs(frequency - TARGET)

        if distance < 0.05:
            game_state["tuned_frequency"] = TARGET
            return True, (
                f"{TARGET:.1f}.\n\n"
                "The static parts like a curtain and there are men in the room with you.\n\n"
                "'—second pallet's short. Tell him the count was short.'\n"
                "'He knows what the count was.'\n"
                "'Then tell him the Harbormaster wants it moved tonight, not Friday. "
                "Pier seven. Same as always.'\n\n"
                "A third voice says something you don't catch, and somebody laughs, and "
                "then it's just carrier tone and the rain on the window.\n\n"
                "You write down the frequency and the hour and sit there a moment longer "
                "than you need to."
            )

        if distance <= 0.15:
            return False, (
                f"{frequency:.1f} — the static thins. Something is *almost* in there, "
                "a rhythm that could be a voice if you moved a hair either way. "
                "You're on top of it. Keep going."
            )

        if distance <= 0.35:
            return False, (
                f"{frequency:.1f} — a voice surfaces and drowns before it's a word. "
                "Close enough to know it's real. Not close enough to use."
            )

        if BAND_LOW - 0.5 <= frequency <= BAND_HIGH + 0.5:
            return False, f"{frequency:.1f} — static, and under it, nothing. Wrong end of the band."

        return False, (
            f"{frequency:.1f} — dead air. That's not even the right neighbourhood. "
            "The note said 415-point-something."
        )

    def attempt(self, solution: str) -> Tuple[bool, str]:
        """Typed-answer path, kept so 'solve' still resolves the puzzle."""
        try:
            frequency = float((solution or "").strip())
        except ValueError:
            return False, "That's not a frequency."
        if abs(frequency - TARGET) < 0.05:
            return True, f"You lock onto {TARGET:.1f} MHz and the smugglers' chatter floods in."
        return False, "Static sputters. That frequency is dead tonight."
