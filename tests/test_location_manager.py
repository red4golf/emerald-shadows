"""Tests for LocationManager."""

import pytest
from emerald_shadows.location_manager import LocationManager
from emerald_shadows.config import INITIAL_GAME_STATE, STARTING_LOCATION


@pytest.fixture
def location_manager():
    return LocationManager()


@pytest.fixture
def game_state():
    return INITIAL_GAME_STATE.copy()


# --- initialization ---

def test_starts_at_police_station(location_manager):
    assert location_manager.current_location == STARTING_LOCATION


def test_all_locations_have_descriptions(location_manager):
    for name, loc in location_manager.locations.items():
        assert loc.description, f"{name} has no description"


def test_all_exits_reference_valid_locations(location_manager):
    for name, loc in location_manager.locations.items():
        for direction, dest in loc.exits.items():
            if dest != "trolley":
                assert dest in location_manager.locations, (
                    f"{name} exit '{direction}' points to unknown location '{dest}'"
                )


# --- movement ---

def test_move_valid_direction(location_manager, game_state):
    result = location_manager.move_to_location("upstairs", game_state)
    assert result is True
    assert location_manager.current_location == "evidence_room"


def test_move_invalid_direction(location_manager, game_state, capsys):
    result = location_manager.move_to_location("nowhere", game_state)
    assert result is False
    out = capsys.readouterr().out
    assert "can't go" in out.lower()


def test_move_requires_flag_blocks_entry(location_manager, game_state, capsys):
    # underground_tunnels requires found_warehouse
    location_manager.current_location = "docks"
    game_state["found_warehouse"] = False
    result = location_manager.move_to_location("underground", game_state)
    assert result is False


def test_move_requires_flag_allows_entry(location_manager, game_state):
    location_manager.current_location = "docks"
    game_state["found_warehouse"] = True
    result = location_manager.move_to_location("underground", game_state)
    assert result is True
    assert location_manager.current_location == "underground_tunnels"


def test_first_visit_shows_historical_note(location_manager, game_state, capsys):
    location_manager.move_to_location("upstairs", game_state)
    out = capsys.readouterr().out
    assert "historical" in out.lower()


def test_second_visit_no_historical_note(location_manager, game_state, capsys):
    # Visit evidence_room for the first time (note shown), go back, visit again
    location_manager.move_to_location("upstairs", game_state)
    capsys.readouterr()  # clear first-visit output
    location_manager.move_to_location("downstairs", game_state)
    capsys.readouterr()  # clear police_station first-visit output
    location_manager.move_to_location("upstairs", game_state)
    out = capsys.readouterr().out
    # Second visit to evidence_room should produce no historical note
    assert "historical" not in out.lower()


# --- items ---

def test_get_available_items(location_manager):
    items = location_manager.get_available_items()
    assert "badge" in items


def test_remove_item(location_manager):
    location_manager.remove_item("badge")
    assert "badge" not in location_manager.get_available_items()


def test_remove_nonexistent_item_is_safe(location_manager):
    # Should not raise
    location_manager.remove_item("ghost_item")


# --- description ---

def test_get_location_description_contains_exits(location_manager):
    desc = location_manager.get_location_description()
    assert "Exits" in desc


def test_get_location_description_contains_items(location_manager):
    desc = location_manager.get_location_description()
    assert "badge" in desc


# --- state serialization ---

def test_state_round_trip(location_manager, game_state):
    location_manager.move_to_location("upstairs", game_state)
    location_manager.remove_item("cipher_wheel")

    state = location_manager.get_state()
    new_manager = LocationManager()
    new_manager.restore_state(state)

    assert new_manager.current_location == "evidence_room"
    assert "cipher_wheel" not in new_manager.locations["evidence_room"].items


def test_state_serializable_to_json(location_manager):
    import json
    state = location_manager.get_state()
    # Must not raise
    serialized = json.dumps(state)
    assert serialized


# --- exits ---

def test_get_valid_exits(location_manager):
    exits = location_manager.get_valid_exits()
    assert "outside" in exits or "upstairs" in exits  # police_station has both
