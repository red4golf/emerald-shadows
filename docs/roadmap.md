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

## Phase 0 — The detective game (done)

The review's core finding was that the mechanics didn't ask the player to be a
detective. They asked the player to be a courier for strings: every "puzzle" was
a password retyped from a note, and there was no way to question anybody. This
phase closed that gap.

- [x] **Real puzzles.** The cipher wheel is a Caesar disc you sweep and read
      (`turn wheel`), cracked by spotting a crib among 25 garbage strings. The
      radio is a band you search with warmer/colder feedback, because the note's
      last digit is rained off. The tunnels carry real Morse decoded against the
      chart in the radio manual. The plate is assembled from three witnesses.
      New `codes.py` holds the transformations as pure functions.
- [x] **Conversation.** `ask <person> about <topic>`, `talk to`, `topics`. Five
      witnesses; topics are global knowledge so a question learned in one place
      can be put anywhere. Content lives in `config_dialogue.py`.
- [x] **Three acts.** Legwork → Heat → Pier Seven, computed from state so saves
      land in the right act. The case now closes on an `arrest` at Pier 7 with
      the evidence in hand, not on a checklist filling up.
- [x] **The casebook.** `case` replaces a bare score with established facts,
      named people, and open threads.
- [x] **Declarative effects.** Examining an item applies a data entry
      (`EXAMINE_DISCOVERIES`) rather than an if/elif chain.

### Softlocks found and fixed while building it

Three of these made the shipped game impossible to finish:

- [x] **You could never get off the trolley.** `off` was routed into the tram's
      movement handler, which only toggled whether it was rolling;
      `exit_trolley()` was written and unit-tested but never wired in. Pioneer
      Square is trolley-only, and it holds the notice that identifies the
      organisation — so the case could not be closed.
- [x] **Re-boarding the trolley left you stuck.** `board_trolley()` was only
      called on the location's first visit, so a second ride never set
      `on_trolley` and could never be got off.
- [x] **`back` was unreachable as an exit.** The parser rewrote it to "south"
      before checking whether the room had an exit named `back` — which is what
      the Eagles hall uses to reach the lounge, where a required item sits.
      Named exits now outrank direction aliases.
- [x] **The notebook was in the smugglers' office**, so Diamond had to find his
      own case notebook in a warehouse. Moved to his desk.
- [x] **EOF crashed the game** with a stack trace instead of exiting cleanly.
- [x] **Structured text was reflowed into a lump.** `print_block` preserves line
      structure for the casebook, charts, briefings and help.

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

- [x] **Anachronism:** Smith Tower elevator operator is now a Pacific war vet
      (was "Korean War vet" — the game is October 1947).
- [x] **Grue restore loaded the oldest save.** `_handle_grue_death` picked
      `saves[-1]` from a newest-first list; now `saves[0]`.
- [x] **Puzzle progress wasn't saved.** `PuzzleManager` now has
      `get_state`/`restore_state` and rides in the save payload
      (`puzzle_state`); old saves without the field load fine.
- [x] **Movement vocabulary split.** Bare named exits ("outside", "upstairs",
      "tavern") now move the player; synonym layer ("o"/"out" → outside,
      "up" ↔ "upstairs", "board" → trolley); new `exits` command lists ways
      out; `take all` / `take everything` implemented.
- [ ] **Dead location refs:** `badge` and `cipher_wheel` list `"warehouse"` in
      `use_locations` (`item_manager.py`), but no such location exists
      (`warehouse_district` / `warehouse_three` / `warehouse_office`). `use`
      silently does nothing there.
- [x] **`INVENTORY_LIMIT` removed** — defined, never read, and a carry limit is
      pure friction in a mystery.
- [ ] **Still unenforced:** `MAX_PUZZLE_ATTEMPTS` and `PUZZLE_TIMEOUT` are
      defined but never read. The reworked puzzles have no attempt limit by
      design (sweeping a band *is* repeated attempts), so these should probably
      just go.
- [x] **Auto-generated gate messages** produced "You need to found warehouse
      first". Authored per-flag messages now live in `config.GATE_MESSAGES`.
- [x] **The solve prompt leaked internals** ("Enter solution for the puzzle at
      evidence_room") in a game whose product is voice.
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
- **Pre-beta fixes.** Movement overhaul (named exits, synonyms, `exits`,
  `take all`), grue restores newest save, puzzle progress persists through
  save/load. 270 tests passing.
