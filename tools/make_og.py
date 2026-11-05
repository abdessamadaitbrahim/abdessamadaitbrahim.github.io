"""Open Graph image (1200 x 630): cream paper, oxblood accent, circular portrait.

Run from anywhere:  python tools/make_og.py   (requires Pillow)
"""
import glob
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
PAPER, INK, MUTED, ACCENT, SAGE, LINE = "#f4eee3", "#1f1a16", "#5d5348", "#8c2f1f", "#566349", "#dcd1be"


def font(names, size):
    pats = []
    for n in names:
        pats += [f"C:/Windows/Fonts/{n}", f"/usr/share/fonts/**/{n}", f"/Library/Fonts/{n}", f"/System/Library/Fonts/**/{n}"]
    for pat in pats:
        hits = glob.glob(pat, recursive=True)
        if hits:
            return ImageFont.truetype(hits[0], size)
    return ImageFont.load_default(size)


serif = font(["georgia.ttf", "DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"], 84)
serif_i = font(["georgiai.ttf", "DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf"], 84)
mono = font(["consola.ttf", "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"], 22)
sans = font(["segoeui.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"], 30)

S = 2  # supersample for smooth circles
im = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(im)
d.rectangle([0, 0, W * S, 10 * S], fill=ACCENT)
d.line([(80 * S, 548 * S), (W * S - 80 * S, 548 * S)], fill=LINE, width=2 * S)

# portrait: circle, thin accent ring, offset dashed outline
cx, cy, r = 905, 290, 175
for a in range(0, 360, 6):  # dashed offset outline
    d.arc([(cx - r + 18) * S, (cy - r + 14) * S, (cx + r + 18) * S, (cy + r + 14) * S], a, a + 3, fill=SAGE, width=2 * S)
d.ellipse([(cx - r - 10) * S, (cy - r - 10) * S, (cx + r + 10) * S, (cy + r + 10) * S], fill=PAPER)
d.ellipse([(cx - r - 9) * S, (cy - r - 9) * S, (cx + r + 9) * S, (cy + r + 9) * S], outline=ACCENT, width=3 * S)
p = Image.open(ROOT / "assets/img/site/portrait.webp").convert("RGB")
side = min(p.size)
top = int((p.height - side) * 0.18)
p = p.crop(((p.width - side) // 2, top, (p.width - side) // 2 + side, top + side)).resize((2 * r * S, 2 * r * S), Image.LANCZOS)
mask = Image.new("L", p.size, 0)
ImageDraw.Draw(mask).ellipse([0, 0, p.size[0], p.size[1]], fill=255)
im.paste(p, ((cx - r) * S, (cy - r) * S), mask)
im = im.resize((W, H), Image.LANCZOS)

d = ImageDraw.Draw(im)
d.text((80, 112), "ENSA TÉTOUAN · BIG DATA & AI ENGINEERING", font=mono, fill=ACCENT)
d.text((80, 170), "Abdessamad", font=serif, fill=INK)
d.text((80, 268), "Ait Brahim", font=serif_i, fill=ACCENT)
d.text((80, 396), "NLP · Computer vision · Deep learning · Big Data", font=sans, fill=MUTED)
d.text((80, 572), "abdessamadaitbrahim.github.io", font=mono, fill=MUTED)
d.text((W - 80, 572), "Open to a PFE internship, January 2027", font=mono, fill=SAGE, anchor="ra")
im.save(ROOT / "assets/img/site/og.png", optimize=True)
print("og.png written")
