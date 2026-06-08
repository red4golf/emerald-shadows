"""Tests for utils module: SaveLoadManager and DisplayManager."""

import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock

from emerald_shadows.utils import SaveLoadManager, DisplayManager
from emerald_shadows.config import INITIAL_GAME_STATE


# --- SaveLoadManager ---

@pytest.fixture
def save_dir(tmp_path):
    return tmp_path / "saves"


@pytest.fixture
def save_manager(save_dir):
    return SaveLoadManager(str(save_dir))


def _make_game_instance(game_state=None, location=None):
    """Build a minimal mock game instance for save/load tests."""
    instance = MagicMock()
    instance.game_state = game_state or INITIAL_GAME_STATE.copy()

    loc_state = {
        "current_location": location or "police_station",
        "locations": {},
        "trolley": {"position": 0, "in_motion": False, "on_trolley": False, "last_stop": None},
    }
    instance.location_manager.get_state.return_value = loc_state

    inv_state = {
        "inventory": ["badge"],
        "notes_found": 0,
        "discovered_combinations": [],
        "removed_items": ["badge"],
    }
    instance.item_manager.get_inventory_state.return_value = inv_state

    return instance


def test_save_creates_file(save_manager, save_dir):
    instance = _make_game_instance()
    assert save_manager.save_game(instance, "test_save") is True
    assert (save_dir / "test_save.json").exists()


def test_save_file_is_valid_json(save_manager, save_dir):
    instance = _make_game_instance()
    save_manager.save_game(instance, "json_check")
    with open(save_dir / "json_check.json") as f:
        data = json.load(f)
    assert "game_state" in data
    assert "location_state" in data
    assert "inventory_state" in data


def test_load_restores_game_state(save_manager, save_dir):
    instance = _make_game_instance(game_state={"has_badge": True})
    save_manager.save_game(instance, "restore_test")

    target = _make_game_instance()
    assert save_manager.load_game(target, "restore_test") is True
    assert target.game_state["has_badge"] is True


def test_load_missing_file_returns_false(save_manager, capsys):
    instance = _make_game_instance()
    result = save_manager.load_game(instance, "does_not_exist")
    assert result is False


def test_list_saves_returns_entries(save_manager):
    for name in ("save_a", "save_b"):
        save_manager.save_game(_make_game_instance(), name)
    saves = save_manager.list_saves()
    names = {s["name"] for s in saves}
    assert "save_a" in names
    assert "save_b" in names


def test_list_saves_sorted_newest_first(save_manager):
    import time
    save_manager.save_game(_make_game_instance(), "first")
    time.sleep(0.01)
    save_manager.save_game(_make_game_instance(), "second")
    saves = save_manager.list_saves()
    assert saves[0]["name"] == "second"


def test_delete_save(save_manager, save_dir):
    save_manager.save_game(_make_game_instance(), "to_delete")
    assert save_manager.delete_save("to_delete") is True
    assert not (save_dir / "to_delete.json").exists()


def test_delete_nonexistent_save(save_manager):
    assert save_manager.delete_save("ghost") is False


# --- DisplayManager ---

def test_get_terminal_size_returns_ints():
    w, h = DisplayManager.get_terminal_size()
    assert isinstance(w, int)
    assert isinstance(h, int)
    assert 60 <= w <= 120


def test_wrap_text_does_not_exceed_width(monkeypatch):
    monkeypatch.setattr(DisplayManager, "get_terminal_size", staticmethod(lambda: (60, 24)))
    long_line = "The rain-slicked streets of Seattle glimmered beneath the neon signs of the post-war era."
    wrapped = DisplayManager.wrap_text(long_line)
    for line in wrapped.splitlines():
        assert len(line) <= 60


def test_wrap_text_handles_empty_string():
    result = DisplayManager.wrap_text("")
    assert isinstance(result, str)


def test_print_text_outputs_to_stdout(capsys):
    DisplayManager.print_text("Hello, Seattle.", wrap=False)
    out = capsys.readouterr().out
    assert "Hello, Seattle." in out


def test_format_location_description_includes_exits():
    desc = DisplayManager.format_location_description(
        "A dark alley.", ["north", "south"], []
    )
    assert "north" in desc
    assert "south" in desc


def test_format_location_description_includes_items():
    desc = DisplayManager.format_location_description(
        "A dark alley.", [], ["badge", "notebook"]
    )
    assert "badge" in desc
    assert "notebook" in desc
