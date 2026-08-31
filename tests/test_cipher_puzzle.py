"""Tests for CipherPuzzle.

The answer is a wheel setting, not a password. The player finds it by sweeping
the disc until an English word falls out of the leading position.
"""

import pytest

from emerald_shadows.codes import caesar_decode, shift_for_letter
from emerald_shadows.puzzles.cipher_puzzle import CIPHERTEXT, SOLUTION_LETTER, CipherPuzzle


@pytest.fixture
def puzzle():
    return CipherPuzzle()


@pytest.fixture
def state():
    return {}


def test_correct_setting_solves(puzzle, state):
    solved, msg = puzzle.interact("turn", "wheel to H", state)
    assert solved is True
    assert "ANGELS" in msg


def test_correct_setting_lowercase(puzzle, state):
    solved, _ = puzzle.interact("turn", "wheel to h", state)
    assert solved is True


def test_bare_letter_accepted(puzzle, state):
    solved, _ = puzzle.interact("turn", "h", state)
    assert solved is True


def test_wrong_setting_does_not_solve(puzzle, state):
    solved, msg = puzzle.interact("turn", "wheel to K", state)
    assert solved is False
    assert "noise" in msg.lower()


def test_sweep_reveals_the_crib(puzzle, state):
    solved, msg = puzzle.interact("turn", "wheel", state)
    assert solved is False
    # Every setting is listed, and exactly one leading word is readable.
    assert "PASSWORD" in msg
    assert msg.count("\n") >= 26


def test_non_letter_setting_is_rejected_kindly(puzzle, state):
    solved, msg = puzzle.interact("turn", "wheel to 7", state)
    assert solved is False
    assert "letters" in msg.lower()


def test_unrelated_verb_is_not_handled(puzzle, state):
    assert puzzle.interact("tune", "415.6", state) is None


def test_ciphertext_decodes_to_readable_plaintext():
    plain = caesar_decode(CIPHERTEXT, shift_for_letter(SOLUTION_LETTER))
    assert plain.startswith("PASSWORD ANGELS")
    assert "PIER SEVEN" in plain


def test_solving_records_the_setting(puzzle, state):
    puzzle.interact("turn", "wheel to H", state)
    assert state["cipher_setting"] == SOLUTION_LETTER


def test_typed_answer_path_still_works(puzzle):
    assert puzzle.attempt("H")[0] is True
    assert puzzle.attempt("K")[0] is False


def test_requires_cipher_wheel_and_notebook(puzzle):
    assert puzzle.check_requirements({"cipher_wheel", "notebook"}) is True
    assert puzzle.check_requirements({"cipher_wheel"}) is False
    assert puzzle.check_requirements({"notebook"}) is False
    assert puzzle.check_requirements(set()) is False


def test_location(puzzle):
    assert puzzle.location == "evidence_room"


def test_briefing_shows_the_ciphertext(puzzle, state):
    assert CIPHERTEXT[:20] in puzzle.briefing(state)
