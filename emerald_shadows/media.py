"""Presentation/media layer for Emerald Shadows.

The game announces narrative *moments* (e.g. ``present("grue_death")``); this
layer decides what the current environment can actually show — ASCII art now,
audio later. It always degrades gracefully: on a non-interactive terminal (or
when disabled by env var) it does nothing, so the game stays "text adventure
first" and the test suite runs untouched.

Design rule: presentation is never allowed to break gameplay. Every public
function here is safe to call unconditionally and never raises into the loop.
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any, Dict, Optional

from . import game_art


def _flag_on(name: str) -> bool:
    """Return True if an env var is set to a truthy value."""
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def art_enabled() -> bool:
    """ASCII art shows only on a real interactive terminal.

    Suppressed when stdout is redirected/captured (pytest, pipes, CI) or when
    EMERALD_NO_ART is set. This is what keeps the 253-test suite output clean.
    """
    if _flag_on("EMERALD_NO_ART"):
        return False
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


def color_enabled() -> bool:
    """ANSI color is allowed only when art is, and honors the NO_COLOR convention."""
    return art_enabled() and not _flag_on("NO_COLOR")


def audio_enabled() -> bool:
    """Audio is opt-in and stays off until the audio backend lands (roadmap phase 3)."""
    return False


# Registry of narrative moments -> presentation assets. Adding a new visual or
# audio beat is a data change here plus a single present("key") call in the game.
# 'audio' paths are placeholders reserved for the roadmap's audio phase.
MOMENTS: Dict[str, Dict[str, Any]] = {
    "grue_death": {
        "art": game_art.GRUE_ART,
        "color": game_art.BRIGHT_GREEN,
        "animate": True,
        "audio": None,  # future: sounds/grue_death.wav
    },
}


def _emit(text: str) -> None:
    """Write text to stdout, falling back to raw UTF-8 bytes when the console's
    encoding (e.g. cp1252 on Windows) can't represent the block-art glyphs."""
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        try:
            sys.stdout.flush()
            sys.stdout.buffer.write(text.encode("utf-8"))
            sys.stdout.buffer.flush()
        except Exception:
            pass


def _render_art(art: str, color: Optional[str], animate: bool) -> None:
    """Print an art block, optionally colorized and revealed line by line."""
    use_color = bool(color) and color_enabled()
    for line in art.strip("\n").splitlines():
        _emit(f"{color}{line}{game_art.RESET}\n" if use_color else f"{line}\n")
        if animate:
            sys.stdout.flush()
            time.sleep(0.04)


def present(moment_key: str) -> bool:
    """Present a narrative moment's media. Returns True if anything was shown.

    Safe to call from anywhere: no-ops on non-interactive terminals and
    swallows any rendering error rather than disturbing the game loop.
    """
    moment = MOMENTS.get(moment_key)
    if not moment:
        return False

    shown = False
    try:
        if moment.get("art") and art_enabled():
            sys.stdout.write("\n")
            _render_art(moment["art"], moment.get("color"), moment.get("animate", False))
            shown = True
        # Audio playback is reserved for roadmap phase 3:
        # if moment.get("audio") and audio_enabled():
        #     _play_audio(moment["audio"])
    except Exception:
        # Presentation must never break gameplay.
        return shown
    return shown
