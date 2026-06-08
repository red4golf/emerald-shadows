"""Tests for CarPuzzle."""

import pytest
from emerald_shadows.puzzles.car_puzzle import CarPuzzle


@pytest.fixture
def puzzle():
    return CarPuzzle()


def test_correct_solution(puzzle):
    solved, msg = puzzle.attempt("WA-4471")
    assert solved is True
    assert "4471" in msg


def test_correct_solution_with_space(puzzle):
    # Spaces should normalize to dashes
    solved, _ = puzzle.attempt("WA 4471")
    assert solved is True


def test_correct_solution_lowercase(puzzle):
    solved, _ = puzzle.attempt("wa-4471")
    assert solved is True


def test_wrong_solution(puzzle):
    solved, msg = puzzle.attempt("WA-9999")
    assert solved is False
    assert msg


def test_requires_notebook(puzzle):
    assert puzzle.check_requirements({"notebook"}) is True
    assert puzzle.check_requirements(set()) is False


def test_location(puzzle):
    assert puzzle.location == "pioneer_square"
