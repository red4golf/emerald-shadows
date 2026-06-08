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


def test_requires_radio_manual(puzzle):
    assert puzzle.check_requirements({"radio_manual"}) is True
    assert puzzle.check_requirements(set()) is False


def test_location(puzzle):
    assert puzzle.location == "warehouse_office"
