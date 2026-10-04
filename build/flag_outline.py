"""Derive coloring-book outline flags from colored construction SVGs.

Method: the colored flag (assets/flags/source-color, derived from Wikimedia Commons
constructions, public domain) is rendered at 60 px/mm for a 66 mm flag; every boundary
between two colour areas becomes a line of constant weight; the result is traced with
potrace to vector. The outer edge gets a slightly heavier rule. Output: assets/flags/outline.
Every outline must still be checked by eye against the official construction sheet.
"""
import os, sys, subprocess, numpy as np
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PX_PER_MM = 60
INNER_MM, OUTER_MM = 0.17, 0.30

def outline(png, out_svg):
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    h, w, _ = a.shape
    e = np.zeros((h, w), bool)
    for dy, dx in ((0, 2), (2, 0)):   # compare with pixel 2 px away (skips anti-alias ramp)
        d = np.abs(a[dy:, dx:] - a[:h - dy, :w - dx]).sum(-1) > 90
        e[:h - dy, :w - dx] |= d
    img = Image.fromarray(np.where(e, 0, 255).astype("uint8"))
    k = int(INNER_MM * PX_PER_MM) | 1
    img = img.filter(ImageFilter.MinFilter(max(3, k - 2)))
    b = int(OUTER_MM * PX_PER_MM)
    arr = np.asarray(img).copy()
    arr[:b, :] = 0; arr[-b:, :] = 0; arr[:, :b] = 0; arr[:, -b:] = 0
    Image.fromarray(arr).convert("1").save("/tmp/flag.pbm")
    subprocess.run(["potrace", "-s", "-t", "6", "-a", "1.0", "-O", "0.2", "-u", "10", "--flat",
                    "-o", out_svg, "/tmp/flag.pbm"], check=True)

if __name__ == "__main__":
    src = sys.argv[1]
    for f in sorted(os.listdir(src)):
        if f.endswith(".png"):
            outline(os.path.join(src, f), os.path.join(ROOT, "assets/flags/outline", f[:-4] + ".svg"))
            print("outline", f)
