"""Tests for district sigils: first-visit art via the media layer."""

import pytest

import emerald_shadows.location_manager as location_manager_module
from emerald_shadows import game_art, media
from emerald_shadows.config_locations import LOCATIONS
from emerald_shadows.location_manager import LocationManager


SIGIL_MOMENTS = [key for key in media.MOMENTS if key.startswith("enter_")]


def test_sigil_moments_map_to_real_locations():
    assert SIGIL_MOMENTS, "expected at least one district sigil"
    for key in SIGIL_MOMENTS:
        location = key[len("enter_"):]
        assert location in LOCATIONS, f"sigil '{key}' names unknown location '{location}'"


@pytest.mark.parametrize("key", SIGIL_MOMENTS)
def test_sigils_fit_minimum_terminal_width(key):
    art = media.MOMENTS[key]["art"]
    lines = art.strip("\n").splitlines()
    assert max(len(line) for line in lines) <= 60


def test_present_location_unknown_location_is_noop():
    assert media.present_location("police_station") is False  # curated out
    assert media.present_location("no_such_place") is False


def test_first_visit_presents_sigil_once(monkeypatch):
    lm = LocationManager()
    shown = []
    monkeypatch.setattr(location_manager_module, "present_location", shown.append)
    monkeypatch.setattr(location_manager_module, "print_text", lambda t, **_: None)

    lm._announce_first_visit("smith_tower")
    lm._announce_first_visit("smith_tower")
    assert shown == ["smith_tower"]


def test_movement_triggers_first_visit_announcement(monkeypatch):
    lm = LocationManager()
    shown = []
    monkeypatch.setattr(location_manager_module, "present_location", shown.append)
    monkeypatch.setattr(location_manager_module, "print_text", lambda t, **_: None)

    game_state = {}
    assert lm.move_to_location("outside", game_state) is True  # street
    assert shown == ["street"]
    # Walking back and out again must not re-announce
    lm.move_to_location("station", game_state)
    lm.move_to_location("outside", game_state)
    assert shown == ["street", "police_station"]
