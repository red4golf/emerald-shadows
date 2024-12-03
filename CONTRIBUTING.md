# Contributing to Emerald Shadows

Thank you for considering contributing to Emerald Shadows! Your input helps make this game better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues. When creating a bug report, please include:

* A clear and descriptive title
* Steps to reproduce the problem
* Specific examples demonstrating the steps
* The behavior you observed
* The behavior you expected
* Your configuration and environment details
* Any relevant save files or game state information

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting an enhancement, include:

* A clear and descriptive title
* Detailed description of the suggested enhancement
* Specific examples of how it would work
* The current behavior (if applicable)
* Why this enhancement would improve the game
* Any potential drawbacks or considerations

### Pull Requests

* Use the provided pull request template
* Keep the scope focused and specific
* Include tests for new functionality
* Update documentation as needed
* Follow the existing code style
* Add screenshots for UI changes
* Include test cases demonstrating functionality
* Document new code thoroughly

## Development Process

1. Fork the repository
2. Create a feature branch from `main`
3. Implement your changes
4. Add/update tests
5. Update documentation
6. Submit a pull request
7. Respond to review feedback

### Style Guidelines

* Follow PEP 8 style guide
* Use type hints for all functions
* Include docstrings (Google style)
* Use descriptive variable names
* Keep functions focused
* Maximum line length of 100 characters
* Use consistent naming conventions

### Testing

* Write unit tests for new code
* Ensure all tests pass
* Include integration tests
* Test edge cases
* Test error conditions
* Include game save/load testing
* Test across different Python versions

### Documentation

* Update README.md for interface changes
* Maintain docstrings
* Comment complex logic
* Update type hints
* Include example usage
* Document new game features
* Update test documentation

## Project Structure

```
emerald-shadows/
├── emerald_shadows/       # Main package directory
│   ├── __init__.py
│   ├── game_manager.py    # Main game loop
│   ├── location_manager.py # Location handling
│   ├── item_manager.py    # Inventory system
│   ├── commands/          # Command handling
│   │   ├── __init__.py
│   │   └── natural_commands.py
│   ├── puzzles/          # Puzzle implementations
│   │   ├── __init__.py
│   │   ├── base_puzzle.py
│   │   ├── cipher_puzzle.py
│   │   ├── morse_puzzle.py
│   │   ├── car_puzzle.py
│   │   ├── radio_puzzle.py
│   │   └── puzzle_manager.py
│   ├── trolley_system.py  # Transportation system
│   └── utils.py          # Utility functions
├── tests/                # Test directory
│   ├── __init__.py
│   ├── test_game_manager.py
│   ├── test_location_manager.py
│   ├── test_item_manager.py
│   ├── test_puzzle_*.py
│   └── test_utils.py
├── docs/                # Documentation
└── requirements.txt     # Dependencies
```

## Coding Standards

### Type Hints
```python
def process_command(command: str, game_state: Dict[str, Any]) -> bool:
    """Process a game command."""
    pass
```

### Docstrings
```python
def validate_move(direction: str, current_location: str) -> bool:
    """
    Validate if a move is possible in the given direction.

    Args:
        direction: The direction to move in
        current_location: The player's current location

    Returns:
        bool: True if move is valid, False otherwise
    """
    pass
```

### Error Handling
```python
try:
    result = process_command(command)
except ValueError as e:
    logging.error(f"Invalid command format: {e}")
    return False
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    return False
```

### Tests
```python
def test_movement_validation():
    """Test the movement validation system."""
    location_manager = LocationManager()
    assert location_manager.validate_move("north", "police_station")
    assert not location_manager.validate_move("up", "street")
```

## Adding New Features

### New Puzzles
1. Create a new class inheriting from BasePuzzle
2. Implement required abstract methods
3. Add puzzle to PuzzleManager
4. Create corresponding test file
5. Update documentation

### New Locations
1. Add location to config_locations.py
2. Add any required items
3. Update location connections
4. Add historical notes
5. Update tests

### New Items
1. Add item description to item_manager.py
2. Define usage conditions
3. Add any combination rules
4. Create test cases
5. Update documentation

## Questions?

If you have any questions about contributing:
1. Check existing documentation
2. Search closed issues
3. Open a new issue with the "question" label

Thank you for contributing to Emerald Shadows!
