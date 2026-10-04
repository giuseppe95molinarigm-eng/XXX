"""Outline maps for all 195 country pages (vector SVG, 96 x 76 mm frame).

Source: Natural Earth 1:10m admin 0 countries + disputed areas (public domain). The de facto
lines are adjusted to United Nations practice where the book says so (Crimea, Golan, East
Jerusalem, Somaliland, Northern Cyprus, Kosovo, Taiwan, Hong Kong, Macao, Baikonur).
The six Phase 1 sample maps (with hand-set insets) are kept from build/maps.py.
Usage: python3 build/maps_all.py <ne_10m_admin_0_countries.geojson> <ne_10m_admin_0_disputed_areas.geojson>
"""
import json, math, os, sys
import numpy as np
from shapely.geometry import shape, Polygon, MultiPolygon, Point, box
from shapely.ops import transform, unary_union
from pyproj import Transformer
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "build"), os.path.join(ROOT, "data")]
from pagemap import CONTINENTS
OUT = os.path.join(ROOT, "assets", "maps")
W, H, PAD, STROKE = 96.0, 76.0, 3.0, 0.30
DONE = {"Italy", "Japan", "United States", "Brazil", "Egypt", "Australia"}

MERGE = {"SOM": ["SOL"], "CYP": ["CYN", "CNM"], "SRB": ["KOS"], "CHN": ["TWN", "HKG", "MAC"], "KAZ": ["KAB"],
         "IND": ["KAS"], "CHL": ["SPI"], "ARG": ["SPI"]}
MOVE = [("Crimea", "RUS", "UKR"), ("Golan Heights", "ISR", "SYR"), ("East Jerusalem", "ISR", "PSX"),
        ("No Man's Land (Jerusalem)", "ISR", "PSX"), ("Mount Scopus", "ISR", "PSX"), ("No Man's Land (Fort Latrun)", "ISR", "PSX")]
# keep only the home territory (lon/lat box, after wrapping) and add a note for what is left out
CLIP = {
    "France": ((-6, 41, 10, 51.5), "Overseas regions are not shown at this scale."),
    "Spain": ((-10, 35.5, 5, 44.5), "The Canary Islands are not shown at this scale."),
    "Portugal": ((-10, 36.8, -6, 42.2), "The Azores and Madeira are not shown at this scale."),
    "Norway": ((4, 57.5, 32, 71.5), "Svalbard and Jan Mayen are not shown at this scale."),
    "Netherlands": ((3, 50.7, 7.5, 53.7), "The Caribbean Netherlands are not shown at this scale."),
    "Ecuador": ((-81.5, -5.1, -75, 1.7), "The Galápagos Islands are not shown at this scale."),
    "Chile": ((-76, -56, -66, -17.4), "Easter Island and other Pacific islands are not shown at this scale."),
    "Colombia": ((-80, -4.5, -66, 13), "San Andrés and Providencia are not shown at this scale."),
    "South Africa": ((16, -35.2, 33.2, -22), "The Prince Edward Islands are not shown at this scale."),
    "New Zealand": ((166, -47.5, 179, -34), "The Chatham Islands and outlying islands are not shown at this scale."),
    "Mauritius": ((57.2, -20.6, 57.9, -19.9), "Rodrigues, Agaléga and other outer islands are not shown at this scale."),
    "Seychelles": ((55.2, -4.9, 56.0, -4.2), "Only the main islands around Mahé are shown."),
    "Honduras": ((-89.5, 12.8, -83, 16.6), None),
    "Venezuela": ((-73.5, 0.5, -59.5, 12.3), None),
    "Equatorial Guinea": ((5.4, -1.6, 11.5, 4), None),
    "Denmark": ((7.8, 54.5, 15.3, 57.9), None),
    "India": ((68, 6.5, 97.5, 37.2), None),
    "Russia": ((19, 41, 191, 82), None),
    "Fiji": ((176.5, -21, 182.5, -15.5), "Rotuma and other outlying islands are not shown at this scale."),
    "Greece": ((19, 34.5, 30, 42), None),
    "Yemen": ((41.5, 11.5, 55, 19.2), None),
}
ISLANDS = {"Kiribati", "Fiji", "Micronesia", "Marshall Islands", "Tuvalu", "Seychelles", "Maldives", "Solomon Islands",
           "Vanuatu", "Tonga", "Samoa", "Bahamas", "Cabo Verde", "Comoros", "Palau", "Sao Tome and Principe",
           "Antigua and Barbuda", "Saint Kitts and Nevis", "Saint Vincent and the Grenadines", "Grenada", "Mauritius"}

def load(ne, disputed):
    feats = json.load(open(ne))["features"]
    g = {}
    for f in feats:
        a = f["properties"]["ADM0_A3"]
        g[a] = shape(f["geometry"]).buffer(0)
    dis = {f["properties"].get("BRK_NAME"): shape(f["geometry"]).buffer(0) for f in json.load(open(disputed))["features"]}
    for name, frm, to in MOVE:
        part = dis[name]
        g[frm] = g[frm].difference(part)
        g[to] = unary_union([g[to], part])
    for k, extra in MERGE.items():
        g[k] = unary_union([g[k]] + [g[e] for e in extra if e in g])
    return g

def parts(geom):
    return list(geom.geoms) if hasattr(geom, "geoms") else [geom]

def wrap(geom, lon0):
    def f(x, y, z=None):
        x = np.asarray(x, dtype=float)
        return (np.where(x < lon0 - 180, x + 360, np.where(x > lon0 + 180, x - 360, x)), y)
    return transform(f, geom)

def path(polys, tx):
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            out.append("M" + " L".join(f"{a:.2f},{b:.2f}" for a, b in (tx(x, y) for x, y in ring.coords)) + "Z")
    return " ".join(out)

def build(name, geom, cap):
    biggest = max(parts(geom), key=lambda p: p.area)
    lon0 = biggest.centroid.x
    geom = wrap(geom, lon0).buffer(0)
    note = None
    if name in CLIP:
        bb, note = CLIP[name]
        geom = geom.intersection(box(*bb))
    elif name not in ISLANDS:
        # drop far-away fragments (overseas territories) automatically
        ea = Transformer.from_crs("EPSG:4326", f"+proj=laea +lat_0={biggest.centroid.y} +lon_0={lon0}", always_xy=True)
        pg = [transform(ea.transform, p) for p in parts(geom)]
        big = max(pg, key=lambda p: p.area)
        lim = max(800e3, 2.5 * math.sqrt(big.area))
        keep = [p for p, q in zip(parts(geom), pg) if q.centroid.distance(big.centroid) < lim]
        if len(keep) < len(pg) and sum(q.area for p, q in zip(parts(geom), pg) if p not in keep) > 50e6:
            note = "Distant islands are not shown at this scale."
        geom = MultiPolygon(keep)
    minx, miny, maxx, maxy = geom.bounds
    proj = f"+proj=laea +lat_0={(miny + maxy) / 2} +lon_0={(minx + maxx) / 2} +datum=WGS84 +units=m"
    fwd = Transformer.from_crs("EPSG:4326", proj, always_xy=True)
    pg = transform(fwd.transform, geom)
    bx = pg.bounds
    s = min((W - 2 * PAD) / (bx[2] - bx[0]), (H - 2 * PAD) / (bx[3] - bx[1]))
    pg = pg.simplify(0.12 / s, preserve_topology=True)
    ox = (W - (bx[2] - bx[0]) * s) / 2
    oy = (H - (bx[3] - bx[1]) * s) / 2
    tx = lambda X, Y: (ox + (X - bx[0]) * s, oy + (bx[3] - Y) * s)
    polys, dots = [], []
    for p in parts(pg):
        if p.is_empty:
            continue
        if p.area * s * s > 0.35:
            holes = [r for r in p.interiors if Polygon(r).area * s * s > 0.2]
            polys.append(Polygon(p.exterior, holes))
        elif name in ISLANDS or p.area * s * s > 0.02:
            x, y = tx(p.centroid.x, p.centroid.y)
            if all((x - a) ** 2 + (y - b) ** 2 > 1.6 ** 2 for a, b in dots):
                dots.append((x, y))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm" class="map">',
           f'<path d="{path(polys, tx)}" fill="#fff" stroke="#000" stroke-width="{STROKE}" stroke-linejoin="round" stroke-linecap="round" fill-rule="evenodd"/>']
    for x, y in dots:
        svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.55" fill="#fff" stroke="#000" stroke-width="0.25"/>')
    if cap:
        lat, lon = cap
        if lon < lon0 - 180: lon += 360
        elif lon > lon0 + 180: lon -= 360
        cx, cy = tx(*fwd.transform(lon, lat))
        label = cap_label(name)
        right = cx < W * 0.62
        svg.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="1.1" fill="#fff" stroke="#000" stroke-width="0.25"/>')
        svg.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="0.45" fill="#000"/>')
        svg.append(f'<text x="{cx + (2 if right else -2):.2f}" y="{cy + 1:.2f}" text-anchor="{"start" if right else "end"}" class="capital-label">{label}</text>')
    svg.append("</svg>")
    return "\n".join(svg), note

def cap_label(name):
    from countries_master import COUNTRIES
    return COUNTRIES[name]["capital"].split(",")[0].replace("*", "")

if __name__ == "__main__":
    g = load(sys.argv[1], sys.argv[2])
    base = json.load(open(os.path.join(ROOT, "data/base-mledoze.json")))
    caps = json.load(open(os.path.join(ROOT, "data/capital-coords.json")))
    a3fix = {"PSE": "PSX", "SSD": "SDS", "XKX": "KOS"}
    notes = {}
    for cont, names in CONTINENTS.items():
        for n in names:
            if n in DONE:
                continue
            a3 = base[n]["cca3"]
            geom = g.get(a3fix.get(a3, a3)) or g.get(a3)
            if geom is None:
                print("MISSING", n, a3); continue
            cap = caps.get(n)
            svg, note = build(n, geom, cap)
            open(os.path.join(OUT, f"map-{a3.lower()}.svg"), "w").write(svg)
            if note:
                notes[n] = note
    json.dump(notes, open(os.path.join(ROOT, "data/map-notes.json"), "w"), indent=1, ensure_ascii=False)
    print("done; notes:", len(notes))
