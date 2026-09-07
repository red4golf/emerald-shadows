"""Tests for trolley boarding position and location-aware boarding."""

import pytest
from emerald_shadows.trolley_system import TrolleySystem
from emerald_shadows.location_manager import LocationManager
from emerald_shadows.config import INITIAL_GAME_STATE


@pytest.fixture()
def trolley():
    return TrolleySystem()


@pytest.fixture()
def location_manager():
    return LocationManager()


# ---------------------------------------------------------------------------
# set_boarding_position — TrolleySystem
# ---------------------------------------------------------------------------

def test_boarding_from_pike_place_sets_position_0(trolley):
    trolley.set_boarding_position("pike_place")
    assert trolley.position == 0


def test_boarding_from_pioneer_square_sets_position_1(trolley):
    trolley.set_boarding_position("pioneer_square")
    assert trolley.position == 1


def test_boarding_from_waterfront_sets_position_2(trolley):
    trolley.set_boarding_position("waterfront")
    assert trolley.position == 2


def test_boarding_from_docks_sets_position_2(trolley):
    """Docks are near the waterfront — should snap to stop 2."""
    trolley.set_boarding_position("docks")
    assert trolley.position == 2


def test_boarding_from_smith_tower_sets_position_3(trolley):
    trolley.set_boarding_position("smith_tower")
    assert trolley.position == 3


def test_boarding_from_unknown_location_defaults_to_0(trolley):
    trolley.set_boarding_position("nowhere_special")
    assert trolley.position == 0


# ---------------------------------------------------------------------------
# Exit from correct stop after boarding
# ---------------------------------------------------------------------------

def test_boarding_from_smith_tower_initial_exit_is_smith_tower(trolley):
    trolley.set_boarding_position("smith_tower")
    current_stop = trolley.routes[trolley.position]
    assert current_stop["exits"]["off"] == "smith_tower"


def test_boarding_from_docks_initial_exit_is_waterfront(trolley):
    trolley.set_boarding_position("docks")
    current_stop = trolley.routes[trolley.position]
    assert current_stop["exits"]["off"] == "waterfront"


def test_boarding_from_pike_place_initial_exit_is_pike_place(trolley):
    trolley.set_boarding_position("pike_place")
    current_stop = trolley.routes[trolley.position]
    assert current_stop["exits"]["off"] == "pike_place"


# ---------------------------------------------------------------------------
# LocationManager._handle_trolley_movement sets position before boarding
# ---------------------------------------------------------------------------

def test_trolley_position_set_correctly_when_boarding_from_smith_tower(location_manager):
    """Boarding the trolley from smith_tower should snap to stop 3."""
    game_state = INITIAL_GAME_STATE.copy()
    location_manager.current_location = "smith_tower"
    location_manager.move_to_location("trolley", game_state)
    assert location_manager.trolley.position == 3


def test_trolley_position_set_correctly_when_boarding_from_docks(location_manager):
    """Boarding from docks should snap to waterfront stop (2)."""
    game_state = INITIAL_GAME_STATE.copy()
    location_manager.current_location = "docks"
    location_manager.move_to_location("trolley", game_state)
    assert location_manager.trolley.position == 2


def test_trolley_exit_reflects_boarding_position(location_manager):
    """After boarding from smith_tower, 'off' exit should return to smith_tower."""
    game_state = INITIAL_GAME_STATE.copy()
    location_manager.current_location = "smith_tower"
    location_manager.move_to_location("trolley", game_state)
    trolley_location = location_manager.locations["trolley"]
    assert trolley_location.exits.get("off") == "smith_tower"


# ---------------------------------------------------------------------------
# Disembarking — regression cover for two bugs that softlocked the game
# ---------------------------------------------------------------------------

def _boarded_manager():
    from emerald_shadows.location_manager import LocationManager

    lm = LocationManager()
    lm.current_location = "smith_tower"
    lm.move_to_location("trolley", {})
    return lm


def test_off_actually_leaves_the_trolley():
    """'off' used to be routed into the movement handler, which only toggled
    whether the tram was rolling. A player who boarded could never get out."""
    lm = _boarded_manager()
    assert lm.current_location == "trolley"

    lm.handle_trolley_command("off")
    assert lm.current_location == "smith_tower"
    assert lm.trolley.on_trolley is False


def test_can_board_and_disembark_more_than_once():
    """board_trolley() was only called on the location's first visit, so the
    second ride left on_trolley False and could never be got off again."""
    lm = _boarded_manager()
    lm.handle_trolley_command("off")

    lm.move_to_location("trolley", {})
    assert lm.trolley.on_trolley is True
    lm.handle_trolley_command("off")
    assert lm.current_location == "smith_tower"


def test_cannot_step_off_a_moving_tram():
    lm = _boarded_manager()
    lm.handle_trolley_command("next")
    assert lm.trolley.in_motion is True

    lm.handle_trolley_command("off")
    assert lm.current_location == "trolley"


def test_riding_to_a_named_stop_and_stepping_off():
    lm = _boarded_manager()
    for _ in range(12):
        stop = lm.trolley.routes[lm.trolley.position]["exits"]["off"]
        if stop == "pioneer_square" and not lm.trolley.in_motion:
            break
        lm.handle_trolley_command("next")
    lm.handle_trolley_command("off")
    assert lm.current_location == "pioneer_square"


def test_pioneer_square_is_reachable_only_by_tram():
    """If this stops being true, the tram bugs stop being fatal — but the
    walkthrough assumes the ride, so it should fail loudly instead."""
    from emerald_shadows.config_locations import LOCATIONS

    approaches = [
        name for name, data in LOCATIONS.items()
        if "pioneer_square" in data["exits"].values()
    ]
    assert approaches == []
