import builtins
from datetime import datetime, timedelta

import pytest

import emerald_shadows.game_manager as game_manager_module
from emerald_shadows.config import REQUIRED_ITEMS, REQUIRED_STATES
from emerald_shadows.game_manager import GameManager


@pytest.fixture()
def game_manager():
    return GameManager()


def test_process_command_moves_character(monkeypatch, game_manager):
    captured = {}

    def fake_move(direction, game_state):
        captured["direction"] = direction
        captured["state"] = game_state
        return True

    monkeypatch.setattr(game_manager.location_manager, "move_to_location", fake_move)

    assert game_manager.process_command("north") is True
    assert captured["direction"] == "north"


def test_process_command_shows_inventory(monkeypatch, game_manager):
    called = {"inventory": False}

    def fake_inventory(game_state=None):
        called["inventory"] = True

    monkeypatch.setattr(game_manager.item_manager, "show_inventory", fake_inventory)

    assert game_manager.process_command("inventory") is True
    assert called["inventory"] is True


def test_process_command_routes_trolley_commands(monkeypatch, game_manager):
    called = {}

    def fake_trolley(command):
        called["command"] = command

    monkeypatch.setattr(game_manager.location_manager, "handle_trolley_command", fake_trolley)
    assert game_manager.process_command("next") is True
    assert called["command"] == "next"


def test_help_command_invokes_show_help(monkeypatch, game_manager):
    called = {"help": False}

    def fake_help():
        called["help"] = True

    monkeypatch.setattr(game_manager, "show_help", fake_help)
    assert game_manager.process_command("help") is True
    assert called["help"] is True


def test_look_command_prints_description(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.location_manager, "get_location_description", lambda: "Dark alley")
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    assert game_manager.process_command("look") is True
    assert any("Dark alley" in message for message in messages)


def test_examine_command_routes_to_item_manager(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.location_manager, "get_available_items", lambda: ["badge"])
    captured = {}

    def fake_examine(item, location_items, state):
        captured.update(item=item, available=location_items)

    monkeypatch.setattr(game_manager.item_manager, "examine_item", fake_examine)
    assert game_manager.process_command("examine badge") is True
    assert captured["item"] == "badge"


def test_use_command_without_item_prompts(monkeypatch, game_manager):
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    assert game_manager.process_command("use") is True
    assert any("Use what?" in msg for msg in messages)


def test_use_command_calls_item_manager(monkeypatch, game_manager):
    used = {}

    def fake_use(item, location, state):
        used.update(item=item, location=location)

    game_manager.location_manager.current_location = "smith_tower"
    monkeypatch.setattr(game_manager.item_manager, "use_item", fake_use)

    assert game_manager.process_command("use notebook") is True
    assert used == {"item": "notebook", "location": "smith_tower"}


def test_combine_command_requires_two_items(monkeypatch, game_manager):
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    assert game_manager.process_command("combine") is True
    assert any("Combine which items" in msg for msg in messages)


def test_combine_command_calls_item_manager(monkeypatch, game_manager):
    called = {}

    def fake_combine(item1, item2, state):
        called.update(one=item1, two=item2)
        return True

    monkeypatch.setattr(game_manager.item_manager, "combine_items", fake_combine)
    assert game_manager.process_command("combine notebook with cipher wheel") is True
    assert called == {"one": "notebook", "two": "cipher wheel"}


def test_process_command_save_uses_default_name(monkeypatch, game_manager):
    saved = {}

    def fake_input(prompt=""):
        return ""  # accept default save name

    def fake_save(instance, save_name):
        saved["name"] = save_name
        return True

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(game_manager.save_load_manager, "save_game", fake_save)

    assert game_manager.process_command("save") is True
    assert saved["name"] == "manual_save"


def test_load_command_reports_missing_saves(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.save_load_manager, "list_saves", lambda: [])
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    assert game_manager.process_command("load") is True
    assert any("No save files found" in msg for msg in messages)


def test_process_command_quit_prompts_for_save(monkeypatch, game_manager):
    saved = {"called": False}

    def fake_input(prompt=""):
        return "n"  # decline save

    def fake_save(*args, **kwargs):
        saved["called"] = True
        return True

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(game_manager.save_load_manager, "save_game", fake_save)

    assert game_manager.process_command("quit") is False
    assert saved["called"] is False


def test_quit_saves_when_requested(monkeypatch, game_manager):
    saved = {"name": None}

    def fake_input(prompt=""):
        return "y"  # request save before quitting

    def fake_save(instance, save_name):
        saved["name"] = save_name
        return True

    monkeypatch.setattr(builtins, "input", fake_input)
    monkeypatch.setattr(game_manager.save_load_manager, "save_game", fake_save)

    assert game_manager.process_command("quit") is False
    assert saved["name"] == "quit_save"


def test_unknown_command_prints_feedback(monkeypatch, game_manager):
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))
    assert game_manager.process_command("kick the door") is True
    assert any("productive" in m.lower() or "help" in m.lower() for m in messages)


def test_unknown_command_does_not_crash(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: None)
    assert game_manager.process_command("xyzzy plover") is True


def test_parse_combine_args_variants(game_manager):
    assert game_manager._parse_combine_args("notebook with cipher wheel") == ("notebook", "cipher wheel")
    assert game_manager._parse_combine_args("cipher wheel and notebook") == ("cipher wheel", "notebook")
    assert game_manager._parse_combine_args("radio manual") == ("radio", "manual")


def test_check_auto_save_triggers(monkeypatch, game_manager):
    saved = {"count": 0}

    def fake_save(instance, name):
        saved["count"] += 1
        return True

    game_manager.last_save_time = datetime.now() - timedelta(seconds=game_manager.auto_save_interval + 5)
    monkeypatch.setattr(game_manager.save_load_manager, "save_game", fake_save)

    game_manager.check_auto_save()
    assert saved["count"] == 1


def test_check_game_progress_requires_all_items_and_states(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.item_manager, "get_inventory", lambda: list(REQUIRED_ITEMS))
    for state in REQUIRED_STATES:
        game_manager.game_state[state] = True

    assert game_manager.check_game_progress() is True


# ---------------------------------------------------------------------------
# look command — darkness awareness
# ---------------------------------------------------------------------------

def test_look_in_dark_location_shows_darkness_warning(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.location_manager, "is_dark", lambda: True)
    game_manager.game_state["flashlight_lit"] = False
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    assert game_manager.process_command("look") is True
    combined = " ".join(messages).lower()
    assert "dark" in combined
    # Must NOT reveal the room description
    assert "dark alley" not in combined


def test_look_in_dark_location_suppresses_room_description(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.location_manager, "is_dark", lambda: True)
    monkeypatch.setattr(game_manager.location_manager, "get_location_description", lambda: "SECRET ROOM TEXT")
    game_manager.game_state["flashlight_lit"] = False
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    game_manager.process_command("look")
    assert not any("SECRET ROOM TEXT" in m for m in messages)


def test_look_in_dark_location_with_flashlight_shows_description(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.location_manager, "is_dark", lambda: True)
    monkeypatch.setattr(game_manager.location_manager, "get_location_description", lambda: "Tunnel walls drip.")
    game_manager.game_state["flashlight_lit"] = True
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    game_manager.process_command("look")
    assert any("Tunnel walls drip." in m for m in messages)


def test_look_in_lit_location_shows_description(monkeypatch, game_manager):
    monkeypatch.setattr(game_manager.location_manager, "is_dark", lambda: False)
    monkeypatch.setattr(game_manager.location_manager, "get_location_description", lambda: "Dark alley")
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))

    game_manager.process_command("look")
    assert any("Dark alley" in m for m in messages)


# ---------------------------------------------------------------------------
# load command — resets _last_location so description redisplays
# ---------------------------------------------------------------------------

def test_load_resets_last_location_on_success(monkeypatch, game_manager):
    saves = [{"name": "slot1", "date": "2026-01-01"}]
    monkeypatch.setattr(game_manager.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(game_manager.save_load_manager, "load_game", lambda inst, name: True)
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: None)
    inputs = iter(["1"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    # Simulate: player was in a room, then loads
    game_manager._last_location = "smith_tower"
    game_manager.process_command("load")
    assert game_manager._last_location is None


def test_load_does_not_reset_last_location_on_cancel(monkeypatch, game_manager):
    saves = [{"name": "slot1", "date": "2026-01-01"}]
    monkeypatch.setattr(game_manager.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: None)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "")  # cancel

    game_manager._last_location = "smith_tower"
    game_manager.process_command("load")
    assert game_manager._last_location == "smith_tower"


def test_last_location_initialises_to_none(game_manager):
    assert game_manager._last_location is None


# ---------------------------------------------------------------------------
# victory text — Roy Hendricks resolution
# ---------------------------------------------------------------------------

def test_victory_mentions_roy_hendricks(monkeypatch, game_manager):
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))
    game_manager.show_victory()
    combined = " ".join(messages)
    assert "Roy Hendricks" in combined


def test_victory_mentions_hendricks_role(monkeypatch, game_manager):
    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))
    game_manager.show_victory()
    combined = " ".join(messages)
    assert "motorman" in combined.lower()


def test_handle_load_displays_slots(monkeypatch, game_manager):
    saves = [
        {"name": "slot1", "date": "2026-02-08"},
        {"name": "slot2", "date": "2026-02-09"},
    ]
    monkeypatch.setattr(game_manager.save_load_manager, "list_saves", lambda: saves)
    monkeypatch.setattr(game_manager.save_load_manager, "load_game", lambda instance, name: True)
    inputs = iter(["1"])

    def fake_input(prompt=""):
        return next(inputs)

    messages = []
    monkeypatch.setattr(game_manager_module, "print_text", lambda text, **_: messages.append(text))
    monkeypatch.setattr(builtins, "input", fake_input)

    assert game_manager.process_command("load") is True
    assert any("1. slot1" in msg for msg in messages)
