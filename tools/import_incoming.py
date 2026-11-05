"""Copy the publishable files from incoming/ into assets/hackathons/<slug>/.

Run from the repository root:  python tools/import_incoming.py
Requires Pillow and pypdf. incoming/ is git-ignored and never published as is.

What is published (everything else in incoming/ stays private):
- photos: event photos (including photos of me and my teammates, allowed since the
  November 2026 update), the robot, the AMAN tower, the SportLineBot manual cover and the
  Water Talent Prize certificate, resized and converted to WebP;
- certificates: converted to WebP (scans straightened);
- presentations: re-saved as lighter PDFs. Slides that show photos of people are dropped
  (SportLineBot slide 2, AMAN slide 16).
Volunteering certificates (assets/volunteering/): the Amazigh New Year certificate as a lighter
PDF, and a REDACTED copy of the Youthpass: page 1 is flattened to an image with the birth date and
place line painted over, so the text is really gone; the script re-reads the output and stops if
the birth data is still extractable. The original Youthpass is never copied. Needs pypdfium2
(pip install pypdfium2) for this step only.
Not published: any STMicroelectronics document.
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


def no_metadata(w):
    try:
        w.metadata = None
    except Exception:
        w.add_metadata({"/Producer": "", "/Creator": ""})


def preview(pil, dst, width=900):
    """First-page preview of a certificate, as WebP (no metadata is written by Pillow)."""
    pil = pil.convert("RGB")
    pil.thumbnail((width, width * 2), Image.LANCZOS)
    pil.save(dst, "WEBP", quality=80, method=6)
    SIZES[dst.relative_to(ROOT / "assets").as_posix()] = list(pil.size)
    print(f"  {dst.relative_to(ROOT)}  {pil.size[0]}x{pil.size[1]}  {dst.stat().st_size // 1024} KB")


def scan_certificate(src, dst_pdf, dst_preview, rotate=0, max_side=1800, quality=72):
    """One-page scanned certificate: rebuild a light PDF from the scan, plus a preview."""
    scan = Image.open(io.BytesIO(PdfReader(src).pages[0].images[0].data)).convert("RGB")
    if rotate:
        scan = scan.rotate(rotate, expand=True)
    scan.thumbnail((max_side, max_side), Image.LANCZOS)
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    scan.save(buf, "PDF", resolution=150, quality=quality)
    w = PdfWriter(clone_from=PdfReader(buf))
    no_metadata(w)
    with open(dst_pdf, "wb") as fh:
        w.write(fh)
    print(f"  {dst_pdf.relative_to(ROOT)}  {src.stat().st_size // 1024} KB -> {dst_pdf.stat().st_size // 1024} KB")
    preview(scan, dst_preview)


BIRTH_MARKERS = ("BORN ON", "15/04/2004", "Sedrat", "Sahl", "Elgharbia")


def youthpass_redacted(src, dst_pdf, dst_preview, dpi=200):
    """Flatten page 1 to an image with the 'BORN ON ...' line painted over; keep pages 2-4 as text."""
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print("  pypdfium2 is not installed: Youthpass skipped (nothing published)")
        return
    from PIL import ImageDraw
    doc = pdfium.PdfDocument(str(src))
    page = doc[0]
    W, H = page.get_size()
    tp = page.get_textpage()
    found = tp.search("BORN ON", match_case=True).get_next()
    if not found:
        raise SystemExit("Youthpass: birth line not found, refusing to publish")
    l, b, r, t = tp.get_charbox(found[0])
    scale = dpi / 72
    img = page.render(scale=scale).to_pil().convert("RGB")
    # full-width band around the line (PDF y grows upwards, image y downwards)
    top = int((H - t - 6) * scale)
    bottom = int((H - b + 8) * scale)
    ImageDraw.Draw(img).rectangle([int(36 * scale), top, int((W - 36) * scale), bottom], fill=(20, 20, 20))
    buf = io.BytesIO()
    img.save(buf, "PDF", resolution=dpi, quality=80)
    flat = PdfReader(buf).pages[0]
    w = PdfWriter()
    w.add_page(flat)
    for p in PdfReader(src).pages[1:]:
        w.add_page(p)
    for p in w.pages:
        p.compress_content_streams()
    no_metadata(w)
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(dst_pdf, "wb") as fh:
        w.write(fh)
    # verification: nothing of the birth line may be extractable from the published file
    text = " ".join((p.extract_text() or "") for p in PdfReader(dst_pdf).pages)
    raw = dst_pdf.read_bytes()
    leaks = [m for m in BIRTH_MARKERS if m.lower() in text.lower() or m.encode() in raw]
    if leaks:
        dst_pdf.unlink()
        raise SystemExit(f"Youthpass redaction failed ({leaks}); output deleted")
    print(f"  {dst_pdf.relative_to(ROOT)}  {len(w.pages)} pages  {dst_pdf.stat().st_size // 1024} KB  (redacted, verified)")
    preview(img, dst_preview)


def main():
    if not SRC.exists():
        print("incoming/ not found, nothing to import")
        return
    w4f, g4h, meca = DST / "water4future-2026", DST / "game4health-2026", DST / "meca-world-cup-2026"
    print("Water4Future")
    webp(SRC / "water4future-2026/aman-prototype-demo.jpg", w4f / "aman-prototype-demo.webp", 900)
    webp(SRC / "water4future-2026/aman-hydroponic-prototype.jpg", w4f / "aman-prototype.webp", 900)
    webp(SRC / "water4future-2026/water-talent-prize.jpg", w4f / "water-talent-prize.webp", 1200)
    webp(SRC / "water4future-2026/attestation-of-participation.jpg", w4f / "attestation-of-participation.webp", 1100)
    pdf(SRC / "water4future-2026/aman-presentation.pdf", w4f / "aman-presentation.pdf", drop_pages={16})
    print("Game4Health")
    webp(SRC / "game4health-2026/pitch-team-stage.jpg", g4h / "pitch-team-stage.webp", 1200)
    webp(SRC / "game4health-2026/pitch-solution-slide.jpg", g4h / "pitch-solution-slide.webp", 1200)
    pdf_image(SRC / "game4health-2026/certificate-of-participation.pdf", g4h / "certificate-of-participation.webp", 1400, rotate=90)
    pdf(SRC / "game4health-2026/heart-guardian-presentation.pdf", g4h / "heart-guardian-presentation.pdf")
    print("MECA WORLD CUP")
    webp(SRC / "meca-world-cup-2026/team-photo-event.jpg", meca / "team-photo.webp", 900)
    webp(SRC / "meca-world-cup-2026/presenting-sportlinebot.jpg", meca / "presenting-sportlinebot.webp", 900)
    webp(SRC / "meca-world-cup-2026/robot-prototype.jpg", meca / "robot-prototype.webp", 900)
    webp(SRC / "meca-world-cup-2026/user-manual-cover.jpg", meca / "user-manual-cover.webp", 900)
    webp(SRC / "meca-world-cup-2026/certificate-of-participation.jpg", meca / "certificate-of-participation.webp", 1400, rotate=90)
    pdf(SRC / "meca-world-cup-2026/sportlinebot-presentation.pdf", meca / "sportlinebot-presentation.pdf", drop_pages={2})
    print("Volunteering")
    vol = ROOT / "assets" / "volunteering"
    scan_certificate(SRC / "volunteering/amazigh-new-year-2022-certificate.pdf", vol / "amazigh-new-year-2022-certificate.pdf", vol / "amazigh-new-year-2022-certificate.webp", rotate=90)
    youthpass_redacted(SRC / "volunteering/youthpass-hand-in-hand-2021.pdf", vol / "youthpass-hand-in-hand-2021.pdf", vol / "youthpass-hand-in-hand-2021.webp")
    sizes_file = ROOT / "tools" / "img_sizes.json"
    sizes = json.loads(sizes_file.read_text(encoding="utf-8"))
    sizes.update(SIZES)
    sizes_file.write_text(json.dumps(sizes), encoding="utf-8")


if __name__ == "__main__":
    main()
