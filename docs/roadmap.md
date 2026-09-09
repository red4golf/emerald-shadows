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
- [x] **Victory art** — CASE CLOSED file stamp before the expense-account memo.
- [x] **Underground tunnels** entrance art — brick arch, solid-black mouth,
      grue-green, revealed line by line on first descent.
- [x] **District sigils** shown once on first arrival, via
      `media.present_location` from the shared first-visit announcer:
      Smith Tower, the docks anchor, the Pike Place Market sign (neon red),
      the Eagles crest banner, and the tunnels arch. Curated on purpose —
      most rooms stay prose-only; the starting bullpen is covered by the
      title screen.
- [ ] Asset guidelines: keep art ≤ 60 columns (DisplayManager's min width);
      curate a few strong pieces rather than art everywhere.

## Phase 2 — CRT / color styling

- [x] **`media.style(text, color)`** — the one place gameplay code asks for
      color; plain text by construction on non-TTY or under `NO_COLOR`.
- [x] **Curated color pass:** title logo in phosphor green, skyline dimmed,
      historical notes dimmed, darkness warning in grue-green, casebook
      headers and `[New line of questioning]` notices in amber. Body prose
      stays uncolored on purpose — color marks *kinds* of information.
- [x] **Legacy console support:** best-effort VT-processing enable on classic
      conhost (`media._ensure_vt`, ctypes, no dependencies); UTF-8 stdout
      reconfigure already lands at startup in `main._enable_utf8_output`.
- [x] **Fallbacks verified end to end:** piped/captured gameplay output
      contains zero escape codes (tested).

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
- [x] **Dead location refs:** `badge`/`cipher_wheel` no longer reference
      nonexistent `"warehouse"`/`"office"` locations; config-integrity tests
      now validate every `use_locations`/`use_effects` key, every exit target,
      and every NPC placement against the location table.
- [x] **`INVENTORY_LIMIT` removed** — defined, never read, and a carry limit is
      pure friction in a mystery.
- [x] **`MAX_PUZZLE_ATTEMPTS` / `PUZZLE_TIMEOUT` removed** — never read, and
      the reworked puzzles have no attempt limit by design (sweeping a band
      *is* repeated attempts).
- [x] **Auto-generated gate messages** produced "You need to found warehouse
      first". Authored per-flag messages now live in `config.GATE_MESSAGES`.
- [x] **The solve prompt leaked internals** ("Enter solution for the puzzle at
      evidence_room") in a game whose product is voice.
- [x] **Trolley quirks:** removed unreachable `look` branch; trolley commands
      typed off the tram now say so instead of silently doing nothing.
- [x] **Cosmetic:** darkness warning is now a single `DARK_WARNING` constant.
      (Duplicate commit in history is permanent — harmless.)

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
- **Detective-game overhaul merged (PR #10).** Real puzzles (cipher wheel you
  turn, radio you tune, Morse you tap, plate fragments), witness dialogue
  (`talk`/`ask`/`topics`), casebook (`case`), three acts, arrest endgame,
  end-to-end walkthrough test. 400 tests passing.
- **Backlog cleared + victory art (PR #11 rework).** Remaining review defects
  fixed on top of the overhaul; config-integrity tests (items, exits, NPCs);
  CASE CLOSED stamp before the victory memo. 411 tests passing.
- **Phase 1 art complete.** Tunnels entrance arch + district sigils
  (Smith Tower, docks, Pike Place, Eagles Hall) on first visit; first-visit
  announcement logic deduplicated between walking and trolley arrival.
  420 tests passing. Next phase: CRT color pass, then the audio pilot.
- **Phase 2 complete (CRT color pass).** `media.style()` contract, curated
  semantic coloring (phosphor title, dim notes, grue-green darkness, amber
  headers/notices), conhost VT enablement, zero-leak fallbacks verified.
  428 tests passing. Next: Phase 3 — the ElevenLabs radio-broadcast pilot.
