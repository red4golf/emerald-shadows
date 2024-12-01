"""Tests for the puzzle solver module."""

import pytest
from emerald_shadows.puzzle_solver import PuzzleSolver

@pytest.fixture
def puzzle_solver():
    """Create a PuzzleSolver instance for testing."""
    return PuzzleSolver()

def test_puzzle_solver_initialization(puzzle_solver):
    """Test that PuzzleSolver initializes correctly."""
    assert isinstance(puzzle_solver.solved_puzzles, set)
    assert len(puzzle_solver.solved_puzzles) == 0

def test_check_requirements(puzzle_solver):
    """Test puzzle requirement checking."""
    # Test with all required items
    inventory = {"radio_manual"}
    success, message = puzzle_solver.check_requirements("warehouse_office", inventory)
    assert success
    assert "radio equipment" in message
    
    # Test with missing items
    inventory = set()
    success, message = puzzle_solver.check_requirements("warehouse_office", inventory)
    assert not success
    assert "need" in message

def test_invalid_location(puzzle_solver):
    """Test handling of invalid locations."""
    success, message = puzzle_solver.check_requirements("invalid_location", set())
    assert not success
    assert "no puzzles" in message.lower()

def test_already_solved_puzzle(puzzle_solver):
    """Test handling of already solved puzzles."""
    inventory = {"radio_manual"}
    puzzle_solver.solved_puzzles.add("warehouse_office")
    
    success, message = puzzle_solver.solve_puzzle("warehouse_office", "test", inventory)
    assert not success
    assert "already solved" in message.lower()