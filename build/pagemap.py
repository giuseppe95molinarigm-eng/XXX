"""PROVISIONAL page map (proposal, not approved).

The Phase 1 Editorial Blueprint is not available to us, so this map is rebuilt from the
Decisions Log and the client's reference images. It checks the total against the
288-page / 18 x 16 working target and recto/verso placement.
Writes page-map/page-map.csv and prints a summary.
"""
import csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 193 UN members + Holy See + State of Palestine, grouped by continent following
# UN M49 regions (Americas split into North/Central/Caribbean vs South America).
CONTINENTS = {
 "Africa": """Algeria;Angola;Benin;Botswana;Burkina Faso;Burundi;Cabo Verde;Cameroon;Central African Republic;Chad;Comoros;Congo;Côte d'Ivoire;Democratic Republic of the Congo;Djibouti;Egypt;Equatorial Guinea;Eritrea;Eswatini;Ethiopia;Gabon;Gambia;Ghana;Guinea;Guinea-Bissau;Kenya;Lesotho;Liberia;Libya;Madagascar;Malawi;Mali;Mauritania;Mauritius;Morocco;Mozambique;Namibia;Niger;Nigeria;Rwanda;Sao Tome and Principe;Senegal;Seychelles;Sierra Leone;Somalia;South Africa;South Sudan;Sudan;Tanzania;Togo;Tunisia;Uganda;Zambia;Zimbabwe""",
 "Asia": """Afghanistan;Armenia;Azerbaijan;Bahrain;Bangladesh;Bhutan;Brunei;Cambodia;China;Cyprus;Georgia;India;Indonesia;Iran;Iraq;Israel;Japan;Jordan;Kazakhstan;Kuwait;Kyrgyzstan;Laos;Lebanon;Malaysia;Maldives;Mongolia;Myanmar;Nepal;North Korea;Oman;Pakistan;Palestine;Philippines;Qatar;Saudi Arabia;Singapore;South Korea;Sri Lanka;Syria;Tajikistan;Thailand;Timor-Leste;Türkiye;Turkmenistan;United Arab Emirates;Uzbekistan;Vietnam;Yemen""",
 "Europe": """Albania;Andorra;Austria;Belarus;Belgium;Bosnia and Herzegovina;Bulgaria;Croatia;Czechia;Denmark;Estonia;Finland;France;Germany;Greece;Holy See;Hungary;Iceland;Ireland;Italy;Latvia;Liechtenstein;Lithuania;Luxembourg;Malta;Moldova;Monaco;Montenegro;Netherlands;North Macedonia;Norway;Poland;Portugal;Romania;Russia;San Marino;Serbia;Slovakia;Slovenia;Spain;Sweden;Switzerland;Ukraine;United Kingdom""",
 "North America": """Antigua and Barbuda;Bahamas;Barbados;Belize;Canada;Costa Rica;Cuba;Dominica;Dominican Republic;El Salvador;Grenada;Guatemala;Haiti;Honduras;Jamaica;Mexico;Nicaragua;Panama;Saint Kitts and Nevis;Saint Lucia;Saint Vincent and the Grenadines;Trinidad and Tobago;United States""",
 "Oceania": """Australia;Fiji;Kiribati;Marshall Islands;Micronesia;Nauru;New Zealand;Palau;Papua New Guinea;Samoa;Solomon Islands;Tonga;Tuvalu;Vanuatu""",
 "South America": """Argentina;Bolivia;Brazil;Chile;Colombia;Ecuador;Guyana;Paraguay;Peru;Suriname;Uruguay;Venezuela""",
}
CONTINENTS = {k: [c.strip() for c in v.split(";")] for k, v in CONTINENTS.items()}

FRONT = [
    ("Half-title", "fixed"), ("Frontispiece or blank", "flex"), ("Title page", "fixed"),
    ("Copyright page: 2025 reference year, sources, UN data credit, borders statement", "fixed"),
    ("Epigraph (client's original line; text in Blueprint, not available)", "fixed"),
    ("Contents", "fixed"), ("How to use this book (flag dots, register, symbols)", "fixed"),
    ("Where in the world? World map to color (spread, left)", "fixed"),
    ("Countries I've visited (spread, right)", "fixed"),
    ("Silent page: Melville quotation (text in Blueprint, not available)", "fixed"),
]
BACK = [
    ("Travel statistics ledger (expanded)", 4), ("My top five (spread)", 2),
    ("Where I Go Next: reader's list + planning block for the next journey", 2),
    ("Favorite memory (single spread)", 2), ("Color register (4 pages, was 8)", 4),
    ("Index of countries", 2), ("Sources and notes", 2), ("Colophon", 1),
]

def build():
    rows = []
    def add(title, kind, continent=""):
        rows.append([len(rows) + 1, "recto" if (len(rows) + 1) % 2 else "verso", kind, title, continent])
    for t, k in FRONT:
        add(t, "front matter" if k == "fixed" else "front matter (flexible)")
    for cont, countries in CONTINENTS.items():
        while (len(rows) + 1) % 2 == 0:                       # opener on a recto
            add("Notes (flexible page)", "flexible", cont)
        add(f"{cont} opener: compass, map, count, quotation", "continent", cont)
        add(f"{cont}: map to color (spread, left)", "continent", cont)
        add(f"{cont}: map to color (spread, right)", "continent", cont)
        for c in countries:
            add(c, "country page", cont)
        add(f"{cont} bucket list: 15 curated experiences", "continent", cont)
        if (len(rows) + 1) % 2:                                # closing spread starts on a verso
            add("Notes (flexible page)", "flexible", cont)
        add(f"{cont} closing spread (left): achievement page", "continent", cont)
        add(f"{cont} closing spread (right): achievement + a memory worth keeping", "continent", cont)
    for t, n in BACK:
        for i in range(n):
            add(t + (f" ({i + 1}/{n})" if n > 1 else ""), "back matter", "")
    return rows

if __name__ == "__main__":
    rows = build()
    n_c = sum(len(v) for v in CONTINENTS.values())
    assert n_c == 195, n_c
    target = 288
    fill = target - len(rows)
    out = os.path.join(ROOT, "page-map", "page-map.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # remaining pages to reach 18 signatures are shown explicitly as unallocated
    for i in range(max(0, fill)):
        rows.append([len(rows) + 1, "recto" if (len(rows) + 1) % 2 else "verso", "UNALLOCATED",
                     "To reconcile with the Blueprint (notes pages, or content to be agreed)", ""])
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["page", "side", "kind", "content", "continent"]); w.writerows(rows)
    kinds = {}
    for r in rows:
        kinds[r[2]] = kinds.get(r[2], 0) + 1
    print("countries", n_c, {k: len(v) for k, v in CONTINENTS.items()})
    print("pages before fill", target - fill, "| fill", fill, "| total", len(rows), "| signatures", len(rows) / 16)
    print(kinds)
    for r in rows:
        if r[3] in ("Italy", "Japan", "United States", "Brazil", "Egypt", "Australia"):
            print(r)
