"""Phase 1 style guide (client-facing, American English) + cover direction.
Writes style-guide/style-guide.html (render to PDF with build/render.mjs)."""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "style-guide")

def inline(path, keep_size=False):
    s = open(os.path.join(ROOT, path)).read()
    s = s[s.index("<svg"):]
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    if not keep_size:
        head, rest = s.split(">", 1)
        s = re.sub(r'\s(width|height)="[^"]*"', '', head) + ">" + rest
    return s

NAVY, GOLD, BEIGE, GREY, PINK = "#1f2a44", "#b8975a", "#efe6d4", "#3b3b3b", "#c7a2a0"

CSS = f"""
.sg .live {{ font-size: 9.5pt; line-height: 1.38; }}
.sg h1 {{ font-family: "Cormorant Garamond", serif; font-weight: 600; font-size: 30pt; letter-spacing: .08em; text-transform: uppercase; margin: 0 0 1mm; line-height: 1.05; }}
.sg h2 {{ font-family: "Cormorant Garamond", serif; font-weight: 600; font-size: 17pt; letter-spacing: .1em; text-transform: uppercase; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: .5pt solid #000; }}
.sg h3 {{ font-size: 7.5pt; letter-spacing: .16em; text-transform: uppercase; font-weight: 600; margin: 5mm 0 1.5mm; }}
.sg p {{ margin: 0 0 2.2mm; }}
.sg .kicker {{ font-size: 7.5pt; letter-spacing: .2em; text-transform: uppercase; margin-bottom: 3mm; }}
.sg .lede {{ font-style: italic; font-size: 11pt; line-height: 1.4; margin-bottom: 6mm; }}
.sg table {{ width: 100%; border-collapse: collapse; font-size: 8.5pt; line-height: 1.3; margin: 1mm 0 3mm; }}
.sg th {{ text-align: left; font-size: 6.8pt; letter-spacing: .12em; text-transform: uppercase; font-weight: 600; border-bottom: .5pt solid #000; padding: 1.2mm 2mm 1.2mm 0; }}
.sg td {{ border-bottom: .25pt solid #000; padding: 1.4mm 2mm 1.4mm 0; vertical-align: top; }}
.sg .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; }}
.sg .note {{ font-size: 8pt; font-style: italic; }}
.sg .tag {{ display: inline-block; font-size: 6.5pt; letter-spacing: .14em; text-transform: uppercase; border: .4pt solid #8a1c1c; color: #8a1c1c; padding: .3mm 1.2mm; margin-left: 1.5mm; vertical-align: middle; }}
.sg .swatches {{ display: flex; gap: 4mm; margin: 2mm 0 3mm; }}
.sg .sw {{ width: 30mm; }}
.sg .sw i {{ display: block; height: 18mm; border: .25pt solid #000; }}
.sg .sw span {{ display: block; font-size: 7.5pt; margin-top: 1mm; line-height: 1.25; }}
.sg .mini {{ width: 60mm; height: 84.86mm; position: relative; background: var(--paper); border: .3pt solid #000; overflow: hidden; }}
.sg .mini > div {{ position: absolute; border: .3pt dashed #8a1c1c; font-size: 5pt; color: #8a1c1c; display: flex; align-items: center; justify-content: center; text-align: center; }}
.sg .weights div {{ display: grid; grid-template-columns: 62mm 1fr; align-items: center; margin: 1.2mm 0; font-size: 8.5pt; }}
.sg .weights .ln {{ display: block; border-top-style: solid; border-color: #000; }}
.sg .dotsdemo {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; margin: 2mm 0 2mm; }}
.sg .dotsdemo > div {{ border: .25pt solid #000; padding: 3mm; font-size: 7.5pt; line-height: 1.3; }}
.sg .dotsdemo .row {{ display: flex; gap: 2.4mm; margin: 2mm 0; }}
.sg .dotsdemo .d {{ display: flex; flex-direction: column; align-items: center; gap: .8mm; font-size: 5.4pt; letter-spacing: .08em; text-transform: uppercase; }}
.sg .dotsdemo .d i {{ width: 5.2mm; height: 5.2mm; border-radius: 50%; border: .6pt solid #000; display: block; }}
.sg .typespec div {{ border-bottom: .25pt solid #000; padding: 1.6mm 0; display: grid; grid-template-columns: 38mm 1fr; align-items: baseline; }}
.sg .typespec small {{ font-size: 7pt; line-height: 1.25; }}
.cover {{ width: 150mm; height: 212mm; position: relative; color: {GOLD}; margin: 0 auto;
  background: {NAVY};
  background-image: repeating-linear-gradient(0deg, rgba(255,255,255,.035) 0 .25mm, transparent .25mm .6mm),
                    repeating-linear-gradient(90deg, rgba(0,0,0,.08) 0 .25mm, transparent .25mm .55mm);
  box-shadow: 0 1.5mm 4mm rgba(0,0,0,.35); border-radius: .6mm 1.6mm 1.6mm .6mm; text-align: center; overflow: hidden; }}
.cover .rose {{ position: absolute; top: 12mm; left: 50%; width: 24mm; margin-left: -12mm; }}
.cover .t1 {{ position: absolute; top: 40mm; left: 0; right: 0; font-family: "Cormorant Garamond", serif; font-weight: 600; font-size: 39pt; letter-spacing: .06em; line-height: 1; }}
.cover .t2 {{ position: absolute; top: 57mm; left: 0; right: 0; font-family: "Cormorant Garamond", serif; font-weight: 600; font-size: 19pt; letter-spacing: .1em; }}
.cover .t3 {{ position: absolute; top: 75mm; left: 0; right: 0; font-family: "EB Garamond", serif; font-size: 10pt; letter-spacing: .2em; }}
.cover .t4 {{ position: absolute; top: 81mm; left: 0; right: 0; font-family: "EB Garamond", serif; font-style: italic; font-size: 11pt; }}
.cover .rule {{ position: absolute; top: 70mm; left: 50%; width: 30mm; margin-left: -15mm; border-top: .4pt solid currentColor; }}
.cover .world {{ position: absolute; top: 97mm; left: 12mm; width: 126mm; }}
.cover .world svg {{ width: 100%; height: auto; }}
.cover .motto {{ position: absolute; bottom: 24mm; left: 0; right: 0; font-family: "EB Garamond", serif; font-size: 9pt; letter-spacing: .3em; }}
.cover .trail {{ position: absolute; bottom: 9mm; left: 40mm; width: 70mm; height: 12mm; }}
.covers {{ display: grid; grid-template-columns: 120mm 48mm; gap: 8mm; align-items: start; }}
.coverwrap {{ width: 120mm; height: 169.6mm; overflow: hidden; }} .coverwrap .cover {{ transform: scale(.8); transform-origin: top left; margin: 0; }}
.thumbcover {{ transform: scale(.32); transform-origin: top left; width: 150mm; height: 212mm; }} .thumbcover .cover {{ margin: 0; box-shadow: none; }}
.thumbwrap {{ width: 48mm; height: 67.84mm; overflow: hidden; margin-bottom: 4mm; }}
"""

def page(n, body, side="recto"):
    return f'<section class="page sg {side}"><div class="proposal-tag">Phase 1 style guide · for approval</div><div class="live">{body}</div><div class="folio">{n}</div></section>'

def cover(bg=NAVY, fg=GOLD):
    trail = ('<svg class="trail" viewBox="0 0 70 12"><path d="M2 9 C 18 13, 30 2, 52 6" fill="none" stroke="currentColor" stroke-width=".35" stroke-dasharray="1 1.4"/>'
             '<path d="M56.6 6.4l2-.1 1.8 2.6h.9l-.9-2.7 2.4-.1.8 1h.7l-.4-1.4.4-1.4h-.7l-.8 1-2.4-.1.9-2.7h-.9l-1.8 2.6-2-.1c-.5 0-.5 1.4 0 1.4z" fill="currentColor"/></svg>')
    return f'''<div class="cover" style="background-color:{bg};color:{fg}">
      <div class="rose">{inline("assets/cover/compass-rose.svg")}</div>
      <div class="t1">THE WORLD</div><div class="t2">COUNTRIES &amp; FLAGS</div><div class="rule"></div>
      <div class="t3">A COLORING JOURNAL</div><div class="t4">for the Places You’ve Visited</div>
      <div class="world">{inline("assets/cover/world-foil.svg")}</div>
      <div class="motto">EXPLORE. COLOR. REMEMBER.</div>{trail}</div>'''

def build():
    flag_it = inline("assets/flags/outline/it.svg")
    p = []
    p.append(page(1, f'''
      <div class="kicker">ElitePublishing · The World: Countries &amp; Flags</div>
      <h1>Style Guide</h1>
      <p class="lede">Phase 1: planning and visual direction. Everything here is a proposal for your review. Nothing in this guide is a print-ready file, and the production values that depend on the printer (spine, board, cloth, foil, final margins) are marked provisional.</p>
      <h2>1 · Principles</h2>
      <p><b>An atlas first, a coloring book second.</b> The page should look finished before a single pencil touches it: generous white space, classical type, one consistent line.</p>
      <p><b>Built for coloring.</b> Every drawing is closed line art with no shading or grey, areas large enough for a colored pencil, and controlled detail. The interior prints in one color, black, on cream uncoated paper; all color comes from the reader.</p>
      <p><b>One system, 195 times.</b> Every country page uses the same frames in the same places. Variation comes only from the content: flag proportions, map shapes, the length of a name or a caption. The six sample pages were chosen to stress-test exactly that.</p>
      <p><b>Facts that hold.</b> One reference year (2025), one source per field for all 195 countries, United Nations treatment of borders, and short factual notes where a dispute affects a figure.</p>
      <h2>2 · What this guide covers</h2>
      <table><tr><th>Section</th><th>Status</th></tr>
      <tr><td>3 Typography and licenses</td><td>Proposed</td></tr>
      <tr><td>4 Page grid and margins</td><td>Proposed; margins provisional until the printer's blank dummy</td></tr>
      <tr><td>5 Line weights</td><td>Proposed; to confirm on the press proof on the actual stock</td></tr>
      <tr><td>6 Flags and the color dots</td><td>Proposal requiring your decision (black-only interior)</td></tr>
      <tr><td>7 Maps</td><td>Proposed</td></tr>
      <tr><td>8 Illustrations and captions</td><td>Proposed</td></tr>
      <tr><td>9 The five facts and the name line</td><td>Applies settled decisions; formats proposed</td></tr>
      <tr><td>10 Palette and cover direction</td><td>Direction only, not a production cover</td></tr></table>'''))

    p.append(page(2, f'''
      <h2>3 · Typography</h2>
      <p>Two classical families, both under the SIL Open Font License 1.1: free for commercial print, embedding permitted, no per-copy fee. The license files travel with the source package and the fonts install directly in InDesign.</p>
      <table><tr><th>Family</th><th>Use</th><th>License</th></tr>
      <tr><td><b>Cormorant Garamond</b> (Christian Thalmann)</td><td>Display: country names, section titles, cover</td><td>SIL OFL 1.1</td></tr>
      <tr><td><b>EB Garamond</b> (Georg Duffner, Octavio Pardo)</td><td>Text, facts, labels, captions, register</td><td>SIL OFL 1.1</td></tr>
      <tr><td><b>Noto Serif JP / CJK, Noto Naskh Arabic</b> and other Noto Serif scripts</td><td>Country names in their own script</td><td>SIL OFL 1.1</td></tr></table>
      <h3>Hierarchy (country page)</h3>
      <div class="typespec">
        <div><small>Country name<br>Cormorant Garamond SemiBold, 46 pt, caps, +20 tracking</small><span style="font-family:'Cormorant Garamond';font-weight:600;font-size:30pt;letter-spacing:.02em">ITALY</span></div>
        <div><small>Name in own language<br>EB Garamond Italic 17 pt; scripts 17–19 pt; transliteration italic 13 pt</small><span style="font-style:italic;font-size:17pt">Italia &nbsp;<span style="font-family:'Noto Serif JP';font-style:normal">日本</span> <span style="font-size:13pt">Nippon</span></span></div>
        <div><small>Labels<br>EB Garamond Medium 7 pt, caps, +160 tracking</small><span class="label">Color the flag · Capital · My visit</span></div>
        <div><small>Fact values<br>EB Garamond 10 pt (9 pt when longer than 26 characters)</small><span style="font-size:10pt">302,068 km² (116,629 sq mi)</span></div>
        <div><small>Caption<br>EB Garamond Italic 9 pt, centered, one sentence per line</small><span style="font-style:italic;font-size:9pt">The Statue of Liberty, New York Harbor.<br>The bald eagle is the national bird.</span></div>
        <div><small>Notes<br>EB Garamond Italic 7 pt, asterisk</small><span style="font-style:italic;font-size:7pt">* Alaska and Hawaii are shown at different scales.</span></div>
        <div><small>A Register of Colors<br>EB Garamond 8.5/10.4 pt, colors in small caps</small><span style="font-size:8.5pt"><b style="letter-spacing:.06em">JAPAN</b> A <span style="font-variant-caps:all-small-caps">white</span> flag with one <span style="font-variant-caps:all-small-caps">red</span> circle in the exact middle.</span></div>
      </div>
      <p class="note">Minimum size anywhere in the interior: 7 pt, except the 5.6 pt color names under the flag dots (all caps, tracked). These are the first thing to check on the press proof.</p>'''))

    mini = '''<div class="mini">
        <div style="left:6.86mm;top:4mm;width:50.29mm;height:10mm">name + own-language name</div>
        <div style="left:6.86mm;top:15.4mm;width:20.6mm;height:21.5mm">flag 72 × 48 max<br>+ dots</div>
        <div style="left:29.7mm;top:15.4mm;width:27.4mm;height:21.7mm">map 96 × 76</div>
        <div style="left:6.86mm;top:37.7mm;width:20.6mm;height:14.3mm">five facts</div>
        <div style="left:29.7mm;top:38.3mm;width:27.4mm;height:18.9mm">illustration plate 96 × 66</div>
        <div style="left:6.86mm;top:53.4mm;width:20.6mm;height:6mm">notes</div>
        <div style="left:6.86mm;top:62mm;width:25.7mm;height:18.3mm">photo 90 × 64</div>
        <div style="left:34.6mm;top:62mm;width:22.3mm;height:18.3mm">my visit 78 × 64</div></div>'''
    p.append(page(3, f'''
      <h2>4 · Page grid and margins</h2>
      <div class="two"><div>
      <p>A4 portrait, 210 × 297 mm, one country per page. Two columns inside a live area of 176 × 267 mm: a 72 mm column for the flag and the facts, an 8 mm gutter, and a 96 mm column for the map and the illustration. The journal band closes every page at the same height: the taped photo frame (90 × 64 mm) and <i>My Visit</i> (date, three ruled lines, the VISITED stamp), as in the Blueprint.</p><p><b>Photo frame.</b> The Blueprint sizes the frame for a standard 9 × 13 cm print. A whole 9 × 13 print (89 × 127 mm) cannot fit on the page beside the other elements, so the frame takes a 9 × 13 print cut in half, or an instant mini print, and says so in one small line. <span class="tag">your decision</span></p>
      <table><tr><th>Margin</th><th>Value</th><th></th></tr>
      <tr><td>Inner (binding side)</td><td>20 mm</td><td>provisional</td></tr>
      <tr><td>Outer</td><td>14 mm</td><td>provisional</td></tr>
      <tr><td>Top / bottom</td><td>14 / 16 mm</td><td>provisional</td></tr>
      <tr><td>Bleed</td><td>3 mm</td><td>nothing bleeds on country pages</td></tr></table>
      <p>The frames stay in the same position on left- and right-hand pages; only the margins swap, so the binding side always has the wider margin. A thread-sewn case binding opens well but not perfectly flat: we expect roughly 4 mm lost on each side of the fold, and the inner margin keeps every element clear of that. The real figure comes from the printer's blank dummy in the final materials; until then these margins are a working assumption, not a production setting.</p>
      <p class="note">See the facing-page preview supplied with the samples.</p>
      </div><div>{mini}<p class="note" style="margin-top:2mm">Frame positions in millimetres, measured from the top-left of the live area. They map 1:1 onto InDesign frames.</p></div></div>
      <h2>5 · Line weights</h2>
      <div class="weights">
        <div><span>Plate frame, My Visit outer frame</span><span class="ln" style="border-top-width:.5pt"></span></div>
        <div><span>Hairlines, fact rules, inner frames</span><span class="ln" style="border-top-width:.25pt"></span></div>
        <div><span>Flag outer edge (0.30 mm)</span><span class="ln" style="border-top-width:.30mm"></span></div>
        <div><span>Flag inner lines (0.17 mm)</span><span class="ln" style="border-top-width:.17mm"></span></div>
        <div><span>Map coastline and border (0.30 mm)</span><span class="ln" style="border-top-width:.30mm"></span></div>
        <div><span>Illustration line (≈ 0.25–0.35 mm at size)</span><span class="ln" style="border-top-width:.3mm"></span></div>
      </div>
      <p>Rule of thumb for colorable art: no enclosed area smaller than about 2 mm across unless it is meant to stay white (the stars on the US and Brazilian flags). Lines under 0.15 mm are avoided because they break up on uncoated stock.</p>'''))

    p.append(page(4, f'''
      <h2>6 · Flags</h2>
      <p>Every flag is drawn from its official construction at its official proportions (2:3 for Italy, 10:19 for the United States, 1:2 for Australia, 7:10 for Brazil), fitted inside a 72 × 48 mm box from the top left. Outlines are vector, derived from the construction drawings and checked against the official specification; for Australia, all six star positions were checked against the Flags Act 1953. Very small details (Brazil's 27 stars, the Egyptian eagle) are kept at the official size rather than enlarged.</p>
      <h3>The color dots: an issue to decide <span class="tag">your decision</span></h3>
      <p>The Decisions Log settles colored dots beneath each flag, in the flag's reading order. But the interior is specified in one color, black. Printed in black only, a dot cannot show its color. Your example in the Blueprint (section 4) shows the dots printed in color. Three ways to keep the idea:</p>
      <div class="dotsdemo">
        <div><b>A · Outline dots with color names</b> (recommended)<div class="row"><span class="d"><i></i>Green</span><span class="d"><i></i>White</span><span class="d"><i></i>Red</span></div>The reader colors the dots first and uses them as a key. Works in black, stays an instruction. Used on the six samples.</div>
        <div><b>B · Names only</b><div class="row" style="font-size:7.5pt;letter-spacing:.12em">GREEN · WHITE · RED</div>Cleanest and shortest, but loses the visual "palette" moment the dots were chosen for.</div>
        <div><b>C · Printed color dots</b><div class="row"><span class="d"><i style="background:#009246"></i>Green</span><span class="d"><i style="background:#fff"></i>White</span><span class="d"><i style="background:#ce2b37"></i>Red</span></div>Needs four-color printing on every country page: a different, more expensive book. Not in the RFQ v2 specification.</div>
      </div>
      <p><b>Reading order</b> (proposed, applied on the samples): the field and the stripes first, as you read them, left to right and top to bottom; then the emblem. Italy: green, white, red. Egypt: red, white, black, then gold for the eagle. Under the dots, one line points to A Register of Colors, where the arrangement is explained in words.</p>
      <h2>7 · Maps</h2>
      <p>Source: Natural Earth 1:10m (public domain), drawn as vector outlines in an equal-area projection centered on each country, inside a 96 × 76 mm frame. Coastlines are generalized for the page (detail under about 0.1 mm is removed; islands under about 0.35 mm² at print size are dropped, with a note when this matters). Capitals are marked with a ringed dot and set in italics. Distant parts get labeled inset boxes at their own scale, with a note (Alaska and Hawaii; the Ryukyu Islands).</p>
      <p><b>Borders.</b> Natural Earth draws de facto lines. Where these differ from United Nations treatment, or where a dispute affects the area figure, the page carries a short factual note (Japan: southern Kuril Islands; Egypt: Halaib Triangle). Before print, each map is checked against the UN Geospatial Information Section maps.</p>'''))

    p.append(page(5, f'''
      <h2>8 · Illustrations and captions</h2>
      <p>Every illustration sits in the same double-ruled plate, 96 × 66 mm, like an engraved plate in an old atlas. The frame gives every subject the same weight on the page, whatever its shape, and keeps the composition tidy where a scene runs to the edge.</p>
      <p><b>Subject rule (settled):</b> a landmark of international standing where one exists; otherwise the officially designated national animal. Nothing is invented to fill space. Where a country has an officially designated animal and the landmark is drawn, the caption names the animal in a second short sentence.</p>
      <p><b>Caption:</b> one or two short sentences, one per line, 9 pt italic, centered. On the samples the longest is Brazil's (two lines); that is the maximum we recommend.</p>
      <p><b>How the samples were made:</b> AI-assisted line art for the subject only (never for maps, borders or flags), generated against a single style reference so all six share one line weight, then cleaned up and converted to true vector paths. AI drawings still contain architectural simplifications, and in production each one gets an illustrator's correction pass against photo references. The raster originals are kept for reference; the pages use the vector files.</p>
      <p><b>Rights:</b> landmarks under active image rights are avoided or cleared. Christ the Redeemer, shown in the original reference images, is licensed by the Archdiocese of Rio de Janeiro for commercial products; the Brazil sample therefore uses Sugarloaf Mountain until you decide whether to seek a license.</p>
      <h2>9 · The five facts and the name line</h2>
      <table><tr><th>Field</th><th>Format</th><th>Source (proposed, same for all 195)</th></tr>
      <tr><td>Capital</td><td>English exonym; note where the seat of government differs</td><td>Constitutions / official sources</td></tr>
      <tr><td>Population</td><td>One decimal, in millions (“59.1 million”); thousands below one million</td><td>UN World Population Prospects 2024, 1 July 2025</td></tr>
      <tr><td>Language</td><td>Main or official language(s), at most two</td><td>Constitutions / official sources</td></tr>
      <tr><td>Area</td><td>Whole km², square miles in parentheses</td><td>National mapping or statistics agency, edition valid in 2025</td></tr>
      <tr><td>Currency</td><td>Name in American English, ISO code in parentheses</td><td>ISO 4217</td></tr></table>
      <p><b>Name line.</b> The country's name in its own language and script, with a transliteration in italics for non-Latin scripts (日本 <i>Nippon</i>, مصر <i>Misr</i>). Where the own-language name is the English name (United States, Australia), we propose showing the formal name instead (<i>United States of America</i>, <i>Commonwealth of Australia</i>) so the line is never empty and never repeats the title. <span class="tag">your decision</span></p>
      <p class="note">The 2025 reference year appears once, on the copyright page, with the UN data credit required by its CC BY 3.0 IGO license.</p>'''))

    p.append(page(6, f'''
      <h2>10 · Palette and cover direction</h2>
      <p>The interior prints black on cream. The palette below is for the case and the jacketless cover only. Screen colors are approximate; cloth and foil are chosen from the printer's physical swatch books, and the foil is a metallic, not a printed ink.</p>
      <div class="swatches">
        <div class="sw"><i style="background:{NAVY}"></i><span><b>Navy</b><br>cloth, option 1<br>{NAVY}</span></div>
        <div class="sw"><i style="background:{PINK}"></i><span><b>Old Pink</b><br>cloth, option 2 (direction only)<br>{PINK}</span></div>
        <div class="sw"><i style="background:linear-gradient(135deg,#8c6c37,#d9bd84 45%,#9b7b45)"></i><span><b>Gold</b><br>foil, front and spine<br>approx. {GOLD}</span></div>
        <div class="sw"><i style="background:{BEIGE}"></i><span><b>Beige</b><br>endpapers / paper tone<br>{BEIGE}</span></div>
        <div class="sw"><i style="background:{GREY}"></i><span><b>Dark grey</b><br>screen and marketing type<br>{GREY}</span></div>
      </div>
      <div class="covers"><div class="coverwrap">{cover()}</div><div>
        <div class="thumbwrap"><div class="thumbcover">{cover(PINK, "#7a5a2e")}</div></div>
        <p class="note">Old Pink cloth with gold: a second direction, not a confirmed choice.</p>
        <p class="note">Developed from your reference cover. The world map is coastlines only, generalized to about 0.5 mm, and the compass rose is redrawn as clean geometry. Fine foil detail fills in on cloth, so the printer confirms minimum line and gap sizes before the artwork is final.</p>
        <p class="note">Foil is shown on the front only. Back-cover foil appeared in your first requirements but is not in RFQ v2; tell us if you want it quoted as an option.</p>
        <p class="note">Spine: an estimated 25 mm, not drawn. The spine and board artwork are set from the printer's template and blank dummy.</p>
      </div></div>'''))
    return "".join(p)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>THE WORLD style guide</title>
<link rel="stylesheet" href="../build/book.css"><style>{CSS}</style></head><body class="screen-gap">{build()}</body></html>'''
    open(os.path.join(OUT, "style-guide.html"), "w").write(html)
    print("ok")
