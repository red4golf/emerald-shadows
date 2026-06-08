"""Tests for the three new location groups: Eagles Hall, Harbormaster's Shack,
and the Anchor Tavern."""

import pytest
import emerald_shadows.item_manager as item_manager_module
from emerald_shadows.config import (
    INITIAL_GAME_STATE,
    REQUIRED_ITEMS,
    REQUIRED_STATES,
)
from emerald_shadows.config_locations import LOCATIONS
from emerald_shadows.item_manager import ITEM_DESCRIPTIONS, ItemManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fresh_state():
    return INITIAL_GAME_STATE.copy()


def manager_with(*items):
    m = ItemManager()
    m.inventory = list(items)
    return m


# ---------------------------------------------------------------------------
# config.py — new wiring
# ---------------------------------------------------------------------------

def test_ches_tip_in_initial_game_state():
    assert "ches_tip" in INITIAL_GAME_STATE
    assert INITIAL_GAME_STATE["ches_tip"] is False


def test_ches_tip_in_required_states():
    assert "ches_tip" in REQUIRED_STATES


def test_meeting_minutes_in_required_items():
    assert "meeting_minutes" in REQUIRED_ITEMS


def test_manifest_in_required_items():
    assert "manifest" in REQUIRED_ITEMS


# ---------------------------------------------------------------------------
# config_locations.py — locations exist
# ---------------------------------------------------------------------------

def test_eagles_hall_in_locations():
    assert "eagles_hall" in LOCATIONS


def test_eagles_lounge_in_locations():
    assert "eagles_lounge" in LOCATIONS


def test_harbormaster_shack_in_locations():
    assert "harbormaster_shack" in LOCATIONS


def test_anchor_tavern_in_locations():
    assert "anchor_tavern" in LOCATIONS


# ---------------------------------------------------------------------------
# Exits — new connections
# ---------------------------------------------------------------------------

def test_street_has_west_exit_to_eagles_hall():
    assert LOCATIONS["street"]["exits"].get("west") == "eagles_hall"


def test_docks_has_shack_exit():
    assert LOCATIONS["docks"]["exits"].get("shack") == "harbormaster_shack"


def test_waterfront_has_tavern_exit():
    assert LOCATIONS["waterfront"]["exits"].get("tavern") == "anchor_tavern"


def test_eagles_hall_exits_back_to_lounge():
    assert LOCATIONS["eagles_hall"]["exits"].get("back") == "eagles_lounge"


def test_eagles_hall_exits_east_to_street():
    assert LOCATIONS["eagles_hall"]["exits"].get("east") == "street"


def test_eagles_lounge_exits_to_hall():
    assert LOCATIONS["eagles_lounge"]["exits"].get("hall") == "eagles_hall"


def test_harbormaster_shack_exits_to_docks():
    assert LOCATIONS["harbormaster_shack"]["exits"].get("outside") == "docks"


def test_anchor_tavern_exits_to_waterfront():
    assert LOCATIONS["anchor_tavern"]["exits"].get("outside") == "waterfront"


# ---------------------------------------------------------------------------
# Items present in new locations
# ---------------------------------------------------------------------------

def test_membership_register_in_eagles_hall():
    assert "membership_register" in LOCATIONS["eagles_hall"]["items"]


def test_meeting_minutes_in_eagles_lounge():
    assert "meeting_minutes" in LOCATIONS["eagles_lounge"]["items"]


def test_manifest_in_harbormaster_shack():
    assert "manifest" in LOCATIONS["harbormaster_shack"]["items"]


def test_anchor_tavern_starts_with_no_items():
    assert LOCATIONS["anchor_tavern"]["items"] == []


# ---------------------------------------------------------------------------
# item_manager — new items exist in ITEM_DESCRIPTIONS
# ---------------------------------------------------------------------------

def test_membership_register_has_description():
    assert "membership_register" in ITEM_DESCRIPTIONS
    assert ITEM_DESCRIPTIONS["membership_register"]["detailed"]


def test_meeting_minutes_has_description():
    assert "meeting_minutes" in ITEM_DESCRIPTIONS
    assert "Voss" in ITEM_DESCRIPTIONS["meeting_minutes"]["detailed"]


def test_manifest_has_description():
    assert "manifest" in ITEM_DESCRIPTIONS
    assert "3,200" in ITEM_DESCRIPTIONS["manifest"]["detailed"]


# ---------------------------------------------------------------------------
# Take messages — new items print specific flavour text
# ---------------------------------------------------------------------------

def test_take_membership_register_prints_flavour(monkeypatch):
    m = ItemManager()
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))
    state = fresh_state()

    result = m.take_item("membership_register", ["membership_register"], state)

    assert result is True
    assert any("roster" in msg.lower() or "porter" in msg.lower() for msg in messages)


def test_take_meeting_minutes_prints_flavour(monkeypatch):
    m = ItemManager()
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))
    state = fresh_state()

    result = m.take_item("meeting_minutes", ["meeting_minutes"], state)

    assert result is True
    assert any("Voss" in msg or "folder" in msg.lower() for msg in messages)


def test_take_manifest_prints_flavour(monkeypatch):
    m = ItemManager()
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))
    state = fresh_state()

    result = m.take_item("manifest", ["manifest"], state)

    assert result is True
    assert any("manifest" in msg.lower() or "board" in msg.lower() for msg in messages)


# ---------------------------------------------------------------------------
# Scoring — new items award points on take
# ---------------------------------------------------------------------------

def test_take_membership_register_awards_score(monkeypatch):
    m = ItemManager()
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.take_item("membership_register", ["membership_register"], state)

    assert state["score"] == 10


def test_take_meeting_minutes_awards_score(monkeypatch):
    m = ItemManager()
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.take_item("meeting_minutes", ["meeting_minutes"], state)

    assert state["score"] == 10


def test_take_manifest_awards_score(monkeypatch):
    m = ItemManager()
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.take_item("manifest", ["manifest"], state)

    assert state["score"] == 10


# ---------------------------------------------------------------------------
# badge use at eagles_hall — flavour only, no state change
# ---------------------------------------------------------------------------

def test_badge_use_at_eagles_hall_prints_porter_message(monkeypatch):
    m = manager_with("badge")
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))
    state = fresh_state()

    m.use_item("badge", "eagles_hall", state)

    combined = " ".join(messages).lower()
    assert "porter" in combined or "back room" in combined


def test_badge_use_at_eagles_hall_does_not_set_ches_tip(monkeypatch):
    m = manager_with("badge")
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.use_item("badge", "eagles_hall", state)

    assert state["ches_tip"] is False


# ---------------------------------------------------------------------------
# badge use at anchor_tavern — sets ches_tip, awards score, idempotent
# ---------------------------------------------------------------------------

def test_badge_use_at_anchor_tavern_sets_ches_tip(monkeypatch):
    m = manager_with("badge")
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.use_item("badge", "anchor_tavern", state)

    assert state["ches_tip"] is True


def test_badge_use_at_anchor_tavern_awards_score(monkeypatch):
    m = manager_with("badge")
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.use_item("badge", "anchor_tavern", state)

    assert state["score"] == 15


def test_badge_use_at_anchor_tavern_idempotent(monkeypatch):
    m = manager_with("badge")
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.use_item("badge", "anchor_tavern", state)
    m.use_item("badge", "anchor_tavern", state)

    assert state["score"] == 15  # awarded once only


def test_badge_use_at_anchor_tavern_prints_ches_dialogue(monkeypatch):
    m = manager_with("badge")
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))
    state = fresh_state()

    m.use_item("badge", "anchor_tavern", state)

    combined = " ".join(messages)
    assert "Ches" in combined or "ship" in combined.lower()


def test_badge_use_elsewhere_does_not_set_ches_tip(monkeypatch):
    m = manager_with("badge")
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: None)
    state = fresh_state()

    m.use_item("badge", "police_station", state)

    assert state["ches_tip"] is False


# ---------------------------------------------------------------------------
# examine new items — detailed descriptions returned
# ---------------------------------------------------------------------------

def test_examine_membership_register_shows_voss(monkeypatch):
    m = manager_with("membership_register")
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))

    m.examine_item("membership_register", [], fresh_state())

    assert any("Voss" in msg for msg in messages)


def test_examine_meeting_minutes_shows_northwest_maritime(monkeypatch):
    m = manager_with("meeting_minutes")
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))

    m.examine_item("meeting_minutes", [], fresh_state())

    combined = " ".join(messages)
    assert "Northwest Maritime" in combined


def test_examine_manifest_shows_weight_discrepancy(monkeypatch):
    m = manager_with("manifest")
    messages = []
    monkeypatch.setattr(item_manager_module, "print_text", lambda t, **_: messages.append(t))

    m.examine_item("manifest", [], fresh_state())

    combined = " ".join(messages)
    assert "3,200" in combined or "850" in combined


# ---------------------------------------------------------------------------
# Location descriptions contain key content markers
# ---------------------------------------------------------------------------

def test_eagles_hall_description_mentions_register():
    desc = LOCATIONS["eagles_hall"]["description"].lower()
    assert "register" in desc


def test_eagles_lounge_description_mentions_minutes():
    desc = LOCATIONS["eagles_lounge"]["description"].lower()
    assert "minutes" in desc


def test_harbormaster_shack_description_mentions_pier_7():
    desc = LOCATIONS["harbormaster_shack"]["description"]
    assert "Pier 7" in desc


def test_anchor_tavern_description_mentions_ches():
    desc = LOCATIONS["anchor_tavern"]["description"].lower()
    # description hints at badge mechanic
    assert "badge" in desc or "two fingers" in desc


# ---------------------------------------------------------------------------
# victory text — Eagles / Voss update
# ---------------------------------------------------------------------------

def test_victory_mentions_eagles_chapter(monkeypatch):
    import emerald_shadows.game_manager as gm_module
    from emerald_shadows.game_manager import GameManager

    gm = GameManager()
    messages = []
    monkeypatch.setattr(gm_module, "print_text", lambda t, **_: messages.append(t))
    gm.show_victory()
    combined = " ".join(messages)
    assert "Eagles" in combined


def test_victory_mentions_voss_member_number(monkeypatch):
    import emerald_shadows.game_manager as gm_module
    from emerald_shadows.game_manager import GameManager

    gm = GameManager()
    messages = []
    monkeypatch.setattr(gm_module, "print_text", lambda t, **_: messages.append(t))
    gm.show_victory()
    combined = " ".join(messages)
    assert "1144" in combined
