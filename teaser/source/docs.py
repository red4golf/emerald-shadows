import sys, os, json, re
sys.path.insert(0, ".")
from build import *
from vo import CUES, WPS

OUT = "deliverables"; os.makedirs(OUT, exist_ok=True)
d = storyboard(); M = d.marks; TOTAL = d.t

def tc(t, ms=False):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:04.1f}" if not ms else f"00:{int(m):02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
def vtt(t): return tc(t, True).replace(",", ".")

# ---- cue timing --------------------------------------------------------------
cues = []
for mk, off, text in CUES:
    start = M[mk] + off
    words = len(text.split())
    cues.append(dict(start=start, text=text, words=words, est=words/WPS))
for i, c in enumerate(cues):
    nxt = cues[i+1]["start"] if i+1 < len(cues) else TOTAL
    c["window"] = nxt - c["start"]              # time before the next line begins
    c["end"] = c["start"] + min(c["est"], c["window"] - 0.05)
    c["fits"] = c["est"] <= c["window"] - 0.1
bad = [c for c in cues if not c["fits"]]
print("cues:", len(cues), "words:", sum(c['words'] for c in cues), "tight:", len(bad))
for c in bad: print("  TIGHT", tc(c["start"]), c["text"], round(c["est"],1), round(c["window"],1))

# ---- captions -----------------------------------------------------------------
with open(f"{OUT}/captions.srt", "w") as f:
    for i, c in enumerate(cues, 1):
        f.write(f"{i}\n{tc(c['start'],True)} --> {tc(c['end'],True)}\n{c['text']}\n\n")
with open(f"{OUT}/captions.vtt", "w") as f:
    f.write("WEBVTT\n\n")
    for c in cues: f.write(f"{vtt(c['start'])} --> {vtt(c['end'])}\n{c['text']}\n\n")
json.dump([dict(n=i+1, start=round(c["start"],2), max_end=round(c["start"]+c["window"]-0.05,2),
                text=c["text"]) for i, c in enumerate(cues)], open(f"{OUT}/narration_cues.json", "w"), indent=1)
open(f"{OUT}/narration_plain.txt", "w").write("\n\n".join(c["text"] for c in cues) + "\n")

# ---- narration script ---------------------------------------------------------
beats = [("B0","Title"),("B1","Bullpen and evidence room"),("B2","The photograph"),("B3","The cipher wheel"),
         ("B4","The witnesses"),("B4_solve","The plate"),("B5","The casebook"),("B6","The Anchor"),
         ("B7","The radio"),("B8","The tunnels"),("B9","Pier 7"),("END","Closing card")]
def beat_of(t):
    name = beats[0][1]
    for k, n in beats:
        if M[k] <= t + 0.01: name = n
    return name
with open(f"{OUT}/narration_script.md", "w") as f:
    f.write("# Emerald Shadows — 2:00 teaser: narration script\n\n")
    f.write("First-person Detective Johnny Diamond. **{} lines, {} words, runs {}.** ".format(
        len(cues), sum(c['words'] for c in cues), tc(TOTAL)))
    f.write("Picture is locked; every line below is timed to what is on screen.\n\n")
    f.write("**Delivery:** low, tired, unhurried. Dry rather than hard-boiled. Pauses between sentences are the pacing — "
            "don't fill them. Target about 145 words per minute; the *Window* column is the time you have before the next line starts, "
            f"and *Read* is the estimate at {WPS} words/sec. Any line whose Read is near its Window should be spoken a touch faster, not trimmed.\n\n")
    f.write("| # | Start | Window | Read | Beat | Line |\n|---|---|---|---|---|---|\n")
    for i, c in enumerate(cues, 1):
        f.write(f"| {i} | {tc(c['start'])} | {c['window']:.1f}s | {c['est']:.1f}s | {beat_of(c['start'])} | {c['text']} |\n")
    f.write("\n## As one read-through\n\n")
    for c in cues: f.write(c["text"] + "\n\n")
    f.write("---\n*Pronunciation: Emerald Shadows; grue = \"groo\"; Pier Seven (the game also writes Pier 7).*\n")

# ---- on-screen gameplay transcript -------------------------------------------
LOGO = re.compile(r"[█╗╔║╝═╚]")
title_tag = None
with open(f"{OUT}/gameplay_transcript.md", "w") as f:
    f.write("# Emerald Shadows — 2:00 teaser: on-screen transcript\n\n")
    f.write("Everything below is text the real game printed during a scripted playthrough (the winning path, run through "
            "the actual game code in a terminal). Commands are shown as typed. Long passages are **excerpted** for running time — "
            "paragraphs are cut, never reworded, and the game's own history asides are left out. Timecodes are when each command is typed.\n\n")
    cur_beat = None; buf = []
    def flush():
        global buf
        while buf and not buf[0].strip(): buf.pop(0)
        while buf and not buf[-1].strip(): buf.pop()
        if buf: f.write("```\n" + "\n".join(buf) + "\n```\n\n")
        buf = []
    f.write("## " + beats[0][1] + f"  ·  0:00\n\n")
    cur_beat = beats[0][1]
    for t0, t1, kind, text in d.log:
        b = beat_of(t0)
        if b != cur_beat:
            flush(); f.write(f"## {b}  ·  {tc(t0)}\n\n"); cur_beat = b
        if kind == "cmd":
            flush(); f.write(f"**{tc(t0)}**  `> {text}`\n\n")
        else:
            if LOGO.search(text):
                if not buf or buf[-1] != "[EMERALD SHADOWS — block-letter title logo]":
                    buf.append("[EMERALD SHADOWS — block-letter title logo]")
            else: buf.append(text)
    flush()
    f.write("## Closing card  ·  %s\n\n```\n[EMERALD SHADOWS — block-letter title logo]\n\n  A NOIR DETECTIVE TEXT ADVENTURE  -  SEATTLE, 1947\n\n"
            "  Download for Windows:\n  github.com/red4golf/emerald-shadows/releases\n```\n" % tc(M["END"]))

json.dump(dict(total=TOTAL, marks=M), open(f"{OUT}/timeline.json", "w"), indent=1)
print("ok", TOTAL)
