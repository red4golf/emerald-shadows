"""Tests for MorsePuzzle."""

import pytest
from emerald_shadows.puzzles.morse_puzzle import MorsePuzzle


@pytest.fixture
def puzzle():
    return MorsePuzzle()


def test_correct_solution(puzzle):
    solved, msg = puzzle.attempt("WAREHOUSE 22")
    assert solved is True
    assert msg


def test_correct_solution_lowercase(puzzle):
    solved, _ = puzzle.attempt("warehouse 22")
    assert solved is True


def test_wrong_solution(puzzle):
    solved, msg = puzzle.attempt("WAREHOUSE 7")
    assert solved is False
    assert msg


def test_requires_flashlight_and_chart(puzzle):
    """You need light to work, and the manual is where the code chart lives."""
    assert puzzle.check_requirements({"flashlight", "radio_manual"}) is True
    assert puzzle.check_requirements({"flashlight"}) is False
    assert puzzle.check_requirements({"radio_manual"}) is False
    assert puzzle.check_requirements(set()) is False


def test_location(puzzle):
    assert puzzle.location == "underground_tunnels"


# --- alternative accepted answers ---

def test_alt_answer_w_dash_22(puzzle):
    solved, _ = puzzle.attempt("W-22")
    assert solved is True


def test_alt_answer_w_space_22(puzzle):
    solved, _ = puzzle.attempt("W 22")
    assert solved is True


def test_alt_answer_warehouse22_no_space(puzzle):
    solved, _ = puzzle.attempt("WAREHOUSE22")
    assert solved is True


def test_alt_answer_w22_lowercase(puzzle):
    solved, _ = puzzle.attempt("w-22")
    assert solved is True


def test_unrelated_string_rejected(puzzle):
    solved, _ = puzzle.attempt("PIER 7")
    assert solved is False


# --- the signal is real Morse, and it decodes ---

def test_signal_is_actual_morse():
    from emerald_shadows.codes import from_morse
    from emerald_shadows.puzzles.morse_puzzle import SIGNAL

    assert set(SIGNAL) <= set(".- /")
    assert from_morse(SIGNAL) == "W22"


def test_tapping_the_decoded_signal_solves(puzzle):
    solved, _ = puzzle.interact("tap", "W22", {})
    assert solved is True


def test_listening_repeats_the_signal(puzzle):
    from emerald_shadows.puzzles.morse_puzzle import SIGNAL

    solved, msg = puzzle.interact("listen", "", {})
    assert solved is False
    assert SIGNAL in msg


def test_tapping_nothing_is_refused(puzzle):
    solved, msg = puzzle.interact("tap", "", {})
    assert solved is False
    assert msg


def test_unrelated_verb_is_not_handled(puzzle):
    assert puzzle.interact("turn", "wheel", {}) is None
