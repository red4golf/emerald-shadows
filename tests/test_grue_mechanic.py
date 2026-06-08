"""Tests for the darkness / grue mechanic in GameManager."""

import builtins
import pytest

import emerald_shadows.game_manager as game_manager_module
from emerald_shadows.game_manager import GameManager


@pytest.fixture()
def gm():
    return GameManager()


# ---------------------------------------------------------------------------
# _check_darkness — non-dark location
# ---------------------------------------------------------------------------

def test_check_darkness_returns_false_in_lit_location(monkeypatch, gm):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: False)
    assert gm._check_darkness() is False


def test_check_darkness_resets_dark_turns_in_lit_location(monkeypatch, gm):
    gm.game_state["dark_turns"] = 3
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: False)
    gm._check_darkness()
    assert gm.game_state["dark_turns"] == 0


# ---------------------------------------------------------------------------
# _check_darkness — dark location with light
# ---------------------------------------------------------------------------

def test_check_darkness_returns_false_when_flashlight_lit(monkeypatch, gm):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    gm.game_state["flashlight_lit"] = True
    assert gm._check_darkness() is False


def test_check_darkness_does_not_increment_turns_with_light(monkeypatch, gm):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    gm.game_state["flashlight_lit"] = True
    gm._check_darkness()
    assert gm.game_state["dark_turns"] == 0


# ---------------------------------------------------------------------------
# _check_darkness — dark location, no light (turn 1: warning)
# ---------------------------------------------------------------------------

def test_check_darkness_first_turn_returns_false(monkeypatch, gm):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    gm.game_state["flashlight_lit"] = False
    gm.game_state["dark_turns"] = 0
    assert gm._check_darkness() is False


def test_check_darkness_first_turn_increments_counter(monkeypatch, gm):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    gm.game_state["flashlight_lit"] = False
    gm.game_state["dark_turns"] = 0
    gm._check_darkness()
    assert gm.game_state["dark_turns"] == 1


def test_check_darkness_first_turn_prints_warning(monkeypatch, gm, capsys):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm.game_state["flashlight_lit"] = False
    gm.game_state["dark_turns"] = 0
    gm._check_darkness()
    assert any("dark" in m.lower() for m in messages)


# ---------------------------------------------------------------------------
# _check_darkness — dark location, no light (turn 2: grue)
# ---------------------------------------------------------------------------

def test_check_darkness_second_turn_calls_grue_death(monkeypatch, gm):
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    gm.game_state["flashlight_lit"] = False
    gm.game_state["dark_turns"] = 1     # already warned once

    grue_called = {"called": False}

    def fake_grue():
        grue_called["called"] = True
        return True

    monkeypatch.setattr(gm, "_handle_grue_death", fake_grue)
    gm._check_darkness()
    assert grue_called["called"] is True


# ---------------------------------------------------------------------------
# _handle_grue_death — no saves available
# ---------------------------------------------------------------------------

def test_grue_death_no_saves_returns_true(monkeypatch, gm):
    monkeypatch.setattr(gm.save_load_manager, "list_saves", lambda: [])
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: None)
    assert gm._handle_grue_death() is True


# ---------------------------------------------------------------------------
# _handle_grue_death — saves available, player declines restore
# ---------------------------------------------------------------------------

def test_grue_death_player_declines_restore_returns_true(monkeypatch, gm):
    saves = [{"name": "autosave", "date": "2026-01-01"}]
    monkeypatch.setattr(gm.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "n")
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: None)
    assert gm._handle_grue_death() is True


# ---------------------------------------------------------------------------
# _handle_grue_death — saves available, player restores successfully
# ---------------------------------------------------------------------------

def test_grue_death_successful_restore_returns_false(monkeypatch, gm):
    saves = [{"name": "autosave", "date": "2026-01-01"}]
    monkeypatch.setattr(gm.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "y")
    monkeypatch.setattr(gm.save_load_manager, "load_game", lambda inst, name: True)
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: None)
    assert gm._handle_grue_death() is False


# ---------------------------------------------------------------------------
# _handle_grue_death — saves available, load fails → game ends
# ---------------------------------------------------------------------------

def test_grue_death_failed_restore_returns_true(monkeypatch, gm):
    saves = [{"name": "autosave", "date": "2026-01-01"}]
    monkeypatch.setattr(gm.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "y")
    monkeypatch.setattr(gm.save_load_manager, "load_game", lambda inst, name: False)
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: None)
    assert gm._handle_grue_death() is True


# ---------------------------------------------------------------------------
# grue message content
# ---------------------------------------------------------------------------

def test_grue_death_prints_eaten_message(monkeypatch, gm):
    monkeypatch.setattr(gm.save_load_manager, "list_saves", lambda: [])
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm._handle_grue_death()
    combined = " ".join(messages).lower()
    assert "grue" in combined
