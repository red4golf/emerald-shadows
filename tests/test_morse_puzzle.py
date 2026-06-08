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


def test_requires_flashlight(puzzle):
    assert puzzle.check_requirements({"flashlight"}) is True
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
