"""Tests for the cipher and Morse codecs."""

import pytest

from emerald_shadows.codes import (
    MORSE_TABLE,
    caesar,
    caesar_decode,
    first_word,
    from_morse,
    morse_chart,
    shift_for_letter,
    sweep,
    to_morse,
)


# --- Caesar ---

def test_caesar_shifts_forward():
    assert caesar("ABC", 1) == "BCD"


def test_caesar_wraps_around_z():
    assert caesar("XYZ", 3) == "ABC"


def test_caesar_preserves_case():
    assert caesar("AbZ", 1) == "BcA"


def test_caesar_passes_through_non_letters():
    assert caesar("A-1 B", 1) == "B-1 C"


def test_caesar_decode_is_the_inverse():
    for shift in range(26):
        assert caesar_decode(caesar("ATTACK AT DAWN", shift), shift) == "ATTACK AT DAWN"


def test_caesar_handles_shift_larger_than_alphabet():
    assert caesar("A", 27) == caesar("A", 1)


def test_caesar_zero_shift_is_identity():
    assert caesar("HELLO", 0) == "HELLO"


# --- wheel settings ---

@pytest.mark.parametrize("letter,expected", [("A", 0), ("B", 1), ("H", 7), ("Z", 25)])
def test_shift_for_letter(letter, expected):
    assert shift_for_letter(letter) == expected


def test_shift_for_letter_is_case_insensitive():
    assert shift_for_letter("h") == shift_for_letter("H")


@pytest.mark.parametrize("bad", ["", "  ", "AB", "1", "?", None])
def test_shift_for_letter_rejects_non_letters(bad):
    assert shift_for_letter(bad) is None


# --- sweep ---

def test_sweep_returns_every_setting():
    result = sweep("HELLO")
    assert len(result) == 26
    assert [letter for letter, _ in result] == list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def test_sweep_finds_the_plaintext_at_the_right_setting():
    ciphertext = caesar("PASSWORD ANGELS", 7)
    assert ("H", "PASSWORD") in sweep(ciphertext)


def test_first_word_of_empty_string():
    assert first_word("   ") == ""


# --- Morse ---

def test_to_morse_encodes_letters_and_digits():
    assert to_morse("W22") == ".-- ..--- ..---"


def test_morse_round_trip():
    assert from_morse(to_morse("WAREHOUSE 22")) == "WAREHOUSE 22"


def test_morse_words_separated_by_slash():
    assert " / " in to_morse("PIER SEVEN")


def test_from_morse_marks_unknown_symbols():
    assert "?" in from_morse("..--..--..--")


def test_morse_table_covers_alphabet_and_digits():
    assert set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") <= set(MORSE_TABLE)


def test_morse_codes_are_unique():
    codes = list(MORSE_TABLE.values())
    assert len(codes) == len(set(codes))


def test_morse_chart_renders_every_entry():
    chart = morse_chart()
    for char in MORSE_TABLE:
        assert char in chart
