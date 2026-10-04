"""World and continent maps (Natural Earth 1:10m, UN-practice adjustments as in maps_all.py).
Writes assets/maps/world-color.svg (all borders, to color), world-ghost.svg (frontispiece, with
graticule), world-six-parts.svg (continent key) and continent-*.svg (opener plates).
Usage: python3 build/worldmaps.py <ne_countries.geojson> <ne_disputed.geojson>"""
import json, os, sys, re
import numpy as np
from shapely.geometry import box, LineString, MultiPolygon, Polygon
from shapely.ops import transform, unary_union
from pyproj import Transformer
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "build"), os.path.join(ROOT, "data")]
from maps_all import load, MERGE
from pagemap import CONTINENTS
OUT = os.path.join(ROOT, "assets", "maps")

def parts(g):
    return list(g.geoms) if hasattr(g, "geoms") else [g]

def d_of(geoms, tx, min_area=0.0):
    out = []
    for g in geoms:
        for p in parts(g):
            if not hasattr(p, "exterior") or p.is_empty or p.area < min_area:
                continue
            for ring in [p.exterior, *p.interiors]:
                out.append("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in (tx(x, y) for x, y in ring.coords)) + "Z")
    return " ".join(out)

def robinson(width):
    fwd = Transformer.from_crs("EPSG:4326", "+proj=robin +lon_0=11 +datum=WGS84 +units=m", always_xy=True)
    def pr(g):
        g = g.intersection(box(-168.9, -58, 191.1, 84))  # recentered at 11°E: cut along the Bering Strait
        def wrapf(x, y, z=None):
            x = np.asarray(x, dtype=float)
            return (np.where(x < -168.9, x + 360, x), y)
        return transform(fwd.transform, transform(wrapf, g))
    return pr, fwd

if __name__ == "__main__":
    g = load(sys.argv[1], sys.argv[2])
    for k, extra in MERGE.items():
        for e in extra:
            g.pop(e, None)
    g.pop("ATA", None)
    pr, fwd = robinson(1)
    proj = {k: pr(v.simplify(0.02)) for k, v in g.items()}
    allg = unary_union([v for v in proj.values() if not v.is_empty])
    minx, miny, maxx, maxy = allg.bounds

    def world(w, stroke, fname, extra=""):
        s = w / (maxx - minx); h = (maxy - miny) * s
        tx = lambda X, Y: ((X - minx) * s, (maxy - Y) * s)
        body = f'<path d="{d_of(proj.values(), tx, (0.25 / s) ** 2)}" fill="#fff" stroke="currentColor" stroke-width="{stroke}" stroke-linejoin="round"/>'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w}mm" height="{h:.1f}mm">{extra(tx, s) if extra else ""}{body}</svg>'
        open(os.path.join(OUT, fname), "w").write(svg)
        return h

    def graticule(tx, s):
        lines = []
        for lon in range(-165, 196, 15):
            ln = LineString([(lon, lat) for lat in np.linspace(-58, 84, 80)])
            lines.append(ln)
        for lat in range(-45, 85, 15):
            lines.append(LineString([(lon, lat) for lon in np.linspace(-168.9, 191.1, 200)]))
        out = []
        for ln in lines:
            p = transform(fwd.transform, ln)
            out.append("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in (tx(x, y) for x, y in p.coords)))
        return f'<path d="{" ".join(out)}" fill="none" stroke="currentColor" stroke-width="0.25"/>'

    print("world-color h", world(260, 0.22, "world-color.svg"))
    print("world-ghost h", world(216, 0.3, "world-ghost.svg", graticule))

    base = json.load(open(os.path.join(ROOT, "data/base-mledoze.json")))
    a3fix = {"PSE": "PSX", "SSD": "SDS"}
    cont_geom = {}
    for cont, names in CONTINENTS.items():
        geoms = [g[a3fix.get(base[n]["cca3"], base[n]["cca3"])] for n in names]
        cont_geom[cont] = geoms
    # six-parts key map: continents drawn as filled outlines with country borders
    s = 176 / (maxx - minx); h = (maxy - miny) * s
    tx = lambda X, Y: ((X - minx) * s, (maxy - Y) * s)
    groups = []
    for i, (cont, geoms) in enumerate(cont_geom.items(), 1):
        pg = [pr(x.simplify(0.02)) for x in geoms]
        u = unary_union(pg)
        c = u.representative_point() if cont != "Europe" else pr(box(10, 50, 11, 51)).centroid
        if cont == "Asia": c = pr(box(95, 40, 96, 41)).centroid
        if cont == "North America & the Caribbean": c = pr(box(-100, 45, -99, 46)).centroid
        if cont == "Oceania": c = pr(box(133, -25, 134, -24)).centroid
        if cont == "Africa": c = pr(box(20, 5, 21, 6)).centroid
        if cont == "South America": c = pr(box(-60, -10, -59, -9)).centroid
        x, y = tx(c.x, c.y)
        groups.append(f'<path d="{d_of([u], tx, (0.3 / s) ** 2)}" fill="#fff" stroke="#000" stroke-width="0.35" stroke-linejoin="round"/>'
                      f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#fff" stroke="#000" stroke-width="0.35"/>'
                      f'<text x="{x:.1f}" y="{y + 1.5:.1f}" text-anchor="middle" font-family="Cormorant Garamond" font-weight="600" font-size="4.6">{i}</text>')
    rest = [v for k, v in proj.items() if not any(k == a3fix.get(base[n]["cca3"], base[n]["cca3"]) for ns in CONTINENTS.values() for n in ns)]
    other = f'<path d="{d_of(rest, tx, (0.3 / s) ** 2)}" fill="#fff" stroke="#000" stroke-width="0.15" stroke-dasharray="0.6 0.6"/>'
    open(os.path.join(OUT, "world-six-parts.svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 176 {h:.1f}" width="176mm" height="{h:.1f}mm">{other}{"".join(groups)}</svg>')

    # continent plates: country borders, local equal-area projection
    clip = {"Europe": (-25, 34, 45, 71.5), "Asia": (25, -11, 150, 56), "North America & the Caribbean": (-170, 7, -52, 72),
            "Oceania": (110, -48, 180, 10), "Africa": (-26, -35.5, 58, 38), "South America": (-82, -56, -34, 13)}
    for cont, geoms in cont_geom.items():
        bb = clip[cont]
        gg = [x.intersection(box(*bb)) for x in geoms]
        if cont == "Oceania":
            gg = [x.intersection(box(110, -48, 180, 10)).union(transform(lambda X, Y, z=None: (np.asarray(X) + 360, Y), x.intersection(box(-180, -48, -150, 10)))) for x in geoms]
        lon0, lat0 = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        f = Transformer.from_crs("EPSG:4326", f"+proj=laea +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m", always_xy=True)
        pg = [transform(f.transform, x) for x in gg if not x.is_empty]
        u = unary_union(pg); bx = u.bounds
        W, H = 150, 120
        s2 = min(W / (bx[2] - bx[0]), H / (bx[3] - bx[1]))
        ox = (W - (bx[2] - bx[0]) * s2) / 2; oy = (H - (bx[3] - bx[1]) * s2) / 2
        t2 = lambda X, Y: (ox + (X - bx[0]) * s2, oy + (bx[3] - Y) * s2)
        pg = [p.simplify(0.15 / s2) for p in pg]
        # draw only real coast and border lines: rings are cut by the clip box, never closed along it
        full = [transform(f.transform, x) for x in (geoms if cont != "Oceania" else gg) if not x.is_empty]
        clipbox = transform(f.transform, box(*bb).segmentize(0.5)) if cont != "Oceania" else None
        segs = []
        for g0 in full:
            for p in parts(g0.simplify(0.15 / s2)):
                if p.is_empty or not hasattr(p, "exterior") or p.area < (0.4 / s2) ** 2:
                    continue
                for ring in [p.exterior, *p.interiors]:
                    ln = LineString(ring.coords)
                    if clipbox is not None:
                        ln = ln.intersection(clipbox)
                    for l in (ln.geoms if hasattr(ln, "geoms") else [ln]):
                        if l.length > 0 and hasattr(l, "coords"):
                            segs.append("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in (t2(x, y) for x, y in l.coords)))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">'
               f'<path d="{" ".join(segs)}" fill="none" stroke="#000" stroke-width="0.28" stroke-linejoin="round" stroke-linecap="round"/></svg>')
        open(os.path.join(OUT, f"continent-{re.sub('[^a-z]+', '-', cont.lower()).strip('-')}.svg"), "w").write(svg)
    print("ok")
