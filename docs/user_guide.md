# Emerald Shadows User Guide

## Getting Started

Welcome to Emerald Shadows, a text adventure game set in 1947 post-war Seattle. As Detective Johnny Diamond, you'll investigate missing medical supplies, explore the city's underground tunnels, and uncover a complex smuggling operation.

### Installation

1. Make sure you have Python 3.8 or newer installed
2. Clone the repository and install it (editable mode recommended during development):
   ```bash
   pip install -e .
   ```
3. Start the game:
   ```bash
   python -m emerald_shadows
   # or just run
   emerald-shadows
   ```

## Basic Commands

- `look`: Examine your surroundings
- `look at [item]` / `examine [item]`: Look at something closely
- `inventory` (`i`): Check what you're carrying
- `take [item]`: Pick up an item (`take all` grabs everything here)
- `drop [item]`: Set something down
- `use [item]`: Put an item to work
- `combine [x] with [y]`: Two clues are sometimes one clue
- `go [direction]`: Move — compass directions and named exits both work
- `exits`: List the ways out
- `case`: Your casebook — established, named, still open
- `score`: The short version of the same thing
- `help`: The full list
- `save` / `load` / `quit`

## Talking to People

Nobody in this city volunteers anything. Ask.

- `talk to [person]`: Walk up to somebody and see what they'll give you
- `ask [person] about [topic]`: Put a specific question
- `topics`: What you currently know enough to ask about

Topics are knowledge, not permission. A question you learn from one person can
be put to anybody — and different people know different pieces of it. That's the
loop: you go back around the city because you have a better question than you had
an hour ago.

You can't ask about something you haven't heard of yet, and some people won't
talk to you at all until you've shown them a reason to. When somebody is worth
talking to, the room tells you they're there.

## Working the Evidence

`solve` lays out whatever the room has to be worked. Most of it you then operate
yourself:

- `turn wheel` / `turn wheel to [letter]`: The cipher disc
- `tune [frequency]`: Sweep a radio band, e.g. `tune 415.3`
- `listen` / `tap [answer]`: Hear a signal, and answer it
- `arrest`: End it — when you can prove it

## Advanced Features

### Inventory System
- No limit on inventory size
- Items can be combined for new discoveries
- Context-sensitive item usage
- Detailed item descriptions available

### Save System
- Save your progress: `save [name]`
- Load a saved game: `load [name]`
- Auto-save every 5 minutes
- View saves: `saves`

### Trolley System
When on the trolley:
- `next`: Move to next stop
- `off`: Exit at current stop
- `status`: View route information

## Locations

### Police Station
Your base of operations, containing:
- Your desk
- Evidence room
- Captain's office

### Pike Place Market
A bustling marketplace where:
- Locals gather
- Information can be found
- Suspicious activities might be observed

### Pioneer Square
Historic heart of Seattle:
- Access to underground tunnels
- Various shops and businesses
- Historical information

### Smith Tower
Tallest building west of the Mississippi:
- Observation deck
- Business offices
- Possible surveillance spot

### Waterfront District
Center of maritime commerce:
- Shipping docks
- Warehouse district
- Suspicious activities

## Tips for Success

1. Examine everything you pick up — a close look is often what opens a new
   line of questioning.
2. Ask everybody about everything. A topic you learn at the bar is worth
   putting to the elevator operator, and vice versa.
3. `case` when you lose the thread. It'll tell you what's still open.
4. The people who help you are rarely the ones you'd expect, and the ones who
   help you at real cost to themselves only do it once.
5. Carry a light source. Seattle has places the lights don't reach.
6. The trolley isn't scenery — Pioneer Square can only be reached by riding it,
   and the motorman is worth more than the fare.

## Puzzle Types

None of these are passwords. You are given materials and a way to work them, and
the answer is what comes out.

### The Cipher Wheel
Two rings of letters, one inside the other — a shift cipher, 1947 field
tradecraft. `turn wheel` walks it through all twenty-six settings and shows you
the memo's first word at each one. Twenty-five of those are noise. Spot the one
that isn't, then `turn wheel to [that letter]` to read the whole thing.

That's how you actually break one of these: you don't guess the key, you look for
a word you expect to see.

### Radio Frequencies
The informant's note has been in a wet coat pocket and lost its last digit. What
you have is a band, not a number. `tune` your way across it — the static thins as
you get warm, and a voice surfaces and drowns before it's a word. Keep going.

### Morse
Somebody is tapping on a pipe in the tunnels. It's real Morse, and the code chart
is folded into the back of the radio manual you're carrying — `examine
radio_manual` to read it. Three characters. Decode it by hand, then `tap` it back.

### The Licence Plate
No trick at all: this is the legwork puzzle. Nobody saw the whole plate. Three
people each saw a different piece of it, and you have to go and ask all three.
`solve` at Pioneer Square shows how much of it you've assembled so far.

## The Three Acts

The case runs in three acts, and you don't choose when they turn — the work does.

**Act One — Legwork.** You ask questions and nobody much minds.

**Act Two — Heat.** You decoded something in a locked room and by morning the
city knows. There's a car at the end of Third that wasn't there before. From here
everything you learn costs somebody something — including a man you came up
through the academy with, who is now sitting on the edge of your desk.

**Act Three — Pier Seven.** The warehouse, the plate, the frequency, the word
that opens the gate. Pier 7 opens south from the docks, and the case does not
close until you go down there and `arrest` — with the evidence in your pocket. A
man with a clipboard and a ship half-unloaded is not an arrest. Turn up
empty-handed and you'll be turned around.

## Historical Context

The game is set in 1947 Seattle, featuring:
- Post-war atmosphere
- Historical landmarks
- Actual city layout
- Period-appropriate details

## Need Help?

If you get stuck:
- Use the `help` command
- Examine your surroundings
- Check your inventory
- Review your notes
- Consider item combinations

Remember, every detail could be important to solving the case!