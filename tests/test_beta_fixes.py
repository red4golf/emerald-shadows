"""Tests for the pre-beta fixes: movement vocabulary, take all,
grue restore picking the newest save, and puzzle state persistence."""

import builtins
import pytest

import emerald_shadows.game_manager as game_manager_module
from emerald_shadows.game_manager import GameManager
from emerald_shadows.puzzles.puzzle_manager import PuzzleManager
from emerald_shadows.utils import SaveLoadManager


@pytest.fixture()
def gm(monkeypatch):
    game = GameManager()
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: None)
    return game


# ---------------------------------------------------------------------------
# Movement: named exits, synonyms, bare-word fallback
# ---------------------------------------------------------------------------

def test_resolve_exit_exact_named_exit(gm):
    assert gm.location_manager.current_location == "police_station"
    assert gm.location_manager.resolve_exit("outside") == "outside"


def test_resolve_exit_synonym_o_for_outside(gm):
    assert gm.location_manager.resolve_exit("o") == "outside"


def test_resolve_exit_up_resolves_to_upstairs(gm):
    assert gm.location_manager.resolve_exit("up") == "upstairs"


def test_resolve_exit_rejects_nonsense(gm):
    assert gm.location_manager.resolve_exit("sideways") is None


def test_bare_named_exit_moves_player(gm):
    gm.process_command("outside")
    assert gm.location_manager.current_location == "street"


def test_bare_o_moves_player_outside(gm):
    gm.process_command("o")
    assert gm.location_manager.current_location == "street"


def test_bare_up_moves_player_upstairs(gm):
    gm.process_command("up")
    assert gm.location_manager.current_location == "evidence_room"


def test_go_up_resolves_to_upstairs(gm):
    gm.process_command("go up")
    assert gm.location_manager.current_location == "evidence_room"


def test_bare_named_exit_only_single_word(gm):
    gm.process_command("outside please")
    assert gm.location_manager.current_location == "police_station"


def test_unknown_word_still_rejected(gm):
    gm.process_command("flarp")
    assert gm.location_manager.current_location == "police_station"


# ---------------------------------------------------------------------------
# exits command
# ---------------------------------------------------------------------------

def test_exits_command_lists_ways_out(monkeypatch):
    gm = GameManager()
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm.process_command("exits")
    combined = " ".join(messages)
    assert "outside" in combined and "upstairs" in combined


# ---------------------------------------------------------------------------
# take all
# ---------------------------------------------------------------------------

def test_take_all_empties_location(gm):
    gm.process_command("take all")
    inventory = gm.item_manager.get_inventory()
    assert "badge" in inventory and "case_file" in inventory
    assert gm.location_manager.get_available_items() == []


def test_take_all_in_empty_location(monkeypatch):
    gm = GameManager()
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm.location_manager.locations["police_station"].items = []
    gm.process_command("take all")
    assert any("nothing here" in m.lower() for m in messages)
    assert gm.item_manager.get_inventory() == []


# ---------------------------------------------------------------------------
# Grue restore picks the NEWEST save
# ---------------------------------------------------------------------------

def test_grue_restore_uses_newest_save(monkeypatch, gm):
    # list_saves() returns newest-first
    saves = [
        {"name": "newest", "date": "2026-06-08"},
        {"name": "oldest", "date": "2026-01-01"},
    ]
    monkeypatch.setattr(gm.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "y")
    loaded = []
    monkeypatch.setattr(
        gm.save_load_manager, "load_game",
        lambda inst, name: loaded.append(name) or True,
    )
    assert gm._handle_grue_death() is False
    assert loaded == ["newest"]


# ---------------------------------------------------------------------------
# Puzzle state persistence
# ---------------------------------------------------------------------------

def test_puzzle_manager_state_roundtrip():
    pm = PuzzleManager()
    pm.solved_puzzles = {"evidence_room", "warehouse_office"}
    state = pm.get_state()

    fresh = PuzzleManager()
    fresh.restore_state(state)
    assert fresh.solved_puzzles == {"evidence_room", "warehouse_office"}


def test_puzzle_manager_restore_tolerates_old_saves():
    pm = PuzzleManager()
    pm.solved_puzzles = {"evidence_room"}
    pm.restore_state(None)  # save predates puzzle_state field
    assert pm.solved_puzzles == set()


def test_save_load_roundtrips_solved_puzzles(tmp_path, monkeypatch):
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: None)
    manager = SaveLoadManager(str(tmp_path / "saves"))

    source = GameManager()
    source.puzzle_manager.solved_puzzles = {"evidence_room"}
    assert manager.save_game(source, "puzzle_roundtrip") is True

    target = GameManager()
    assert target.puzzle_manager.solved_puzzles == set()
    assert manager.load_game(target, "puzzle_roundtrip") is True
    assert target.puzzle_manager.solved_puzzles == {"evidence_room"}
