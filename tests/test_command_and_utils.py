import pytest

from emerald_shadows.commands.natural_commands import NaturalCommandHandler
from emerald_shadows.input_validator import InputValidator
from emerald_shadows.utils import DisplayManager


class TestNaturalCommandHandler:
    def setup_method(self):
        self.handler = NaturalCommandHandler()

    def test_direction_alias_shortcut(self):
        command, argument = self.handler.understand_command("n")
        assert command == "go"
        assert argument == "north"

    def test_trolley_command_passthrough(self):
        command, argument = self.handler.understand_command("status")
        assert command == "status"
        assert argument == ""

    def test_single_word_inventory_alias(self):
        command, argument = self.handler.understand_command("inv")
        assert command == "inventory"
        assert argument == ""

    def test_explicit_go_phrase_trims_to_prefix(self):
        command, argument = self.handler.understand_command("north side docks")
        assert command == "go"
        assert argument == "north"

    def test_go_to_phrase_strips_prefix(self):
        command, argument = self.handler.understand_command("go to warehouse three")
        assert command == "go"
        assert argument == "warehouse three"

    def test_unknown_command_returns_empty(self):
        command, argument = self.handler.understand_command("whistle softly")
        assert command == ""
        assert argument == ""


class TestInputValidator:
    def test_validate_puzzle_input_accepts_alpha(self):
        assert InputValidator.validate_puzzle_input("ANGELS") is True
        assert InputValidator.validate_puzzle_input("angels") is True

    def test_validate_puzzle_input_rejects_invalid_length_or_chars(self):
        assert InputValidator.validate_puzzle_input("", min_length=1) is False
        assert InputValidator.validate_puzzle_input("1", valid_chars="ABC") is False
        long_value = "A" * 60
        assert InputValidator.validate_puzzle_input(long_value, max_length=10) is False

    def test_validate_direction_is_case_insensitive(self):
        valid = {"North", "South"}
        assert InputValidator.validate_direction("north", valid) is True
        assert InputValidator.validate_direction("WEST", valid) is False

    def test_validate_command_normalizes(self):
        commands = {"look", "inventory"}
        assert InputValidator.validate_command(" LOOK  ", commands) is True
        assert InputValidator.validate_command("nop", commands) is False

    def test_validate_item_name_allows_underscores(self):
        assert InputValidator.validate_item_name("radio_manual") is True
        assert InputValidator.validate_item_name("broken lamp!") is False


class TestDisplayManager:
    def test_wrap_text_respects_indent_and_width(self, monkeypatch):
        monkeypatch.setattr(
            DisplayManager,
            "get_terminal_size",
            staticmethod(lambda: (40, 24)),
        )
        text = "The rain-soaked streets glimmer beneath the neon signs."
        wrapped = DisplayManager.wrap_text(text, indent=4)
        for line in wrapped.splitlines():
            if line:
                assert line.startswith(" " * 4)
                assert len(line) <= 40

    def test_print_text_can_skip_wrapping(self, monkeypatch, capsys):
        monkeypatch.setattr(
            DisplayManager,
            "wrap_text",
            staticmethod(lambda *args, **kwargs: pytest.fail("should not wrap")),
        )
        DisplayManager.print_text("Plain output", wrap=False)
        captured = capsys.readouterr()
        assert "Plain output" in captured.out
