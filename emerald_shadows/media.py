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


_vt_ready = False


def _ensure_vt() -> None:
    """Best-effort: enable ANSI (VT) processing on legacy Windows consoles.

    Windows Terminal understands ANSI out of the box; classic conhost supports
    it but only after SetConsoleMode enables ENABLE_VIRTUAL_TERMINAL_PROCESSING.
    Failure is harmless — color_enabled() gating means we only ever get here on
    an interactive terminal, and a console that refuses just shows plain text
    with stray codes suppressed by the NO_COLOR escape hatch.
    """
    global _vt_ready
    if _vt_ready or os.name != "nt":
        _vt_ready = True
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)  # VT processing
    except Exception:
        pass
    _vt_ready = True


def color_enabled() -> bool:
    """ANSI color is allowed only when art is, and honors the NO_COLOR convention."""
    if not (art_enabled() and not _flag_on("NO_COLOR")):
        return False
    _ensure_vt()
    return True


def style(text: str, color: str) -> str:
    """Wrap text in an ANSI color when the terminal can take it; otherwise
    return it unchanged. The single place gameplay code asks for color, so
    the NO_COLOR / non-TTY contract holds everywhere by construction."""
    if not color or not color_enabled():
        return text
    return f"{color}{text}{game_art.RESET}"


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
    "victory": {
        "art": game_art.VICTORY_ART,
        "color": game_art.AMBER,
        "animate": True,
        "audio": None,  # future: sounds/victory_radio.wav
    },
    # District sigils — shown once, on first arrival. Key form: "enter_<location>".
    "enter_smith_tower": {
        "art": game_art.SMITH_TOWER_SIGIL,
        "color": game_art.AMBER,
        "animate": False,
        "audio": None,
    },
    "enter_docks": {
        "art": game_art.DOCKS_SIGIL,
        "color": None,
        "animate": False,
        "audio": None,
    },
    "enter_pike_place": {
        "art": game_art.PIKE_PLACE_SIGIL,
        "color": game_art.RED,  # neon
        "animate": False,
        "audio": None,
    },
    "enter_eagles_hall": {
        "art": game_art.EAGLES_HALL_SIGIL,
        "color": game_art.AMBER,
        "animate": False,
        "audio": None,
    },
    "enter_underground_tunnels": {
        "art": game_art.TUNNELS_SIGIL,
        "color": game_art.BRIGHT_GREEN,  # what waits below is grue-adjacent
        "animate": True,
        "audio": None,  # future: sounds/tunnel_drip.wav
    },
}


def present_location(location: str) -> bool:
    """Present a location's first-visit sigil, if it has one. Safe no-op otherwise."""
    return present(f"enter_{location}")


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
