"""Tests for RadioPuzzle."""

import pytest
from emerald_shadows.puzzles.radio_puzzle import RadioPuzzle


@pytest.fixture
def puzzle():
    return RadioPuzzle()


def test_correct_solution(puzzle):
    solved, msg = puzzle.attempt("415.6")
    assert solved is True
    assert "415.6" in msg


def test_wrong_solution(puzzle):
    solved, msg = puzzle.attempt("999.9")
    assert solved is False
    assert msg


def test_wrong_solution_with_whitespace(puzzle):
    # Whitespace should be stripped
    solved, _ = puzzle.attempt("  415.6  ")
    assert solved is True


def test_requires_manual_and_note(puzzle):
    """The manual tunes the set; the note names the band."""
    assert puzzle.check_requirements({"radio_manual", "informant_note"}) is True
    assert puzzle.check_requirements({"radio_manual"}) is False
    assert puzzle.check_requirements(set()) is False


def test_location(puzzle):
    assert puzzle.location == "warehouse_office"


# --- the dial is swept, and the static guides you ---

def test_exact_frequency_solves(puzzle):
    solved, msg = puzzle.interact("tune", "415.6", {})
    assert solved is True
    assert "Harbormaster" in msg


def test_one_notch_off_reports_almost(puzzle):
    solved, msg = puzzle.interact("tune", "415.5", {})
    assert solved is False
    assert "almost" in msg.lower()


def test_further_off_reports_a_drowned_voice(puzzle):
    solved, msg = puzzle.interact("tune", "415.9", {})
    assert solved is False
    assert "drowns" in msg.lower()


def test_wrong_band_reports_dead_air(puzzle):
    solved, msg = puzzle.interact("tune", "88.5", {})
    assert solved is False
    assert "dead air" in msg.lower()


def test_non_numeric_input_is_refused(puzzle):
    solved, msg = puzzle.interact("tune", "angels", {})
    assert solved is False
    assert "not a frequency" in msg.lower()


def test_tried_frequencies_are_remembered(puzzle):
    state = {}
    puzzle.interact("tune", "415.1", state)
    puzzle.interact("tune", "415.4", state)
    assert state["frequencies_tried"] == [415.1, 415.4]


def test_solving_records_the_frequency(puzzle):
    state = {}
    puzzle.interact("tune", "415.6", state)
    assert state["tuned_frequency"] == 415.6
