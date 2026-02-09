import builtins

import pytest

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

    def fake_inventory():
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
