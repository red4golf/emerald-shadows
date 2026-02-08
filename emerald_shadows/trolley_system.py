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
                "description": "Downtown Stop",
                "exits": {"off": "pike_place"},
                "history": "The Downtown trolley stop has served Pike Place Market since 1907, connecting shoppers to Seattle's famous public market."
            },
            1: {
                "description": "Pioneer Square Stop", 
                "exits": {"off": "pioneer_square"},
                "history": "Pioneer Square's trolley stop dates back to the 1890s, serving Seattle's historic first neighborhood."
            },
            2: {
                "description": "Waterfront Stop",
                "exits": {"off": "waterfront"},
                "history": "The Waterfront trolley line, established in the early 1900s, was crucial for maritime commerce and shipyard workers."
            },
            3: {
                "description": "Smith Tower Stop",
                "exits": {"off": "smith_tower"},
                "history": "Added in 1914 when Smith Tower opened, this stop served Seattle's first skyscraper."
            }
        }
        self.in_motion = False
        self.on_trolley = False
        self.last_stop = None

    @property
    def current_stop(self) -> int:
        return self.position

    def board_trolley(self) -> str:
        if self.on_trolley:
            return ""
        self.on_trolley = True
        self.in_motion = False
        return """
        You board the electric trolley. The wooden seats and brass fixtures speak to an earlier era.
        
        Current Stop: Downtown (Pike Place)
        
        Trolley Instructions:
        - Type 'next' to move to the next stop
        - Type 'off' to exit at the current stop
        - Type 'look' to see current stop
        - Type 'status' to see route information
        - Type 'history' to learn about the current stop
        
        The trolley follows a fixed route:
        Downtown → Pioneer Square → Waterfront → Smith Tower
        """

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
                return (f"\nThe trolley arrives at: {current_stop['description']}\n"
                       f"You can type 'off' to exit or 'next' to continue."), current_stop['exits']
            
            self.in_motion = True
            self._advance_position()
            next_stop = self.routes[self.position]
            return ("\nThe trolley begins moving to the next stop...",
                    {"next": "trolley", "off": next_stop['exits']['off']})
                    
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
            
            status = f"""
            Current Stop: {current_stop['description']}
            Next Stop: {next_stop['description']}
            Stops remaining on route: {stops_remaining}
            
            Complete Route:
            Downtown → Pioneer Square → Waterfront → Smith Tower
            """
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

    def get_state(self) -> TrolleyState:
        return TrolleyState(
            position=self.position,
            in_motion=self.in_motion,
            on_trolley=self.on_trolley,
            last_stop=self.last_stop
        )

    def restore_state(self, state: TrolleyState) -> None:
        self.position = state.position
        self.in_motion = state.in_motion
        self.on_trolley = state.on_trolley
        self.last_stop = state.last_stop
