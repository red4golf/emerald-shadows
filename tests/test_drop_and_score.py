"""Tests for the drop command and score system."""

import pytest

import emerald_shadows.game_manager as game_manager_module
from emerald_shadows.game_manager import GameManager
from emerald_shadows.item_manager import ItemManager
from emerald_shadows.config import INITIAL_GAME_STATE


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def gm():
    return GameManager()


@pytest.fixture()
def item_manager():
    return ItemManager()


@pytest.fixture()
def game_state():
    return INITIAL_GAME_STATE.copy()


# ---------------------------------------------------------------------------
# drop_item — ItemManager
# ---------------------------------------------------------------------------

def test_drop_item_removes_from_inventory(item_manager):
    item_manager.inventory.append("notebook")
    assert item_manager.drop_item("notebook") is True
    assert "notebook" not in item_manager.get_inventory()


def test_drop_item_returns_false_when_not_carrying(item_manager, capsys):
    assert item_manager.drop_item("notebook") is False


def test_drop_item_prints_message(item_manager, capsys):
    item_manager.inventory.append("badge")
    item_manager.drop_item("badge")
    out = capsys.readouterr().out
    assert "badge" in out.lower()


def test_drop_item_does_not_affect_other_inventory(item_manager):
    item_manager.inventory.extend(["badge", "notebook"])
    item_manager.drop_item("badge")
    assert "notebook" in item_manager.get_inventory()


# ---------------------------------------------------------------------------
# _handle_drop_item — GameManager
# ---------------------------------------------------------------------------

def test_handle_drop_calls_drop_and_add(monkeypatch, gm):
    dropped = {}
    added = {}

    monkeypatch.setattr(gm.item_manager, "drop_item", lambda item: dropped.update(item=item) or True)
    monkeypatch.setattr(gm.location_manager, "add_item", lambda item: added.update(item=item))

    gm._handle_drop_item("badge")
    assert dropped.get("item") == "badge"
    assert added.get("item") == "badge"


def test_handle_drop_no_item_prints_prompt(monkeypatch, gm):
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm._handle_drop_item("")
    assert any("drop what" in m.lower() for m in messages)


def test_handle_drop_skips_add_when_drop_fails(monkeypatch, gm):
    added = {"called": False}
    monkeypatch.setattr(gm.item_manager, "drop_item", lambda item: False)
    monkeypatch.setattr(gm.location_manager, "add_item", lambda item: added.update(called=True))
    gm._handle_drop_item("ghost_item")
    assert added["called"] is False


# ---------------------------------------------------------------------------
# Score — taking items
# ---------------------------------------------------------------------------

def test_taking_badge_awards_score(item_manager, game_state):
    item_manager.take_item("badge", ["badge"], game_state)
    assert game_state["score"] == 10


def test_taking_binoculars_awards_score(item_manager, game_state):
    item_manager.take_item("binoculars", ["binoculars"], game_state)
    assert game_state["score"] == 10


def test_taking_cipher_wheel_awards_score(item_manager, game_state):
    item_manager.take_item("cipher_wheel", ["cipher_wheel"], game_state)
    assert game_state["score"] == 10


def test_taking_note_awards_five_points(item_manager, game_state):
    item_manager.take_item("note_1", ["note_1"], game_state)
    assert game_state["score"] == 5


def test_taking_all_five_notes_awards_bonus(item_manager, game_state):
    for n in ["note_1", "note_2", "note_3", "note_4", "note_5"]:
        item_manager.take_item(n, [n], game_state)
    # 5 notes × 5pts + 10pt bonus = 35
    assert game_state["score"] == 35


# ---------------------------------------------------------------------------
# Score — examining key items
# ---------------------------------------------------------------------------

def test_examining_informant_note_awards_score(item_manager, game_state):
    item_manager.inventory.append("informant_note")
    item_manager.examine_item("informant_note", [], game_state)
    assert game_state["score"] == 10


def test_examining_informant_note_only_awards_once(item_manager, game_state):
    item_manager.inventory.append("informant_note")
    item_manager.examine_item("informant_note", [], game_state)
    item_manager.examine_item("informant_note", [], game_state)
    assert game_state["score"] == 10


def test_examining_bulletin_notice_awards_score(item_manager, game_state):
    item_manager.inventory.append("bulletin_notice")
    item_manager.examine_item("bulletin_notice", [], game_state)
    assert game_state["score"] == 10


# ---------------------------------------------------------------------------
# Score — combining items
# ---------------------------------------------------------------------------

def test_combining_items_awards_score(item_manager, game_state):
    item_manager.inventory.extend(["notebook", "cipher_wheel"])
    item_manager.combine_items("notebook", "cipher_wheel", game_state)
    assert game_state["score"] == 15


def test_combining_items_only_awards_once(item_manager, game_state):
    item_manager.inventory.extend(["notebook", "cipher_wheel"])
    item_manager.combine_items("notebook", "cipher_wheel", game_state)
    item_manager.combine_items("notebook", "cipher_wheel", game_state)
    assert game_state["score"] == 15


# ---------------------------------------------------------------------------
# Score — solving puzzles
# ---------------------------------------------------------------------------

def test_solving_puzzle_awards_score():
    from emerald_shadows.puzzles.puzzle_manager import PuzzleManager
    game_state = INITIAL_GAME_STATE.copy()
    pm = PuzzleManager(solution_provider=lambda loc: "415.6")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert game_state["score"] == 25


def test_wrong_puzzle_answer_awards_no_score():
    from emerald_shadows.puzzles.puzzle_manager import PuzzleManager
    game_state = INITIAL_GAME_STATE.copy()
    pm = PuzzleManager(solution_provider=lambda loc: "000.0")
    pm.handle_puzzle("warehouse_office", {"radio_manual"}, game_state)
    assert game_state["score"] == 0


# ---------------------------------------------------------------------------
# Score — binoculars use
# ---------------------------------------------------------------------------

def test_binoculars_at_observation_deck_awards_score(item_manager, game_state):
    item_manager.inventory.append("binoculars")
    item_manager.use_item("binoculars", "observation_deck", game_state)
    assert game_state["score"] == 10


def test_binoculars_score_only_awarded_once(item_manager, game_state):
    item_manager.inventory.append("binoculars")
    item_manager.use_item("binoculars", "observation_deck", game_state)
    item_manager.use_item("binoculars", "observation_deck", game_state)
    assert game_state["score"] == 10


# ---------------------------------------------------------------------------
# Score — display
# ---------------------------------------------------------------------------

def test_handle_score_prints_score(monkeypatch, gm):
    gm.game_state["score"] = 42
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm._handle_score(None)
    assert any("42" in m for m in messages)


def test_show_inventory_includes_score(item_manager, game_state, capsys):
    game_state["score"] = 75
    item_manager.show_inventory(game_state)
    out = capsys.readouterr().out
    assert "75" in out
