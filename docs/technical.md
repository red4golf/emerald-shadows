# Emerald Shadows Technical Documentation

## Architecture Overview

### Core Components

#### 1. Game Manager (`game_manager.py`)
The central controller for game state and flow.
- Handles command processing
- Manages game loop
- Coordinates between subsystems
- Handles save/load operations
- Manages auto-save functionality

Key Classes:
```python
class GameManager:
    """Main game manager class handling game state and core gameplay loop."""
    def __init__(self)
    def process_command(self, command: str) -> bool
    def start_game(self) -> None
```

#### 2. Location Manager (`location_manager.py`)
Manages game locations and movement.
- Location state tracking
- Movement validation
- Item placement
- Historical information
- Trolley system integration

Key Classes:
```python
@dataclass
class Location:
    """Data structure for location information."""
    name: str
    description: str
    exits: Dict[str, str]
    items: List[str]
    first_visit: bool
    requires: Optional[str]
    historical_note: Optional[str]

class LocationManager:
    """Manages game locations and movement between them."""
    def move_to_location(self, direction: str, game_state: Dict) -> bool
    def get_location_description(self) -> str
```

#### Dialogue (`dialogue.py`, `config_dialogue.py`)
Conversation engine plus its content, kept apart.

- **Topics are global knowledge.** `DialogueManager.known_topics` is a set of
  topic keys. Learning one from any source lets Diamond raise it with anyone;
  each NPC answers only for the topics they have an entry for, and deflects in
  character otherwise. This is what makes re-canvassing the city worthwhile.
- **Content is data.** `config_dialogue.NPCS` maps a person to their topics, and
  each topic entry may carry `unlocks`, `sets`, `score`, `fragment`, `gives`,
  `requires`/`locked` and `once`. Adding a witness or a line of questioning is a
  data change; the engine never needs touching.
- **Persistence.** `get_state()`/`restore_state()` round-trip through the save
  file. Saves predating dialogue restore to the starting topics.

#### Acts (`acts.py`)
Three-act progression. `ACT_REQUIREMENTS` maps an act number to the state flags
that must all be true to stand in it, and `current_act()` **computes** the act
rather than storing it — so a loaded save always lands in the right one.
`check_advance()` tracks the last act shown (in `game_state["act_seen"]`, so it
survives save/load) and never walks backwards. Act 3 sets `act_three`, which is
the plain flag gating the Pier 7 location.

The case is closed by `arrest` at Pier 7 with `FINALE_ITEMS` in hand — not by a
checklist filling up. `GameManager.check_game_progress()` reads one flag,
`case_closed`.

#### Casebook (`casebook.py`)
Renders the `case` command from three flag-gated tables (`FACTS`, `PEOPLE`,
`OPEN`). Every line is gated on a game-state flag, so the casebook can never
claim more than the player has earned. A test asserts every referenced flag
actually exists, since a typo would otherwise silently never render.

#### Codes (`codes.py`)
Caesar and Morse codecs as pure functions, no game state and no I/O. `sweep()`
returns all 26 wheel settings paired with the first word each yields — the
crib-based break the cipher puzzle is built on. Kept separate so the
transformations are cheap to test and the puzzle classes stay thin.

#### Puzzle protocol (`puzzles/base_puzzle.py`)
Puzzles are *operated*, not answered. A subclass declares the verbs it responds
to via `verbs()` and handles them in `interact(verb, argument, game_state)`,
returning `None` when the verb isn't its business or `(solved, message)` when it
is. `briefing(game_state)` supplies the working materials shown by `solve`.
`attempt()` remains for the one puzzle that still takes a typed answer (the
licence plate) and as a typed fallback on the others.

`PuzzleManager.handle_puzzle()` shows the briefing and only prompts for a typed
answer when the puzzle exposes no verbs.

#### Display (`utils.py`)
`print_text` reflows a paragraph to the terminal, which is right for prose and
wrong for anything whose line structure carries meaning. `print_block` preserves
every line break and wraps only lines that genuinely overrun, aligning
continuations to the line's own indent. Use it for the casebook, puzzle
briefings, charts, help, and the act openings.

#### 3. Config System (`config.py`)
Game configuration and constants.
- Game settings
- File paths
- Command sets
- State requirements
- Display settings

Key Features:
```python
# Version Information
GAME_VERSION: Final[str]
SAVE_FILE_VERSION: Final[str]

# Settings Classes
@dataclass(frozen=True)
class TerminalSettings:
    """Terminal display configuration."""
    min_width: int
    max_width: int
    default_width: int
    default_height: int
```

### State Management

#### Game State
- Tracks player progress
- Manages inventory
- Records puzzle completion
- Handles location states

```python
INITIAL_GAME_STATE: Final[Dict[str, Any]] = {
    "morse_attempts": 0,
    "has_badge": False,
    # ... other state variables
}
```

#### Save System
- Auto-save functionality
- Multiple save slots
- State validation
- File management

### Error Handling

#### Exception Hierarchy
```python
class LocationError(Exception):
    """Custom exception for location-related errors."""
    pass

# Error handling in functions
try:
    # Operation
except LocationError as e:
    logging.error(f"Location error: {e}")
    print_text(str(e))
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    print_text("An unexpected error occurred.")
```

### Logging System

#### Configuration
```python
LOG_FORMAT: Final[str] = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

def setup_logging() -> logging.Handler:
    """Configure logging for the game."""
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    return handler
```

## Implementation Guidelines

### Code Style
- Use type hints
- Follow PEP 8
- Document with docstrings
- Use consistent error handling
- Implement logging

### Testing
- Unit tests for core functionality
- Integration tests for systems
- Test save/load operations
- Test error conditions

### Performance Considerations
- Efficient state management
- Proper resource cleanup
- Memory management
- File system operations

## Extending the Game

### Adding New Features
1. Plan the feature
2. Update configuration
3. Implement core logic
4. Add error handling
5. Update documentation
6. Add tests

### Adding New Locations
1. Update `config_locations.py`
2. Add historical notes
3. Define requirements
4. Update location manager

### Adding New Puzzles
1. Create puzzle class
2. Define requirements
3. Implement validation
4. Add to puzzle manager

## Deployment

### Requirements
- Python 3.8+
- Required packages in requirements.txt
- Proper file permissions
- Sufficient disk space

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration
1. Set up logging directory
2. Configure save directory
3. Verify permissions
4. Test installation

## Maintenance

### Logging
- Regular log rotation
- Error monitoring
- Performance tracking
- Usage statistics

### Save Files
- Regular cleanup
- Size management
- Version compatibility
- Backup strategy