"""Portrait-based icons: header avatar and circular favicons.

Run from anywhere:  python tools/make_icons.py   (requires Pillow)
Writes assets/img/site/avatar.webp (96 px, square, shown as a circle by CSS),
favicon.ico (16/32/48), assets/img/site/favicon-32.png, apple-touch-icon.png (180)
and icon-512.png. All are cropped to the face of assets/img/site/portrait.webp.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "assets" / "img" / "site"
ACCENT, PAPER = (140, 47, 31, 255), (244, 238, 227, 255)
FACE = (120, 60, 500, 440)  # square box around the face in the 600 x 639 portrait


def face():
    return Image.open(SITE / "portrait.webp").convert("RGB").crop(FACE)


def circle_icon(size, ring=True):
    """Circular portrait on a transparent background with a thin oxblood ring."""
    S = 4  # supersample for smooth edges
    big = size * S
    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    pad = 0
    if ring:
        ring_w = max(1, round(size / 28)) * S
        d.ellipse([0, 0, big - 1, big - 1], fill=ACCENT)
        gap = max(1, round(size / 40)) * S
        d.ellipse([ring_w, ring_w, big - 1 - ring_w, big - 1 - ring_w], fill=PAPER)
        pad = ring_w + gap
    inner = big - 2 * pad
    ph = face().resize((inner, inner), Image.LANCZOS)
    mask = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, inner - 1, inner - 1], fill=255)
    out.paste(ph, (pad, pad), mask)
    return out.resize((size, size), Image.LANCZOS)


def main():
    face().resize((96, 96), Image.LANCZOS).save(SITE / "avatar.webp", "WEBP", quality=82, method=6)
    circle_icon(32).save(SITE / "favicon-32.png", optimize=True)
    # iOS masks the touch icon itself, so it gets a full square of paper behind the circle
    touch = Image.new("RGBA", (180, 180), PAPER)
    touch.alpha_composite(circle_icon(164), (8, 8))
    touch.convert("RGB").save(SITE / "apple-touch-icon.png", optimize=True)
    circle_icon(512).save(SITE / "icon-512.png", optimize=True)
    circle_icon(256).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    for f in ("avatar.webp", "favicon-32.png", "apple-touch-icon.png", "icon-512.png"):
        print(f, (SITE / f).stat().st_size // 1024, "KB")
    print("favicon.ico", (ROOT / "favicon.ico").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
