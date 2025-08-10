"""Simplified trolley system used for navigation tests.

The implementation is intentionally lightweight; it models a circular
route through eight iconic Seattle locations. The class exposes a small
API required by the unit tests and can be expanded for richer gameplay.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Stop:
    description: str
    exits: Dict[str, str]


class TrolleySystem:
    """Manage a tiny trolley that loops around the city."""

    def __init__(self) -> None:
        self.current_stop: int = 0
        self.on_trolley: bool = False
        self.stops: Dict[int, Stop] = {
            0: Stop("Downtown Stop", {"off": "pike_place"}),
            1: Stop("Pioneer Square Stop", {"off": "pioneer_square"}),
            2: Stop("Waterfront Stop", {"off": "waterfront"}),
            3: Stop("Smith Tower Stop", {"off": "smith_tower"}),
            4: Stop("Capitol Hill Stop", {"off": "capitol_hill"}),
            5: Stop("University District Stop", {"off": "university_district"}),
            6: Stop("Ballard Stop", {"off": "ballard"}),
            7: Stop("International District Stop", {"off": "international_district"}),
        }

    def board_trolley(self) -> bool:
        """Board the trolley; return False if already aboard."""
        if self.on_trolley:
            return False
        self.on_trolley = True
        return True

    def exit_trolley(self) -> Optional[str]:
        """Exit the trolley and return the location name."""
        if not self.on_trolley:
            return None
        self.on_trolley = False
        return self.stops[self.current_stop].exits["off"]

    def next_stop(self) -> bool:
        """Advance to the next stop if on the trolley."""
        if not self.on_trolley:
            return False
        self.current_stop = (self.current_stop + 1) % len(self.stops)
        return True

    def get_stop_description(self) -> str:
        """Describe the current stop."""
        if not self.on_trolley:
            return "You are not on the trolley."
        return f"{self.stops[self.current_stop].description}"
