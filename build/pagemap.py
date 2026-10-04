"""PROVISIONAL page map (proposal, not approved): Blueprint Phase 1 (272 pp.) updated with the
Decisions Log toward the 288-page / 18 x 16 working target.

Changes against the Blueprint: One Hundred Places removed; national animal moved to the
illustration; achievement page absorbed into each continent's closing spread (Notes from the
Continent); continent bucket lists added (one spread per continent); expanded travel ledger;
Top Five spread; one Favorite Memory spread; Where I Go Next kept with a planning block;
Register of Colors cut from 8 to 4 pages; Melville moved to the silent Departure page.
Writes page-map/page-map.csv and prints a summary.
"""
import csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 193 UN members + Holy See + State of Palestine. Blueprint atlas order of continents;
# countries alphabetical within each continent (UN M49 regions).
CONTINENTS = {
 "Europe": """Albania;Andorra;Austria;Belarus;Belgium;Bosnia and Herzegovina;Bulgaria;Croatia;Czechia;Denmark;Estonia;Finland;France;Germany;Greece;Holy See;Hungary;Iceland;Ireland;Italy;Latvia;Liechtenstein;Lithuania;Luxembourg;Malta;Moldova;Monaco;Montenegro;Netherlands;North Macedonia;Norway;Poland;Portugal;Romania;Russia;San Marino;Serbia;Slovakia;Slovenia;Spain;Sweden;Switzerland;Ukraine;United Kingdom""",
 "Africa": """Algeria;Angola;Benin;Botswana;Burkina Faso;Burundi;Cabo Verde;Cameroon;Central African Republic;Chad;Comoros;Congo;Côte d'Ivoire;Democratic Republic of the Congo;Djibouti;Egypt;Equatorial Guinea;Eritrea;Eswatini;Ethiopia;Gabon;Gambia;Ghana;Guinea;Guinea-Bissau;Kenya;Lesotho;Liberia;Libya;Madagascar;Malawi;Mali;Mauritania;Mauritius;Morocco;Mozambique;Namibia;Niger;Nigeria;Rwanda;Sao Tome and Principe;Senegal;Seychelles;Sierra Leone;Somalia;South Africa;South Sudan;Sudan;Tanzania;Togo;Tunisia;Uganda;Zambia;Zimbabwe""",
 "Asia": """Afghanistan;Armenia;Azerbaijan;Bahrain;Bangladesh;Bhutan;Brunei;Cambodia;China;Cyprus;Georgia;India;Indonesia;Iran;Iraq;Israel;Japan;Jordan;Kazakhstan;Kuwait;Kyrgyzstan;Laos;Lebanon;Malaysia;Maldives;Mongolia;Myanmar;Nepal;North Korea;Oman;Pakistan;Palestine;Philippines;Qatar;Saudi Arabia;Singapore;South Korea;Sri Lanka;Syria;Tajikistan;Thailand;Timor-Leste;Türkiye;Turkmenistan;United Arab Emirates;Uzbekistan;Vietnam;Yemen""",
 "North America & the Caribbean": """Antigua and Barbuda;Bahamas;Barbados;Belize;Canada;Costa Rica;Cuba;Dominica;Dominican Republic;El Salvador;Grenada;Guatemala;Haiti;Honduras;Jamaica;Mexico;Nicaragua;Panama;Saint Kitts and Nevis;Saint Lucia;Saint Vincent and the Grenadines;Trinidad and Tobago;United States""",
 "South America": """Argentina;Bolivia;Brazil;Chile;Colombia;Ecuador;Guyana;Paraguay;Peru;Suriname;Uruguay;Venezuela""",
 "Oceania": """Australia;Fiji;Kiribati;Marshall Islands;Micronesia;Nauru;New Zealand;Palau;Papua New Guinea;Samoa;Solomon Islands;Tonga;Tuvalu;Vanuatu""",
}
CONTINENTS = {k: [c.strip() for c in v.split(";")] for k, v in CONTINENTS.items()}

FRONT = [  # Part I, as Blueprint pp. 1-16
    ("Half-title", "front matter"), ("Frontispiece: ghosted antique world map", "front matter"),
    ("Title page", "front matter"), ("Copyright and imprint (2025 data note, borders note, UN data credit)", "front matter"),
    ("This Journal Belongs To", "front matter"),
    ("Epigraph: 'A map shows the world as it is. What follows is the world as you found it.'", "front matter"),
    ("Contents (1/2)", "front matter"), ("Contents (2/2)", "front matter"),
    ("Before You Set Out: essay (1/4)", "front matter"), ("Before You Set Out: essay (2/4)", "front matter"),
    ("Before You Set Out: essay (3/4)", "front matter"), ("Before You Set Out: essay (4/4)", "front matter"),
    ("How to Use This Journal: annotated specimen page (1/2)", "front matter"),
    ("How to Use This Journal: annotated specimen page (2/2)", "front matter"),
    ("A Note on Color, Paper and Pencils", "front matter"), ("Blank", "pacing"),
]
BEFORE = [  # Part II; One Hundred Places removed
    ("Part title: Before You Begin", "journal"), ("The Traveler's Profile", "journal"),
    ("The Symbols of This Book (five fact icons, stamp)", "journal"),
    ("Where in the World? world map to color", "journal"), ("Countries I've Visited: 195-line checklist", "journal"),
    ("The Journeys Already Made (1/2)", "journal"), ("The Journeys Already Made (2/2)", "journal"),
    ("The World in Six Parts (1/2)", "journal"), ("The World in Six Parts (2/2)", "journal"),
    ("Blank", "pacing"),
    ("Departure: Melville, 'It is not down in any map; true places never are.' + compass rose", "journal"),
]
AFTER = [  # Part IV
    ("Blank", "pacing"), ("Part title: After the Journey", "journal"),
    *[(f"The Traveler's Ledger, expanded travel statistics ({i}/4)", "journal") for i in range(1, 5)],
    ("My Top Five (1/2)", "journal"), ("My Top Five (2/2)", "journal"),
    ("The Best Things (1/2)", "journal"), ("The Best Things (2/2)", "journal"),
    ("People Met Along the Way (1/2)", "journal"), ("People Met Along the Way (2/2)", "journal"),
    ("Words Worth Keeping (1/2)", "journal"), ("Words Worth Keeping (2/2)", "journal"),
    ("Favorite Memory, single spread (1/2)", "journal"), ("Favorite Memory, single spread (2/2)", "journal"),
    ("Where I Go Next: the reader's list", "journal"), ("Where I Go Next: planning block for the next journey", "journal"),
    *[(f"A Register of Colors ({i}/4)", "register") for i in range(1, 5)],
    *[(f"Index of Countries ({i}/4)", "journal") for i in range(1, 5)],
    ("Notes (flexible)", "flexible"), ("Notes (flexible)", "flexible"),
    ("Colophon", "front matter"),
]

def build():
    rows = []
    def add(title, kind, part, cont=""):
        n = len(rows) + 1
        rows.append([n, "recto" if n % 2 else "verso", kind, title, cont, part])
    for t, k in FRONT:
        add(t, k, "I Front Matter")
    for t, k in BEFORE:
        add(t, k, "II Before You Begin")
    for cont, countries in CONTINENTS.items():
        assert len(rows) % 2 == 1, "opener must start on a verso"
        add(f"{cont} opener: essay, country count, population", "continent", "III The Countries", cont)
        add(f"{cont} opener: title plate, compass, map, quotation", "continent", "III The Countries", cont)
        for c in countries:
            add(c, "country page", "III The Countries", cont)
        if len(countries) % 2:
            add("Note on the dependencies and territories of the Caribbean", "continent", "III The Countries", cont)
        add(f"{cont} bucket list: 15 curated experiences (1/2)", "continent", "III The Countries", cont)
        add(f"{cont} bucket list: 15 curated experiences (2/2)", "continent", "III The Countries", cont)
        add(f"{cont} closing spread: Notes from the Continent", "continent", "III The Countries", cont)
        add(f"{cont} closing spread: achievement page", "continent", "III The Countries", cont)
    for t, k in AFTER:
        add(t, k, "IV After the Journey")
    return rows

if __name__ == "__main__":
    rows = build()
    assert sum(len(v) for v in CONTINENTS.values()) == 195
    out = os.path.join(ROOT, "page-map", "page-map.csv")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["page", "side", "kind", "content", "continent", "part"]); w.writerows(rows)
    print("total", len(rows), "signatures", len(rows) / 16)
    for r in rows:
        if r[3] in ("Italy", "Japan", "United States", "Brazil", "Egypt", "Australia") or "Register" in r[3] and "1/4" in r[3]:
            print(r[:4])
