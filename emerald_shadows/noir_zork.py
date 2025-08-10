"""Simple noir detective adventure set in the Pacific Northwest.

This module implements a lightweight text adventure inspired by the
classic *Zork* series but filtered through the lens of a 1947 radio
mystery.  It is intentionally small yet extendable so additional
locations, items and puzzles can be added over time.  The game can be
run directly as a script::

    python -m emerald_shadows.noir_zork -p

Use the ``-p``/``--play`` flag to start the interactive session. The
world map is a deliberately comedic take on post-war Seattle and its
neighbouring cities. Players navigate using cardinal directions,
collect quirky items and can save or load their progress.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import argparse
import json
from pathlib import Path
from typing import Dict, List

SAVE_FILE = Path("saves") / "noir_zork_save.json"


@dataclass
class Location:
    """A spot on the map."""

    name: str
    description: str
    exits: Dict[str, str]
    items: List[str] = field(default_factory=list)
    banter: str = ""


WORLD: Dict[str, Location] = {
    "Seattle": Location(
        name="Seattle",
        description=(
            "Rain beads on the brim of your fedora. Pike Place smells of "
            "yesterday's fish and tomorrow's trouble."
        ),
        exits={"north": "Vancouver", "south": "Portland", "east": "Spokane", "west": "Olympic Peninsula"},
        items=["notebook"],
        banter="The newsboy shouts: 'Read all about it! Detective loses hat, solves case!'",
    ),
    "Vancouver": Location(
        name="Vancouver",
        description="A smoky jazz joint where the sax is smooth and the coffee is rough.",
        exits={"south": "Seattle"},
        items=["trench coat"],
        banter="A trumpeter eyes you suspiciously. 'You from the States? Prove it.'",
    ),
    "Portland": Location(
        name="Portland",
        description="Roses, rain and a warehouse full of questionable crates.",
        exits={"north": "Seattle"},
        items=["coffee"],
        banter="A dock worker grins: 'Buddy, around here the beans are stronger than the mayor.'",
    ),
    "Spokane": Location(
        name="Spokane",
        description="A dry town with a wet river and too many secrets.",
        exits={"west": "Seattle"},
        items=["cigar"],
        banter="A riverboat captain mutters about smugglers and missing rum barrels.",
    ),
    "Olympic Peninsula": Location(
        name="Olympic Peninsula",
        description="Misty forests where the trees whisper and the owls gossip.",
        exits={"east": "Seattle"},
        items=["mysterious package"],
        banter="A ranger tips his hat. 'Careful, detective. The moss here has witnesses.'",
    ),
}


@dataclass
class Player:
    location: str = "Seattle"
    inventory: List[str] = field(default_factory=list)


class Game:
    """Core game engine."""

    def __init__(self) -> None:
        self.player = Player()

    # ----- Persistence -------------------------------------------------
    def save(self, filename: Path = SAVE_FILE) -> None:
        filename.parent.mkdir(parents=True, exist_ok=True)
        state = {"location": self.player.location, "inventory": self.player.inventory}
        filename.write_text(json.dumps(state))
        print(f"Game saved to {filename}.")

    def load(self, filename: Path = SAVE_FILE) -> None:
        if not filename.exists():
            print("No save file found.")
            return
        state = json.loads(filename.read_text())
        self.player.location = state.get("location", "Seattle")
        self.player.inventory = state.get("inventory", [])
        print(f"Loaded game from {filename}.")

    # ----- Helpers -----------------------------------------------------
    @property
    def location(self) -> Location:
        return WORLD[self.player.location]

    def look(self) -> None:
        loc = self.location
        print(loc.description)
        if loc.items:
            print("You see:", ", ".join(loc.items))
        else:
            print("Nothing catches your eye.")

    def move(self, direction: str) -> None:
        direction = direction.lower()
        if direction in self.location.exits:
            self.player.location = self.location.exits[direction]
            self.look()
        else:
            print("You can't go that way, gumshoe.")

    def take(self, item: str) -> None:
        loc = self.location
        if item in loc.items:
            loc.items.remove(item)
            self.player.inventory.append(item)
            print(f"You pocket the {item}.")
        else:
            print("There's no {item} here.".format(item=item))

    def talk(self) -> None:
        print(self.location.banter or "Nobody here wants to chat.")

    def show_inventory(self) -> None:
        if self.player.inventory:
            print("You carry:", ", ".join(self.player.inventory))
        else:
            print("Your pockets are as empty as a politician's promise.")

    def help(self) -> None:
        print("Commands: look, go <direction>, take <item>, talk, inventory, save, load, quit")

    # ----- Main loop ---------------------------------------------------
    def run(self) -> None:
        print("\nWelcome to Emerald Shadows: Mirror Noir Edition\n")
        self.look()
        while True:
            try:
                command = input("\n> ").strip()
            except EOFError:
                print()
                break
            if not command:
                continue
            parts = command.split()
            verb = parts[0].lower()
            arg = " ".join(parts[1:]) if len(parts) > 1 else ""

            if verb in {"north", "south", "east", "west"}:
                self.move(verb)
            elif verb == "go":
                self.move(arg)
            elif verb == "look":
                self.look()
            elif verb == "take":
                self.take(arg)
            elif verb in {"inventory", "i"}:
                self.show_inventory()
            elif verb == "talk":
                self.talk()
            elif verb == "save":
                self.save()
            elif verb == "load":
                self.load()
            elif verb == "help":
                self.help()
            elif verb == "quit":
                print("So long, detective.")
                break
            else:
                print("That move's not in the manual, pal.")


def main(argv: List[str] | None = None) -> None:
    """Entry point for launching the noir sandbox."""
    parser = argparse.ArgumentParser(description="Emerald Shadows noir sandbox")
    parser.add_argument("-p", "--play", action="store_true", help="start interactive game")
    args = parser.parse_args(argv)
    if args.play:
        Game().run()
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - entry point
    main()
