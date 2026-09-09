"""Tests for the CRT color pass: the style() contract and its fallbacks."""

import pytest

from emerald_shadows import casebook, game_art, media
from emerald_shadows.config import INITIAL_GAME_STATE


ESC = "\x1b"


def test_style_plain_when_not_a_tty():
    # Under pytest stdout is captured, so color must be off by default.
    assert media.style("hello", game_art.AMBER) == "hello"


def test_style_colors_when_terminal_allows(monkeypatch):
    monkeypatch.setattr(media, "color_enabled", lambda: True)
    styled = media.style("hello", game_art.AMBER)
    assert styled.startswith(game_art.AMBER)
    assert styled.endswith(game_art.RESET)
    assert "hello" in styled


def test_no_color_wins_even_on_a_tty(monkeypatch):
    monkeypatch.setattr(media, "art_enabled", lambda: True)
    monkeypatch.setenv("NO_COLOR", "1")
    assert media.color_enabled() is False
    assert media.style("hello", game_art.RED) == "hello"


def test_empty_color_is_a_noop(monkeypatch):
    monkeypatch.setattr(media, "color_enabled", lambda: True)
    assert media.style("hello", "") == "hello"


def test_ensure_vt_is_safe_to_call():
    media._ensure_vt()
    media._ensure_vt()  # idempotent


def test_casebook_render_has_no_ansi_codes_when_color_disabled():
    from copy import deepcopy
    text = casebook.render(deepcopy(INITIAL_GAME_STATE), [], {})
    assert ESC not in text


def test_casebook_render_colors_headers_when_enabled(monkeypatch):
    from copy import deepcopy
    monkeypatch.setattr(media, "color_enabled", lambda: True)
    text = casebook.render(deepcopy(INITIAL_GAME_STATE), [], {})
    assert game_art.AMBER in text and game_art.RESET in text


def test_historical_note_has_no_ansi_codes_when_color_disabled(monkeypatch):
    import emerald_shadows.location_manager as lm_module
    from emerald_shadows.location_manager import LocationManager

    lm = LocationManager()
    messages = []
    monkeypatch.setattr(lm_module, "print_text", lambda t, **_: messages.append(t))
    lm._announce_first_visit("street")
    assert messages and all(ESC not in m for m in messages)
