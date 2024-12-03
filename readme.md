# Emerald Shadows

![Game Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A noir detective text adventure set in 1947 post-war Seattle. Investigate mysterious events, decode messages, and uncover the truth behind suspicious activities centered around Smith Tower.

## Features

### Core Gameplay
- Rich, atmospheric text-based gameplay
- Intuitive natural language commands
- Strategic inventory management
- Complex puzzle-solving mechanics

### Setting & Story
- Historically accurate 1947 Seattle locations
- Film noir atmosphere and storytelling
- Detailed historical notes and context
- Multiple interweaving mysteries

### Locations
- Police headquarters
- Smith Tower
- Historic trolley system
- Warehouse district
- Observation points
- Downtown streets

### Puzzle Types
- Radio frequency scanning
- Morse code interception
- Surveillance operations
- Code breaking
- Item combinations
- Environmental puzzles

### Game Systems
- Intelligent command parsing
- Comprehensive save/load system
- Auto-save functionality
- Detailed help system
- Progress tracking

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Command line terminal
- 50MB free disk space

### Basic Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/emerald-shadows.git
cd emerald-shadows

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python -m emerald_shadows
```

### Development Installation
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
flake8 emerald_shadows/
```

## Quick Start Guide

### Basic Commands
```
look        - Examine your surroundings
inventory   - Check your items
take [item] - Pick up an item
examine     - Look at something closely
go [dir]    - Move in a direction
help        - Show available commands
```

### Movement
- Use cardinal directions: north, south, east, west
- Or shortcuts: n, s, e, w
- Additional: up, down when available

### Game Progress
1. Start at police headquarters
2. Gather initial evidence
3. Explore the city
4. Solve interconnected puzzles
5. Uncover the truth

## Project Structure
```
emerald-shadows/
├── emerald_shadows/       # Main package
│   ├── __init__.py
│   ├── game_manager.py   # Core game logic
│   ├── location_manager.py
│   ├── item_manager.py
│   ├── config.py
│   ├── game_art.py      # ASCII art
│   ├── commands/        # Command handling
│   ├── puzzles/        # Puzzle system
│   └── utils.py
├── tests/              # Test suite
├── docs/              # Documentation
│   ├── technical.md
│   ├── development.md
│   └── user_guide.md
└── requirements.txt   # Dependencies
```

## Documentation
- [User Guide](docs/user_guide.md) - Complete gameplay guide
- [Technical Documentation](docs/technical.md) - System architecture and implementation
- [Development Guide](docs/development.md) - Contributing and development setup

## Development

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_location_manager.py

# Run with coverage
pytest --cov=emerald_shadows tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Include docstrings
- Add unit tests

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License
This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md)

## Acknowledgments
- Inspired by classic text adventures
- Historical information from Seattle Municipal Archives
- Built with Python 3.8+
- Thanks to all contributors

## Support
- Check the [User Guide](docs/user_guide.md)
- Open an issue for bugs
- See [development guide](docs/development.md) for contributing
- Contact: [your-email@example.com]

## Version History
- 1.0.0 (2024-12-02)
  - Initial release
  - Core game features
  - Basic puzzle system
  - Save/load functionality

## Roadmap
- Additional puzzles and locations
- Enhanced historical content
- Improved command parsing
- Extended puzzle system
- Additional game modes