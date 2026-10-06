# Emerald Shadows — 2:00 promo teaser

| File | What it is |
|---|---|
| `emerald_shadows_teaser_silent.mp4` | Final picture, 1920x1080, 30 fps, no audio, ~2:00 |
| `emerald_shadows_teaser_captioned_review.mp4` | Same picture with the narration burned in as captions (for checking timing only) |
| `narration_script.md` | Timecoded first-person Diamond narration, 22 lines / ~211 words, with the time window for each line |
| `narration_plain.txt` | The same lines, plain, one per paragraph (paste into ElevenLabs or read from) |
| `narration_cues.json` | Start time and latest end time of each line, for lining up generated audio |
| `captions.srt`, `captions.vtt` | Caption files for the narration |
| `gameplay_transcript.md` | Exactly what is on screen, with timecodes (game output, excerpted, never reworded) |
| `timeline.json` | Beat markers |
| `source/` | The scripts that produced it |

How it was made: the real game was run in a terminal (80x25) through its winning path by script, so there are no typos or dead ends.
The captured screens were replayed with typed commands, excerpted for running time, and rendered through a CRT monitor frame.
Nothing in the game repo was changed.

Rebuild: `python3 capture_full2.py` (needs `pexpect`, game on PYTHONPATH) -> `python3 assets.py` -> `python3 render.py`. Needs ffmpeg, Pillow, numpy.
Edit `build.py` for picture, `vo.py` for narration; `docs.py` regenerates the script, captions and transcript from them.
