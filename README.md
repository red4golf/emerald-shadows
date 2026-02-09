# Emerald Shadows

A noir detective text adventure set in 1947 post-war Seattle. As Detective Johnny Diamond you will interrogate witnesses, decode clandestine transmissions, and navigate the city’s trolley lines while piecing together a smuggling ring that stretches from Smith Tower to the docks.

## Highlights

- **Fully text-driven investigation** with natural-language style commands.
- **Historically grounded locations** including police headquarters, Smith Tower, and the underground tunnels.
- **Rich inventory & puzzle systems** covering Morse code, cipher wheels, radio scans, and item combinations.
- **Integrated trolley network** for moving between districts.
- **Auto-save plus manual save slots** so you never lose a lead.

## Installation

### Prerequisites
- Python 3.8 or newer
- `pip`
- Terminal/command prompt access

### Steps
```bash
# Clone the repository
git clone https://github.com/red4golf/emerald-shadows.git
cd emerald-shadows

# (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install the package in editable mode with dev tooling
pip install -r requirements.txt
```

## Running the Game
```bash
python -m emerald_shadows
```

During play you can always type `help` to see the available actions. Common verbs include `look`, `inventory`, `take <item>`, `use <item>`, `go <direction>`, and `solve` for puzzles.

## Project Structure
```
emerald-shadows/
├── emerald_shadows/
│   ├── game_manager.py        # Core game loop
│   ├── location_manager.py    # Movement + descriptions
│   ├── item_manager.py        # Inventory handling
│   ├── puzzles/               # Puzzle subsystems
│   ├── commands/              # Natural-language parsing
│   └── utils.py               # Display + save helpers
├── tests/                     # Pytest suite
├── docs/
│   ├── user_guide.md
│   ├── technical.md
│   └── development.md
├── requirements.txt
└── setup.py
```

## Documentation
- **Gameplay/User Guide**: `docs/user_guide.md`
- **Technical Overview**: `docs/technical.md`
- **Development Guide**: `docs/development.md`

## Development

Run the automated checks before submitting a change:
```bash
pytest                        # run unit tests
pytest --cov=emerald_shadows  # run with coverage reporting
flake8 emerald_shadows        # style checks
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/awesome-improvement`
3. Commit your work: `git commit -m "Describe change"`
4. Push the branch and open a PR

See `CONTRIBUTING.md` for the full process and expectations.

## License

This project is released under the MIT License — see [LICENSE.md](LICENSE.md).
