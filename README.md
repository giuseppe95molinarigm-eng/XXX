# THE WORLD: Countries & Flags · Phase 1 revision

Repository di lavoro di ElitePublishing per la Fase 1 (pianificazione e direzione visiva). Il materiale per il cliente è in American English; il report interno è in italiano: **`REPORT-INTERNO-fase1.md`**.

## LIBRO COMPLETO (consegna finale)
- `delivery/THE-WORLD-Countries-and-Flags-interior.pdf`: interno completo, 288 pagine A4 (210 × 297 mm) con 3 mm di abbondanza (TrimBox/BleedBox impostati), solo nero, tutto vettoriale, font incorporati (nessun Type 3).
- `delivery/THE-WORLD-cover-preview.pdf`: anteprima della copertina in tela navy con oro.
- `delivery/THE-WORLD-cover-foil-artwork-ESTIMATED-SPINE.pdf`: impianto del foil (fronte + dorso) su misure stimate (dorso 25 mm): da riallineare al template dello stampatore.
- Rigenerazione: `python3 build/book.py && node build/render_book.mjs && python3 build/merge_book.py` (dati in `data/countries_master.py`, testi in `data/book_text.py`).

## File della revisione Fase 1 (superati dal libro completo)
- `delivery/THE-WORLD-Phase1-Delivery.pdf`: tutto in un unico PDF di 28 pagine, con indice e segnalibri.
- `delivery/THE-WORLD-Phase1-Source-Package.zip`: PDF singoli e sorgenti per il cliente, senza documenti interni.

## Consegna al cliente (PDF singoli)
| File | Contenuto |
|---|---|
| `client/THE-WORLD-Phase1-revision-notes.pdf` | Cosa contiene la consegna, 12 decisioni richieste, informazioni mancanti, voci di costo, fasi future |
| `style-guide/THE-WORLD-style-guide.pdf` | Style guide e direzione copertina |
| `sample-pages/THE-WORLD-sample-country-pages.pdf` | 6 pagine paese (carta crema simulata) |
| `sample-pages/THE-WORLD-sample-country-pages-PRINT-white.pdf` | Le stesse 6 pagine come andrebbero in stampa (solo nero) |
| `sample-pages/THE-WORLD-spread-preview.pdf` | Anteprima della doppia pagina affrontata (margine di cucitura) |
| `color-register/THE-WORLD-color-register-10-specimens.pdf` | 10 voci campione del registro colori |
| `color-register/THE-WORLD-color-register-density-test-*.pdf` | Test di densità: 8,5 pt (5 pp.), 9 pt (6 pp.), 8,5 pt con budget di lunghezza (4 pp.) |
| `page-map/THE-WORLD-page-map-PROPOSAL.pdf` | Page map a 288 pagine (Blueprint + Decisions Log) |
| `client/THE-WORLD-front-matter-text-revisions.pdf` | Correzioni ai testi iniziali del Blueprint |

## Sorgenti
- `assets/illustrations/vector/`: illustrazioni vettoriali (potrace). I raster AI originali sono in `source-ai-raster/`; prompt e impostazioni in `prompts.json`.
- `assets/maps/`: mappe vettoriali (Natural Earth 1:10m, pubblico dominio).
- `assets/flags/outline/`: bandiere a contorno vettoriale; le costruzioni a colori sono in `source-color/`.
- `assets/cover/`: rosa dei venti e mappa del mondo per il foil (solo direzione).
- `assets/fonts/`: Cormorant Garamond, EB Garamond, Noto Naskh Arabic, Noto Serif JP (sottoinsieme), tutti SIL OFL 1.1 con le licenze.
- `data/samples.json`: testi stampati. `data/sample-data.csv`: dati con fonti e stato di verifica. `data/color-register-specimens.json`: voci del registro.
- `build/book.css`: sistema pagina in mm/pt, mappabile 1:1 su InDesign.

InDesign non era disponibile: non ci sono `.indd`/`.idml`, e i PDF sono anteprime (font Type 3), non PDF di stampa.

## Rigenerare
Servono Python 3 (shapely, pyproj, pillow, numpy, pyreadr, pandas), potrace, Node con Playwright e Chromium.
```bash
python3 build/maps.py <ne_10m_admin_0_countries.geojson>    # mappe
node build/rasterize.mjs 4320 <tmp> assets/flags/source-color/*.svg && python3 build/flag_outline.py <tmp>
python3 build/trace.py                                      # illustrazioni -> SVG
python3 build/pages.py && python3 build/register.py && python3 build/styleguide.py
python3 build/pagemap.py && python3 build/pagemap_doc.py
python3 build/cover.py <ne_10m_admin_0_countries.geojson>
node build/render.mjs <file.html> <out.pdf>                 # CHROMIUM=/percorso/chrome se serve
REPLICATE_API_TOKEN=... python3 build/generate_illustrations.py <out_dir>   # il token non va mai salvato
```
