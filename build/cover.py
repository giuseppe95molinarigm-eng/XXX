"""Cover direction (front board only). NOT a production cover: board size, spine width and
foil artwork are set from the printer's template and blank dummy.
Writes assets/cover/world-foil.svg, assets/cover/compass-rose.svg, style-guide/cover-direction.html
"""
import json, math, os, sys
from shapely.geometry import shape, MultiPolygon, Polygon
from shapely.ops import transform, unary_union
from pyproj import Transformer
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def world_svg(ne_path, width=150.0, stroke=0.3):
    feats = json.load(open(ne_path))["features"]
    fwd = Transformer.from_crs("EPSG:4326", "+proj=robin +lon_0=0 +datum=WGS84 +units=m", always_xy=True)
    polys = []
    for f in feats:
        if f["properties"]["ADM0_A3"] == "ATA":
            continue                                   # Antarctica omitted on the cover (design choice)
        g = transform(fwd.transform, shape(f["geometry"]).buffer(0).simplify(0.05)).buffer(0)
        polys.append(g)
    land = unary_union(polys)                          # coastlines only: foil cannot hold 195 borders
    minx, miny, maxx, maxy = land.bounds
    s = width / (maxx - minx)
    land = land.simplify(0.5 / s)                      # generalise to ~0.5 mm: foil-safe detail
    keep = [p for p in land.geoms if p.area * s * s > 2.0]
    h = (maxy - miny) * s
    d = []
    for p in keep:
        for ring in [p.exterior]:
            d.append("M" + " L".join(f"{(x - minx) * s:.2f},{(maxy - y) * s:.2f}" for x, y in ring.coords) + "Z")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {h:.1f}" width="{width}mm" height="{h:.1f}mm">'
            f'<path d="{" ".join(d)}" fill="none" stroke="currentColor" stroke-width="{stroke}" stroke-linejoin="round"/></svg>')

def compass_svg():
    r1, r2 = 20, 6
    pts = []
    parts = []
    for i in range(8):
        a = math.radians(i * 45 - 90)
        R = r1 if i % 2 == 0 else r1 * 0.62
        ax, ay = R * math.cos(a), R * math.sin(a)
        for side in (-1, 1):
            b = math.radians(i * 45 - 90 + side * 22.5)
            bx, by = r2 * 0.55 * math.cos(b) * (1.6 if i % 2 else 1), r2 * 0.55 * math.sin(b) * (1.6 if i % 2 else 1)
            fill = "currentColor" if side == 1 else "none"
            parts.append(f'<path d="M0,0 L{ax:.2f},{ay:.2f} L{bx:.2f},{by:.2f}Z" fill="{fill}" stroke="currentColor" stroke-width=".35" stroke-linejoin="round"/>')
    rings = ('<circle r="14.5" fill="none" stroke="currentColor" stroke-width=".35"/>'
             '<circle r="13.4" fill="none" stroke="currentColor" stroke-width=".2"/>')
    ticks = "".join(
        f'<line x1="{13.4 * math.cos(math.radians(t)):.2f}" y1="{13.4 * math.sin(math.radians(t)):.2f}" '
        f'x2="{(14.5 if t % 45 else 15.6) * math.cos(math.radians(t)):.2f}" y2="{(14.5 if t % 45 else 15.6) * math.sin(math.radians(t)):.2f}" '
        f'stroke="currentColor" stroke-width=".2"/>' for t in range(0, 360, 15))
    letters = "".join(f'<text x="{x}" y="{y}" font-family="Cormorant Garamond" font-weight="600" font-size="4" text-anchor="middle" fill="currentColor">{l}</text>'
                      for l, x, y in (("N", 0, -22.6), ("E", 24.4, 1.4), ("S", 0, 25.4), ("W", -24.4, 1.4)))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-27 -27 54 54">{rings}{ticks}{"".join(parts)}{letters}</svg>'

if __name__ == "__main__":
    out = os.path.join(ROOT, "assets", "cover"); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "world-foil.svg"), "w").write(world_svg(sys.argv[1]))
    open(os.path.join(out, "compass-rose.svg"), "w").write(compass_svg())
    print("ok")
