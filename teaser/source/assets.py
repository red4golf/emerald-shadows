"""Static CRT assets: monitor bezel, glass (vignette/reflection/rounded corners), scanline mask."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
SX, SY, SW, SH = 190, 107, 1540, 866        # screen window inside the frame

def bezel():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    # dim studio backdrop with a soft pool of light behind the monitor
    d = np.sqrt(((x - W/2)/(W*0.62))**2 + ((y - H/2)/(H*0.7))**2)
    bg = (22 - 16*np.clip(d, 0, 1))[..., None] * np.array([1.0, 1.05, 1.0])
    img = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB")
    dr = ImageDraw.Draw(img)
    # monitor body
    body = (60, 38, W-60, H-38)
    dr.rounded_rectangle(body, radius=70, fill=(52, 53, 50))
    # bevel highlights
    hi = Image.new("RGBA", (W, H), (0,0,0,0)); hd = ImageDraw.Draw(hi)
    hd.rounded_rectangle(body, radius=70, outline=(95,97,92,170), width=3)
    hd.rounded_rectangle((70,48,W-70,H-48), radius=62, outline=(10,10,9,200), width=6)
    img.paste(hi, (0,0), hi)
    # inner recess around the glass
    rec = (SX-34, SY-34, SX+SW+34, SY+SH+34)
    dr.rounded_rectangle(rec, radius=84, fill=(12,12,11))
    dr.rounded_rectangle(rec, radius=84, outline=(70,72,68), width=2)
    # little LED + label under the glass
    ly = SY + SH + 62
    dr.ellipse((W-250, ly-7, W-236, ly+7), fill=(70, 230, 120))
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 17)
        dr.text((200, ly-10), "EMERALD SHADOWS", font=f, fill=(120,124,116))
    except Exception: pass
    # vent slots
    for i in range(6):
        dr.rounded_rectangle((W-420+i*22, ly-8, W-412+i*22, ly+8), radius=3, fill=(18,18,17))
    return img.filter(ImageFilter.GaussianBlur(0.6))

def glass():
    """Full-frame RGBA overlay: dark rounded-corner mask outside the glass, vignette, soft reflection."""
    ov = np.zeros((H, W, 4), np.float32)
    # rounded-rect alpha for the screen window
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rounded_rectangle((SX, SY, SX+SW, SY+SH), radius=58, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    inside = np.asarray(m, np.float32)/255
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    # corners: black only inside the window's bounding box but outside its rounded shape
    rect = np.zeros((H, W), np.float32); rect[SY:SY+SH, SX:SX+SW] = 1
    ov[..., 3] = (rect * (1 - inside)) * 255
    ov[..., :3] = 4
    # vignette inside
    d = np.sqrt(((x-(SX+SW/2))/(SW*0.55))**2 + ((y-(SY+SH/2))/(SH*0.58))**2)
    vig = np.clip((d-0.62)/0.55, 0, 1)**1.8 * 0.62
    ov[..., 3] = np.maximum(ov[..., 3], vig*255*inside)
    base = ov.copy()
    # glass reflection: faint diagonal sheen, top-left
    sheen = np.clip(1 - np.abs((x - SX)*0.9 + (y - SY)*0.55 - 520)/260, 0, 1) * inside
    sheen *= np.clip(1 - (y-SY)/(SH*0.9), 0, 1)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = base[..., :3]; out[..., 3] = base[..., 3]
    # composite a white sheen under the dark: do as separate small-alpha white layer
    white = np.zeros((H, W, 4), np.float32); white[..., :3] = 235; white[..., 3] = sheen*26
    a = out[..., 3:4]/255; b = white[..., 3:4]/255
    rgb = (out[..., :3]*a*(1-b) + white[..., :3]*b) 
    alpha = a*(1-b) + b
    res = np.dstack([np.where(alpha > 0, rgb/np.maximum(alpha, 1e-6), 0), alpha*255])
    return Image.fromarray(np.clip(res, 0, 255).astype(np.uint8), "RGBA")

def scan():
    """Multiply mask: gentle scanlines + faint RGB triad mask."""
    y = np.arange(SH)[:, None]; x = np.arange(SW)[None, :]
    line = 1.0 - 0.28*((y % 3) == 2)
    tri = np.stack([1.0 - 0.06*((x % 3) != c) for c in range(3)], -1)
    m = line[..., None]*tri
    return Image.fromarray(np.clip(m*255, 0, 255).astype(np.uint8), "RGB")

if __name__ == "__main__":
    bezel().save("bezel.png"); glass().save("glass.png"); scan().save("scan.png")
    print("ok")
