"""Case cover for THE WORLD (cloth + gold foil). Two files:
  book/THE-WORLD-cover-foil-artwork.pdf  one-color foil artwork (black = foil) on the full case flat
  book/THE-WORLD-cover-preview.pdf       navy cloth simulation with gold, for approval/marketing
Case dimensions are ESTIMATES (spine 25 mm, joints 8 mm, turn-in 15 mm): the printer's case template replaces them."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "build")]
from book import svg_file

TURN, BOARD_W, BOARD_H, JOINT, SPINE = 15, 213, 303, 8, 25
W = TURN * 2 + BOARD_W * 2 + JOINT * 2 + SPINE
H = TURN * 2 + BOARD_H
FX = TURN + BOARD_W + JOINT * 2 + SPINE      # front board left edge
SX = TURN + BOARD_W + JOINT                  # spine left edge
COMPASS = svg_file("assets/cover/compass-rose.svg")
WORLD = svg_file("assets/cover/world-foil.svg")
TRAIL = ('<svg viewBox="0 0 70 12"><path d="M2 9 C 18 13, 30 2, 52 6" fill="none" stroke="currentColor" stroke-width=".35" stroke-dasharray="1 1.4"/>'
         '<path d="M56.6 6.4l2-.1 1.8 2.6h.9l-.9-2.7 2.4-.1.8 1h.7l-.4-1.4.4-1.4h-.7l-.8 1-2.4-.1.9-2.7h-.9l-1.8 2.6-2-.1c-.5 0-.5 1.4 0 1.4z" fill="currentColor"/></svg>')

def front(x, y):
    return f'''<div style="position:absolute;left:{x}mm;top:{y}mm;width:{BOARD_W}mm;height:{BOARD_H}mm;text-align:center">
      <div style="position:absolute;top:24mm;left:50%;width:30mm;margin-left:-15mm">{COMPASS}</div>
      <div style="position:absolute;top:64mm;width:100%;font-family:'Cormorant Garamond';font-weight:600;font-size:52pt;letter-spacing:.06em">THE WORLD</div>
      <div style="position:absolute;top:87mm;width:100%;font-family:'Cormorant Garamond';font-weight:600;font-size:24pt;letter-spacing:.12em">COUNTRIES &amp; FLAGS</div>
      <div style="position:absolute;top:103mm;left:50%;width:40mm;margin-left:-20mm;border-top:.5mm solid currentColor"></div>
      <div style="position:absolute;top:110mm;width:100%;font-family:'EB Garamond';font-weight:500;font-size:13pt;letter-spacing:.24em">A COLORING JOURNAL</div>
      <div style="position:absolute;top:118mm;width:100%;font-family:'EB Garamond';font-style:italic;font-size:15pt">for the Places You’ve Visited</div>
      <div style="position:absolute;top:140mm;left:16.5mm;width:180mm">{WORLD.replace('stroke-width="0.3"', 'stroke-width="0.32"')}</div>
      <div style="position:absolute;top:262mm;width:100%;font-family:'EB Garamond';font-weight:500;font-size:11pt;letter-spacing:.34em">EXPLORE. COLOR. REMEMBER.</div>
      <div style="position:absolute;top:276mm;left:61.5mm;width:90mm;height:15mm">{TRAIL}</div></div>'''

def spine(x, y):
    return f'''<div style="position:absolute;left:{x}mm;top:{y}mm;width:{SPINE}mm;height:{BOARD_H}mm">
      <div style="position:absolute;top:16mm;left:50%;width:13mm;margin-left:-6.5mm">{COMPASS}</div>
      <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(90deg);white-space:nowrap;
        font-family:'Cormorant Garamond';font-weight:600;font-size:17pt;letter-spacing:.14em">THE WORLD <span style="font-size:11pt;letter-spacing:.16em">· COUNTRIES &amp; FLAGS</span></div></div>'''

def page(fg, bg, guides):
    g = ""
    if guides:
        def v(xx, lab):
            return f'<div style="position:absolute;left:{xx}mm;top:0;height:{H}mm;border-left:.2mm dashed #e2007a"></div><div style="position:absolute;left:{xx + 1}mm;top:2mm;font:6pt sans-serif;color:#e2007a">{lab}</div>'
        def hh(yy):
            return f'<div style="position:absolute;top:{yy}mm;left:0;width:{W}mm;border-top:.2mm dashed #e2007a"></div>'
        g = (v(TURN, "board edge") + v(TURN + BOARD_W, "board edge") + v(SX, "spine 25 mm (estimate)") + v(SX + SPINE, "") +
             v(FX, "front board") + v(FX + BOARD_W, "turn-in 15 mm") + hh(TURN) + hh(TURN + BOARD_H) +
             f'<div style="position:absolute;left:{TURN + 10}mm;top:{TURN + 10}mm;font:8pt sans-serif;color:#e2007a;width:150mm">'
             f'FOIL ARTWORK, gold, one hit. Black = foil. Pink = guides, do not print.<br>All case dimensions are estimates: spine 25 mm, joints 8 mm, turn-in 15 mm, '
             f'boards 213 × 303 mm. Replace with the printer’s case template before plates are made. Back board: no foil (RFQ v2).</div>')
    return f'''<section style="width:{W}mm;height:{H}mm;position:relative;overflow:hidden;background:{bg};color:{fg}">{g}{front(FX, TURN)}{spine(SX, TURN)}</section>'''

if __name__ == "__main__":
    css = f'''<link rel="stylesheet" href="../build/print.css"><style>@page{{size:{W}mm {H}mm;margin:0}}body{{margin:0}}
      .cloth{{background-image:repeating-linear-gradient(0deg,rgba(255,255,255,.035) 0 .25mm,transparent .25mm .6mm),repeating-linear-gradient(90deg,rgba(0,0,0,.08) 0 .25mm,transparent .25mm .55mm)}}</style>'''
    os.makedirs(os.path.join(ROOT, "book"), exist_ok=True)
    open(os.path.join(ROOT, "book/cover-foil.html"), "w").write(f"<!doctype html><html><head><meta charset='utf-8'>{css}</head><body>{page('#000', '#fff', True)}</body></html>")
    prev = page("#c9a865", "#1f2a44", False).replace('<section style="', '<section class="cloth" style="', 1)
    open(os.path.join(ROOT, "book/cover-preview.html"), "w").write(f"<!doctype html><html><head><meta charset='utf-8'>{css}</head><body>{prev}</body></html>")
    print("flat", W, "x", H, "mm")
