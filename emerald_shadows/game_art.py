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