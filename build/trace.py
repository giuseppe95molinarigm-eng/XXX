"""Trace the AI line-art rasters into true vector SVG with potrace.

Raster sources (AI generated, google/nano-banana-pro via Replicate) stay in
assets/illustrations/source-ai-raster/ for reference only; the page uses the traced
vector in assets/illustrations/vector/. Cleanup applied before tracing:
 - flatten to pure black/white at a fixed threshold (removes grey anti-alias haze)
 - remove isolated specks below `turdsize` (stray AI marks)
 - optional per-image masks (rectangles to whiten) listed in MASKS
"""
import os, subprocess, glob
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets/illustrations/source-ai-raster")
DST = os.path.join(ROOT, "assets/illustrations/vector")
THRESH = 150
MASKS = {  # file stem -> list of (x0, y0, x1, y1) px rectangles to whiten
}
for f in sorted(glob.glob(os.path.join(SRC, "*.png"))):
    stem = os.path.splitext(os.path.basename(f))[0]
    if os.path.exists(os.path.join(DST, stem + ".svg")) and os.path.getmtime(os.path.join(DST, stem + ".svg")) > os.path.getmtime(f):
        continue
    im = Image.open(f).convert("L")
    d = ImageDraw.Draw(im)
    for r in MASKS.get(stem, []):
        d.rectangle(r, fill=255)
    bw = im.point(lambda v: 0 if v < THRESH else 255, "1")
    pbm = f"/tmp/{stem}.pbm"; bw.save(pbm)
    out = os.path.join(DST, stem + ".svg")
    subprocess.run(["potrace", "-s", "-t", "30", "-a", "1.0", "-O", "0.3", "-u", "10",
                    "--flat", "-o", out, pbm], check=True)
    print(stem, im.size, os.path.getsize(out) // 1024, "KB")
