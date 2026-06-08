"""Tests for PuzzleManager (formerly split across PuzzleSolver + PuzzleManager)."""

import pytest
from emerald_shadows.puzzles.puzzle_manager import PuzzleManager
from emerald_shadows.config import INITIAL_GAME_STATE


def _manager(answer: str) -> PuzzleManager:
    """Return a PuzzleManager whose solution_provider always returns *answer*."""
    return PuzzleManager(solution_provider=lambda loc: answer)


@pytest.fixture
def game_state():
    return INITIAL_GAME_STATE.copy()


# --- unknown location ---

def test_unknown_location_returns_false(game_state):
    pm = _manager("anything")
    assert pm.handle_puzzle("invalid_location", set(), game_state) is False


# --- missing items ---

def test_missing_items_blocks_puzzle(game_state, capsys):
    pm = _manager("415.6")
    result = pm.handle_puzzle("warehouse_office", set(), game_state)
    assert result is False
    out = capsys.readouterr().out
    assert "radio_manual" in out


# --- already solved ---

def test_already_solved_blocks_retry(game_state, capsys):
    pm = _manager("415.6")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    result = pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert result is False
    out = capsys.readouterr().out
    assert "already" in out.lower()


# --- correct solutions ---

def test_radio_puzzle_correct_solution(game_state):
    pm = _manager("415.6")
    assert pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state) is True
    assert game_state["found_warehouse"] is True


def test_cipher_puzzle_correct_solution(game_state):
    pm = _manager("ANGELS")
    assert pm.handle_puzzle("evidence_room", {"cipher_wheel", "notebook"}, game_state) is True
    assert game_state["decoded_notes"] is True


def test_morse_puzzle_correct_solution(game_state):
    pm = _manager("WAREHOUSE 22")
    assert pm.handle_puzzle("underground_tunnels", {"flashlight"}, game_state) is True
    assert game_state["observed_activity"] is True


# --- wrong solutions ---

def test_radio_puzzle_wrong_solution(game_state):
    pm = _manager("999.9")
    assert pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state) is False
    assert game_state["found_warehouse"] is False


def test_cipher_puzzle_wrong_solution(game_state):
    pm = _manager("WRONG")
    assert pm.handle_puzzle("evidence_room", {"cipher_wheel", "notebook"}, game_state) is False


# --- no solution entered ---

def test_no_solution_entered_returns_false(game_state):
    pm = PuzzleManager(solution_provider=lambda loc: "")
    assert pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state) is False


# --- solved_puzzles tracking ---

def test_solved_puzzles_set_updated(game_state):
    pm = _manager("415.6")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert "warehouse_office" in pm.solved_puzzles


# --- score on solve ---

def test_score_increments_on_correct_solve(game_state):
    pm = _manager("415.6")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert game_state["score"] == 25


def test_score_unchanged_on_wrong_answer(game_state):
    pm = _manager("000.0")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert game_state["score"] == 0


def test_score_not_double_awarded_on_second_solve_attempt(game_state):
    """Solving the same puzzle twice only awards points once."""
    pm = _manager("415.6")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    # Second call blocked by already_solved guard — score stays at 25
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert game_state["score"] == 25


# --- should_trigger_on_use ---

def test_trigger_on_use_returns_true_for_required_item(game_state):
    pm = PuzzleManager()
    assert pm.should_trigger_on_use("radio_manual", "warehouse_office") is True


def test_trigger_on_use_returns_false_for_non_required_item(game_state):
    pm = PuzzleManager()
    assert pm.should_trigger_on_use("badge", "warehouse_office") is False


def test_trigger_on_use_returns_false_when_no_puzzle_at_location(game_state):
    pm = PuzzleManager()
    assert pm.should_trigger_on_use("radio_manual", "police_station") is False


def test_trigger_on_use_returns_false_when_puzzle_already_solved(game_state):
    pm = _manager("415.6")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert pm.should_trigger_on_use("radio_manual", "warehouse_office") is False


def test_trigger_on_use_cipher_wheel_at_evidence_room(game_state):
    pm = PuzzleManager()
    assert pm.should_trigger_on_use("cipher_wheel", "evidence_room") is True


def test_trigger_on_use_flashlight_at_underground_tunnels(game_state):
    pm = PuzzleManager()
    assert pm.should_trigger_on_use("flashlight", "underground_tunnels") is True


def test_trigger_on_use_notebook_at_pioneer_square(game_state):
    pm = PuzzleManager()
    assert pm.should_trigger_on_use("notebook", "pioneer_square") is True
