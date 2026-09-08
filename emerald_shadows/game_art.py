# ASCII art elements for Emerald Shadows

from .utils import clear_screen, print_text

# --- Optional ANSI styling -------------------------------------------------
# Raw escape codes. Callers must confirm the terminal can take color before
# using these (see media.art_enabled / NO_COLOR handling). Defined here so all
# visual assets live in one place.
RESET = "\033[0m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
AMBER = "\033[33m"
BRIGHT_GREEN = "\033[92m"

# Two eyes and a maw surfacing out of the dark. You never really see a grue —
# you see what little the dark lets you. Kept under 60 columns so it survives a
# narrow terminal (DisplayManager clamps width to a 60-column minimum).
# --- District sigils -------------------------------------------------------
# Small marks shown once, on first arrival at a landmark. Curated, not
# exhaustive: most rooms get prose only. All pieces stay under 60 columns
# (DisplayManager's minimum terminal width).

# Forty-two stories of terracotta and ambition, pyramid cap lit.
SMITH_TOWER_SIGIL = r"""
              /\
             /  \
            |----|
            | [] |
            | [] |
            | [] |
            | [] |
          __|    |__
         |  [] []  |
         |  [] []  |
         |__[]_[]__|
"""

# The working waterfront.
DOCKS_SIGIL = r"""
             __
            (  )
             ||
         ----++----
             ||
             ||
         \   ||   /
          \_ || _/
            \||/
             --
"""

# The Public Market Center sign and clock, neon since the thirties.
PIKE_PLACE_SIGIL = r"""
     _____________________________
    |   PUBLIC  MARKET  CENTER    |
    |_____________________________|
        ||      .-"-.      ||
        ||     ( 7:05 )    ||
        ||      `---'      ||
"""

# The crest over the door at Seventh and Union.
EAGLES_HALL_SIGIL = r"""
      ______________________________
     / FRATERNAL ORDER OF EAGLES    \
     \   Aerie No. 1 --- Est. 1898  /
      `----------------------------'
"""

# The mouth of the underground. The dark inside is not decorative.
TUNNELS_SIGIL = r"""
          .-===========-.
         //   _______   \\
        ||   /███████\   ||
        ||   |███████|   ||
        ||   |███████|   ||
      __||___|███████|___||__
"""

# The case-file stamp shown before the closing expense-account memo.
# Kept under 60 columns (DisplayManager's minimum terminal width).
VICTORY_ART = r"""
 ______________________________________________
|                                              |
|  SEATTLE POLICE DEPT. — DETECTIVE DIVISION   |
|  CASE No. 447-E — NORTHWEST MARITIME IMPORTS |
|                                              |
|       ╔═══════════════════════════╗          |
|       ║   C A S E   C L O S E D   ║          |
|       ╚═══════════════════════════╝          |
|                                              |
|  Det. J. Diamond ............. October 1947  |
|______________________________________________|
"""

GRUE_ART = r"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░██░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░
░░░░░░░░░░██░░░░░░░░░░░░░░░░░░░░██░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░█ V V V V V V █░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
"""

TITLE_ART = r"""
███████╗███╗   ███╗███████╗██████╗  █████╗ ██╗     ██████╗ 
██╔════╝████╗ ████║██╔════╝██╔══██╗██╔══██╗██║     ██╔══██╗
█████╗  ██╔████╔██║█████╗  ██████╔╝███████║██║     ██║  ██║
██╔══╝  ██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║██║     ██║  ██║
███████╗██║ ╚═╝ ██║███████╗██║  ██║██║  ██║███████╗██████╔╝
╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝ 
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███████╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║███████╗
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝
"""

SEATTLE_SKYLINE = r"""
                                                     /\      
                              __________            /  \     
                             |          \      __  /    \    
           __                | |[]  []  |\    |  |/      \   
    []    |  |     []       | |    _    | [] | []      []|  
    ||====|  |=====||       | |   |_|   |    |  |        |  
    ||    |  |     ||    [] | |         |    |  |  []    |  
    ||____|  |___  ||    ||=|_|     _   |    |  |   _    |  
    ||====|  |===| ||    || ===    |_|  |    |  |  |_|   |  
 _  ||    |  |   | ||    ||        []  []    |  |   []   |  
|_| ||    |  |   | ||__  ||     _     ||  _ |  |    _    |  
    ||    |  |   | |===| ||    |_|    || |_||  |   |_|   |  
 [] ||    |  |   | |   | ||    []     ||    |  |    []   |  
 ||_||    |  |   | |   | ||    ||     ||    |  |    ||   |  
 |===|    |  |   | |   | ||    ||     ||    |  |    ||   |  
 |   |    |  |   | |   | ||    ||     ||    |  |    ||   |  
 |___|====|__|===|_|===|_||====||=====||====|__|====||===|  
    |     |  |   | |   |  |     |      |     |  |     |     
    |     |  |   | |   |  |     |      |     |  |     |     
____|_____|__|___|_|___|__|_____|______|_____|__|_____|______
"""

def display_title_screen() -> None:
    """Display the game's title screen with both logo and skyline."""
    clear_screen()
    print(TITLE_ART)
    print_text(
        "Seattle, Washington. October 1947.\n"
        "The war is two years over and the city hasn't slept.\n"
        "Neither have you.\n"
    )
    print(SEATTLE_SKYLINE)
    print_text(
        "\nYou are Johnny Diamond, Detective.\n"
        "You are standing at the beginning of a long investigation.\n"
        "It is not, as yet, dark.\n\n"
        "Type 'help' for commands. Press Enter to begin your investigation..."
    )
    input()