"""Static font instances for the print PDF (avoids Type 3 fonts from variable fonts).
Display/text: EB Garamond 400/500/600 (+italic 400/500), Cormorant Garamond 500/600 (+italic 500).
Native-script names: Noto Serif families, instanced at 400 (or 500) and subset to the glyphs used.
All fonts SIL OFL 1.1. Usage: python3 build/fonts.py <dir with downloaded Noto VF files>"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "data")]
from countries_master import R
OUT = os.path.join(ROOT, "assets/fonts/static"); os.makedirs(OUT, exist_ok=True)
F = os.path.join(ROOT, "assets/fonts")

def inst(src, dst, wght, extra=None, text=None):
    f = TTFont(src)
    if "fvar" in f:
        axes = {a.axisTag: a for a in f["fvar"].axes}
        loc = {"wght": max(axes["wght"].minValue, min(wght, axes["wght"].maxValue))} if "wght" in axes else {}
        if "wdth" in axes: loc["wdth"] = 100
        f = instancer.instantiateVariableFont(f, loc, updateFontNames=True)
    if text is not None:
        o = subset.Options(); o.layout_features = ["*"]; o.name_IDs = ["*"]; o.notdef_outline = True
        s = subset.Subsetter(o); s.populate(text=text); s.subset(f)
    f.save(os.path.join(OUT, dst)); print(dst, os.path.getsize(os.path.join(OUT, dst)) // 1024, "KB")

if __name__ == "__main__":
    src = sys.argv[1]
    for w in (400, 500, 600):
        inst(f"{F}/EBGaramond-VF.ttf", f"EBGaramond-{w}.ttf", w)
    for w in (400, 500):
        inst(f"{F}/EBGaramond-Italic-VF.ttf", f"EBGaramond-Italic-{w}.ttf", w)
    for w in (500, 600):
        inst(f"{F}/CormorantGaramond-VF.ttf", f"CormorantGaramond-{w}.ttf", w)
    inst(f"{F}/CormorantGaramond-Italic-VF.ttf", "CormorantGaramond-Italic-500.ttf", 500)
    inst(f"{F}/NotoNaskhArabic-VF.ttf", "NotoNaskhArabic-400.ttf", 400)
    names = "".join(r["local"] for r in R) + "日本中国대한민국조선"
    for fam in ["notoserifhebrew", "notoserifdevanagari", "notoserifbengali", "notoserifsinhala", "notoserifthai",
                "notoseriflao", "notoserifkhmer", "notoserifmyanmar", "notoseriftibetan", "notoserifgeorgian",
                "notoserifarmenian", "notoserifethiopic", "notosansthaana", "notoserifkr", "notoserifsc", "notoserifjp"]:
        inst(f"{src}/{fam}.ttf", f"{fam}-500.ttf", 500, text=names + " ")
