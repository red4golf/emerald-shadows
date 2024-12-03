# Emerald Shadows User Guide

Welcome to Emerald Shadows, a noir detective text adventure set in 1947 post-war Seattle.

## Getting Started

### Installation
1. Ensure Python 3.8 or higher is installed
2. Download and extract the game
3. Open a terminal in the game directory
4. Run: `python -m emerald_shadows`

### Basic Controls
Type commands and press Enter to interact with the game world. Commands can be written in natural language - the game will understand your intent.

#### Example Commands:
```
> look around the office
You're in a dimly lit detective's office. A wooden desk sits in the center...

> examine the desk
The desk is worn but well-maintained. Several items catch your eye: a telephone, a stack of papers, and an old coffee mug.

> take papers
You pick up the stack of papers. They appear to be case files.
```

## Game Commands

### Movement
Navigate through locations using compass directions or obvious paths.

#### Basic Movement Examples:
```
> go north
Moving north to the hallway...

> s
Moving south to the lobby...

> walk to the door
Moving to the door on the east side...
```

#### Complex Movement Examples:
```
> enter the smith tower
You push through the revolving doors into the grand lobby of Smith Tower...

> climb stairs
You ascend the staircase to the second floor...

> follow the suspicious man
You discretely follow the man down the dimly lit alley...
```

### Investigation
Examine your surroundings and interact with objects to uncover clues.

#### Investigation Examples:
```
> look
The police archives are dimly lit by fluorescent lights. Metal filing cabinets line the walls...

> examine filing cabinet
The cabinet is labeled "1946-1947". One drawer is slightly ajar...

> search drawer
Inside the drawer, you find several case files and an unmarked envelope...

> read envelope
The envelope contains a coded message written in what appears to be invisible ink...
```

### Item Interaction
Items can be combined, used, and examined for clues.

#### Basic Item Examples:
```
> inventory
You are carrying:
- A worn leather notebook
- A police badge
- A blacklight
- Some blank papers

> examine notebook
The notebook contains various case notes and a strange sequence of numbers...

> use blacklight on papers
Under the blacklight, hidden writing becomes visible on the papers!
```

#### Complex Item Combinations:
```
> combine radio parts with antenna
You assemble the parts into a working radio receiver...

> use radio in observation post
You set up the radio and begin scanning frequencies...

> use developed photo with cipher key
Comparing the photo with the cipher key reveals a hidden message!
```

### Puzzle Solutions

#### Radio Frequency Puzzle Example:
```
> examine radio
The radio can tune to different frequencies. A note mentions "7.15"...

> tune radio to 7.15
Static crackles, then a voice emerges: "Package arriving at midnight..."

> note frequency in notebook
You record the frequency and message in your notebook.
```

#### Code Breaking Example:
```
> examine cipher message
The message contains repeating patterns of numbers: 3-15-4-5...

> use decoder ring
Setting the decoder ring to position 3, you begin to decrypt:
"MEET AT SMITH TOWER"...
```

#### Trolley System Navigation:
```
> check trolley schedule
Current Routes:
- Downtown Loop (Stops: Central, Pike, Union)
- Harbor Line (Stops: Waterfront, Warehouse, Docks)

> board trolley
You board the Downtown Loop trolley.

> ask conductor about Pike Street
"Pike Street? That's where all those suspicious deliveries have been..."
```

### Advanced Gameplay Examples

#### Surveillance Operation:
```
> set up observation post
You establish a hidden vantage point overlooking the warehouse entrance.

> use binoculars
Through the binoculars, you observe workers moving crates under cover of darkness.

> photograph suspicious activity
You capture photos of the workers and license plates.
```

#### Environmental Puzzle:
```
> examine broken window
The window is shattered, with glass shards scattered below.

> use gloves
Wearing gloves, you carefully examine the glass fragments.

> analyze break pattern
The break pattern suggests the window was broken from the inside out...
```

#### Historical Investigation:
```
> research Smith Tower history
You learn about the building's significance in 1947 Seattle...

> ask librarian about newspaper archives
The librarian directs you to articles about recent suspicious activities...

> cross-reference dates
The dates of the suspicious activities align with your other evidence!
```

## Game Progress Tips

### Case Development Example:
```
Initial Clue:
> examine police report
A report of suspicious activity at Smith Tower...

Following Lead:
> interview security guard
"I saw strange lights in the tower late at night..."

Gathering Evidence:
> photograph night activities
You document unusual patterns of movement...

Connecting Dots:
> compare photos with schedules
The activities match the pattern in your decoded messages!
```

### Evidence Collection Best Practices:
1. Document everything in your notebook
   ```
   > write in notebook
   Added observation about suspicious lights to case notes...
   ```

2. Photograph key scenes
   ```
   > photograph crime scene
   You take detailed photos of the disturbance...
   ```

3. Collect physical evidence
   ```
   > bag evidence
   You carefully collect and label the suspicious substance...
   ```

## Troubleshooting Common Issues

### Command Recognition:
If a command isn't working, try rephrasing:
```
Instead of:
> use key with door
Try:
> unlock door
or
> insert key into lock
```

### Navigation Help:
If you're lost:
```
> check map
Displays available locations and current position...

> review notes
Shows your documented locations and clues...
```

### Puzzle Assistance:
When stuck on a puzzle:
```
> examine clues
Reviews all relevant clues in your notebook...

> review evidence
Displays collected evidence and possible connections...
```

## Support and Additional Help

### Saving Progress:
```
> save game mysterious_lights
Game saved as "mysterious_lights.save"

> load game mysterious_lights
Loading previous investigation progress...
```

### Getting Help:
```
> help
Displays this guide of commands...

> hint
Provides a subtle hint about your current objective...
```

Remember, Emerald Shadows rewards thorough investigation and creative thinking. Take your time, examine everything, and maintain detailed notes. The truth behind the mysterious activities in post-war Seattle awaits your discovery!