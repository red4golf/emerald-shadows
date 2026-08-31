"""Basic natural language command parsing for Emerald Shadows."""

from __future__ import annotations

from typing import Dict, Tuple

_ARTICLES = {"the", "a", "an"}


_ADDRESS_PREFIXES = ("to ", "with ", "at ")


def _strip_articles(text: str) -> str:
    """Remove leading articles from a noun phrase: 'the note' -> 'note'."""
    words = text.split()
    if words and words[0] in _ARTICLES:
        words = words[1:]
    return " ".join(words)


def _strip_person(text: str) -> str:
    """Normalise how a player addresses somebody: 'to the barman' -> 'barman'."""
    text = text.strip()
    for prefix in _ADDRESS_PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break
    return _strip_articles(text)


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
            "load": "load",
            "score": "score",
            "exits": "exits",
            "ways": "exits",
            # Investigation
            "case": "case",
            "casebook": "case",
            "review": "case",
            "notes": "case",
            "topics": "topics",
            "questions": "topics",
            "listen": "listen",
            "arrest": "arrest",
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
            "read": "examine",
            "look": "look",
            "use": "use",
            "combine": "combine",
            "mix": "combine",
            "solve": "solve",
            "drop": "drop",
            "leave": "drop",
            "put": "drop",
            "discard": "drop",
            # Conversation
            "ask": "ask",
            "question": "ask",
            "talk": "talk",
            "speak": "talk",
            "interrogate": "talk",
            # Puzzle operation
            "turn": "turn",
            "rotate": "turn",
            "spin": "turn",
            "tune": "tune",
            "tap": "tap",
            "send": "tap",
            "listen": "listen",
            "arrest": "arrest",
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

        # "look at <item>" → examine <item>
        if command.startswith("look at "):
            noun = _strip_articles(command[len("look at "):].strip())
            return "examine", noun

        # "ask <person> about <topic>" → ("ask", "person|topic")
        if first_word in ("ask", "question"):
            return "ask", self._parse_ask(command[len(first_word):].strip())

        # "talk to <person>" → ("talk", "person")
        if first_word in ("talk", "speak", "interrogate"):
            return "talk", _strip_person(command[len(first_word):].strip())

        # Single word commands (inventory, help, look, score, etc.)
        if command in self.single_word_aliases:
            return self.single_word_aliases[command], ""

        # Direction-only commands ("north")
        if first_word in self.direction_aliases and len(words) == 1:
            return "go", self.direction_aliases[first_word]

        # Explicit "go" commands or direction synonyms
        if first_word in self.direction_aliases:
            return "go", self.direction_aliases[first_word]

        verb = self.verb_aliases.get(first_word)
        if not verb:
            return "", ""

        argument = _strip_articles(command[len(first_word):].strip())
        if verb == "go" and argument.startswith("to "):
            argument = argument[3:].strip()
        if verb == "take" and argument.startswith("up "):
            argument = _strip_articles(argument[3:].strip())
        if verb in ("tap", "listen") and argument.startswith("to "):
            argument = _strip_articles(argument[3:].strip())
        return verb, argument

    @staticmethod
    def _parse_ask(rest: str) -> str:
        """Split 'ches about the harbormaster' into 'ches|harbormaster'.

        Either half may be empty: 'ask about the sedan' leaves the person for the
        game to infer from who's standing there, and a bare 'ask ches' just opens
        the conversation.
        """
        rest = rest.strip()
        for separator in (" about ", " re ", " regarding "):
            if separator in rest:
                person, topic = rest.split(separator, 1)
                return f"{_strip_person(person)}|{_strip_articles(topic.strip())}"
        if rest.startswith("about "):
            return f"|{_strip_articles(rest[len('about '):].strip())}"
        return f"{_strip_person(rest)}|"
