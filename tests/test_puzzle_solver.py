"""Tests for PuzzleManager.

Puzzles are now *operated* rather than answered: the cipher wheel is turned, the
radio dial is swept, the tunnel signal is tapped back. Only the licence-plate
puzzle still takes a typed answer, so it's the one that goes through
``solution_provider``.
"""

from copy import deepcopy

import pytest

from emerald_shadows.config import INITIAL_GAME_STATE
from emerald_shadows.puzzles.puzzle_manager import PuzzleManager

CIPHER_KIT = {"cipher_wheel", "notebook"}
RADIO_KIT = {"radio_manual", "informant_note"}
TUNNEL_KIT = {"flashlight", "radio_manual"}
ALL_FRAGMENTS = ["photo", "harold", "ches"]


def _manager(answer: str) -> PuzzleManager:
    """A PuzzleManager whose typed-answer provider always returns *answer*."""
    return PuzzleManager(solution_provider=lambda loc: answer)


@pytest.fixture
def game_state():
    # Deep copy: the initial state holds mutable lists that must not be shared
    # between tests.
    return deepcopy(INITIAL_GAME_STATE)


# --- unknown location ---

def test_unknown_location_returns_false(game_state):
    pm = _manager("anything")
    assert pm.handle_puzzle("invalid_location", set(), game_state) is False


def test_interact_at_location_without_puzzle(game_state):
    pm = PuzzleManager()
    assert pm.interact("police_station", "turn", "wheel", set(), game_state) is False


# --- missing items ---

def test_missing_items_blocks_puzzle(game_state, capsys):
    pm = _manager("415.6")
    assert pm.handle_puzzle("warehouse_office", set(), game_state) is False
    assert "radio_manual" in capsys.readouterr().out


def test_missing_items_blocks_interaction(game_state, capsys):
    pm = PuzzleManager()
    # Consumed (the verb belongs to this room) but refused for want of the kit.
    assert pm.interact("evidence_room", "turn", "wheel to h", set(), game_state) is True
    assert game_state["decoded_notes"] is False
    assert "cipher_wheel" in capsys.readouterr().out


# --- the cipher wheel is turned ---

def test_cipher_solved_by_turning_to_correct_setting(game_state):
    pm = PuzzleManager()
    assert pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state) is True
    assert game_state["decoded_notes"] is True
    assert game_state["score"] == 25


def test_cipher_wrong_setting_does_not_solve(game_state):
    pm = PuzzleManager()
    pm.interact("evidence_room", "turn", "wheel to k", CIPHER_KIT, game_state)
    assert game_state["decoded_notes"] is False
    assert game_state["score"] == 0


def test_cipher_sweep_shows_every_setting(game_state, capsys):
    pm = PuzzleManager()
    pm.interact("evidence_room", "turn", "wheel", CIPHER_KIT, game_state)
    out = capsys.readouterr().out
    # The crib: one readable word among twenty-five garbage strings.
    assert "PASSWORD" in out
    assert game_state["decoded_notes"] is False


# --- the radio is swept ---

def test_radio_solved_on_correct_frequency(game_state):
    pm = PuzzleManager()
    assert pm.interact("warehouse_office", "tune", "415.6", RADIO_KIT, game_state) is True
    assert game_state["found_warehouse"] is True


def test_radio_near_miss_gives_warmer_feedback(game_state, capsys):
    pm = PuzzleManager()
    pm.interact("warehouse_office", "tune", "415.5", RADIO_KIT, game_state)
    assert game_state["found_warehouse"] is False
    assert "almost" in capsys.readouterr().out.lower()


def test_radio_far_miss_is_dead_air(game_state, capsys):
    pm = PuzzleManager()
    pm.interact("warehouse_office", "tune", "220.0", RADIO_KIT, game_state)
    assert game_state["found_warehouse"] is False
    assert "dead air" in capsys.readouterr().out.lower()


# --- the tunnel signal is tapped back ---

def test_morse_solved_by_tapping_decoded_signal(game_state):
    pm = PuzzleManager()
    assert pm.interact("underground_tunnels", "tap", "W22", TUNNEL_KIT, game_state) is True
    assert game_state["observed_activity"] is True


def test_morse_accepts_spelled_out_answer(game_state):
    pm = PuzzleManager()
    pm.interact("underground_tunnels", "tap", "warehouse 22", TUNNEL_KIT, game_state)
    assert game_state["observed_activity"] is True


def test_morse_wrong_answer_does_not_solve(game_state):
    pm = PuzzleManager()
    pm.interact("underground_tunnels", "tap", "W19", TUNNEL_KIT, game_state)
    assert game_state["observed_activity"] is False


def test_listening_repeats_the_signal(game_state, capsys):
    pm = PuzzleManager()
    assert pm.interact("underground_tunnels", "listen", "", TUNNEL_KIT, game_state) is True
    # Real Morse, not a description of Morse.
    assert ".--" in capsys.readouterr().out


# --- the plate is assembled, then typed ---

def test_car_puzzle_takes_typed_answer(game_state):
    game_state["plate_fragments"] = ALL_FRAGMENTS
    pm = _manager("WA-4471")
    assert pm.handle_puzzle("pioneer_square", {"notebook"}, game_state) is True
    assert game_state["identified_vehicle"] is True


def test_car_puzzle_rejects_wrong_plate(game_state):
    game_state["plate_fragments"] = ALL_FRAGMENTS
    pm = _manager("WA-1234")
    assert pm.handle_puzzle("pioneer_square", {"notebook"}, game_state) is False
    assert game_state["identified_vehicle"] is False


def test_car_briefing_shows_partial_plate(game_state, capsys):
    game_state["plate_fragments"] = ["photo"]
    pm = _manager("")
    pm.handle_puzzle("pioneer_square", {"notebook"}, game_state)
    assert "WA-44??" in capsys.readouterr().out


def test_no_solution_entered_returns_false(game_state):
    game_state["plate_fragments"] = ALL_FRAGMENTS
    pm = PuzzleManager(solution_provider=lambda loc: "")
    assert pm.handle_puzzle("pioneer_square", {"notebook"}, game_state) is False


# --- already solved ---

def test_already_solved_blocks_retry(game_state, capsys):
    pm = PuzzleManager()
    pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state)
    capsys.readouterr()
    assert pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state) is True
    assert "already" in capsys.readouterr().out.lower()


def test_score_not_double_awarded(game_state):
    pm = PuzzleManager()
    pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state)
    pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state)
    assert game_state["score"] == 25


def test_solved_puzzles_set_updated(game_state):
    pm = PuzzleManager()
    pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state)
    assert "evidence_room" in pm.solved_puzzles


# --- should_trigger_on_use ---

def test_trigger_on_use_returns_true_for_required_item(game_state):
    assert PuzzleManager().should_trigger_on_use("radio_manual", "warehouse_office") is True


def test_trigger_on_use_returns_false_for_non_required_item(game_state):
    assert PuzzleManager().should_trigger_on_use("badge", "warehouse_office") is False


def test_trigger_on_use_returns_false_when_no_puzzle_at_location(game_state):
    assert PuzzleManager().should_trigger_on_use("radio_manual", "police_station") is False


def test_trigger_on_use_returns_false_when_puzzle_already_solved(game_state):
    pm = PuzzleManager()
    pm.interact("evidence_room", "turn", "wheel to h", CIPHER_KIT, game_state)
    assert pm.should_trigger_on_use("cipher_wheel", "evidence_room") is False


def test_trigger_on_use_cipher_wheel_at_evidence_room(game_state):
    assert PuzzleManager().should_trigger_on_use("cipher_wheel", "evidence_room") is True


def test_trigger_on_use_flashlight_at_underground_tunnels(game_state):
    assert PuzzleManager().should_trigger_on_use("flashlight", "underground_tunnels") is True


def test_trigger_on_use_notebook_at_pioneer_square(game_state):
    assert PuzzleManager().should_trigger_on_use("notebook", "pioneer_square") is True


# --- verbs are scoped to their room ---

def test_verbs_at_reports_room_verbs():
    pm = PuzzleManager()
    assert pm.verbs_at("evidence_room") == {"turn"}
    assert pm.verbs_at("warehouse_office") == {"tune"}
    assert pm.verbs_at("pioneer_square") == set()
    assert pm.verbs_at("police_station") == set()


def test_wrong_verb_for_room_is_not_consumed(game_state):
    pm = PuzzleManager()
    assert pm.interact("evidence_room", "tune", "415.6", CIPHER_KIT, game_state) is False
