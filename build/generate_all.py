"""Generate the vignette for every country (google/nano-banana-pro on Replicate), using the
Colosseum as style reference so all 195 share one line. Token from REPLICATE_API_TOKEN only.
Skips files that already exist. Usage: python3 build/generate_all.py [workers]"""
import json, os, re, sys, time, subprocess, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "build"), os.path.join(ROOT, "data")]
from pagemap import CONTINENTS
from countries_master import COUNTRIES
TOK = os.environ["REPLICATE_API_TOKEN"]
OUT = os.path.join(ROOT, "assets/illustrations/source-ai-raster")
EXISTING = {"Italy": "italy-colosseum", "Japan": "japan-fuji-chureito", "United States": "usa-statue-of-liberty",
            "Brazil": "brazil-sugarloaf", "Egypt": "egypt-giza", "Australia": "australia-opera-house"}
STYLE = ("Use the attached image ONLY as a style reference: match its line weight, its uniform black outline, its level of detail "
         "and its clean coloring-book drawing style exactly. Do not copy its subject. Draw a new black and white line art illustration "
         "for a premium adult coloring book: clean confident ink outlines of uniform medium weight, every shape closed and large enough "
         "to color with a colored pencil, no shading, no hatching, no stippling, no gray, no solid black fills, pure white background, "
         "no text, no lettering, no border, the whole subject fully inside the frame with generous white margin on all sides, nothing "
         "cropped, architecturally and geographically accurate. Subject: ")

NOREF = ("Black and white line art illustration for a premium adult coloring book, in a vintage engraving-inspired but simplified "
         "modern style: clean confident black ink outlines of uniform medium weight, every shape closed and large enough to color with a "
         "colored pencil, controlled architectural detail, no shading, no hatching, no stippling, no gray, no solid black fills, pure white "
         "background, no text, no lettering, no border, the whole subject fully inside the frame with generous white margin, nothing cropped, "
         "architecturally and geographically accurate. Subject: ")

def slug(n):
    return EXISTING.get(n) or re.sub(r"[^a-z0-9]+", "-", n.lower().replace("ô", "o").replace("é", "e").replace("ü", "u")).strip("-")

def api(req, timeout=120):
    for i in range(8):
        try:
            return json.load(urllib.request.urlopen(req, timeout=timeout))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(10 * (i + 1)); continue
            raise
        except Exception:
            time.sleep(10 * (i + 1))
    raise RuntimeError("api failed")

def gen(name, ref):
    out = os.path.join(OUT, slug(name) + ".png")
    if os.path.exists(out):
        return name, "exists"
    subject = COUNTRIES[name]["subject"].split(". ")[0]
    if ref:
        inp = {"prompt": STYLE + subject + f" ({name}).", "image_input": [ref], "aspect_ratio": "4:3", "resolution": "2K", "output_format": "png"}
    else:  # no reference image: the reference leaked into some subjects (Colosseum copied)
        inp = {"prompt": NOREF + subject + f" ({name}). Show only this subject and nothing else; no other monuments.",
               "aspect_ratio": "4:3", "resolution": "2K", "output_format": "png"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(f"https://api.replicate.com/v1/models/google/nano-banana-pro/predictions",
                data=json.dumps({"input": inp}).encode(),
                headers={"Authorization": "Bearer " + TOK, "Content-Type": "application/json", "Prefer": "wait=60"})
            p = api(req)
            while p["status"] not in ("succeeded", "failed", "canceled"):
                time.sleep(4)
                p = api(urllib.request.Request(p["urls"]["get"], headers={"Authorization": "Bearer " + TOK}), 60)
            if p["status"] == "succeeded":
                o = p["output"]; o = o[0] if isinstance(o, list) else o
                urllib.request.urlretrieve(o, out + ".tmp"); os.replace(out + ".tmp", out)
                return name, "ok"
            err = p.get("error")
        except Exception as e:
            err = str(e)
        time.sleep(15)
    return name, f"FAILED {err}"

if __name__ == "__main__":
    r = subprocess.run(["curl", "-s", "-X", "POST", "-H", "Authorization: Bearer " + TOK, "-F",
                        f"content=@{OUT}/italy-colosseum.png;type=image/png", "https://api.replicate.com/v1/files"],
                       capture_output=True, text=True, check=True)
    ref = json.loads(r.stdout)["urls"]["get"]
    names = [n for v in CONTINENTS.values() for n in v]
    if os.environ.get("NOREF_NAMES"):
        names = os.environ["NOREF_NAMES"].split(";"); ref = None
    with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 4) as ex:
        for n, s in ex.map(lambda n: gen(n, ref), names):
            print(n, s, flush=True)
