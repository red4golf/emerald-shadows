from typing import Tuple, Dict, Optional
from dataclasses import dataclass
import logging

@dataclass
class TrolleyState:
    position: int
    in_motion: bool
    on_trolley: bool
    last_stop: Optional[str] = None

class TrolleySystem:
    def __init__(self):
        self.position = 0
        self.routes = {
            0: {
                "description": "Pike Place Stop — foot of the Market hill",
                "exits": {"off": "pike_place"},
                "history": (
                    "The tram stops at the base of Pike Street where it meets the waterfront, "
                    "a block below the market stalls. Fishmongers have been hauling their catch "
                    "up this hill since 1907. The smell of Dungeness crab and salt water is "
                    "strongest here. On a clear morning you can see the Olympic Mountains "
                    "across the Sound from this corner."
                )
            },
            1: {
                "description": "Pioneer Square Stop — Yesler Way and First Avenue",
                "exits": {"off": "pioneer_square"},
                "history": (
                    "This is where Seattle began. Henry Yesler built his sawmill at the "
                    "foot of this hill in 1852, and logs were skidded down to the waterfront "
                    "along what became Yesler Way — the original Skid Road. The term traveled "
                    "east with the men who'd worked these docks and ended up meaning something "
                    "darker. The neighborhood has been rebuilt in brick since the Great Fire "
                    "of 1889, but the grade of the street remembers the logs."
                )
            },
            2: {
                "description": "Waterfront Stop — Pier 54",
                "exits": {"off": "waterfront"},
                "history": (
                    "Ivar Haglund opened his fish bar at Pier 54 in 1938, and the smell of "
                    "clam chowder has competed with diesel exhaust at this stop ever since. "
                    "During the war, this pier handled equipment bound for the Pacific. "
                    "The Puget Sound ferries depart from further north — the Kalakala to "
                    "Bremerton, the Indianola boats for the peninsula. Half of Bremerton's "
                    "naval shipyard workers ride the tram past this stop every morning."
                )
            },
            3: {
                "description": "Smith Tower Stop — Second Avenue and Yesler",
                "exits": {"off": "smith_tower"},
                "history": (
                    "The tram has stopped here since L.C. Smith opened his tower in 1914, "
                    "when the building was the talk of the entire Pacific Coast. The stop "
                    "is the end of the line on this route — after this, the tram reverses "
                    "back toward the waterfront. The dock company that owns this line has "
                    "been trying to shut it down for two years. The longshoremen's union "
                    "has been fighting them. So far, the union is winning."
                )
            }
        }
        self.in_motion = False
        self.on_trolley = False
        self.last_stop = None

    # Maps game location names to the nearest trolley stop index
    _BOARDING_POSITIONS: Dict[str, int] = {
        "pike_place": 0,
        "pioneer_square": 1,
        "waterfront": 2,
        "docks": 2,
        "smith_tower": 3,
    }

    @property
    def current_stop(self) -> int:
        return self.position

    def set_boarding_position(self, location: str) -> None:
        """Snap the trolley to the stop nearest to where the player boarded."""
        self.position = self._BOARDING_POSITIONS.get(location, 0)

    def board_trolley(self) -> str:
        if self.on_trolley:
            return ""
        self.on_trolley = True
        self.in_motion = False
        return (
            "You step aboard the Waterfront Electric. The motorman doesn't acknowledge you — "
            "that's standard on this line. The wooden bench seats are worn to a shine. "
            "The overhead wire crackles as the tram gets moving. Out the window, the "
            "rain-slicked waterfront slides past.\n\n"
            "Current Stop: Pike Place — foot of the Market hill\n\n"
            "Tram commands:\n"
            "  next    — ride to the next stop\n"
            "  off     — step off at the current stop\n"
            "  status  — check the route\n"
            "  history — learn about where you are\n\n"
            "Route: Pike Place → Pioneer Square → Waterfront → Smith Tower"
        )

    def _advance_position(self) -> None:
        if self.position < len(self.routes) - 1:
            self.position += 1
        else:
            self.position = 0
        self.last_stop = self.routes[self.position]['description']

    def handle_movement(self) -> Tuple[str, Dict[str, str]]:
        try:
            current_stop = self.routes[self.position]
            
            if self.in_motion:
                self.in_motion = False
                self.last_stop = current_stop['description']
                return (
                    f"\nThe tram shudders to a stop. {current_stop['description']}.\n"
                    f"Type 'off' to step out or 'next' to ride on."
                ), current_stop['exits']

            self.in_motion = True
            self._advance_position()
            next_stop = self.routes[self.position]
            return (
                "\nThe overhead wire crackles and the tram lurches forward into the rain...",
                {"next": "trolley", "off": next_stop['exits']['off']}
            )
                    
        except Exception as e:
            logging.error(f"Error in trolley movement: {e}")
            return "There was a problem with the trolley. Please try again.", {"off": "pike_place"}

    def exit_trolley(self) -> Optional[str]:
        if not self.on_trolley:
            return None
        self.on_trolley = False
        self.in_motion = False
        return self.routes[self.position]['exits']['off']

    def next_stop(self) -> bool:
        if not self.on_trolley:
            return False
        self._advance_position()
        return True

    def get_stop_description(self) -> str:
        if not self.on_trolley:
            return "You are not on the trolley."
        current_stop = self.routes[self.position]
        return f"Stop {self.position + 1}: {current_stop['description']}"

    def get_status(self) -> str:
        try:
            current_stop = self.routes[self.position]
            next_stop = self.routes[(self.position + 1) % len(self.routes)]
            stops_remaining = len(self.routes) - self.position - 1

            status = (
                f"Current stop: {current_stop['description']}\n"
                f"Next stop: {next_stop['description']}\n"
                f"Stops remaining on route: {stops_remaining}\n\n"
                f"Full route: Pike Place → Pioneer Square → Waterfront → Smith Tower"
            )
            return status
            
        except Exception as e:
            logging.error(f"Error getting trolley status: {e}")
            return "Unable to determine trolley status."

    def get_history(self) -> str:
        try:
            return f"\nHistorical Note: {self.routes[self.position]['history']}"
        except Exception as e:
            logging.error(f"Error getting stop history: {e}")
            return "Historical information unavailable."

    def get_state(self) -> dict:
        return {
            "position": self.position,
            "in_motion": self.in_motion,
            "on_trolley": self.on_trolley,
            "last_stop": self.last_stop,
        }

    def restore_state(self, state: dict) -> None:
        if isinstance(state, TrolleyState):
            # Handle legacy TrolleyState objects from old saves
            self.position = state.position
            self.in_motion = state.in_motion
            self.on_trolley = state.on_trolley
            self.last_stop = state.last_stop
        else:
            self.position = state.get("position", 0)
            self.in_motion = state.get("in_motion", False)
            self.on_trolley = state.get("on_trolley", False)
            self.last_stop = state.get("last_stop", None)
