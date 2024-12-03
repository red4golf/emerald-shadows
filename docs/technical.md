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