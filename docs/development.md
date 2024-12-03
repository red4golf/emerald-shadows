# Development Guide for Emerald Shadows

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv)
- Text editor or IDE

### Development Environment Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/emerald-shadows.git
cd emerald-shadows
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

## Project Structure

```
emerald-shadows/
├── emerald_shadows/       # Main package
│   ├── __init__.py
│   ├── game_manager.py   # Game loop and state
│   ├── location_manager.py
│   ├── item_manager.py
│   ├── config.py        # Game configuration
│   ├── game_art.py      # ASCII art
│   ├── commands/        # Command handling
│   ├── puzzles/         # Puzzle system
│   └── utils.py
├── tests/              # Test files
├── docs/              # Documentation
└── saves/             # Save file directory
```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use descriptive variable names
- Comment complex logic

Example:
```python
def process_command(self, command: str) -> bool:
    """
    Process a game command and return whether to continue.
    
    Args:
        command: The user's input command
        
    Returns:
        bool: True if game should continue, False to end
    """
    if not command:
        return True
```

### Error Handling
- Use custom exceptions
- Log all errors
- Provide user-friendly messages
- Clean up resources

Example:
```python
try:
    self.move_to_location(direction)
except LocationError as e:
    logging.error(f"Location error: {e}")
    print_text("You cannot go that way.")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    print_text("An error occurred.")
```

### Testing
- Write unit tests for new features
- Test error conditions
- Test edge cases
- Maintain test coverage

Example test:
```python
def test_move_to_invalid_location():
    location_manager = LocationManager()
    result = location_manager.move_to_location("invalid", {})
    assert result is False
```

## Adding New Features

### Adding a New Location
1. Update `config_locations.py`:
```python
NEW_LOCATION = {
    "name": "warehouse",
    "description": "A dusty warehouse...",
    "exits": {"north": "street", "south": "dock"},
    "items": ["crate", "rope"],
    "requires": "found_key",
    "historical_note": "This warehouse..."
}
```

2. Add to location manager:
```python
self.locations[NEW_LOCATION["name"]] = Location(**NEW_LOCATION)
```

### Adding a New Puzzle
1. Create puzzle class:
```python
class NewPuzzle:
    def __init__(self):
        self.requirements = ["item1", "item2"]
        
    def solve(self, inventory: List[str]) -> bool:
        return all(item in inventory for item in self.requirements)
```

2. Register with puzzle manager:
```python
self.puzzles["new_puzzle"] = NewPuzzle()
```

### Adding a New Command
1. Update command handler:
```python
def handle_new_command(self, args: str) -> None:
    """Handle the new command."""
    # Implementation
```

2. Register command:
```python
COMPLEX_COMMANDS.add("new_command")
handlers["new_command"] = self.handle_new_command
```

## Release Process

1. Update version:
```python
GAME_VERSION = "1.1.0"
SAVE_FILE_VERSION = "1.1"
```

2. Update changelog:
```markdown
## [1.1.0] - 2024-12-02
### Added
- New warehouse location
- Additional puzzles
### Fixed
- Bug in movement system
```

3. Run tests:
```bash
pytest tests/
```

4. Create release:
```bash
git tag v1.1.0
git push origin v1.1.0
```

## Troubleshooting

### Common Issues
1. Save file errors:
   - Check permissions
   - Verify save directory
   - Check file format

2. Location errors:
   - Validate location data
   - Check requirements
   - Verify connections

3. Game state errors:
   - Check initialization
   - Verify state updates
   - Validate save data

### Debugging
- Use logging:
```python
logging.debug(f"Processing command: {command}")
logging.error(f"Failed to move: {e}")
```

- Check log file:
```bash
tail -f emerald_shadows.log
```

## Support

### Reporting Issues
- Use issue template
- Include logs
- Describe steps
- Provide save file

### Getting Help
- Check documentation
- Review examples
- Ask in discussions
- Contact maintainers