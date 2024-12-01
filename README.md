# Emerald Shadows: A Detective Adventure

Emerald Shadows is a detective text adventure game set in 1947 post-war Seattle. Players take on the role of Detective Johnny Diamond investigating a mysterious case involving missing medical supplies, smuggling operations, and the city's historic underground tunnels.

## Features

- Rich, historically accurate setting in 1947 Seattle
- Complex puzzle-solving gameplay including:
  - Morse code decoding
  - Radio frequency puzzles
  - Car surveillance challenges
  - Cipher decryption
- Multiple locations to explore including:
  - Pike Place Market
  - Pioneer Square
  - Smith Tower
  - Seattle Underground
  - Waterfront District
  - Warehouse District
- Advanced inventory system with:
  - Combinable items
  - Context-sensitive item usage
  - Detailed item descriptions
- Historic trolley system for transportation
- Auto-save functionality
- Historical facts about Seattle's post-war era
- Comprehensive save/load system with multiple save slots

## Installation

1. Clone the repository:
```bash
git clone https://github.com/red4golf/emerald-shadows.git
cd emerald-shadows
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Game Commands

### Basic Commands
- `look`: Examine your surroundings
- `inventory`: Check your belongings
- `help`: Display available commands
- `history`: Learn historical facts about your location
- `quit`: Exit the game

### Movement & Investigation
- `go [direction]`: Move to a new location
- `take [item]`: Pick up an item
- `examine [item]`: Look at an item closely
- `talk`: Speak to anyone present
- `solve`: Attempt to solve a puzzle in your location

### Item Interaction
- `use [item]`: Use an item in your inventory
- `combine [item1] [item2]`: Try to use two items together

### Save System
- `save [name]`: Save your game with optional name
- `load [name]`: Load a saved game
- `saves`: List available save files

### Trolley System
When on the trolley:
- `next`: Move to next stop
- `off`: Exit at current stop
- `status`: View route information
- `history`: Learn about current stop

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.