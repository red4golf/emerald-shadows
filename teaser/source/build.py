"""Storyboard for the 2-minute Emerald Shadows teaser. Every line of game text on screen
comes from the real game's output (run_full2.json); beats only choose which lines to show."""
import sys, json
sys.path.insert(0, ".")
from engine import *

segs = json.load(open("run_full2.json"))
def seg(cmd, n=0):
    i = [k for k, s in enumerate(segs) if s["cmd"] == cmd][n]
    ls = parse(segs[i]["out"])
    return ls[1:] if cmd else ls          # drop the pty's echo of the typed command
def pick(lines, *spec):
    """Choose lines from real output; a blank line stands in wherever the excerpt skips ahead."""
    out, last = [], None
    for sp in spec:
        a, b = (sp, sp) if isinstance(sp, int) else sp
        if last is not None and a > last + 1 and lines[a][0].strip() and out and out[-1][0].strip():
            out.append(BLANK)
        out.extend(lines[a:b+1]); last = b
    return out

def storyboard():
    d = Director()
    # ---- B0  power-on + title -------------------------------------------------
    d.mark("B0"); d.poweron(0.9); d.hold(0.25, cursor=False)
    title = parse(segs[0]["out"])[1:]                       # logo, tagline, skyline, ...
    d.emit(title[0:12], lps=20, after=0.35)                  # the block-letter logo
    d.emit([BLANK], lps=30)
    d.emit_typed([title[13], title[14]], cps=34, gap=0.15)   # "Seattle, Washington. October 1947. ..."
    d.hold(3.2)
    # ---- B1  bullpen / evidence room ---------------------------------------
    d.cut(0.30); d.mark("B1")
    d.hold(0.25, cursor=False)
    d.emit(pick(seg(""), (2, 11)), lps=8, after=3.4)
    d.type("upstairs", cps=14)
    d.emit(pick(seg("upstairs"), (0, 8)), lps=8, after=2.6)
    # ---- B2  the photograph -----------------------------------------------
    d.cut(0.30); d.mark("B2")
    d.type("examine photo", cps=15, pre=0.4)
    d.emit(pick(seg("examine photo"), (0, 14)), lps=8, after=4.4)
    # ---- B3  the cipher wheel --------------------------------------------
    d.cut(0.30); d.mark("B3")
    d.type("turn wheel to c", cps=15, pre=0.4)
    d.emit(pick(seg("turn wheel to c"), (1, 5)), lps=9, after=0.9)
    d.type("turn wheel to q", cps=15, pre=0.2, post=0.2)
    d.emit(pick(seg("turn wheel to q"), (1, 5)), lps=9, after=0.7)
    d.type("turn wheel to h", cps=15, pre=0.2, post=0.2)
    d.mark("B3_h")
    d.emit(pick(seg("turn wheel to h"), (1, 5), 7), lps=8, after=4.0)
    # ---- B4  witnesses -----------------------------------------------------
    d.cut(0.30); d.mark("B4")
    d.type("ask harold about sedan", cps=17, pre=0.4)
    d.emit(pick(seg("ask harold about sedan"), (0, 9)), lps=8, after=3.2)
    d.cut(0.30); d.mark("B4_roy")
    d.type("ask roy about frequency", cps=17, pre=0.3)
    d.emit(pick(seg("ask roy about frequency"), (0, 1), (3, 4), (8, 9)), lps=8, after=2.4)
    d.type("examine informant_note", cps=17, pre=0.2)
    d.mark("B4_note")
    d.emit(pick(seg("examine informant_note"), 1, (2, 3), (5, 6), 8, (9, 10)), lps=8, after=3.4)
    # ---- B4c the plate -----------------------------------------------------
    d.cut(0.30); d.mark("B4_solve")
    d.type("solve", cps=10, pre=0.4)
    d.emit(pick(seg("solve"), (1, 2), (4, 6), (10, 13)), lps=8, after=3.4)
    # ---- B5  the casebook ---------------------------------------------------
    d.cut(0.30); d.mark("B5")
    d.type("case", cps=10, pre=0.4)
    d.emit(pick(seg("case"), (1, 3), (17, 19), (21, 27)), lps=9, after=3.6)
    # ---- B6  the Anchor ---------------------------------------------------
    d.cut(0.30); d.mark("B6")
    d.type("use badge", cps=14, pre=0.4)
    d.emit(pick(seg("use badge"), (0, 6), (8, 10)), lps=8, after=3.4)
    # ---- B7  the radio ------------------------------------------------------
    d.cut(0.30); d.mark("B7")
    d.type("tune 415.3", cps=14, pre=0.4)
    d.emit(pick(seg("tune 415.3"), (1, 2)), lps=7, after=1.4)
    d.type("tune 415.6", cps=14, pre=0.2, post=0.25)
    d.mark("B7_hit")
    d.emit(pick(seg("tune 415.6"), (1, 11)), lps=7, after=3.6)
    # ---- B8  the tunnels ----------------------------------------------------
    d.cut(0.30); d.mark("B8")
    d.type("underground", cps=13, pre=0.4)
    d.emit(pick(seg("underground"), (1, 9)), lps=9, after=2.9)
    d.type("use flashlight", cps=13, pre=0.2)
    d.mark("B8_tap")
    d.emit(pick(seg("use flashlight"), 10, (12, 17)), lps=8, after=2.0)
    d.type("tap W22", cps=13, pre=0.2)
    d.emit(pick(seg("tap W22"), (1, 2)), lps=8, after=2.2)
    # ---- B9  Pier 7 -------------------------------------------------------
    d.cut(0.30); d.mark("B9")
    d.type("south", cps=10, pre=0.4)
    p7 = seg("south", -1)
    d.emit(pick(p7, (0, 12)), lps=8, after=0.6)
    d.waiting(4.2)
    # ---- end card -----------------------------------------------------------
    d.cut(0.35); d.mark("END")
    logo = [L(l[0], 3) for l in title[0:12]]
    card = [BLANK] + logo + [BLANK,
        L("  A NOIR DETECTIVE TEXT ADVENTURE  -  SEATTLE, 1947", 2), BLANK,
        L("  Download for Windows:", 0),
        L("  github.com/red4golf/emerald-shadows/releases", 3)]
    d.emit(card[:14], lps=22, after=0.3, log=False)
    d.emit(card[14:], lps=2.2, after=0.0, log=False)
    d.hold(6.4)
    d.poweroff(0.7)
    return d

if __name__ == "__main__":
    d = storyboard()
    print(f"total {d.t:.1f}s  ({len(d.frames)} frames)")
    for k, v in d.marks.items(): print(f"  {k:8s} {v:6.1f}")
