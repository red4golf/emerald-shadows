"""Basic natural language command parsing for Emerald Shadows."""

from __future__ import annotations

from typing import Dict, Tuple

class NaturalCommandHandler:
    """Translate player input into normalized commands the game understands."""

    def __init__(self) -> None:
        self.direction_aliases: Dict[str, str] = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "u": "up",
            "d": "down",
            "north": "north",
            "south": "south",
            "east": "east",
            "west": "west",
            "up": "up",
            "down": "down",
            "forward": "north",
            "back": "south"
        }

        self.single_word_aliases: Dict[str, str] = {
            "i": "inventory",
            "inv": "inventory",
            "inventory": "inventory",
            "look": "look",
            "examine": "examine",
            "inspect": "examine",
            "quit": "quit",
            "exit": "quit",
            "help": "help",
            "save": "save",
            "load": "load"
        }

        self.verb_aliases: Dict[str, str] = {
            "go": "go",
            "move": "go",
            "travel": "go",
            "walk": "go",
            "take": "take",
            "grab": "take",
            "get": "take",
            "pick": "take",
            "examine": "examine",
            "inspect": "examine",
            "look": "look",
            "use": "use",
            "combine": "combine",
            "mix": "combine",
            "solve": "solve"
        }

        self.trolley_commands = {"next", "off", "status", "history"}

    def understand_command(self, raw_command: str) -> Tuple[str, str]:
        """Return the normalized command type and argument string."""
        if not raw_command:
            return "", ""

        command = raw_command.strip().lower()
        if not command:
            return "", ""

        words = command.split()
        first_word = words[0]

        # Handle trolley commands directly
        if first_word in self.trolley_commands:
            return first_word, ""

        # Single word commands (inventory, help, look, etc.)
        if command in self.single_word_aliases:
            return self.single_word_aliases[command], ""

        # Direction-only commands ("north")
        if first_word in self.direction_aliases and len(words) == 1:
            return "go", self.direction_aliases[first_word]

        # Explicit "go" commands or synonyms
        if first_word in self.direction_aliases:
            return "go", self.direction_aliases[first_word]

        verb = self.verb_aliases.get(first_word)
        if not verb:
            return "", ""

        argument = command[len(first_word):].strip()
        if verb == "go" and argument.startswith("to "):
            argument = argument[3:].strip()
        return verb, argument
