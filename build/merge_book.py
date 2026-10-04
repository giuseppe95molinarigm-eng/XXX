"""Merge the rendered chunks into book/THE-WORLD-interior.pdf and set print boxes.
MediaBox = BleedBox = 216 x 303 mm; TrimBox = 210 x 297 mm (3 mm bleed on every side)."""
import glob, os
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MM = 72 / 25.4
w = PdfWriter()
for f in sorted(glob.glob(os.path.join(ROOT, "book/pdf/part-*.pdf"))):
    for p in PdfReader(f).pages:
        w.add_page(p)
for p in w.pages:
    W, H = float(p.mediabox.width), float(p.mediabox.height)
    p.bleedbox = RectangleObject([0, 0, W, H])
    p.trimbox = RectangleObject([3 * MM, 3 * MM, W - 3 * MM, H - 3 * MM])
w.add_metadata({"/Title": "THE WORLD: Countries & Flags. A Coloring Journal for the Places You've Visited", "/Author": "ElitePublishing"})
out = os.path.join(ROOT, "book/THE-WORLD-Countries-and-Flags-interior.pdf")
w.write(out)
print(len(w.pages), "pages ->", out, os.path.getsize(out) // 1024 // 1024, "MB")
