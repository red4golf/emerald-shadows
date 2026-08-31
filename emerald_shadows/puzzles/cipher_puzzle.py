"""Cipher wheel puzzle — evidence_room.

The wheel is a Caesar disc: two rings of letters, one inside the other. The
player rotates it and reads what falls out. There is no password to retype —
the answer is the setting that turns noise into English, and the crib is the
word the notebook says to expect.
"""

from typing import Dict, Set, Tuple

from ..codes import caesar_decode, shift_for_letter, sweep
from .base_puzzle import BasePuzzle, Interaction

# The seized memo as it sits in Diamond's notebook. Enciphered with a simple
# alphabet shift — 1947 field tradecraft, not the Enigma.
CIPHERTEXT = (
    "WHZZDVYK HUNLSZ HKTPAZ ILHYLY HA WPLY ZLCLU HMALY "
    "TPKUPNOA HZR VUSF MVY AOL OHYIVYTHZALY IBYU AOPZ"
)

# Setting H: the outer A aligned with the inner H.
SOLUTION_LETTER = "H"


class CipherPuzzle(BasePuzzle):
    """Player must find the wheel setting that decodes the smugglers' memo."""

    def __init__(self) -> None:
        super().__init__(
            location="evidence_room",
            required_items={"cipher_wheel", "notebook"},
            description="The cipher wheel and the coded memo, side by side on the work table.",
        )

    def briefing(self, game_state: Dict) -> str:
        return (
            "You flatten the memo on the work table and set the cipher wheel beside it.\n\n"
            "Two rings of letters, one inside the other. Turn the outer ring and every "
            "letter in the message moves with it. Twenty-six settings. Twenty-five of "
            "them will be nonsense.\n\n"
            "   " + CIPHERTEXT[:49] + "\n"
            "   " + CIPHERTEXT[50:] + "\n\n"
            "  turn wheel              - run through every setting, watch the first word\n"
            "  turn wheel to <letter>  - commit to a setting and read the whole memo"
        )

    def verbs(self) -> Set[str]:
        return {"turn"}

    def interact(self, verb: str, argument: str, game_state: Dict) -> Interaction:
        if verb != "turn":
            return None

        argument = self._normalise(argument)
        if not argument:
            return False, self._sweep_table()

        shift = shift_for_letter(argument)
        if shift is None:
            return False, (
                "The settings are letters, Diamond. Try 'turn wheel to H' — or just "
                "'turn wheel' to walk through all of them."
            )

        plain = caesar_decode(CIPHERTEXT, shift)
        if argument.upper() == SOLUTION_LETTER:
            game_state["cipher_setting"] = SOLUTION_LETTER
            return True, (
                f"You align the outer A with the inner {SOLUTION_LETTER}. The rings settle "
                "into a detent somebody wore smooth a long time ago.\n\n"
                f"   {plain}\n\n"
                "Twenty-six settings and only one of them is English. This isn't evidence "
                "of the thing. It's the thing — the password, the pier, and the hour, "
                "typed out by a man who then told someone else to burn it."
            )
        return False, (
            f"Setting {argument.upper()}:\n\n   {plain[:58]}...\n\nStill noise. Turn it again."
        )

    @staticmethod
    def _normalise(argument: str) -> str:
        """Accept 'wheel', 'the wheel to H', 'to h', or a bare letter."""
        text = (argument or "").strip().lower()
        for prefix in ("the ", "cipher ", "wheel", "dial"):
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        if text.startswith("to "):
            text = text[3:].strip()
        return text

    def _sweep_table(self) -> str:
        """Show every setting's leading word — how you actually crack one of these."""
        rows = [f"   {letter}   {word}" for letter, word in sweep(CIPHERTEXT)]
        return (
            "You walk the wheel through all twenty-six settings, watching the memo's "
            "first word change each time.\n\n" + "\n".join(rows) + "\n\n"
            "One of those is a word. When you see it: 'turn wheel to <letter>'."
        )

    def attempt(self, solution: str) -> Tuple[bool, str]:
        """Accept a bare setting letter, for players who'd rather type an answer."""
        text = (solution or "").strip().upper()
        shift = shift_for_letter(text)
        if shift is not None and text == SOLUTION_LETTER:
            return True, caesar_decode(CIPHERTEXT, shift)
        return False, "That setting leaves the memo in nonsense."
