"""Compose the complete interior (288 pages) of THE WORLD: Countries & Flags.

Every page follows the page map in build/pagemap.py. Output: book/html/part-XX.html chunks,
rendered by build/render_book.py into book/THE-WORLD-interior.pdf.
"""
import json, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "build"), os.path.join(ROOT, "data")]
from pagemap import build as build_map, CONTINENTS
from countries_master import COUNTRIES, FORMAL, AREA, POP_OVERRIDE
from book_text import CONTINENT, BUCKET, CARIBBEAN_NOTE, COLOR_NOTE, PROFILE_FIELDS, BEST_THINGS, TOP_FIVE, LEDGER
from pages import ICONS, STAMP
OUT = os.path.join(ROOT, "book", "html")
BASE = json.load(open(os.path.join(ROOT, "data/base-mledoze.json")))
MAPNOTES = json.load(open(os.path.join(ROOT, "data/map-notes.json")))
POP = json.load(open(os.path.join(ROOT, "data/population-2025.json")))
ROWS = build_map()
PAGE_OF = {r[3]: r[0] for r in ROWS if r[2] == "country page"}
REGISTER_PAGE = next(r[0] for r in ROWS if r[3].startswith("A Register of Colors"))
K = 0.3861021585
ILL = {"Italy": "italy-colosseum", "Japan": "japan-fuji-chureito", "United States": "usa-statue-of-liberty",
       "Brazil": "brazil-sugarloaf", "Egypt": "egypt-giza", "Australia": "australia-opera-house"}
MANUAL_MAPS = {"Italy": "ita", "Japan": "jpn", "United States": "usa", "Brazil": "bra", "Egypt": "egy", "Australia": "aus"}

def slug(n):
    return ILL.get(n) or re.sub(r"[^a-z0-9]+", "-", n.lower().replace("ô", "o").replace("é", "e").replace("ü", "u")).strip("-")

def svg_file(path, keep_size=False):
    s = open(os.path.join(ROOT, path)).read()
    s = s[s.index("<svg"):]
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    if keep_size:
        return s
    head, rest = s.split(">", 1)
    return re.sub(r'\s(width|height)="[^"]*"', "", head) + ">" + rest

def ratio(svg):
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    return vb[2] / vb[3]

def esc(t):
    return html.escape(t, quote=False)

# ------------------------------------------------------------------ formatting
def fmt_pop(n):
    if n in POP_OVERRIDE:
        return POP_OVERRIDE[n]
    v = POP[n]
    if v >= 1e6:
        return f"{v / 1e6:.1f} million"
    if v >= 1e4:
        return f"{round(v / 1000) * 1000:,}"
    return f"{round(v / 100) * 100:,}"

def fmt_area(n):
    a = AREA.get(n, BASE[n]["area"])
    m = a * K
    if a < 1:
        return f"{a:.2f} km² ({m:.2f} sq mi)"
    if a < 100:
        return f"{a:.0f} km² ({m:.0f} sq mi)" if a >= 10 else f"{a:.1f} km² ({m:.1f} sq mi)"
    return f"{round(a):,} km² ({round(m):,} sq mi)"

def colors(reg):
    seen, out = set(), []
    for c in re.findall(r"\{([^}]+)\}", reg):
        k = c.lower()
        if k not in seen:
            seen.add(k); out.append(k)
    return out

def reg_html(reg):
    return re.sub(r"\{([^}]+)\}", lambda m: f'<span class="sc">{esc(m.group(1).lower())}</span>', esc(reg).replace("&#x27;", "'"))

def script_class(n, text):
    if n == "Japan": return "jp"
    if n == "China": return "sc"
    if n in ("South Korea", "North Korea"): return "kr"
    return "native-fonts" if any(ord(ch) > 0x24F and not 0x1E00 <= ord(ch) <= 0x1EFF for ch in text) else ""

# ------------------------------------------------------------------ page shells
def sheet(n, body, folio=True, cls=""):
    side = "recto" if n % 2 else "verso"
    f = f'<div class="folio">{n}</div>' if folio else ""
    return f'<section class="sheet"><div class="page {side} {cls}" data-page="{n}"><div class="live">{body}</div>{f}</div></section>'

def lines(k, h=8.5):
    return "".join(f'<div style="height:{h}mm;border-bottom:.25pt solid #000"></div>' for _ in range(k))

def title_block(kicker, title, sub=None, center=False):
    al = "center" if center else "left"
    return (f'<div style="text-align:{al}"><div class="kicker">{kicker}</div>' if kicker else f'<div style="text-align:{al}">') + \
           f'<h1 class="pagetitle" style="margin-top:2mm">{title}</h1>' + (f'<p class="pagesub">{sub}</p>' if sub else "") + "</div>"

COMPASS = svg_file("assets/cover/compass-rose.svg")

def sized(svg, w, h=None):
    h = h or w
    return svg.replace("<svg ", f'<svg width="{w}mm" height="{h}mm" ', 1).replace('class="stamp"', "")


# ------------------------------------------------------------------ country page
MISSING = []
def illus(name):
    p = f"assets/illustrations/vector/{slug(name)}.svg"
    if not os.path.exists(os.path.join(ROOT, p)):
        MISSING.append(name); return ""
    return svg_file(p)

def country_page(n, name):
    c = COUNTRIES[name]
    b = BASE[name]
    flag = svg_file(f"assets/flags/outline/{b['cca2']}.svg")
    r = ratio(flag)
    fw, fh = (72.0, 72.0 / r) if 72.0 / r <= 48 else (48 * r, 48.0)
    dots_top = 44.5 + fh + 4.5
    dots = "".join(f'<div class="dot"><i></i><span>{esc(col)}</span></div>' for col in colors(c["register"]))
    if c["local"]:
        cls = script_class(name, c["local"])
        native = f'<span class="native {"script " + cls if cls else ""}">{esc(c["local"])}</span>'
        if c["translit"]:
            native += f'<span class="translit">{esc(c["translit"])}</span>'
    else:
        native = f'<span class="formal">{esc(FORMAL.get(name, name))}</span>'
    facts = {"Capital": c["capital"], "Population": fmt_pop(name), "Language": c["language"],
             "Area": fmt_area(name), "Currency": c["currency"]}
    fact_html = "".join(
        f'<div class="fact">{ICONS[k]}<span class="k">{k}</span><span class="v{" long" if len(v) > 26 else ""}">{esc(v)}</span></div>'
        for k, v in facts.items())
    notes = list(c["notes"])
    if name in MAPNOTES and MAPNOTES[name] not in notes:
        notes.append(MAPNOTES[name])
    if name == "Bulgaria":
        pass
    notes_html = "".join(f"<p>{esc(x)}</p>" for x in notes)
    mapf = f"assets/maps/map-{MANUAL_MAPS.get(name, b['cca3'].lower())}.svg"
    subj = c["subject"]
    if "national bird" in subj:
        first, second = subj.rsplit(". ", 1)
        caption = f"{esc(first)}.<br>{esc(second)}."
    else:
        caption = esc(subj) + "."
    cont = next(k for k, v in CONTINENTS.items() if name in v)
    body = f'''
    <div class="abs label continent">{ICONS['pin']}{esc(cont)}</div>
    <div class="abs country-name fit">{esc(name)}</div>
    <div class="abs local">{native}</div>
    <div class="abs head-rule"></div>
    <div class="abs label flag-label">Color the flag</div>
    <div class="abs flag" style="width:{fw:.2f}mm;height:{fh:.2f}mm">{flag}</div>
    <div class="abs dots" style="top:{dots_top:.2f}mm">{dots}</div>
    <div class="abs register-ref" style="top:{dots_top + 13:.2f}mm">Which part takes which color: see A Register of Colors, page {REGISTER_PAGE}.</div>
    <div class="abs leftcol"><div class="facts">{fact_html}</div><div class="notes">{notes_html}</div></div>
    <div class="abs map">{svg_file(mapf)}</div>
    <div class="abs plate"><div class="inner">{illus(name)}</div></div>
    <div class="abs caption">{caption}</div>
    <div class="abs photo"><div class="tape"></div><div class="inside">{ICONS['camera']}<span class="label">Tape your photo here</span></div><div class="size">Takes a 9 × 13 cm print cut in half, or an instant mini print</div></div>
    <div class="abs visit"><div class="inner"><h4>My Visit</h4>
      <div class="row">Date I visited:<span class="line short"></span>/<span class="line short"></span>/<span class="line year"></span></div>
      <div class="row">Note:<span class="line"></span></div>
      <div class="row"><span class="line" style="margin-right:22mm"></span></div>
      <div class="row"><span class="line" style="margin-right:22mm"></span></div>
      {STAMP}</div></div>'''
    return sheet(n, body)

# ------------------------------------------------------------------ front matter
def half_title(n):
    return sheet(n, '<div style="position:absolute;top:62mm;width:100%;text-align:center"><div class="display" style="font-size:30pt;letter-spacing:.22em">The World</div>'
                    '<div style="font-family:Cormorant Garamond;font-weight:500;font-size:15pt;letter-spacing:.2em;margin-top:5mm">COUNTRIES &amp; FLAGS</div></div>', folio=False)

def frontispiece(n):
    w = svg_file("assets/maps/world-ghost.svg")
    return (f'<section class="sheet"><div class="page verso" data-page="{n}" style="overflow:visible">'
            f'<div style="position:absolute;left:-3mm;top:-3mm;width:216mm;height:303mm;display:flex;align-items:center;justify-content:center;overflow:hidden">'
            f'<div style="flex:none;width:690mm;color:#ececec">{w}</div></div>'
            f'<div class="kicker" style="position:absolute;bottom:18mm;width:100%;text-align:center;letter-spacing:.3em">Explore. Color. Remember.</div></div></section>')

def title_page(n):
    return sheet(n, f'''<div style="position:absolute;top:40mm;width:100%;text-align:center">
      <div class="display" style="font-size:40pt;letter-spacing:.08em">The World</div>
      <div class="display" style="font-size:19pt;letter-spacing:.16em;margin-top:5mm">Countries &amp; Flags</div>
      <div class="ornament" style="margin:9mm 0"><i></i></div>
      <div style="font-style:italic;font-size:15pt">A Coloring Journal for the Places You’ve Visited</div>
      <div style="width:30mm;margin:22mm auto 0">{COMPASS}</div></div>
      <div style="position:absolute;bottom:18mm;width:100%;text-align:center" class="kicker">[Imprint] · [City]</div>''', folio=False)

def copyright_page(n):
    t = """<p>First published in 2026 by [Imprint Name], [City].</p>
<p>Text copyright © 2026 [Author]. Illustrations copyright © 2026 [Illustrator]. Design and compilation copyright © 2026 [Imprint Name].</p>
<p>The moral right of the author and illustrator has been asserted.</p>
<p>All rights reserved. No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without the prior written permission of the publisher.</p>
<p>The maps, outlines and flags in this book are drawn to be colored. They are not intended for navigational, official or diplomatic use. Borders follow United Nations practice. Where a dispute affects a country’s figures, a short note in small type on that page explains it. The publisher takes no position on territories under dispute.</p>
<p>All figures refer to 2025. Population figures are United Nations estimates for 1 July 2025, rounded: United Nations, Department of Economic and Social Affairs, Population Division, <i>World Population Prospects 2024</i>, licensed under CC BY 3.0 IGO. Areas are official national figures or compiled from the open dataset mledoze/countries (ODbL). Map outlines are drawn from Natural Earth (public domain); flag outlines follow the official constructions published on Wikimedia Commons (public domain).</p>
<p>A catalogue record for this book is available from the [national library].</p>
<p>ISBN [000-0-00000-000-0]</p>
<p>Printed and bound in [country]. Printed on FSC-certified 100 gsm cream uncoated paper, chosen for its response to pencil.</p>
<p>First edition<br>10 9 8 7 6 5 4 3 2 1</p>"""
    return sheet(n, f'<div style="position:absolute;bottom:6mm;width:120mm;font-size:7.6pt;line-height:1.45">{t}</div>', folio=False)

def ownership(n):
    rows = "".join(f'<div class="fieldrow" style="height:14mm">{lab}<span class="line"></span></div>' for lab in ["Name", "Home"])
    return sheet(n, f'''<div style="position:absolute;top:30mm;left:18mm;right:18mm;border:.5pt solid #000;padding:1.4mm">
      <div style="border:.25pt solid #000;padding:16mm 14mm 14mm">
      <div class="center"><div class="display" style="font-size:16pt;letter-spacing:.2em">This Journal Belongs To</div>
      <div class="ornament" style="margin:7mm 0 10mm"><i></i></div></div>
      {rows}
      <div class="fieldrow" style="height:14mm">Begun on the<span class="line" style="flex:none;width:14mm"></span>day of<span class="line"></span>, 20<span class="line" style="flex:none;width:10mm"></span></div>
      <div class="fieldrow" style="height:14mm">in<span class="line"></span></div>
      <p style="font-style:italic;font-size:9.5pt;text-align:center;margin:16mm 0 2mm">Should this journal be found far from its owner,<br>the finder is kindly asked to return it to the address above.</p>
      <div style="width:24mm;margin:10mm 0 0 auto">{sized(STAMP, 24)}</div></div></div>''', folio=False)

def epigraph(n):
    return sheet(n, '<div style="position:absolute;top:58mm;left:18mm;right:18mm;text-align:center;font-family:Cormorant Garamond;font-style:italic;font-size:17pt;line-height:1.45">'
                    'A map shows the world as it is.<br>What follows is the world as you found it.</div>', folio=False)

def contents(n, part):
    def row(t, p, indent=0, strong=False):
        st = "font-family:Cormorant Garamond;font-weight:600;font-size:12pt;letter-spacing:.12em;text-transform:uppercase" if strong else "font-size:10.5pt"
        return (f'<div style="display:flex;align-items:baseline;gap:2mm;margin:{2.6 if strong else 1.1}mm 0 0 {indent}mm;{st}">'
                f'<span>{t}</span><span style="flex:1;border-bottom:.4pt dotted #000;transform:translateY(-1mm)"></span><span>{p}</span></div>')
    pg = lambda key: next(r[0] for r in ROWS if r[3].startswith(key))
    if part == 1:
        items = [row("Part I · Front Matter", 1, strong=True), row("Before You Set Out", 9, 6), row("How to Use This Journal", 13, 6),
                 row("A Note on Color, Paper and Pencils", 15, 6),
                 row("Part II · Before You Begin", 17, strong=True), row("The Traveler’s Profile", 18, 6), row("The Symbols of This Book", 19, 6),
                 row("Where in the World?", 20, 6), row("Countries I’ve Visited", 21, 6), row("The Journeys Already Made", 22, 6),
                 row("The World in Six Parts", 24, 6), row("Departure", 27, 6),
                 row("Part III · The Countries", 28, strong=True)]
        for cont in CONTINENTS:
            items.append(row(cont, pg(f"{cont} opener"), 6))
        body = title_block("", "Contents") + '<div style="margin-top:12mm">' + "".join(items) + "</div>"
    else:
        items = [row("Part IV · After the Journey", pg("Part title: After the Journey"), strong=True)]
        for t, k in [("The Traveler’s Ledger", "The Traveler's Ledger"), ("My Top Five", "My Top Five"), ("The Best Things", "The Best Things"),
                     ("People Met Along the Way", "People Met"), ("Words Worth Keeping", "Words Worth Keeping"), ("Favorite Memory", "Favorite Memory"),
                     ("Where I Go Next", "Where I Go Next"), ("A Register of Colors", "A Register of Colors"), ("Index of Countries", "Index of Countries"),
                     ("Notes", "Notes"), ("Colophon", "Colophon")]:
            items.append(row(t, pg(k), 6))
        body = '<div style="margin-top:28mm">' + "".join(items) + "</div>"
    return sheet(n, body)

ESSAY = [
 ("""There is a kind of memory that resists photography. It belongs to the half hour when the light changed over an unfamiliar street, or to the taste of something you could not name and never found again, or to the particular quality of being lost somewhere that did not frighten you. Photographs multiply. These do not. They need somewhere to be kept.""",
  """That is the reason for this book."""),
 ("""It began with an ordinary observation: most of us travel a great deal more than we remember. A passport fills with stamps, a phone fills with images, and within a few years a decade of journeys has compressed itself into five or six anecdotes told at dinner. At the same time, the world stays oddly unfamiliar. One hundred and ninety-five countries, each with a flag, a border, a language, and a name for itself, and most of us could sketch perhaps twenty of them. This journal was made to slow both of those things down. It gives your travels a place to settle, and it gives the world back some of its detail.""",
  """Inside you will find one page for every country on earth. Each one carries the same things: the country’s name in English and in its own language, its outline, its flag drawn as an open line, a short register of facts, a drawing of what the country is best known for, and, at the foot of the page, two spaces that belong entirely to you. There is no correct order in which to approach them, and no obligation to approach them all. Some readers will color a country the week they return from it. Others will sit down on a winter evening and fill in twenty years of travel at once, which is a very good way to spend an evening."""),
 ("""<i>On coloring.</i> The flags are printed as outlines. Beneath each one, a row of small circles names its colors in the order they appear, and at the back of the book A Register of Colors explains, in plain words, which part takes which color. Colored pencil suits this paper best. It is uncoated and slightly warm, and it takes graphite and pencil beautifully, though it will not forgive a marker pen, which is likely to strike through to the country behind. Work lightly at first and build up. And do not be too careful. A flag colored slightly imperfectly, on an airplane, with the wrong shade of blue because it was the only blue in the tin, will mean far more in fifteen years than one colored to specification.""",
  """<i>On recording.</i> The lower half of each page asks for two things. One is a photograph, printed small and taped in place. The other, headed My Visit, asks only for a date and a few lines. Resist the impulse to summarize the trip. A single specific detail will outlast a paragraph of description: the name of a street, the price of a coffee, a misunderstanding at a ticket window, the weather on the morning you arrived. Write it in the first days after you come home, while the detail is still sharp and before you have decided what the journey meant."""),
 ("""<i>On the other pages.</i> Beyond the countries, the book keeps a second set of records. Near the front there is a map of the world to color as you go and a running list of every country you have visited. Each continent closes with fifteen experiences worth the journey, a page to mark what you achieved there, and room for the notes that belong to no single country, which is where the long train journeys and the difficult borders tend to end up. And at the back there is a ledger: your totals, your top fives, your best meal, the strangers whose names you never learned, the words you brought home from other languages, one favorite memory, and the places you mean to go next.""",
  """<i>On making it yours.</i> Nothing in this book is precious. Tape a boarding pass over a map. Glue in a ticket, a receipt, a pressed leaf, a label steamed off a bottle. Correct the facts if they have changed, and they will. Write in the margins. The most valuable copies of a journal like this one are always the ones that have been used badly: thickened at the spine, dog-eared, over-full, annotated in three different pens by a person who was in a hurry.""",
  """And then there is what happens later. For the first few years this will be a record, something you add to and check against. After that it quietly changes function. You will open it looking for one thing and find a country you had almost forgotten, with a date in your own handwriting and four lines about a bus, and the whole afternoon will come back with a clarity you had no right to expect. That is the part of this book that cannot be designed. It only arrives with time, and it arrives in proportion to what you put in.""",
  """The world is large and none of us will see all of it. That is not a reason to be modest about the attempt.""",
  """<span style="font-family:Cormorant Garamond;font-style:italic;font-size:14pt">Begin anywhere.</span>"""),
]

def essay(n, i):
    paras = ESSAY[i - 1]
    ps = "".join(f'<p class="{"flush" if j == 0 else ""}">{p}</p>' for j, p in enumerate(paras))
    if i == 1:
        head = ('<div style="margin:36mm 0 16mm;text-align:center"><div class="display" style="font-size:26pt;letter-spacing:.14em">Before You Set Out</div>'
                '<div style="font-style:italic;font-size:12pt;margin-top:4mm">On the making of this journal, and the several ways to fill it</div>'
                '<div class="ornament" style="margin-top:8mm"><i></i></div></div>')
        body = head + f'<div class="prose" style="margin:0 12mm;font-size:11.5pt">{ps}</div>'
    else:
        body = f'<div class="prose" style="margin:10mm 12mm 0;font-size:11.5pt">{ps}</div>'
    return sheet(n, body)

def howto(n, i):
    if i == 1:
        spec = country_page(n, "Italy")
        inner = re.search(r'<div class="page[^"]*"[^>]*>(.*)</div></section>$', spec, flags=re.S).group(1)
        marks = [(1, 2, 2), (2, 2, 9), (3, 4, 22), (4, 2, 46), (5, 2, 102), (6, 2, 128), (7, 128, 46), (8, 128, 150), (9, 128, 192),
                 (10, 25, 218), (11, 160, 218), (12, 190, 262)]
        m = "".join(f'<div style="position:absolute;left:{x}mm;top:{y}mm;width:6.4mm;height:6.4mm;border-radius:50%;background:#000;color:#fff;'
                    f'font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center;transform:scale(1.25)">{k}</div>' for k, x, y in marks)
        body = (title_block("", "How to Use This Journal") +
                f'<div style="position:absolute;top:22mm;left:12mm;width:151.2mm;height:213.8mm;border:.5pt solid #000;overflow:hidden">'
                f'<div style="zoom:.72;position:relative;width:210mm;height:297mm"><div class="page recto" style="position:relative">{inner}</div>{m}</div></div>')
        return sheet(n, body)
    items = [("The continent", "Where the country sits in this book, and the section it belongs to."),
             ("The name", "In English, then in the country’s own language and script, with a transliteration in italics where the script is not Latin."),
             ("Color the flag", "Every flag is drawn at its official proportions, as an open outline for you to color."),
             ("The color circles", "The flag’s colors, in the order they appear. Color the circles first and use them as your key; A Register of Colors at the back explains which part takes which color."),
             ("Five facts", "Capital, population, language, area and currency, all for 2025. Areas are given in square kilometers and square miles."),
             ("Notes", "Short facts in small type: disputed borders, capitals with a story, islands too small to show."),
             ("The map", "The country’s outline with its capital. Every country is drawn at the same visual size, not to the same scale, so that each one can be colored."),
             ("The drawing", "A landmark the country is known for, drawn to be colored, with a one-line caption."),
             ("Your photograph", "Tape in a small print: half a 9 × 13 cm photo, or an instant mini print."),
             ("My Visit", "The date and a few lines. One sharp detail is worth more than a summary."),
             ("The stamp", "Color it in when the country is claimed."),
             ("The page number", "Every country is also listed in the Index at the back, with a box to tick.")]
    lst = "".join(f'<div style="display:grid;grid-template-columns:9mm 1fr;margin-bottom:5.2mm"><div style="width:6.4mm;height:6.4mm;border-radius:50%;background:#000;color:#fff;font-size:9pt;font-weight:600;display:flex;align-items:center;justify-content:center">{k}</div>'
                  f'<div><div class="label" style="margin:.8mm 0 1.4mm">{t}</div><div style="font-size:10pt;line-height:1.38">{d}</div></div></div>' for k, (t, d) in enumerate(items, 1))
    return sheet(n, f'<div style="margin-top:18mm">{lst}</div>')

def color_note(n):
    ps = "".join(f"<p class='flush'>{p}</p>" for p in COLOR_NOTE.split("\n\n"))
    return sheet(n, title_block("", "A Note on Color, Paper and Pencils") + f'<div class="prose" style="margin-top:12mm;font-size:11pt;text-align:left">{ps}</div>')

def blank(n):
    return sheet(n, "", folio=False)

def part_title(n, numeral, title, line):
    return sheet(n, f'''<div style="position:absolute;top:70mm;width:100%;text-align:center">
      <div style="width:26mm;margin:0 auto 12mm">{COMPASS}</div>
      <div class="kicker">Part {numeral}</div>
      <div class="display" style="font-size:30pt;letter-spacing:.16em;margin-top:5mm">{title}</div>
      <div class="ornament" style="margin:8mm 0"><i></i></div>
      <div style="font-style:italic;font-size:12pt">{line}</div></div>''', folio=False)

def profile(n):
    rows = "".join(f'<div class="fieldrow" style="height:13.5mm">{f}<span class="line"></span></div>' + (lines(1, 9.5) if i >= 5 else "")
                   for i, f in enumerate(PROFILE_FIELDS))
    return sheet(n, title_block("", "The Traveler’s Profile", "A record of the person holding this book") + f'<div style="margin-top:10mm">{rows}</div>')

def symbols(n):
    ic = [("Capital", "The capital city, also marked on the map with a ringed dot."), ("Population", "People living in the country in 2025 (United Nations estimate)."),
          ("Language", "The main or official languages."), ("Area", "Total area in square kilometers, with square miles in parentheses."),
          ("Currency", "The currency in use, with its international code.")]
    rows = "".join(f'<div style="display:grid;grid-template-columns:14mm 1fr;align-items:center;padding:4mm 0;border-bottom:.25pt solid #000">'
                   f'<div style="width:8mm">{sized(ICONS[k], 8)}</div><div><div class="label">{k}</div><div style="font-size:10pt;margin-top:1.4mm">{d}</div></div></div>' for k, d in ic)
    extra = (f'<div style="display:grid;grid-template-columns:14mm 1fr;align-items:center;padding:4mm 0;border-bottom:.25pt solid #000">'
             f'<div style="display:flex;gap:1mm"><i style="width:4.6mm;height:4.6mm;border:.6pt solid #000;border-radius:50%;display:block"></i></div>'
             f'<div><div class="label">Color circles</div><div style="font-size:10pt;margin-top:1.4mm">The colors of the flag, in the order they appear. Color them first and use them as your key.</div></div></div>'
             f'<div style="display:grid;grid-template-columns:14mm 1fr;align-items:center;padding:4mm 0;border-bottom:.25pt solid #000">'
             f'<div style="width:11mm">{sized(STAMP, 11)}</div>'
             f'<div><div class="label">Visited</div><div style="font-size:10pt;margin-top:1.4mm">Color the stamp when you have been there.</div></div></div>'
             f'<div style="display:grid;grid-template-columns:14mm 1fr;align-items:center;padding:4mm 0;border-bottom:.25pt solid #000">'
             f'<div style="font-size:12pt;padding-left:2mm">*</div><div><div class="label">Notes</div><div style="font-size:10pt;margin-top:1.4mm">A short fact in small type, below the register: a disputed border, a capital with a story, islands too small to show.</div></div></div>')
    return sheet(n, title_block("", "The Symbols of This Book") + f'<div style="margin-top:12mm;border-top:.25pt solid #000">{rows}{extra}</div>')

def world_color(n):
    w = svg_file("assets/maps/world-color.svg")
    return sheet(n, f'''<div style="position:absolute;left:-45.5mm;top:45.5mm;width:267mm;height:176mm;transform:rotate(-90deg);">
      <div style="display:flex;justify-content:space-between;align-items:baseline"><div class="display" style="font-size:22pt">Where in the World?</div>
      <div style="font-style:italic;font-size:11pt">Color each country when you have been there</div></div>
      <div style="margin-top:8mm;color:#000">{w}</div></div>''')

def visited_list(n):
    cols = []
    for c in range(4):
        items = "".join(f'<div style="display:flex;align-items:flex-end;gap:1.4mm;height:4.95mm;font-size:6.4pt"><span style="width:4.6mm;text-align:right">{i}</span><span class="box" style="width:2.6mm;height:2.6mm;margin-bottom:.6mm"></span><span class="line" style="flex:1;margin-bottom:.6mm"></span></div>'
                        for i in range(c * 49 + 1, min(c * 49 + 50, 196)))
        cols.append(f"<div>{items}</div>")
    return sheet(n, title_block("", "Countries I’ve Visited", "In the order you reach them") +
                 f'<div style="margin-top:6mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm">{"".join(cols)}</div>')

def journeys(n, i):
    rows = "".join("<tr><td></td><td></td><td></td><td></td></tr>" for _ in range(20))
    head = title_block("", "The Journeys Already Made", "For the travels that happened before this book") if i == 1 else '<div style="height:20mm"></div>'
    return sheet(n, head + f'<table class="journal" style="margin-top:10mm"><tr><th style="width:16mm">Year</th><th style="width:44mm">Place</th><th style="width:36mm">With</th><th>One line</th></tr>{rows}</table>')

def six_parts(n, i):
    pg = lambda key: next(r[0] for r in ROWS if r[3].startswith(key))
    if i == 1:
        m = svg_file("assets/maps/world-six-parts.svg")
        txt = ("This book divides the world into six parts, following the regions used by the United Nations, with the Americas split into "
               "North America and the Caribbean, and South America. A few countries sit on two continents; the book places them where the "
               "United Nations does. Russia appears in Europe. Türkiye, Cyprus, Georgia, Armenia, Azerbaijan and Kazakhstan appear in Asia. "
               "Mexico, Central America and the island nations of the Caribbean appear with North America. The Holy See and the State of "
               "Palestine, which hold permanent observer status at the United Nations, complete the 195.")
        return sheet(n, title_block("", "The World in Six Parts") + f'<div style="margin-top:10mm">{m}</div><p style="font-size:10.4pt;line-height:1.5;margin-top:10mm;text-align:justify">{txt}</p>')
    rows = ""
    for k, (cont, names) in enumerate(CONTINENTS.items(), 1):
        popsum = sum(POP[x] for x in names)
        first = pg(f"{cont} opener"); last = max(r[0] for r in ROWS if r[4] == cont)
        rows += (f'<tr><td style="font-family:Cormorant Garamond;font-weight:600;font-size:14pt">{k}</td><td style="font-size:11pt">{cont}</td>'
                 f'<td style="text-align:right">{len(names)}</td><td style="text-align:right">{popsum / 1e6:,.0f} million</td><td style="text-align:right">{first}–{last}</td></tr>')
    tot = sum(POP[x] for v in CONTINENTS.values() for x in v)
    rows += f'<tr><td></td><td style="font-size:11pt"><i>The world</i></td><td style="text-align:right">195</td><td style="text-align:right">{tot / 1e9:.2f} billion</td><td></td></tr>'
    return sheet(n, f'''<div style="margin-top:30mm"><table class="journal six"><tr><th></th><th>Part</th><th style="text-align:right">Countries</th><th style="text-align:right">People, 2025</th><th style="text-align:right">Pages</th></tr>{rows}</table>
      <p style="font-size:8pt;font-style:italic;margin-top:4mm">Population totals add up the United Nations estimates for the countries in each part; they do not include dependent territories.</p></div>
      <style>.six td{{height:13mm;font-size:10pt;padding-right:3mm}}</style>''')

def departure(n):
    return sheet(n, f'''<div style="position:absolute;top:84mm;width:100%;text-align:center">
      <div style="width:22mm;margin:0 auto 16mm">{COMPASS}</div>
      <div style="font-family:Cormorant Garamond;font-style:italic;font-size:17pt">It is not down in any map; true places never are.</div>
      <div class="kicker" style="margin-top:6mm">Herman Melville, <i style="text-transform:none;letter-spacing:.04em">Moby-Dick</i>, 1851</div></div>''', folio=False)

# ------------------------------------------------------------------ continents
def cslug(cont):
    return re.sub("[^a-z]+", "-", cont.lower()).strip("-")

def opener_essay(n, cont):
    names = CONTINENTS[cont]
    popsum = sum(POP[x] for x in names)
    t = CONTINENT[cont]
    return sheet(n, f'''<div style="margin:30mm 10mm 0">
      <div class="kicker">{len(names)} countries · {popsum / 1e6:,.0f} million people (2025)</div>
      <div class="display" style="font-size:24pt;margin-top:4mm">{cont}</div>
      <div class="ornament" style="justify-content:flex-start;margin:7mm 0 9mm"><i></i></div>
      <div class="prose" style="font-size:11.5pt">{"".join(f"<p class='flush'>{p}</p>" for p in t["essay"].split(chr(10)+chr(10)))}</div></div>''')

def opener_plate(n, cont):
    t = CONTINENT[cont]
    m = svg_file(f"assets/maps/continent-{cslug(cont)}.svg")
    fs = 34 if len(cont) < 14 else 22
    return sheet(n, f'''<div style="position:absolute;inset:-4mm -6mm -6mm -6mm;border:.5pt solid #000"></div>
      <div style="position:absolute;inset:-2.6mm -4.6mm -4.6mm -4.6mm;border:.25pt solid #000"></div>
      <div style="position:absolute;top:10mm;width:100%;text-align:center">
      <div style="width:20mm;margin:0 auto 8mm">{COMPASS}</div>
      <div class="display" style="font-size:{fs}pt;letter-spacing:.18em">{cont}</div>
      <div style="font-family:Cormorant Garamond;font-style:italic;font-size:15pt;margin-top:4mm">{t["deck"]}</div>
      <div class="ornament" style="margin:7mm 0 6mm"><i></i></div>
      <div style="width:150mm;margin:0 auto">{m}</div>
      <div style="font-style:italic;font-size:11.5pt;margin-top:10mm">{t["invitation"]}</div></div>''', folio=False)

def caribbean_note(n):
    return sheet(n, title_block("North America & the Caribbean", "Islands That Are Not Countries") +
                 f'<p class="prose" style="margin-top:9mm">{CARIBBEAN_NOTE}</p>'
                 f'<div class="label" style="margin-top:8mm">Territories I have visited</div><div style="margin-top:2mm">{lines(11)}</div>')

def bucket(n, cont, i):
    items = BUCKET[cont]
    chunk = items[:8] if i == 1 else items[8:]
    start = 1 if i == 1 else 9
    rows = "".join(f'''<div style="display:grid;grid-template-columns:8mm 1fr;padding:3.4mm 0 2.6mm;border-bottom:.25pt solid #000">
        <span class="box" style="width:4mm;height:4mm;margin-top:.6mm"></span>
        <div><div style="font-size:11pt"><span style="font-family:Cormorant Garamond;font-weight:600">{k}.</span> {esc(t)} <i style="font-size:9pt">· {esc(w)}</i></div>
        <div class="fieldrow" style="height:8mm;font-size:8.5pt">Done on<span class="line" style="flex:none;width:26mm"></span>with<span class="line"></span></div></div></div>'''
                   for k, (t, w) in enumerate(chunk, start))
    head = title_block(cont, "Bucket List", "Fifteen experiences worth the journey") if i == 1 else '<div style="height:24mm"></div>'
    return sheet(n, head + f'<div style="margin-top:7mm;border-top:.25pt solid #000">{rows}</div>')

def notes_continent(n, cont):
    prompts = ["The border crossings", "The long journeys between places", "The things that belonged to no single country"]
    blocks = "".join(f'<div class="label" style="margin-top:7mm">{p}</div><div style="margin-top:1mm">{lines(6)}</div>' for p in prompts)
    return sheet(n, title_block(cont, "Notes from the Continent") + blocks)

def achievement(n, cont):
    names = CONTINENTS[cont]
    per = (len(names) + 2) // 3
    cols = "".join("<div>" + "".join(f'<div style="display:flex;gap:1.6mm;align-items:center;height:{min(5.2, 92 / per):.2f}mm;font-size:7.6pt"><span class="box" style="width:2.6mm;height:2.6mm"></span>{esc(x)}</div>'
                                     for x in names[c * per:(c + 1) * per]) + "</div>" for c in range(3))
    seal = f'''<svg viewBox="-20 -20 40 40" style="width:34mm;height:34mm"><defs><path id="sa-{cslug(cont)}" d="M-13.5 0a13.5 13.5 0 0 1 27 0"/><path id="sb-{cslug(cont)}" d="M-15.6 0a15.6 15.6 0 0 0 31.2 0"/></defs>
      <circle r="19" fill="none" stroke="#000" stroke-width=".5"/><circle r="17.6" fill="none" stroke="#000" stroke-width=".25"/><circle r="10.6" fill="none" stroke="#000" stroke-width=".35"/>
      <text font-family="Cormorant Garamond" font-weight="600" font-size="3.4" letter-spacing=".6" text-anchor="middle"><textPath href="#sa-{cslug(cont)}" startOffset="50%">{cont.upper().replace("&", "&amp;") if len(cont) < 16 else "N. AMERICA &amp; CARIBBEAN"}</textPath></text>
      <text font-family="Cormorant Garamond" font-weight="600" font-size="3.2" letter-spacing="1" text-anchor="middle"><textPath href="#sb-{cslug(cont)}" startOffset="50%">COMPLETED</textPath></text>
      <path d="M0 -7l2 4.6 5 .4-3.8 3.3 1.2 4.9L0 2.6l-4.4 2.6 1.2-4.9L-7 -3l5-.4z" fill="none" stroke="#000" stroke-width=".35" stroke-linejoin="round"/></svg>'''
    return sheet(n, title_block(cont, "Achievement") +
                 f'''<div style="display:flex;align-items:center;gap:6mm;margin-top:8mm"><div style="flex:1">
                 <div class="fieldrow" style="font-size:12pt;height:12mm">I have visited<span class="line" style="flex:none;width:16mm"></span>of the {len(names)} countries of {cont}.</div>
                 <div class="fieldrow">Continent completed on<span class="line"></span></div></div>{seal}</div>
                 <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:3mm;margin-top:7mm;padding-top:4mm;border-top:.25pt solid #000">{cols}</div>
                 <div class="label" style="margin-top:7mm">A memory worth keeping</div><div style="margin-top:1mm">{lines(4)}</div>''')

# ------------------------------------------------------------------ after the journey
def ledger(n, i):
    if i <= 2:
        items = LEDGER[:9] if i == 1 else LEDGER[9:]
        rows = "".join(f'<div class="fieldrow" style="height:22mm;font-size:11pt">{t}<span class="line"></span></div>' for t in items)
        head = title_block("", "The Traveler’s Ledger", "The numbers, filled in by hand") if i == 1 else '<div style="height:22mm"></div>'
        return sheet(n, head + f'<div style="margin-top:6mm">{rows}</div>')
    rows = "".join("<tr><td></td><td></td><td></td><td></td><td></td></tr>" for _ in range(21))
    head = title_block("", "Year by Year", "Trips, countries and the year's best moment") if i == 3 else '<div style="height:20mm"></div>'
    return sheet(n, head + f'<table class="journal" style="margin-top:10mm"><tr><th style="width:16mm">Year</th><th style="width:16mm">Trips</th><th style="width:22mm">Countries</th><th style="width:24mm">New ones</th><th>Best moment</th></tr>{rows}</table>')

def topfive(n, i):
    cats = TOP_FIVE[:6] if i == 1 else TOP_FIVE[6:]
    boxes = "".join(f'<div><div class="label" style="margin-bottom:1.5mm">{c}</div>' +
                    "".join(f'<div style="display:flex;align-items:flex-end;gap:2mm;height:7.4mm;font-size:9pt"><span style="font-family:Cormorant Garamond;font-weight:600">{k}</span><span class="line" style="flex:1;margin-bottom:1mm"></span></div>' for k in range(1, 6)) +
                    "</div>" for c in cats)
    head = title_block("", "My Top Five") if i == 1 else '<div style="height:14mm"></div>'
    return sheet(n, head + f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12mm 10mm;margin-top:12mm">{boxes}</div>')

def best(n, i):
    items = BEST_THINGS[:5] if i == 1 else BEST_THINGS[5:]
    blocks = "".join(f'<div class="label" style="margin-top:7mm">{t}</div><div>{lines(4)}</div>' for t in items)
    head = title_block("", "The Best Things", "The memories people actually retell") if i == 1 else ""
    return sheet(n, head + blocks)

def people(n, i):
    rows = "".join("<tr><td></td><td></td><td></td></tr>" for _ in range(20))
    head = title_block("", "People Met Along the Way", "For the people whose surnames were never learned") if i == 1 else '<div style="height:20mm"></div>'
    return sheet(n, head + f'<table class="journal" style="margin-top:10mm"><tr><th style="width:42mm">Name</th><th style="width:40mm">Where</th><th>One line</th></tr>{rows}</table>')

def words(n, i):
    rows = "".join("<tr><td></td><td></td><td></td><td></td></tr>" for _ in range(20))
    head = title_block("", "Words Worth Keeping", "Phrases picked up in other languages") if i == 1 else '<div style="height:20mm"></div>'
    return sheet(n, head + f'<table class="journal" style="margin-top:10mm"><tr><th style="width:36mm">The word</th><th style="width:30mm">Language</th><th style="width:50mm">What it means</th><th>Where I heard it</th></tr>{rows}</table>')

def memory(n, i):
    if i == 1:
        return sheet(n, title_block("", "Favorite Memory") + f'''<div style="position:absolute;top:34mm;left:0;right:0;bottom:6mm;border:.5pt solid #000;padding:1.4mm">
          <div style="height:100%;border:.25pt solid #000;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3mm">
          <div style="width:9mm">{sized(ICONS["camera"], 9, 8)}</div><span class="label">A photograph, a ticket, a drawing</span></div></div>''')
    return sheet(n, f'''<div style="margin-top:20mm"><div class="fieldrow">Where<span class="line"></span></div><div class="fieldrow">When<span class="line"></span></div>
      <div class="fieldrow">With<span class="line"></span></div><div class="label" style="margin-top:9mm">The moment</div>{lines(18)}</div>''')

def next_list(n):
    rows = "".join(f'<div style="display:grid;grid-template-columns:8mm 1fr 1fr;gap:4mm;align-items:end;height:10.6mm"><span style="font-family:Cormorant Garamond;font-weight:600;font-size:11pt">{k}</span><span class="line"></span><span class="line"></span></div>' for k in range(1, 21))
    return sheet(n, title_block("", "Where I Go Next", "My own list, written when I know what I want") +
                 f'<div style="display:grid;grid-template-columns:8mm 1fr 1fr;gap:4mm;margin-top:10mm"><span></span><span class="label">The place</span><span class="label">Why</span></div>{rows}')

def next_plan(n):
    f = ["The destination", "When", "With whom", "What this journey is for"]
    rows = "".join(f'<div class="fieldrow" style="height:16mm;font-size:11pt">{t}<span class="line"></span></div>' for t in f)
    three = "".join(f'<div style="display:flex;align-items:flex-end;gap:3mm;height:12mm"><span class="box" style="width:4mm;height:4mm;margin-bottom:1mm"></span><span class="line" style="flex:1;margin-bottom:1mm"></span></div>' for _ in range(3))
    return sheet(n, f'''<div style="position:absolute;top:18mm;left:6mm;right:6mm;border:.5pt solid #000;padding:1.4mm"><div style="border:.25pt solid #000;padding:12mm 12mm 14mm">
      <div class="center"><div class="kicker">Where I Go Next</div><div class="display" style="font-size:20pt;margin-top:3mm">The Next Journey</div><div class="ornament" style="margin:6mm 0 4mm"><i></i></div></div>
      {rows}<div class="label" style="margin-top:9mm">Three things to arrange</div>{three}
      <div class="label" style="margin-top:9mm">The first thing I will do when I arrive</div>{lines(2, 10)}</div></div>''')

def index_pages(n, i):
    allc = sorted(PAGE_OF, key=lambda s: s.replace("Côte", "Cote").replace("Türk", "Turk"))
    chunk = allc[(i - 1) * 49:i * 49]
    half = (len(chunk) + 1) // 2
    def col(cs):
        return "".join(f'<div style="display:flex;align-items:center;gap:2mm;height:9.6mm;border-bottom:.25pt solid #000;font-size:9.4pt"><span class="box"></span><span style="flex:1">{esc(c)}</span><span>{PAGE_OF[c]}</span></div>' for c in cs)
    head = title_block("", "Index of Countries", "Tick each one as you go") if i == 1 else '<div style="height:20mm"></div>'
    top = 6 if i == 1 else 0
    return sheet(n, head + f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10mm;margin-top:{top}mm"><div>{col(chunk[:half])}</div><div>{col(chunk[half:])}</div></div>')

def notes_page(n):
    return sheet(n, '<div class="label" style="margin-top:6mm">Notes</div>' + f'<div style="margin-top:2mm">{lines(29)}</div>')

def colophon(n):
    t = """<p>This book was designed and typeset by ElitePublishing.</p>
<p>The display type is Cormorant Garamond, designed by Christian Thalmann. The text type is EB Garamond, designed by Georg Duffner and Octavio Pardo after the types of Claude Garamont. Names in their own scripts are set in the Noto Serif family. All are published under the SIL Open Font License.</p>
<p>Maps are drawn from Natural Earth. Population figures are from the United Nations World Population Prospects 2024.</p>
<p>Illustrations: [Illustrator].</p>
<p>Printed on FSC-certified 100 gsm cream uncoated paper, thread-sewn and case-bound in cloth, by [printer], [country].</p>
<p>First edition, 2026.</p>"""
    return sheet(n, f'<div style="position:absolute;bottom:40mm;left:20mm;right:20mm;text-align:center;font-size:9pt;line-height:1.6;font-style:italic">'
                    f'<div style="width:14mm;margin:0 auto 8mm;font-style:normal">{COMPASS}</div>{t}</div>', folio=False)

# ------------------------------------------------------------------ dispatch
def render_row(r):
    n, side, kind, t, cont = r[0], r[1], r[2], r[3], r[4]
    m = re.search(r"\((\d)/\d\)", t); i = int(m.group(1)) if m else 1
    if kind == "country page": return country_page(n, t)
    if t == "Half-title": return half_title(n)
    if t.startswith("Frontispiece"): return frontispiece(n)
    if t == "Title page": return title_page(n)
    if t.startswith("Copyright"): return copyright_page(n)
    if t.startswith("This Journal"): return ownership(n)
    if t.startswith("Epigraph"): return epigraph(n)
    if t.startswith("Contents"): return contents(n, i)
    if t.startswith("Before You Set Out"): return essay(n, i)
    if t.startswith("How to Use"): return howto(n, i)
    if t.startswith("A Note on Color"): return color_note(n)
    if t == "Blank": return blank(n)
    if t.startswith("Part title: Before"): return part_title(n, "II", "Before You Begin", "Everything you can fill in tonight, before you go anywhere new.")
    if t.startswith("Part title: After"): return part_title(n, "IV", "After the Journey", "Where the travels become a body of work.")
    if t.startswith("The Traveler's Profile"): return profile(n)
    if t.startswith("The Symbols"): return symbols(n)
    if t.startswith("Where in the World"): return world_color(n)
    if t.startswith("Countries I've Visited"): return visited_list(n)
    if t.startswith("The Journeys Already Made"): return journeys(n, i)
    if t.startswith("The World in Six Parts"): return six_parts(n, i)
    if t.startswith("Departure"): return departure(n)
    if "opener: essay" in t: return opener_essay(n, cont)
    if "opener: title plate" in t: return opener_plate(n, cont)
    if t.startswith("Note on the dependencies"): return caribbean_note(n)
    if "bucket list" in t: return bucket(n, cont, i)
    if "Notes from the Continent" in t: return notes_continent(n, cont)
    if "achievement page" in t: return achievement(n, cont)
    if t.startswith("The Traveler's Ledger"): return ledger(n, i)
    if t.startswith("My Top Five"): return topfive(n, i)
    if t.startswith("The Best Things"): return best(n, i)
    if t.startswith("People Met"): return people(n, i)
    if t.startswith("Words Worth Keeping"): return words(n, i)
    if t.startswith("Favorite Memory"): return memory(n, i)
    if t.startswith("Where I Go Next: the reader"): return next_list(n)
    if t.startswith("Where I Go Next: planning"): return next_plan(n)
    if t.startswith("Index of Countries"): return index_pages(n, i)
    if t.startswith("Notes (flexible)"): return notes_page(n)
    if t == "Colophon": return colophon(n)
    if t.startswith("A Register of Colors"): return None
    raise ValueError(t)

FIT_JS = """<script>
Promise.all([...document.fonts].map(f => f.load().catch(() => null))).then(() => document.fonts.ready).then(() => {
  document.querySelectorAll('.country-name.fit').forEach(el => {
    let s = 46;
    while (el.scrollWidth > el.clientWidth + 1 && s > 31) { s -= 1; el.style.fontSize = s + 'pt'; }
    if (el.scrollWidth > el.clientWidth + 1) { el.classList.add('two'); el.style.fontSize = '30pt';
      el.parentNode.querySelector('.local').classList.add('low'); }
  });
  document.body.dataset.done = '1';
});</script>"""

def register_html():
    entries = "".join(f'<p class="e"><b>{esc(n)}</b> <span class="pg">{PAGE_OF[n]}</span> {reg_html(COUNTRIES[n]["register"])}</p>'
                      for n in sorted(PAGE_OF, key=lambda s: s.replace("Côte", "Cote").replace("Türk", "Turk")))
    intro = ("Find the country, then color the flag in the order given. Left and right are as you look at the page; colors are in small capitals. "
             "Shades vary between official versions of a flag, so choose the pencil that looks right to you.")
    sheets = ""
    for k in range(4):
        n = REGISTER_PAGE + k
        side = "recto" if n % 2 else "verso"
        head = (f'<div class="kicker">After the Journey</div><h1 class="pagetitle" style="margin-top:2mm">A Register of Colors</h1><p class="intro">{intro}</p>'
                if k == 0 else '<div class="label runhead">A Register of Colors</div>')
        sheets += (f'<section class="sheet"><div class="page {side}" data-page="{n}"><div class="live">{head}<div class="cols">'
                   f'<div class="col" id="c{2 * k}"></div><div class="col" id="c{2 * k + 1}"></div></div></div><div class="folio">{n}</div></div></section>')
    css = """.intro{font-size:8.6pt;line-height:1.35;font-style:italic;margin:2mm 0 4mm}.runhead{margin-bottom:5mm}
      .cols{display:grid;grid-template-columns:1fr 1fr;column-gap:6mm}.col{overflow:hidden}
      .e{margin:0 0 .7mm;font-size:8.5pt;line-height:10.1pt;break-inside:avoid;hyphens:auto}
      .e b{font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:.92em}.e .pg{font-size:.85em}
      .sc{font-variant-caps:all-small-caps;letter-spacing:.03em}"""
    js = """<script>Promise.all([...document.fonts].map(f=>f.load().catch(()=>null))).then(()=>document.fonts.ready).then(()=>{const pool=[...document.querySelectorAll('#pool .e')];
      const cols=[...Array(8).keys()].map(i=>document.getElementById('c'+i));
      for(const c of cols){const live=c.closest('.live');c.style.height=(live.getBoundingClientRect().bottom-c.getBoundingClientRect().top)+'px';}
      let k=0;
      for(const e of pool){cols[k].appendChild(e);
        if(cols[k].scrollHeight>cols[k].clientHeight+0.5){cols[k].removeChild(e);k++;
          if(k>7){document.body.dataset.overflow='1';break;}cols[k].appendChild(e);}}
      document.getElementById('pool').remove();document.body.dataset.done='1';});</script>"""
    return doc(sheets + f'<div id="pool" style="width:85mm">{entries}</div>', css, js)

def doc(body, css="", js=FIT_JS):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><link rel="stylesheet" href="../../build/print.css">'
            f'<style>{css}</style></head><body>{body}{js}</body></html>')

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
    chunks, cur, start = [], [], 1
    for r in ROWS:
        h = render_row(r)
        if h is None:
            if "(1/4)" not in r[3]:
                continue
            if cur:
                chunks.append((start, cur)); cur = []
            chunks.append((r[0], "REGISTER"))
            start = r[0] + 4
            continue
        if not cur:
            start = r[0]
        cur.append(h)
        if len(cur) == 24:
            chunks.append((start, cur)); cur = []
    if cur:
        chunks.append((start, cur))
    done = set()
    for k, (s, c) in enumerate(chunks):
        if c == "REGISTER":
            if s in done: continue
            done.add(s)
            open(os.path.join(OUT, f"part-{k:02d}-p{s:03d}.html"), "w").write(register_html())
        else:
            open(os.path.join(OUT, f"part-{k:02d}-p{s:03d}.html"), "w").write(doc("".join(c)))
    print(len(chunks), "chunks; missing illustrations:", sorted(set(MISSING)))
