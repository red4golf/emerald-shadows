# Emerald Shadows

A noir detective text adventure set in 1947 post-war Seattle. As Detective Johnny Diamond you will interrogate witnesses, decode clandestine transmissions, and navigate the city’s trolley lines while piecing together a smuggling ring that stretches from Smith Tower to the docks.

## Highlights

- **Witnesses you actually interrogate.** `ask <person> about <topic>`. Topics are
  knowledge, not permission — a question you learn at the bar can be put to the
  elevator operator, and different people hold different pieces of the same fact.
- **Puzzles you work rather than answer.** Spin a Caesar disc through 26 settings
  and watch for the one that turns noise into English. Sweep a radio band for a
  frequency the rain took the last digit off. Decode real Morse against the chart
  in your radio manual. No passwords to retype from a note.
- **A case in three acts.** Legwork, then heat — the city notices you're asking —
  then Pier 7 after midnight, where the case closes only if you can prove it.
- **A casebook**, not a score. `case` shows what's established, who's named, and
  what's still open.
- **Historically grounded locations** including police headquarters, Smith Tower,
  the Eagles hall, and the tunnels under Pioneer Square.
- **Integrated trolley network** for moving between districts.
- **Auto-save on every change of scene**, plus manual save slots.

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

During play, `help` lists everything. The verbs you'll reach for most:

| | |
|---|---|
| `look`, `examine <item>`, `take <item>` | the basics |
| `talk to <person>`, `ask <person> about <topic>`, `topics` | working a witness |
| `solve`, `turn wheel`, `tune <freq>`, `listen`, `tap <answer>` | working the evidence |
| `case` | where you are and what's left |
| `arrest` | when you can prove it |

## Project Structure
```
emerald-shadows/
├── emerald_shadows/
│   ├── game_manager.py        # Core game loop
│   ├── acts.py                # Three-act progression + the finale gate
│   ├── casebook.py            # The `case` command
│   ├── dialogue.py            # Conversation engine
│   ├── config_dialogue.py     # Who knows what (data)
│   ├── codes.py               # Caesar + Morse codecs (pure functions)
│   ├── location_manager.py    # Movement + descriptions
│   ├── item_manager.py        # Inventory handling
│   ├── puzzles/               # Puzzle subsystems
│   ├── commands/              # Natural-language parsing
│   ├── media.py               # Optional art/audio layer
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
