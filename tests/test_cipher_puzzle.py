"""Tests for CipherPuzzle."""

import pytest
from emerald_shadows.puzzles.cipher_puzzle import CipherPuzzle


@pytest.fixture
def puzzle():
    return CipherPuzzle()


def test_correct_solution(puzzle):
    solved, msg = puzzle.attempt("ANGELS")
    assert solved is True
    assert "ANGELS" in msg


def test_correct_solution_lowercase(puzzle):
    solved, _ = puzzle.attempt("angels")
    assert solved is True


def test_wrong_solution(puzzle):
    solved, msg = puzzle.attempt("DEMONS")
    assert solved is False
    assert msg


def test_requires_cipher_wheel_and_notebook(puzzle):
    assert puzzle.check_requirements({"cipher_wheel", "notebook"}) is True
    assert puzzle.check_requirements({"cipher_wheel"}) is False
    assert puzzle.check_requirements({"notebook"}) is False
    assert puzzle.check_requirements(set()) is False


def test_location(puzzle):
    assert puzzle.location == "evidence_room"
