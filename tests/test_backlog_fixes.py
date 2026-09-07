"""Tests for the backlog cleanup: item/location reference integrity,
trolley command feedback, darkness text dedup, and victory art."""

import pytest

import emerald_shadows.location_manager as location_manager_module
from emerald_shadows import game_art, media
from emerald_shadows.config_locations import LOCATIONS
from emerald_shadows.game_manager import GameManager, DARK_WARNING
from emerald_shadows.item_manager import ITEM_DESCRIPTIONS


# ---------------------------------------------------------------------------
# Config integrity: item data may only reference locations that exist
# ---------------------------------------------------------------------------

def test_use_locations_reference_real_locations():
    for item, data in ITEM_DESCRIPTIONS.items():
        for loc in data.get("use_locations", []):
            assert loc in LOCATIONS, f"{item} use_locations references unknown location '{loc}'"


def test_use_effect_keys_reference_real_locations():
    for item, data in ITEM_DESCRIPTIONS.items():
        for loc in data.get("use_effects", {}):
            if loc == "all":
                continue
            assert loc in LOCATIONS, f"{item} use_effects references unknown location '{loc}'"


def test_npc_locations_reference_real_locations():
    from emerald_shadows.config_dialogue import NPCS
    for key, npc in NPCS.items():
        assert npc["location"] in LOCATIONS, f"NPC '{key}' placed in unknown location '{npc['location']}'"


def test_location_exits_reference_real_locations():
    for name, data in LOCATIONS.items():
        for exit_name, target in data["exits"].items():
            assert target in LOCATIONS, f"{name} exit '{exit_name}' leads to unknown location '{target}'"


# ---------------------------------------------------------------------------
# Trolley commands respond off the tram instead of silently doing nothing
# ---------------------------------------------------------------------------

def test_trolley_command_off_trolley_prints_message(monkeypatch):
    gm = GameManager()
    messages = []
    monkeypatch.setattr(location_manager_module, "print_text", lambda t, **_: messages.append(t))
    assert gm.location_manager.current_location != "trolley"
    gm.location_manager.handle_trolley_command("status")
    assert any("not aboard" in m.lower() for m in messages)


def test_trolley_invalid_command_lists_options(monkeypatch):
    gm = GameManager()
    messages = []
    monkeypatch.setattr(location_manager_module, "print_text", lambda t, **_: messages.append(t))
    gm.location_manager.current_location = "trolley"
    gm.location_manager.handle_trolley_command("juggle")
    combined = " ".join(messages)
    assert "next" in combined and "status" in combined


# ---------------------------------------------------------------------------
# Darkness warning is a single shared constant
# ---------------------------------------------------------------------------

def test_dark_warning_constant_used_by_look(monkeypatch):
    import emerald_shadows.game_manager as gm_module
    gm = GameManager()
    messages = []
    monkeypatch.setattr(gm_module, "print_text", lambda t, **_: messages.append(t))
    monkeypatch.setattr(gm.location_manager, "is_dark", lambda: True)
    gm.game_state["flashlight_lit"] = False
    gm._handle_look(None)
    assert DARK_WARNING in messages


# ---------------------------------------------------------------------------
# Victory art
# ---------------------------------------------------------------------------

def test_victory_moment_registered():
    assert "victory" in media.MOMENTS
    assert media.MOMENTS["victory"]["art"] == game_art.VICTORY_ART


@pytest.mark.parametrize("art", [game_art.GRUE_ART, game_art.VICTORY_ART], ids=["grue", "victory"])
def test_art_fits_minimum_terminal_width(art):
    lines = art.strip("\n").splitlines()
    assert max(len(line) for line in lines) <= 60


def test_victory_art_lines_align():
    lines = [l for l in game_art.VICTORY_ART.strip("\n").splitlines()]
    # Every boxed row (starting with '|') must be the same width
    boxed = [l for l in lines if l.startswith("|")]
    assert len(set(len(l) for l in boxed)) == 1, "victory stamp rows are ragged"
