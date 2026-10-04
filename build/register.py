"""Color register: specimen sheet (10 real entries) and 4-page density test (195 entries).

The density test sets the 10 approved-for-review entries as written and fills the other
185 with neutral placeholder text whose LENGTH is estimated from the flag's complexity
(S simple stripes/blocks, M stripes + simple symbol, C coat of arms / seal / inscription /
detailed figure). Placeholders print in grey italic so nobody mistakes them for copy.
Pagination happens in the browser: entries flow into 2-column pages of fixed height and
the page count is reported on the last page.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from pagemap import CONTINENTS, build as build_map
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "color-register")

C = set("""Afghanistan;Albania;Andorra;Angola;Belarus;Belize;Bhutan;Bolivia;Brazil;Brunei;Cambodia;Croatia;Cyprus;Dominica;Dominican Republic;Ecuador;Egypt;El Salvador;Equatorial Guinea;Eswatini;Fiji;Guatemala;Haiti;Holy See;Iran;Iraq;Kazakhstan;Kenya;Kiribati;Kyrgyzstan;Liechtenstein;Malta;Mexico;Moldova;Mongolia;Montenegro;Mozambique;Nepal;Nicaragua;Papua New Guinea;Paraguay;Portugal;San Marino;Saudi Arabia;Serbia;Slovakia;Slovenia;South Africa;South Korea;Spain;Sri Lanka;Turkmenistan;Uganda;United States;Zimbabwe;Australia;New Zealand;Tuvalu;United Kingdom;Grenada;Costa Rica;Venezuela;Zambia""".split(";"))
S = set("""Italy;France;Germany;Belgium;Ireland;Austria;Netherlands;Luxembourg;Russia;Estonia;Lithuania;Latvia;Bulgaria;Hungary;Romania;Chad;Mali;Guinea;Nigeria;Côte d'Ivoire;Sierra Leone;Gabon;Yemen;Colombia;Ukraine;Poland;Monaco;Indonesia;Japan;Bangladesh;Palau;Laos;Peru;Botswana;Thailand;Mauritius;Armenia;Benin;Madagascar;Sweden;Denmark;Finland;Norway;Iceland;Switzerland;Czechia;Bahamas;Jamaica;Sudan;Kuwait;United Arab Emirates;Bahrain;Qatar;Trinidad and Tobago;Gambia;Congo;Tanzania;Seychelles;Guinea-Bissau""".split(";"))
EST = {"S": 75, "M": 155, "C": 285}     # natural length if written freely
BUDGET = {"S": 70, "M": 125, "C": 215}  # proposed maximum average per type to fit 4 pages
FILL = ("This line stands in for an entry that has not been written yet; its length is estimated "
        "from the kind of flag, so that the four pages can be judged for density before the remaining "
        "entries are drafted and approved by the client in the agreed plain-language pattern. ") * 3

def cls(n):
    return "C" if n in C else "S" if n in S else "M"

def entry_html(name, page, text, real):
    return (f'<p class="e{"" if real else " ph"}"><b>{name}</b> <span class="pg">{page}</span> {text}</p>')

CSS = """
.reg .live { top: 14mm; }
.reg h1 { font-family: "Cormorant Garamond", serif; font-weight: 600; font-size: 26pt; letter-spacing: .1em; margin: 0 0 2mm; text-transform: uppercase; }
.reg .intro { font-size: 9pt; line-height: 1.3; font-style: italic; margin: 0 0 4mm; columns: 1; }
.reg .cols { columns: 2; column-gap: 6mm; column-fill: auto; }
.reg .e { margin: 0 0 1.2mm; font-size: var(--fs); line-height: var(--lh); text-align: left; hyphens: auto; break-inside: avoid; }
.reg .e b { font-weight: 600; text-transform: uppercase; letter-spacing: .06em; font-size: .92em; }
.reg .e .pg { font-size: .85em; }
.reg .e c { font-variant: small-caps; letter-spacing: .03em; font-variant-caps: all-small-caps; }
.reg .e.ph { color: #8c8c8c; font-style: italic; }
.reg .runhead { position: absolute; top: 0; left: 0; }
.result { position: absolute; bottom: 3mm; left: 0; right: 0; text-align: center; font-size: 7pt; color: #8a1c1c; }
.spec h2 { font-family: "Cormorant Garamond", serif; font-weight: 600; font-size: 20pt; letter-spacing: .08em; text-transform: uppercase; margin: 0 0 1mm; }
.spec .sub { font-size: 9.5pt; font-style: italic; margin: 0 0 6mm; line-height: 1.35; }
.spec .item { display: grid; grid-template-columns: 26mm 1fr; column-gap: 5mm; padding: 2.6mm 0; border-top: .25pt solid #000; }
.spec .item:last-child { border-bottom: .25pt solid #000; }
.spec .thumb svg { width: 26mm; height: auto; display: block; }
.spec .entry { font-size: 10pt; line-height: 1.32; }
.spec .entry b { text-transform: uppercase; letter-spacing: .06em; font-weight: 600; font-size: .9em; }
.spec .entry c { font-variant-caps: all-small-caps; letter-spacing: .03em; }
.spec .why { font-size: 8pt; font-style: italic; margin-top: 1mm; color: #444; }
.spec .len { font-size: 7pt; color: #8a1c1c; }
.spec ol { font-size: 9pt; line-height: 1.35; margin: 0 0 5mm; padding-left: 5mm; }
"""

PAGINATE = """
<script>
document.fonts.ready.then(() => {
const fs = document.body.dataset.fs, lh = document.body.dataset.lh, limit = 4;
document.documentElement.style.setProperty('--fs', fs); document.documentElement.style.setProperty('--lh', lh);
const pool = [...document.querySelectorAll('#pool .e')];
const tpl = document.getElementById('tpl');
let pages = [];
function newPage(first) {
  const n = tpl.content.firstElementChild.cloneNode(true);
  if (!first) { n.querySelector('.intro-block').remove(); n.querySelector('.cols').style.marginTop = '7mm'; } else n.querySelector('.runhead').remove();
  document.getElementById('book').appendChild(n);
  const cols = n.querySelector('.cols');
  const live = n.querySelector('.live');
  const top = cols.getBoundingClientRect().top - live.getBoundingClientRect().top;
  cols.style.height = (live.getBoundingClientRect().height - top) + 'px';
  pages.push(n); return cols;
}
let cols = newPage(true);
for (const e of pool) {
  cols.appendChild(e);
  if (cols.scrollWidth > cols.clientWidth + 1) { cols.removeChild(e); cols = newPage(false); cols.appendChild(e); }
}
pages.forEach((p, i) => { p.querySelector('.folio').textContent = REG_START + i; });
const last = pages[pages.length - 1];
const r = document.createElement('div'); r.className = 'result';
r.textContent = `Density test at ${fs}/${lh}: ${pool.length} entries need ${pages.length} pages (target ${limit}). ` +
  (pages.length <= limit ? 'FITS.' : 'DOES NOT FIT.') + ' Grey = estimated-length placeholders.';
last.appendChild(r);
document.getElementById('pool').remove();
document.body.dataset.done = '1';
});
</script>"""

def density_html(spec, fs, lh, reg_start, folios, est=EST):
    texts = {e["country"]: e["text"] for e in spec["entries"]}
    names = sorted((n for v in CONTINENTS.values() for n in v), key=lambda s: s.replace("Côte", "Cote"))
    pool = []
    for n in names:
        if n in texts:
            pool.append(entry_html(n, folios[n], texts[n], True))
        else:
            pool.append(entry_html(n, folios[n], FILL[:est[cls(n)]].rsplit(" ", 1)[0] + ".", False))
    intro = ("How to use this register: find the country, then color the flag in the order given. "
             "Left and right are as you look at the page. Colors are in small capitals.")
    tpl = f'''<template id="tpl"><section class="page reg verso"><div class="live">
      <div class="runhead label">Color Register</div>
      <div class="intro-block"><h1>Color Register</h1><p class="intro">{intro}</p></div>
      <div class="cols"></div></div><div class="folio"></div></section></template>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Color register density test</title>
<link rel="stylesheet" href="../build/book.css"><style>{CSS}</style></head>
<body class="screen-gap" data-fs="{fs}" data-lh="{lh}">{tpl}<div id="book"></div><div id="pool" class="reg"><div class="cols">{"".join(pool)}</div></div>
<script>const REG_START = {reg_start};</script>{PAGINATE}</body></html>'''

def specimen_html(spec, folios):
    def flag(code):
        s = open(os.path.join(ROOT, f"assets/flags/outline/{code}.svg")).read()
        s = s[s.index("<svg"):]; s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
        head, rest = s.split(">", 1)
        return re.sub(r'\s(width|height)="[^"]*"', '', head) + ">" + rest
    codes = {"Japan": "jp", "Egypt": "eg", "United States": "us", "Brazil": "br", "Belize": "bz", "Nepal": "np",
             "Bhutan": "bt", "South Africa": "za", "Sri Lanka": "lk", "Saudi Arabia": "sa"}
    items = []
    for e in spec["entries"]:
        n = len(re.sub("<[^>]+>", "", e["text"]))
        items.append(f'''<div class="item"><div class="thumb">{flag(codes[e["country"]])}</div><div>
          <div class="entry"><b>{e["country"]}</b> &nbsp;{e["text"]}</div>
          <div class="why">Why this one: {e["why"]} <span class="len">({n} characters)</span></div></div></div>''')
    pattern = "".join(f"<li>{p}</li>" for p in spec["pattern"])
    half = 5
    pages = []
    for i, chunk in enumerate((items[:half], items[half:])):
        head = (f'''<h2>Color Register · ten specimen entries</h2>
          <p class="sub">For approval before the other 185 entries are written. Each entry follows the same pattern:</p><ol>{pattern}</ol>''' if i == 0 else "")
        pages.append(f'''<section class="page spec recto"><div class="proposal-tag">Phase 1 · for approval</div><div class="live">{head}{"".join(chunk)}</div><div class="folio">{i + 1}</div></section>''')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Color register specimens</title>
<link rel="stylesheet" href="../build/book.css"><style>{CSS}</style></head><body class="screen-gap">{"".join(pages)}</body></html>'''

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    spec = json.load(open(os.path.join(ROOT, "data/color-register-specimens.json")))
    rows = build_map()
    folios = {r[3]: r[0] for r in rows if r[2] == "country page"}
    reg_start = next(r[0] for r in rows if r[3].startswith("Color register"))
    open(os.path.join(OUT, "specimens.html"), "w").write(specimen_html(spec, folios))
    for fs, lh, tag in (("8.5pt", "10.4pt", "8.5pt"), ("9pt", "11pt", "9pt")):
        open(os.path.join(OUT, f"density-test-{tag}.html"), "w").write(density_html(spec, fs, lh, reg_start, folios))
    # same type size, placeholders cut to the proposed length budget per flag type
    open(os.path.join(OUT, "density-test-8.5pt-budget.html"), "w").write(
        density_html(spec, "8.5pt", "10.4pt", reg_start, folios, BUDGET))
    counts = {k: sum(1 for v in CONTINENTS.values() for n in v if cls(n) == k) for k in "SMC"}
    est = sum(EST[cls(n)] for v in CONTINENTS.values() for n in v)
    print("classes", counts, "estimated characters (placeholders only)", est)
