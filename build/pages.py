"""Build the six sample country pages (HTML -> PDF via build/render.mjs).

Inputs: data/samples.json, assets/maps, assets/flags/outline, assets/illustrations/vector.
Outputs (sample-pages/): country-pages.html (screen, paper simulation),
country-pages-print.html (white, as it would go to press), spread-preview.html.
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "sample-pages")

def svg_file(path):
    s = open(os.path.join(ROOT, path)).read()
    s = s[s.index("<svg"):]
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    # let CSS size it: drop fixed width/height on the root element only
    head, rest = s.split(">", 1)
    head = re.sub(r'\s(width|height)="[^"]*"', '', head)
    return head + ">" + rest

def viewbox_ratio(svg):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    return vb[2] / vb[3]

ICONS = {
 "pin": '<svg viewBox="0 0 10 13"><path d="M5 12.4C2.2 8.6 1 6.6 1 4.8a4 4 0 0 1 8 0c0 1.8-1.2 3.8-4 7.6z" fill="none" stroke="#000" stroke-width="1"/><circle cx="5" cy="4.8" r="1.5" fill="#000"/></svg>',
 "Capital": '<svg viewBox="0 0 10 10"><circle cx="5" cy="5" r="4.4" fill="none" stroke="#000" stroke-width=".7"/><path d="M5 2.2l.8 1.9 2 .1-1.6 1.3.6 2-1.8-1.1-1.8 1.1.6-2L2.2 4.2l2-.1z" fill="#000"/></svg>',
 "Population": '<svg viewBox="0 0 10 10"><circle cx="3.4" cy="3.2" r="1.5" fill="none" stroke="#000" stroke-width=".7"/><circle cx="6.8" cy="3.6" r="1.3" fill="none" stroke="#000" stroke-width=".7"/><path d="M.8 9c0-2.2 1.2-3.4 2.6-3.4S6 6.8 6 9M5.6 6.2c.4-.4.8-.6 1.2-.6 1.3 0 2.4 1.1 2.4 3.2" fill="none" stroke="#000" stroke-width=".7"/></svg>',
 "Language": '<svg viewBox="0 0 10 10"><path d="M1 1.6h8v5.2H4.2L2 8.8V6.8H1z" fill="none" stroke="#000" stroke-width=".7" stroke-linejoin="round"/><path d="M2.8 3.4h4.4M2.8 5h3" stroke="#000" stroke-width=".6"/></svg>',
 "Area": '<svg viewBox="0 0 10 10"><rect x="1.6" y="1.6" width="6.8" height="6.8" fill="none" stroke="#000" stroke-width=".7"/><path d="M.6 3V.6H3M7 .6h2.4V3M9.4 7v2.4H7M3 9.4H.6V7" fill="none" stroke="#000" stroke-width=".5"/></svg>',
 "Currency": '<svg viewBox="0 0 10 10"><circle cx="5" cy="5" r="4.4" fill="none" stroke="#000" stroke-width=".7"/><circle cx="5" cy="5" r="3.1" fill="none" stroke="#000" stroke-width=".4"/></svg>',
 "camera": '<svg viewBox="0 0 14 12"><path d="M1 3.4h3l1.2-2h3.6l1.2 2h3v7.6H1z" fill="none" stroke="#000" stroke-width=".7" stroke-linejoin="round"/><circle cx="7" cy="7" r="2.4" fill="none" stroke="#000" stroke-width=".7"/></svg>',
}
PLANE = 'M-3.2 .6l2-.1 1.8 2.6h.9l-.9-2.7 2.4-.1.8 1h.7l-.4-1.4.4-1.4h-.7l-.8 1-2.4-.1.9-2.7h-.9l-1.8 2.6-2-.1c-.5 0-.5 1.4 0 1.4z'
STAMP = f'''<svg class="stamp" viewBox="-10 -10 20 20"><defs><path id="arc" d="M-6.1 0a6.1 6.1 0 0 1 12.2 0"/></defs>
<circle r="9.4" fill="none" stroke="#000" stroke-width=".35"/><circle r="8.6" fill="none" stroke="#000" stroke-width=".18"/>
<circle r="4.3" fill="none" stroke="#000" stroke-width=".18"/>
<text font-family="EB Garamond" font-size="2.1" letter-spacing=".7" text-anchor="middle"><textPath href="#arc" startOffset="50%">VISITED</textPath></text>
<path d="{PLANE}" fill="none" stroke="#000" stroke-width=".3" stroke-linejoin="round" transform="rotate(-30) scale(.9)"/></svg>'''

FLAG_BOX = (72.0, 48.0)

def page_html(c, side, register_page, tag=True):
    flag = svg_file(f"assets/flags/outline/{c['flag']}.svg")
    r = viewbox_ratio(flag)
    fw, fh = (FLAG_BOX[0], FLAG_BOX[0] / r) if FLAG_BOX[0] / r <= FLAG_BOX[1] else (FLAG_BOX[1] * r, FLAG_BOX[1])
    dots_top = 44.5 + fh + 4.5
    dots = "".join(f'<div class="dot"><i></i><span>{n}</span></div>' for n in c["flag_colors"])
    loc = c["local"]
    if loc["script"] == "formal":
        local = f'<span class="formal">{loc["text"]}</span>'
    else:
        dir_ = ' dir="rtl"' if loc["script"] == "ar" else ""
        lang = {"jp": ' lang="ja"', "ar": ' lang="ar"'}.get(loc["script"], "")
        local = f'<span class="native {loc["script"]}"{lang}{dir_}>{loc["text"]}</span>'
        if loc["translit"]:
            local += f'<span class="translit">{loc["translit"]}</span>'
    facts = "".join(
        f'<div class="fact">{ICONS[k]}<span class="k">{k}</span><span class="v{" long" if len(v) > 26 else ""}">{v}</span></div>'
        for k, v in c["facts"].items())
    notes = "".join(f"<p>{n}</p>" for n in c["notes"])
    return f'''
<section class="page {side}" id="{c['id']}">
  {'<div class="proposal-tag">Phase 1 sample · for approval</div>' if tag else ''}
  <div class="live">
    <div class="abs label continent">{ICONS['pin']}{c['continent']}</div>
    <div class="abs country-name">{c['name']}</div>
    <div class="abs local">{local}</div>
    <div class="abs head-rule"></div>

    <div class="abs label flag-label">Color the flag</div>
    <div class="abs flag" style="width:{fw:.2f}mm;height:{fh:.2f}mm">{flag}</div>
    <div class="abs dots" style="top:{dots_top:.2f}mm">{dots}</div>
    <div class="abs register-ref" style="top:{dots_top + 12.5:.2f}mm">Which part takes which color: see A Register of Colors, page {register_page}.</div>

    <div class="abs facts">{facts}</div>
    <div class="abs notes">{notes}</div>

    <div class="abs map">{svg_file(f"assets/maps/map-{c['id'].lower()}.svg")}</div>
    <div class="abs plate"><div class="inner">{svg_file(f"assets/illustrations/vector/{c['illustration']}.svg")}</div></div>
    <div class="abs caption">{'<br>'.join(x if x.endswith('.') else x + '.' for x in c['caption'].split('. '))}</div>

    <div class="abs photo"><div class="tape"></div><div class="inside">{ICONS['camera']}<span class="label">Tape your photo here</span></div><div class="size">Takes a 9 × 13 cm print cut in half, or an instant mini print</div></div>
    <div class="abs visit"><div class="inner">
      <h4>My Visit</h4>
      <div class="row">Date I visited:<span class="line short"></span>/<span class="line short"></span>/<span class="line year"></span></div>
      <div class="row">Note:<span class="line"></span></div>
      <div class="row"><span class="line" style="margin-right:22mm"></span></div>
      <div class="row"><span class="line" style="margin-right:22mm"></span></div>
      {STAMP}
    </div></div>
  </div>
  <div class="folio">{c['page']}</div>
</section>'''

def doc(body, extra_css="", print_mode=False, title="THE WORLD sample pages"):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="../build/book.css"><style>{extra_css}</style></head>
<body class="{'print' if print_mode else 'screen-gap'}">{body}</body></html>'''

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    data = json.load(open(os.path.join(ROOT, "data/samples.json")))
    order = ["ITA", "JPN", "USA", "BRA", "EGY", "AUS"]
    cs = {c["id"]: c for c in data["countries"]}
    side = lambda c: "recto" if c["page"] % 2 else "verso"
    pages = "".join(page_html(cs[i], side(cs[i]), data["register_page"]) for i in order)
    open(os.path.join(OUT, "country-pages.html"), "w").write(doc(pages))
    pages_p = "".join(page_html(cs[i], side(cs[i]), data["register_page"], tag=False) for i in order)
    open(os.path.join(OUT, "country-pages-print.html"), "w").write(doc(pages_p, print_mode=True))
    # Facing-page preview: in the provisional map Egypt is p.29 (recto); show p.28 placeholder? Instead
    # pair two real samples as they would face each other: USA (206, verso) beside a recto page.
    # We pair Japan (92, verso) with Italy rendered as a recto to judge the gutter on both sides.
    left = page_html(cs["JPN"], "verso", data["register_page"], tag=False)
    right_c = dict(cs["ITA"]); right_c["page"] = cs["JPN"]["page"] + 1
    right = page_html(right_c, "recto", data["register_page"], tag=False)
    spread_css = """@page { size: 420mm 297mm; margin: 0; }
      .spread { width: 420mm; height: 297mm; display: flex; position: relative; }
      .spread .page { margin: 0; }
      .gutter { position: absolute; left: 210mm; top: 0; height: 297mm; width: 0; border-left: .3pt dashed #8a1c1c; }
      .gutter-zone { position: absolute; top: 0; height: 297mm; width: 8mm; left: 202mm;
                     background: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.10) 50%, rgba(0,0,0,0) 100%); }
      .spread-note { position: absolute; bottom: 2.5mm; left: 0; right: 0; text-align: center; font-size: 7pt; color: #8a1c1c; }"""
    spread = f'''<div class="spread">{left}{right}<div class="gutter-zone"></div><div class="gutter"></div>
      <div class="spread-note">Facing-page preview only: shaded band = approx. 4 mm each side lost in a sewn case binding (to confirm on the printer's blank dummy). The rule stays one country per page; the right-hand page is Italy used as a stand-in for the country that follows Japan.</div></div>'''
    open(os.path.join(OUT, "spread-preview.html"), "w").write(doc(spread, spread_css))
    print("ok")
