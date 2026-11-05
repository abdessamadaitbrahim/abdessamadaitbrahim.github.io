"""Portrait-based icons: header photo and circular favicons.

Run from anywhere:  python tools/make_icons.py   (requires Pillow)
Source: incoming/site/abdessamad-prof.png (720 x 720 studio portrait, git-ignored).
Writes, all cropped square and centred on the face, without metadata:
- assets/img/site/abdessamad-prof-96.webp and abdessamad-prof-192.webp (header photo, 1x and 2x;
  CSS shows it as a circle with a thin accent ring);
- favicon.ico (16/32/48), assets/img/site/favicon-32.png, apple-touch-icon.png (180) and
  icon-512.png, as circles with a thin oxblood ring.
The large hero portrait (assets/img/site/portrait.webp) is not touched.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "assets" / "img" / "site"
SRC = ROOT / "incoming" / "site" / "abdessamad-prof.png"
ACCENT, PAPER = (140, 47, 31, 255), (244, 238, 227, 255)
HEAD = (140, 22, 580, 462)   # hair to chin with a little shoulder, for the header photo
FACE = (165, 75, 555, 465)   # tighter, for tiny favicons


def crop(box):
    # convert() drops the source's ancillary chunks; the saves below write no EXIF/XMP
    return Image.open(SRC).convert("RGB").crop(box)


def circle_icon(size, ring=True, box=FACE):
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
    ph = crop(box).resize((inner, inner), Image.LANCZOS)
    mask = Image.new("L", (inner, inner), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, inner - 1, inner - 1], fill=255)
    out.paste(ph, (pad, pad), mask)
    return out.resize((size, size), Image.LANCZOS)


def main():
    if not SRC.exists():
        raise SystemExit(f"missing source photo: {SRC.relative_to(ROOT)}")
    head = crop(HEAD)
    for px in (96, 192):
        head.resize((px, px), Image.LANCZOS).save(SITE / f"abdessamad-prof-{px}.webp", "WEBP", quality=84, method=6)
    circle_icon(32).save(SITE / "favicon-32.png", optimize=True)
    # iOS masks the touch icon itself, so it gets a full square of paper behind the circle
    touch = Image.new("RGBA", (180, 180), PAPER)
    touch.alpha_composite(circle_icon(164, box=HEAD), (8, 8))
    touch.convert("RGB").save(SITE / "apple-touch-icon.png", optimize=True)
    circle_icon(512, box=HEAD).save(SITE / "icon-512.png", optimize=True)
    circle_icon(256).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    for f in ("abdessamad-prof-96.webp", "abdessamad-prof-192.webp", "favicon-32.png", "apple-touch-icon.png", "icon-512.png"):
        print(f, (SITE / f).stat().st_size // 1024, "KB")
    print("favicon.ico", (ROOT / "favicon.ico").stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
