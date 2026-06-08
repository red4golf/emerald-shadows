# Emerald Shadows — Roadmap

A living plan for the future of the game. Captures the current review findings,
the architectural direction, and the phased work. Update as things ship.

Guiding principle: **text adventure first.** Art and audio are an optional,
degradable layer on top. The game must remain fully playable — and the test
suite must stay green — with zero art and zero audio. We stay true to the Zork
DNA (parser, rooms, grue, inventory, dry wit) while making it ours through the
noir voice, real 1947 Seattle history, and a multimedia skin Zork never had.

---

## Vision

Three threads, all hanging off one small **media layer**:

1. **ASCII art at key moments** — 80s/90s style, used sparingly for impact
   (grue death, victory, the tunnels, district headers).
2. **Diegetic audio (ElevenLabs)** — sound that comes from a *source in the
   world*: the radio when you tune to 415.6 MHz, an intro "radio drama"
   voiceover. Pre-generated and shipped as files, never called at runtime.
3. **Zork homage, our own spin** — keep the homage explicit, layer the noir
   detective-radio-drama identity on top.

---

## Architecture: the media layer

The game announces narrative **moments**; a thin media layer decides what the
current environment can actually show. The game never knows whether a moment
triggers art, audio, both, or nothing.

- `emerald_shadows/game_art.py` — visual + style **assets** (art strings, ANSI
  color constants).
- `emerald_shadows/media.py` — **orchestration**: a `MOMENTS` registry mapping a
  key to `{art, color, animate, audio}`, plus `present(moment_key)`.
- Game code calls `present("grue_death")` at dramatic beats.

Safety contract (already enforced):

- **Degrades gracefully.** `art_enabled()` is True only on an interactive TTY;
  redirected/captured output (pytest, pipes, CI) shows nothing. `EMERALD_NO_ART`
  force-disables.
- **Color is opt-in and respects `NO_COLOR`** (`color_enabled()`).
- **Never crashes gameplay.** `present()` swallows rendering errors; art writes
  fall back to raw UTF-8 bytes when the console encoding (cp1252 on Windows)
  can't represent the block glyphs.

Adding a new visual/audio beat = add art to `game_art.py`, add an entry to
`MOMENTS`, and drop one `present("key")` call at the right spot.

---

## Phase 1 — ASCII art moments

Cheap, high-impact, no new dependencies, reversible.

- [x] **Media layer seam** (`media.py`) with capability detection + safety contract.
- [x] **Grue death art**, wired through `present("grue_death")` with a slow,
      line-by-line reveal. *(Vertical slice — proves the whole pattern.)*
- [ ] **Victory art** for the expense-account memo ending.
- [ ] **Underground tunnels** entrance art (sets up the grue threat).
- [ ] **Per-district header sigils** (small, ≤ 60 cols) shown on first visit.
- [ ] Asset guidelines: keep art ≤ 60 columns (DisplayManager's min width);
      curate a few strong pieces rather than art everywhere.

## Phase 2 — CRT / color styling

- [ ] Optional ANSI color pass (amber or green phosphor tint for the retro feel).
- [ ] Confirm `NO_COLOR` + non-TTY fallbacks across all art.
- [ ] Consider a one-time `sys.stdout.reconfigure(encoding="utf-8")` at startup
      so Unicode art (incl. existing `TITLE_ART`) is robust on legacy consoles.

## Phase 3 — Diegetic audio (ElevenLabs)

Decision: **pre-generate, don't call the API at runtime.** Content is fixed, so
author the lines once with ElevenLabs during development, commit the audio
files, and ship them — players need no API key, no network, no latency, no cost,
and it works offline.

- [ ] Pick playback approach (Windows `winsound` is WAV-only; ElevenLabs returns
      MP3 — either export/convert to WAV or use a cross-platform player such as
      `pygame.mixer` / `simpleaudio`).
- [ ] **Non-blocking + skippable**: play on a background thread; any key/Enter
      cuts it. The `> ` prompt must never freeze.
- [ ] **Off by default, fully optional**: no audio deps installed → game runs
      identically, tests stay green. Add `audio_enabled()` + a settings flag.
- [ ] **Pilot: the radio broadcast.** When the player tunes to 415.6 MHz, play
      the smuggler chatter. Most "ours," proves the concept end to end.
- [ ] **Intro voiceover** — a "previously, on the radio…" cold open in the
      Johnny Dollar / Richard Diamond register the victory memo already nods to.
- [ ] Keep audio diegetic — radio/tavern, not a narrator over every room.

---

## Bug & consistency backlog (from the review)

Fold these in alongside the feature work.

- [ ] **Anachronism:** `config_locations.py` describes the Smith Tower elevator
      operator as a "Korean War vet" — the game is October 1947; the Korean War
      began 1950. Make him a WWII / Pacific vet.
- [ ] **Dead location refs:** `badge` and `cipher_wheel` list `"warehouse"` in
      `use_locations` (`item_manager.py`), but no such location exists
      (`warehouse_district` / `warehouse_three` / `warehouse_office`). `use`
      silently does nothing there.
- [ ] **Unenforced config:** `INVENTORY_LIMIT`, `MAX_PUZZLE_ATTEMPTS`,
      `PUZZLE_TIMEOUT` are defined but never read; puzzle "fail" text implies
      limited attempts that don't exist. Wire up or remove.
- [ ] **Trolley quirks:** unreachable `command == "look"` branch in
      `location_manager.handle_trolley_command`; `status`/`history` typed off the
      trolley silently no-op.
- [ ] **Cosmetic:** darkness-warning text duplicated in `_handle_look` and
      `_check_darkness`; duplicate git commit in history.

---

## Larger design opportunities (post-multimedia)

Bigger swings to deepen the noir RPG once the multimedia layer lands:

- **Real interrogation/dialogue.** The README promises "interrogate witnesses,"
  but the only reactive NPC is Ches (`use badge` at the Anchor Tavern). A topic
  + evidence dialogue system would close the biggest promise/mechanics gap.
- **Make the devices real.** A cipher wheel that actually rotates, a radio you
  scan across frequencies, Morse you tap — turn "type the answer you already
  read" into genuine interaction.
- **Stakes.** A turn/time budget (the 2 AM broadcast framing), branching
  outcomes, multiple endings tied to the expense-memo epilogue.
- **A casebook/objectives view** so players can see what the case still needs
  (today the only feedback is a score number; dropping a required item silently
  breaks the win condition).
- **More content, same engine.** New districts / a second case — the
  data-driven design scales to this trivially.
- **Web/graphical port.** JSON saves + clean I/O separation make this feasible.

---

## Status log

- **Phase 1 started.** Media layer + grue-death vertical slice landed; 253
  tests still passing. Next up: victory + tunnels art.
