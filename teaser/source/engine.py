"""Terminal timeline + frame renderer. No game logic here: it replays text the real game produced."""
import re, random, functools, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 30
COLS, ROWS = 80, 25
FONT_SIZE, CW, CH = 27, 16.25, 32
LW, LH = int(round(COLS*CW)), ROWS*CH           # 1300 x 800
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
BG = (4, 10, 6)
PALETTE = {0: (88, 238, 128), 1: (36, 104, 62), 2: (255, 176, 36), 3: (196, 255, 206)}
SGR = {"0": 0, "": 0, "2": 1, "33": 2, "92": 3}
ANSI_ALL = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
SGR_RE = re.compile(r"\x1b\[([0-9;]*)m")

# ---------------------------------------------------------------- parsing
def parse(out):
    """Raw pty output -> list of (text, styles) lines. styles is a str of digits, one per char."""
    out = out.replace("\r\n", "\n").replace("\r", "")
    out = re.sub(r"\x1b\[(?:H|2J|3J)", "", out)
    lines, text, sty, cur, pos = [], [], [], 0, 0
    for m in re.finditer(r"\x1b\[([0-9;]*)m|\n|[^\x1b\n]+", out):
        tok = m.group(0)
        if tok == "\n":
            lines.append(("".join(text), "".join(sty))); text, sty = [], []
        elif tok.startswith("\x1b"):
            cur = SGR.get(m.group(1), cur)
        else:
            text.append(tok); sty.append(str(cur) * len(tok))
    lines.append(("".join(text), "".join(sty)))
    return lines

def plain(l): return l[0]
def L(s, style=0): return (s, str(style)*len(s))
BLANK = ("", "")

# ---------------------------------------------------------------- rendering
@functools.lru_cache(maxsize=2500)
def line_img(text, styles, cursor):
    im = Image.new("RGB", (LW, CH), BG); d = ImageDraw.Draw(im)
    for i, ch in enumerate(text):
        if ch != " ":
            d.text((int(round(i*CW)), 1), ch, font=FONT, fill=PALETTE[int(styles[i])])
    if cursor is not None:
        x0 = int(round(cursor*CW)); d.rectangle((x0, 3, x0+int(CW)-2, CH-3), fill=PALETTE[0])
        if cursor < len(text) and text[cursor] != " ":
            d.text((x0, 1), text[cursor], font=FONT, fill=BG)
    return np.asarray(im)

def render_state(view, cursor_row, cursor_col):
    rows = []
    for r in range(ROWS):
        t, s = view[r] if r < len(view) else BLANK
        rows.append(line_img(t, s, cursor_col if r == cursor_row else None))
    return np.concatenate(rows, 0)

def apply_effect(arr, eff, rng):
    kind = eff[0]
    if kind == "on":                      # CRT power-on: a line blooms, then opens vertically
        p = eff[1]; out = np.zeros_like(arr); mid = LH//2
        if p < 0.35:
            q = p/0.35; w = int(LW*(0.10 + 0.90*q)); x0 = (LW-w)//2
            out[mid-2:mid+2, x0:x0+w] = int(110 + 145*q)
        else:
            q = (p-0.35)/0.65; half = max(3, int((q**1.7)*(LH//2)))
            reg = arr[mid-half:mid+half].astype(np.float32)*(0.2 + 0.8*q) + (1-q)**2*150
            out[mid-half:mid+half] = np.clip(reg, 0, 255)
            out[mid-2:mid+2] = np.maximum(out[mid-2:mid+2], int(255*(1-q)**0.5))
        return out
    if kind == "off":
        return apply_effect(arr, ("on", 1-eff[1]), rng)
    if kind == "glitch":
        k = eff[1]; out = arr.copy()
        for _ in range(rng.randint(6, 12)):
            y = rng.randrange(0, LH-40); h = rng.randint(6, 60); dx = rng.randint(-120, 120)
            out[y:y+h] = np.roll(out[y:y+h], dx, axis=1)
        out = np.clip(out.astype(np.float32) * (1.0 + 0.6*(k % 2)) + rng.randint(0, 25), 0, 255)
        noise = np.random.default_rng(k).integers(0, 90, size=out.shape[:2], dtype=np.int16)
        mask = (np.random.default_rng(k+99).random(out.shape[:2]) < 0.22)
        out = np.where(mask[..., None], out + noise[..., None]*0.9, out)
        return np.clip(out, 0, 255).astype(np.uint8)
    if kind == "fade":
        return (arr.astype(np.float32) * eff[1]).astype(np.uint8)
    return arr

# ---------------------------------------------------------------- director
class Director:
    def __init__(s):
        s.lines = []; s.cur = BLANK; s.frames = []; s.log = []; s.marks = {}
        s.rng = random.Random(1947); s.blink_phase = 0
    @property
    def t(s): return len(s.frames) / FPS
    def mark(s, name): s.marks[name] = s.t
    # -- view helpers
    def _view(s):
        v = s.lines + [s.cur]
        v = v[-ROWS:]
        return v, len(v)-1
    def _snap(s, n=1, cursor=True, eff=None):
        v, row = s._view()
        for _ in range(max(1, int(round(n)))):
            blink_on = ((len(s.frames)//8) % 2 == 0)       # ~1.9 Hz
            col = len(s.cur[0]) if (cursor and blink_on) else None
            s.frames.append((tuple(v), row, col, eff if not callable(eff) else eff(len(s.frames))))
    def _snap_t(s, sec, cursor=True): s._snap(sec*FPS, cursor)
    # -- primitives
    def hold(s, sec, cursor=True): s._snap_t(sec, cursor)
    def blank(s, sec=0.0):
        s.lines, s.cur = [], BLANK
        if sec: s._snap_t(sec, cursor=False)
    def poweron(s, sec=0.8):
        n = int(sec*FPS)
        for i in range(n):
            s.frames.append(((), 0, None, ("on", (i+1)/n)))
    def poweroff(s, sec=0.5):
        s.lines, s.cur = s.lines, s.cur
        v, row = s._view(); n = int(sec*FPS)
        for i in range(n): s.frames.append((tuple(v), row, None, ("off", (i+1)/n)))
        s.lines, s.cur = [], BLANK
    def cut(s, sec=0.28):
        v, row = s._view(); n = int(sec*FPS)
        for i in range(n): s.frames.append((tuple(v), row, None, ("glitch", i+1+s.rng.randint(0, 999))))
        s.lines, s.cur = [], BLANK
    def fadeout(s, sec=1.0):
        v, row = s._view(); n = int(sec*FPS)
        for i in range(n): s.frames.append((tuple(v), row, None, ("fade", 1-(i+1)/n)))
    def _commit(s):
        if s.cur != BLANK or s.cur == ("", ""): pass
    def prompt(s):
        s.lines.append(BLANK) if s.lines else None
        s.cur = L("> ", 0)
    def type(s, text, cps=15, pre=0.25, post=0.35, log=True):
        s.prompt() if not s.cur[0].startswith(">") else None
        s._snap_t(pre)
        t0 = s.t
        for ch in text:
            s.cur = (s.cur[0]+ch, s.cur[1]+"0")
            d = 1.0/cps * s.rng.uniform(0.55, 1.45) * (2.2 if ch in " ," and s.rng.random() < .15 else 1)
            s._snap(d*FPS, cursor=True)
        s._snap_t(post)
        s.lines.append(s.cur); s.cur = BLANK
        if log: s.log.append((t0, s.t, "cmd", text))
    def press_enter(s, pre=0.4):
        s.prompt(); s._snap_t(pre); s.lines.append(s.cur); s.cur = BLANK
    def emit(s, lines, lps=8, after=0.0, log=True, kind="out"):
        t0 = s.t
        for ln in lines:
            s.lines.append(ln); s._snap(FPS/lps, cursor=False)
            if log: s.log.append((s.t, s.t, kind, ln[0]))
        if after: s._snap_t(after, cursor=False)
    def emit_typed(s, lines, cps=40, log=True, gap=0.18):
        for ln in lines:
            s.cur = BLANK
            for i, ch in enumerate(ln[0]):
                s.cur = (s.cur[0]+ch, s.cur[1]+ln[1][i]); s._snap(FPS/cps, cursor=True)
            s.lines.append(s.cur); s.cur = BLANK; s._snap_t(gap, cursor=False)
            if log: s.log.append((s.t, s.t, "out", ln[0]))
    def waiting(s, sec):              # sit at an empty prompt with the cursor blinking
        s.prompt(); s._snap_t(sec, cursor=True)

# ---------------------------------------------------------------- output
def frame_iter(frames, lo=0, hi=None):
    rng = random.Random(7)
    hi = len(frames) if hi is None else hi
    last_key, last_arr = None, None
    for i in range(lo, hi):
        view, row, col, eff = frames[i]
        key = (view, row, col)
        if key != last_key:
            last_arr = render_state(view, row, col); last_key = key
        arr = last_arr
        if eff: arr = apply_effect(arr, eff, rng)
        yield arr

FILTER = (
    "[0:v]pad=1540:866:120:33:color=0x040a06,split=2[a][b];"
    "[b]gblur=sigma=9:steps=2[bl];"
    "[a][bl]blend=all_mode=addition:all_opacity=0.50,format=rgb24[c1];"
    "[c1]lenscorrection=k1=-0.03:k2=-0.008:i=bilinear,rgbashift=rh=-1:bh=1[c2];"
    "[c2][2:v]blend=all_mode=multiply[c3];"
    "[c3]noise=alls=6:allf=t+u,eq=brightness='-0.012+0.014*sin(t*41)+0.006*sin(t*7.3)':eval=frame[c4];"
    "[1:v][c4]overlay=190:107[o1];[o1][3:v]overlay=0:0:format=auto,format=yuv420p[v]"
)

def encode(frames, out, lo=0, hi=None, crf=17, preset="medium"):
    hi = len(frames) if hi is None else hi
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{LW}x{LH}", "-r", str(FPS), "-i", "-",
           "-loop", "1", "-framerate", str(FPS), "-i", "bezel.png",
           "-loop", "1", "-framerate", str(FPS), "-i", "scan.png",
           "-loop", "1", "-framerate", str(FPS), "-i", "glass.png",
           "-filter_complex", FILTER, "-map", "[v]", "-r", str(FPS), "-frames:v", str(hi-lo),
           "-c:v", "libx264", "-crf", str(crf), "-preset", preset, "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for arr in frame_iter(frames, lo, hi):
            p.stdin.write(arr.tobytes())
    finally:
        p.stdin.close(); p.wait()
