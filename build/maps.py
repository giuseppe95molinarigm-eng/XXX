"""Country outline maps for the sample pages.

Source: Natural Earth 1:10m Admin 0 Countries (public domain), de facto boundaries.
Output: true vector SVG line art (stroked paths), sized in millimetres to the map
frame of the country page. Any difference between Natural Earth's de facto lines
and UN treatment is recorded in data/sample-data.csv and on the page notes.

Usage: python3 build/maps.py <path to ne_10m_admin_0_countries.geojson>
"""
import json, sys, os
from shapely.geometry import shape, Polygon, MultiPolygon, box
from shapely.ops import transform
from pyproj import Transformer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "maps")
FRAME_W, FRAME_H = 96.0, 80.0          # mm, map frame on the country page
STROKE = 0.30                            # mm, coastline / border weight
PAD = 3.0                                # mm, breathing room inside the frame

CAPITALS = {  # lon, lat, label, label side
    "ITA": (12.4964, 41.9028, "Rome", "r"),
    "JPN": (139.6917, 35.6895, "Tokyo", "l"),
    "USA": (-77.0369, 38.9072, "Washington, D.C.", "l"),
    "BRA": (-47.8828, -15.7939, "Brasília", "r"),
    "EGY": (31.2357, 30.0444, "Cairo", "r"),
    "AUS": (149.1300, -35.2809, "Canberra", "l"),
}

def laea(lat0, lon0):
    return f"+proj=laea +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m"

def albers(lat1, lat2, lat0, lon0):
    return f"+proj=aea +lat_1={lat1} +lat_2={lat2} +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m"

# Each view: projection, lon/lat clip box, frame rectangle in mm (x, y, w, h).
VIEWS = {
    "ITA": [dict(proj=laea(42, 12.5), clip=(6, 35, 19, 48), rect=(0, 0, FRAME_W, FRAME_H))],
    "JPN": [
        dict(proj=laea(37, 137.5), clip=(128.5, 30.0, 146.5, 46.0), rect=(0, 0, FRAME_W, FRAME_H)),
        dict(proj=laea(26.5, 127.5), clip=(122.5, 23.5, 131.5, 30.0), rect=(2, 2, 30, 26), inset="Ryukyu Islands"),
    ],
    "USA": [
        dict(proj=albers(29.5, 45.5, 37.5, -96), clip=(-125, 24, -66, 50), rect=(0, 0, FRAME_W, 54)),
        dict(proj=albers(55, 65, 50, -154), clip=(-190, 50, -129, 72), rect=(0, 56, 46, 24), inset="Alaska"),
        dict(proj=laea(20.5, -157.5), clip=(-161, 18.5, -154.5, 22.5), rect=(50, 56, 46, 24), inset="Hawaii"),
    ],
    "BRA": [dict(proj=laea(-14, -52), clip=(-74.5, -34.5, -34.0, 5.5), rect=(0, 0, FRAME_W, FRAME_H))],
    "EGY": [dict(proj=laea(26.5, 30), clip=(24, 21, 37.5, 32), rect=(0, 0, FRAME_W, FRAME_H))],
    "AUS": [dict(proj=laea(-27, 134), clip=(112, -44, 154.5, -9), rect=(0, 0, FRAME_W, FRAME_H))],
}

def wrap(geom):
    """Shift eastern-hemisphere Aleutians to negative longitudes."""
    def f(x, y, z=None):
        import numpy as np
        x = np.asarray(x); return (np.where(x > 0, x - 360, x), y)
    return transform(f, geom)

def path_d(geom, tx):
    parts = []
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            pts = [tx(x, y) for x, y in ring.coords]
            parts.append("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in pts) + "Z")
    return " ".join(parts)

def build(feat, code):
    geom = shape(feat["geometry"])
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {FRAME_W} {FRAME_H}" '
           f'width="{FRAME_W}mm" height="{FRAME_H}mm" class="map">']
    for i, v in enumerate(VIEWS[code]):
        g = wrap(geom) if code == "USA" and v.get("inset") == "Alaska" else geom
        g = g.intersection(box(*v["clip"]))
        fwd = Transformer.from_crs("EPSG:4326", v["proj"], always_xy=True)
        pg = transform(fwd.transform, g)
        x, y, w, h = v["rect"]
        minx, miny, maxx, maxy = pg.bounds
        s = min((w - 2 * PAD) / (maxx - minx), (h - 2 * PAD) / (maxy - miny))
        # scale-aware generalisation: drop specks and over-fine coastline detail
        tol = 0.12 / s
        pg = pg.simplify(tol, preserve_topology=True)
        min_area = 0.06 if v.get("inset") else 0.35          # mm2
        keep = []
        for p in (pg.geoms if isinstance(pg, MultiPolygon) else [pg]):
            if p.area * s * s <= min_area:
                continue
            # keep real enclaves (e.g. San Marino inside Italy), drop sliver holes
            holes = [r for r in p.interiors if Polygon(r).area * s * s > 0.2]
            keep.append(Polygon(p.exterior, holes))
        pg = MultiPolygon(keep)
        minx, miny, maxx, maxy = pg.bounds
        ox = x + (w - (maxx - minx) * s) / 2
        oy = y + (h - (maxy - miny) * s) / 2
        tx = lambda X, Y: (ox + (X - minx) * s, oy + (maxy - Y) * s)
        if v.get("inset"):
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#000" '
                       f'stroke-width="0.2"/>')
            svg.append(f'<text x="{x + 1.6}" y="{y + h - 1.6}" class="inset-label">{v["inset"]}</text>')
        svg.append(f'<path d="{path_d(pg, tx)}" fill="#fff" stroke="#000" stroke-width="{STROKE}" '
                   f'stroke-linejoin="round" stroke-linecap="round" fill-rule="evenodd"/>')
        if i == 0:
            lon, lat, label, side = CAPITALS[code]
            cx, cy = fwd.transform(lon, lat)
            cx, cy = tx(cx, cy)
            svg.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="1.1" fill="#fff" stroke="#000" stroke-width="0.25"/>')
            svg.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="0.45" fill="#000"/>')
            dx, anchor = (2.0, "start") if side == "r" else (-2.0, "end")
            svg.append(f'<text x="{cx + dx:.2f}" y="{cy + 1.0:.2f}" text-anchor="{anchor}" class="capital-label">{label}</text>')
    svg.append("</svg>")
    return "\n".join(svg)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(sys.argv[1]))
    feats = {f["properties"]["ADM0_A3"]: f for f in data["features"]}
    for code in VIEWS:
        open(os.path.join(OUT, f"map-{code.lower()}.svg"), "w").write(build(feats[code], code))
        print("wrote", code)
