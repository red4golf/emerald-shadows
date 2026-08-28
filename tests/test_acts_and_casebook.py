"""Tests for the three-act structure, the casebook, and the Pier 7 finale."""

from copy import deepcopy

import pytest

from emerald_shadows import acts, casebook
from emerald_shadows.config import INITIAL_GAME_STATE

ACT_TWO_FLAGS = ["decoded_notes", "identified_organization"]
ACT_THREE_FLAGS = [
    "found_warehouse", "observed_activity", "identified_suspect", "identified_vehicle",
]


@pytest.fixture
def state():
    return deepcopy(INITIAL_GAME_STATE)


def _reach_act(state, act):
    if act >= 2:
        for flag in ACT_TWO_FLAGS:
            state[flag] = True
    if act >= 3:
        for flag in ACT_THREE_FLAGS:
            state[flag] = True
    return state


# --- act computation ---

def test_starts_in_act_one(state):
    assert acts.current_act(state) == 1


def test_act_two_requires_a_decoded_memo_and_a_name(state):
    state["decoded_notes"] = True
    assert acts.current_act(state) == 1
    state["identified_organization"] = True
    assert acts.current_act(state) == 2


def test_act_three_requires_the_full_investigation(state):
    _reach_act(state, 2)
    for flag in ACT_THREE_FLAGS[:-1]:
        state[flag] = True
    assert acts.current_act(state) == 2
    state[ACT_THREE_FLAGS[-1]] = True
    assert acts.current_act(state) == 3


def test_act_is_derived_not_stored(state):
    """A loaded save lands in the right act without carrying the act itself."""
    _reach_act(state, 3)
    assert acts.current_act(deepcopy(state)) == 3


# --- advancement ---

def test_advance_fires_once_per_act(state):
    _reach_act(state, 2)
    assert acts.check_advance(state) == 2
    assert acts.check_advance(state) is None


def test_advance_from_one_to_three_reports_three(state):
    _reach_act(state, 3)
    assert acts.check_advance(state) == 3


def test_act_never_walks_backwards(state):
    _reach_act(state, 2)
    acts.check_advance(state)
    # A flag going missing must not demote the player back to act one.
    state["decoded_notes"] = False
    acts.check_advance(state)
    assert state["act_seen"] == 2


def test_each_later_act_has_an_opening(state):
    assert acts.opening_text(2)
    assert acts.opening_text(3)
    assert acts.opening_text(1) is None


def test_missing_for_next_act_lists_outstanding_flags(state):
    assert set(acts.missing_for_next_act(state)) == set(ACT_TWO_FLAGS)
    _reach_act(state, 3)
    assert acts.missing_for_next_act(state) == []


def test_act_label_names_the_act(state):
    assert "Legwork" in acts.act_label(state)
    _reach_act(state, 3)
    assert "Pier Seven" in acts.act_label(state)


# --- the finale's evidence requirement ---

def test_arrest_needs_the_evidence():
    assert acts.missing_finale_items([]) == list(acts.FINALE_ITEMS)


def test_arrest_satisfied_by_a_full_pocket():
    assert acts.missing_finale_items(list(acts.FINALE_ITEMS)) == []


def test_every_finale_item_is_a_real_item():
    from emerald_shadows.item_manager import ITEM_DESCRIPTIONS

    for item in acts.FINALE_ITEMS:
        assert item in ITEM_DESCRIPTIONS


def test_every_finale_item_can_be_found_in_the_world():
    from emerald_shadows.config_locations import LOCATIONS

    placed = {item for loc in LOCATIONS.values() for item in loc.get("items", [])}
    assert set(acts.FINALE_ITEMS) <= placed


# --- casebook ---

def test_casebook_reports_the_act(state):
    assert "Act 1" in casebook.render(state, [], {})


def test_casebook_lists_open_threads_at_the_start(state):
    assert "OPEN" in casebook.render(state, [], {})


def test_casebook_promotes_a_thread_to_established(state):
    state["decoded_notes"] = True
    rendered = casebook.render(state, [], {})
    assert "ESTABLISHED" in rendered
    assert "Password 'angels'" in rendered


def test_casebook_never_claims_more_than_is_earned(state):
    rendered = casebook.render(state, [], {})
    assert "ESTABLISHED" not in rendered
    assert "PEOPLE" not in rendered


def test_casebook_names_people_once_identified(state):
    state["mathers_confessed"] = True
    rendered = casebook.render(state, [], {})
    assert "PEOPLE" in rendered
    assert "Walt Mathers" in rendered


def test_casebook_shows_the_partial_plate(state):
    state["plate_fragments"] = ["photo"]
    assert "WA-44??" in casebook.render(state, [], {})


def test_casebook_hides_the_plate_before_any_fragment(state):
    assert "WA-" not in casebook.render(state, [], {})


def test_casebook_points_at_the_pier_in_act_three(state):
    _reach_act(state, 3)
    assert "Pier 7" in casebook.render(state, [], {})


def test_every_casebook_flag_exists_in_initial_state():
    """A typo'd flag would silently never render."""
    known = set(INITIAL_GAME_STATE) | {"tuned_frequency", "case_closed", "act_three"}
    for entry in casebook.FACTS + casebook.PEOPLE + casebook.OPEN:
        assert entry["flag"] in known, f"unknown flag {entry['flag']}"
