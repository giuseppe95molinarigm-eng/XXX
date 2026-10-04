"""Regenerate the sample illustrations on Replicate (google/nano-banana-pro).

The API token is read from the environment (REPLICATE_API_TOKEN) and is never stored.
Prompts and settings: assets/illustrations/prompts.json. Output goes to a scratch folder;
promoted files are copied by hand into assets/illustrations/source-ai-raster/ after review,
then traced with build/trace.py.
Usage: REPLICATE_API_TOKEN=... python3 build/generate_illustrations.py <out_dir> [name ...]
"""
import json, os, sys, time, subprocess, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = "google/nano-banana-pro"

def call(token, inp, out):
    req = urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions",
        data=json.dumps({"input": inp}).encode(),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "Prefer": "wait=60"})
    p = json.load(urllib.request.urlopen(req, timeout=120))
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(3)
        p = json.load(urllib.request.urlopen(urllib.request.Request(p["urls"]["get"], headers={"Authorization": "Bearer " + token}), timeout=60))
    if p["status"] != "succeeded":
        raise RuntimeError(p.get("error"))
    o = p["output"]; o = o[0] if isinstance(o, list) else o
    urllib.request.urlretrieve(o, out)

def upload(token, path):
    r = subprocess.run(["curl", "-s", "-X", "POST", "-H", "Authorization: Bearer " + token,
                        "-F", f"content=@{path};type=image/png", "https://api.replicate.com/v1/files"],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)["urls"]["get"]

if __name__ == "__main__":
    token = os.environ["REPLICATE_API_TOKEN"]
    out_dir = sys.argv[1]; names = sys.argv[2:]
    spec = json.load(open(os.path.join(ROOT, "assets/illustrations/prompts.json")))
    ref = upload(token, os.path.join(ROOT, "assets/illustrations/source-ai-raster/italy-colosseum.png"))
    for name, g in spec["generations"].items():
        if names and name not in names:
            continue
        inp = {"prompt": g["prompt"], "aspect_ratio": g["aspect_ratio"], "resolution": "2K", "output_format": "png"}
        if g["uses_style_reference"]:
            inp["image_input"] = [ref]
        call(token, inp, os.path.join(out_dir, name + ".png"))
        print("ok", name)
