"""Tests for ItemManager."""

import pytest
from emerald_shadows.item_manager import ItemManager
from emerald_shadows.config import INITIAL_GAME_STATE


@pytest.fixture
def item_manager():
    return ItemManager()


@pytest.fixture
def game_state():
    return INITIAL_GAME_STATE.copy()


# --- take_item ---

def test_take_item_adds_to_inventory(item_manager, game_state):
    assert item_manager.take_item("badge", ["badge"], game_state) is True
    assert "badge" in item_manager.get_inventory()


def test_take_item_sets_has_badge(item_manager, game_state):
    item_manager.take_item("badge", ["badge"], game_state)
    assert game_state["has_badge"] is True


def test_take_item_missing_from_location(item_manager, game_state):
    assert item_manager.take_item("notebook", [], game_state) is False
    assert "notebook" not in item_manager.get_inventory()


def test_take_note_increments_counter(item_manager, game_state):
    item_manager.take_item("note_1", ["note_1"], game_state)
    assert item_manager.notes_found == 1


def test_take_five_notes_sets_found_all_notes(item_manager, game_state):
    notes = [f"note_{i}" for i in range(1, 6)]
    for note in notes:
        item_manager.take_item(note, [note], game_state)
    assert game_state.get("found_all_notes") is True


# --- examine_item ---

def test_examine_item_in_inventory(item_manager, game_state):
    item_manager.inventory.append("cipher_wheel")
    # Should not raise; we check that examined_cipher is set
    item_manager.examine_item("cipher_wheel", [], game_state)
    assert game_state["examined_cipher"] is True


def test_examine_informant_note_sets_frequency_flag(item_manager, game_state):
    item_manager.inventory.append("informant_note")
    item_manager.examine_item("informant_note", [], game_state)
    assert game_state["found_emergency_frequency"] is True


def test_examine_bulletin_notice_sets_organization_flag(item_manager, game_state):
    item_manager.inventory.append("bulletin_notice")
    item_manager.examine_item("bulletin_notice", [], game_state)
    assert game_state["identified_organization"] is True


def test_examine_item_not_in_inventory_or_location(item_manager, game_state, capsys):
    item_manager.examine_item("ghost_item", [], game_state)
    out = capsys.readouterr().out
    assert "don't see" in out.lower()


# --- use_item ---

def test_use_item_not_in_inventory(item_manager, game_state, capsys):
    item_manager.use_item("badge", "police_station", game_state)
    out = capsys.readouterr().out
    assert "don't have" in out.lower()


def test_use_item_in_valid_location(item_manager, game_state, capsys):
    item_manager.inventory.append("badge")
    item_manager.use_item("badge", "smith_tower", game_state)
    out = capsys.readouterr().out
    assert "badge" in out.lower()


def test_use_binoculars_sets_surveilled_docks(item_manager, game_state):
    item_manager.inventory.append("binoculars")
    item_manager.use_item("binoculars", "observation_deck", game_state)
    assert game_state["surveilled_docks"] is True
    assert game_state.get("observed_activity", False) is False  # no longer set by binoculars


# --- combine_items ---

def test_combine_sets_decoded_notes(item_manager, game_state):
    item_manager.inventory.extend(["notebook", "cipher_wheel"])
    assert item_manager.combine_items("notebook", "cipher_wheel", game_state) is True
    assert game_state["decoded_notes"] is True


def test_combine_already_discovered(item_manager, game_state, capsys):
    item_manager.inventory.extend(["notebook", "cipher_wheel"])
    item_manager.combine_items("notebook", "cipher_wheel", game_state)
    result = item_manager.combine_items("notebook", "cipher_wheel", game_state)
    assert result is False
    out = capsys.readouterr().out
    assert "already" in out.lower()


def test_combine_missing_item(item_manager, game_state, capsys):
    item_manager.inventory.append("notebook")
    assert item_manager.combine_items("notebook", "cipher_wheel", game_state) is False


def test_combine_incompatible_items(item_manager, game_state, capsys):
    item_manager.inventory.extend(["badge", "binoculars"])
    assert item_manager.combine_items("badge", "binoculars", game_state) is False


# --- inventory state serialization ---

def test_inventory_state_round_trip(item_manager, game_state):
    item_manager.inventory.extend(["notebook", "cipher_wheel"])
    item_manager.combine_items("notebook", "cipher_wheel", game_state)

    state = item_manager.get_inventory_state()
    new_manager = ItemManager()
    new_manager.restore_inventory_state(state)

    assert new_manager.get_inventory() == item_manager.get_inventory()
    assert new_manager.notes_found == item_manager.notes_found
    # Combination should still be considered discovered after restore
    from emerald_shadows.item_manager import ITEM_COMBINATIONS
    combo = frozenset(["notebook", "cipher_wheel"])
    assert combo in new_manager.discovered_combinations


def test_inventory_state_serializable_to_json(item_manager, game_state):
    import json
    item_manager.inventory.extend(["notebook", "cipher_wheel"])
    item_manager.combine_items("notebook", "cipher_wheel", game_state)
    state = item_manager.get_inventory_state()
    # Must not raise
    serialized = json.dumps(state)
    assert serialized


# --- show_inventory ---

def test_show_empty_inventory(item_manager, capsys):
    item_manager.show_inventory()
    out = capsys.readouterr().out
    assert "empty" in out.lower()


def test_show_inventory_lists_items(item_manager, capsys):
    item_manager.inventory.append("badge")
    item_manager.show_inventory()
    out = capsys.readouterr().out
    assert "badge" in out


# --- binoculars at waterfront sets surveilled_docks ---

def test_binoculars_at_waterfront_sets_surveilled_docks(item_manager, game_state):
    item_manager.inventory.append("binoculars")
    item_manager.use_item("binoculars", "waterfront", game_state)
    assert game_state["surveilled_docks"] is True


def test_binoculars_at_waterfront_does_not_set_observed_activity(item_manager, game_state):
    item_manager.inventory.append("binoculars")
    item_manager.use_item("binoculars", "waterfront", game_state)
    assert game_state.get("observed_activity", False) is False


def test_binoculars_surveilled_docks_set_once_regardless_of_location(item_manager, game_state):
    """Using binoculars at observation_deck then waterfront awards points only once."""
    item_manager.inventory.append("binoculars")
    item_manager.use_item("binoculars", "observation_deck", game_state)
    score_after_first = game_state["score"]
    item_manager.use_item("binoculars", "waterfront", game_state)
    assert game_state["score"] == score_after_first  # no additional points
