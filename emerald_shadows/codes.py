"""Cipher and code utilities for Emerald Shadows.

Pure functions with no game state and no I/O. The puzzles that use these are
meant to be *worked*, not guessed, so the transformations here are the real
thing: a Caesar disc that actually rotates and a Morse table that actually
decodes. Keeping them free of side effects makes them cheap to test and
lets the puzzle classes stay thin.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# --------------------------------------------------------------------------
# Caesar shift — the cipher wheel
# --------------------------------------------------------------------------

def shift_for_letter(letter: str) -> Optional[int]:
    """Convert a wheel setting ('align outer A with inner N') to a shift.

    Returns None when the input isn't a single letter A-Z.
    """
    letter = (letter or "").strip().upper()
    if len(letter) != 1 or letter not in _ALPHABET:
        return None
    return _ALPHABET.index(letter)


def caesar(text: str, shift: int) -> str:
    """Shift every letter in ``text`` forward by ``shift``. Non-letters pass through."""
    shift %= 26
    out: List[str] = []
    for char in text:
        upper = char.upper()
        if upper in _ALPHABET:
            rotated = _ALPHABET[(_ALPHABET.index(upper) + shift) % 26]
            out.append(rotated if char.isupper() else rotated.lower())
        else:
            out.append(char)
    return "".join(out)


def caesar_decode(text: str, shift: int) -> str:
    """Undo a Caesar shift of ``shift``."""
    return caesar(text, -shift)


def first_word(text: str) -> str:
    """The first whitespace-delimited token of a string, or '' when empty."""
    parts = text.strip().split()
    return parts[0] if parts else ""


def sweep(ciphertext: str) -> List[Tuple[str, str]]:
    """Every wheel setting paired with the first word it yields.

    This is what a real cipher disc gives you: spin it, watch the leading word,
    stop when something readable falls out. Returns 26 (setting_letter, word)
    pairs in wheel order.
    """
    return [
        (_ALPHABET[shift], first_word(caesar_decode(ciphertext, shift)))
        for shift in range(26)
    ]


# --------------------------------------------------------------------------
# Morse
# --------------------------------------------------------------------------

MORSE_TABLE: Dict[str, str] = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}

_MORSE_REVERSE: Dict[str, str] = {code: char for char, code in MORSE_TABLE.items()}


def to_morse(text: str) -> str:
    """Encode text as Morse. Letters are space-separated, words by ' / '."""
    words = []
    for word in text.strip().upper().split():
        words.append(" ".join(MORSE_TABLE[c] for c in word if c in MORSE_TABLE))
    return " / ".join(w for w in words if w)


def from_morse(morse: str) -> str:
    """Decode Morse back to text. Unknown symbols become '?'."""
    words = []
    for word in morse.strip().split("/"):
        letters = [_MORSE_REVERSE.get(sym, "?") for sym in word.split()]
        if letters:
            words.append("".join(letters))
    return " ".join(words)


def morse_chart(columns: int = 4) -> str:
    """Render the Morse table as a fixed-width chart for in-game reference."""
    entries = [f"{char} {code:<6}" for char, code in MORSE_TABLE.items()]
    lines = []
    for i in range(0, len(entries), columns):
        lines.append("   " + "  ".join(e.ljust(9) for e in entries[i:i + columns]).rstrip())
    return "\n".join(lines)
