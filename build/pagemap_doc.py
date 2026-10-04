"""Render the PROVISIONAL page map (flatplan + section table) to page-map/page-map.html."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pagemap import CONTINENTS, build as build_map
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COL = {"front matter": "#1f2a44", "journal": "#5d6b57", "pacing": "#ffffff", "continent": "#b8975a",
       "country page": "#e9e1cf", "register": "#8a1c1c", "flexible": "#cfd6e4"}

def rows_full():
    return build_map()

def sections(rows):
    out, cur = [], None
    for r in rows:
        key = (r[2], r[4]) if r[2] in ("country page",) else (r[2], r[4], r[3].split(" (")[0].split(":")[0])
        if cur and cur["key"] == key:
            cur["to"] = r[0]; cur["n"] += 1
        else:
            cur = {"key": key, "from": r[0], "to": r[0], "n": 1, "kind": r[2], "title": r[3], "cont": r[4]}
            out.append(cur)
    return out

def html():
    rows = rows_full()
    samples = {"Italy", "Japan", "United States", "Brazil", "Egypt", "Australia"}
    cells = []
    for r in rows:
        border = "2px solid #8a1c1c" if r[3] in samples else ".3pt solid #999"
        pat = f"background:{COL[r[2]]};"
        cells.append(f'<div class="c" style="{pat}border:{border}" title="{r[0]} {r[3]}"><span>{r[0]}</span></div>')
    table = []
    for s in sections(rows):
        rng = f'{s["from"]}' if s["from"] == s["to"] else f'{s["from"]}–{s["to"]}'
        if s["kind"] == "country page":
            title = f'{s["cont"]}: {s["n"]} country pages, alphabetical (one country per page)'
        else:
            title = s["title"].split(" (")[0] if s["n"] > 1 else s["title"]
        table.append(f'<tr><td>{rng}</td><td>{s["n"]}</td><td>{title}</td></tr>')
    sample_list = ", ".join(f"{r[3]} p. {r[0]}" for r in rows if r[3] in samples)
    counts = {}
    for r in rows:
        counts[r[2]] = counts.get(r[2], 0) + 1
    legend = "".join(f'<span><i style="background:{COL[k]}"></i>{k} ({counts.get(k, 0)})</span>' for k in COL)
    css = """
    .pm .live { font-size: 8.5pt; line-height: 1.3; }
    .pm h1 { font-family: "Cormorant Garamond"; font-weight: 600; font-size: 24pt; letter-spacing: .08em; text-transform: uppercase; margin: 0 0 1mm; }
    .pm .lede { font-style: italic; font-size: 9.5pt; margin: 0 0 3mm; }
    .grid { display: grid; grid-template-columns: repeat(16, 1fr); gap: .6mm; margin: 2mm 0; }
    .c { height: 8.6mm; position: relative; }
    .c span { position: absolute; left: .5mm; top: .2mm; font-size: 4.6pt; color: #555; }
    .legend { display: flex; flex-wrap: wrap; gap: 2mm 5mm; font-size: 7.5pt; margin: 2mm 0; }
    .legend i { display: inline-block; width: 3mm; height: 3mm; border: .3pt solid #999; margin-right: 1mm; vertical-align: -0.5mm; }
    table { width: 100%; border-collapse: collapse; font-size: 7.6pt; }
    td, th { border-bottom: .25pt solid #000; padding: .7mm 2mm .7mm 0; text-align: left; vertical-align: top; }
    th { font-size: 6.5pt; letter-spacing: .12em; text-transform: uppercase; border-bottom: .5pt solid #000; }
    .pm p { margin: 0 0 2mm; }
    """
    half = (len(table) + 1) // 2
    p1 = f'''<section class="page pm recto"><div class="proposal-tag">Proposal · not approved</div><div class="live">
      <h1>Page Map · 288 pages</h1>
      <p class="lede">The Phase 1 Blueprint page map (272 pages, four parts) updated with every decision settled since. A proposal for your approval, not a final extent.</p>
      <p><b>What changed against the Blueprint.</b> One Hundred Places removed (−2). Register of Colors cut from 8 to 4 pages (−4). A bucket list of 15 experiences for every continent, one spread each (+12). The achievement page absorbed into each continent's closing spread, at no page cost. Travel ledger expanded from 2 to 4 pages (+2); My Top Five (+2) and one Favorite Memory spread (+2) added; Where I Go Next keeps the reader's list and adds a planning block. Two pacing blanks keep Part III opening on a spread and Part IV opening on a right-hand page; two flexible notes pages before the colophon complete the eighteenth signature. The epigraph is your original line; the Melville quotation now sits alone on the Departure page before Europe.</p>
      <p><b>Sample pages in this map:</b> {sample_list}. One country per page, atlas order of continents as in the Blueprint (Europe, Africa, Asia, North America &amp; the Caribbean, South America, Oceania), countries alphabetical within each continent.</p>
      <div class="legend">{legend}<span><i style="border:2px solid #8a1c1c"></i>Phase 1 sample</span></div>
      <div class="grid">{"".join(cells)}</div>
      <p style="font-size:7.5pt;font-style:italic">Each row is one 16-page signature. Odd numbers are right-hand pages.</p>
    </div><div class="folio">1</div></section>'''
    p2 = f'''<section class="page pm verso"><div class="live">
      <table><tr><th>Pages</th><th>#</th><th>Content</th></tr>{"".join(table[:half])}</table>
    </div><div class="folio">2</div></section>'''
    p3 = f'''<section class="page pm recto"><div class="live">
      <table><tr><th>Pages</th><th>#</th><th>Content</th></tr>{"".join(table[half:])}</table>
      <h3 style="font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;margin:5mm 0 2mm">Open points</h3>
      <p>1. Color register: our density test shows four pages hold all 195 entries only at 8.5 pt with a length budget per entry; at 9 pt it needs six pages, which would replace the two notes pages and one more spread.</p>
      <p>2. The Blueprint places the Departure page on p. 28 and Europe on p. 29, which would split the two-page continent opener across a turn. Here Part III begins on p. 28 so that each opener (essay left, title plate right) is a true spread.</p>
      <p>3. Transcontinental countries follow UN M49 (Russia in Europe; Türkiye, Cyprus, Georgia, Armenia, Azerbaijan, Kazakhstan in Asia), explained on The World in Six Parts.</p>
      <p>4. Country short names follow UN usage (Türkiye, Czechia, Côte d'Ivoire, Cabo Verde, Eswatini, Timor-Leste) with common American English for a few (United States, United Kingdom, Russia, Iran, Vietnam, Laos, Syria, South Korea, North Korea, Tanzania, Bolivia, Venezuela, Moldova, Micronesia, Palestine). The Holy See page is titled "Holy See", with Vatican City State for the territory and its figures.</p>
    </div><div class="folio">3</div></section>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>THE WORLD page map proposal</title>
<link rel="stylesheet" href="../build/book.css"><style>{css}</style></head><body class="screen-gap">{p1}{p2}{p3}</body></html>'''

if __name__ == "__main__":
    open(os.path.join(ROOT, "page-map", "page-map.html"), "w").write(html())
    print("ok")
