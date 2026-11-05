"""Copy the publishable files from incoming/ into assets/hackathons/<slug>/.

Run from the repository root:  python tools/import_incoming.py
Requires Pillow and pypdf. incoming/ is git-ignored and never published as is.

What is published (everything else in incoming/ stays private):
- photos: only the robot, the AMAN tower without people, the SportLineBot manual cover
  and the Water Talent Prize certificate, resized and converted to WebP;
- certificates: converted to WebP (scans straightened);
- presentations: re-saved as lighter PDFs. Slides that show photos of people are dropped
  (SportLineBot slide 2, AMAN slide 16).
Not published: photos of me, the Youthpass PDF (date of birth), any volunteering file,
any STMicroelectronics document.
"""
import io
import json
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "incoming"
DST = ROOT / "assets" / "hackathons"
SIZES = {}


def webp(src, dst, max_side, rotate=0, quality=80):
    im = Image.open(src).convert("RGB")
    if rotate:
        im = im.rotate(rotate, expand=True)
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=quality, method=6)
    SIZES[dst.relative_to(ROOT / "assets").as_posix()] = list(im.size)
    print(f"  {dst.relative_to(ROOT)}  {im.size[0]}x{im.size[1]}  {dst.stat().st_size // 1024} KB")


def pdf_image(src, dst, max_side, rotate=0):
    """A one-page scanned PDF certificate becomes a WebP image."""
    data = PdfReader(src).pages[0].images[0].data
    tmp = io.BytesIO(data)
    webp(tmp, dst, max_side, rotate)


def pdf(src, dst, drop_pages=(), max_side=1400, quality=60):
    r = PdfReader(src)
    w = PdfWriter()
    for i, page in enumerate(r.pages, start=1):
        if i not in drop_pages:
            w.add_page(page)
    for page in w.pages:
        for img in page.images:
            try:
                pil = img.image
                if pil.mode in ("RGBA", "LA", "P", "PA"):
                    continue  # keep transparency as is
                if max(pil.size) > max_side:
                    pil = pil.copy()
                    pil.thumbnail((max_side, max_side), Image.LANCZOS)
                img.replace(pil.convert("RGB"), quality=quality)
            except Exception:
                pass
        page.compress_content_streams()
    w.add_metadata({"/Producer": "", "/Creator": ""})
    dst.parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "wb") as fh:
        w.write(fh)
    print(f"  {dst.relative_to(ROOT)}  {len(w.pages)} pages  {src.stat().st_size // 1024} KB -> {dst.stat().st_size // 1024} KB")


def main():
    if not SRC.exists():
        print("incoming/ not found, nothing to import")
        return
    w4f, g4h, meca = DST / "water4future-2026", DST / "game4health-2026", DST / "meca-world-cup-2026"
    print("Water4Future")
    webp(SRC / "water4future-2026/aman-hydroponic-prototype.jpg", w4f / "aman-prototype.webp", 900)
    webp(SRC / "water4future-2026/water-talent-prize.jpg", w4f / "water-talent-prize.webp", 1200)
    webp(SRC / "water4future-2026/attestation-of-participation.jpg", w4f / "attestation-of-participation.webp", 1100)
    pdf(SRC / "water4future-2026/aman-presentation.pdf", w4f / "aman-presentation.pdf", drop_pages={16})
    print("Game4Health")
    pdf_image(SRC / "game4health-2026/certificate-of-participation.pdf", g4h / "certificate-of-participation.webp", 1400, rotate=90)
    pdf(SRC / "game4health-2026/heart-guardian-presentation.pdf", g4h / "heart-guardian-presentation.pdf")
    print("MECA WORLD CUP")
    webp(SRC / "meca-world-cup-2026/robot-prototype.jpg", meca / "robot-prototype.webp", 900)
    webp(SRC / "meca-world-cup-2026/user-manual-cover.jpg", meca / "user-manual-cover.webp", 900)
    webp(SRC / "meca-world-cup-2026/certificate-of-participation.jpg", meca / "certificate-of-participation.webp", 1400, rotate=90)
    pdf(SRC / "meca-world-cup-2026/sportlinebot-presentation.pdf", meca / "sportlinebot-presentation.pdf", drop_pages={2})
    sizes_file = ROOT / "tools" / "img_sizes.json"
    sizes = json.loads(sizes_file.read_text(encoding="utf-8"))
    sizes.update(SIZES)
    sizes_file.write_text(json.dumps(sizes), encoding="utf-8")


if __name__ == "__main__":
    main()
