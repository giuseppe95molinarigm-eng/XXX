# THE WORLD: Countries & Flags · Report interno, Fase 1 (revisione)

Cliente: Ranier Verginie (Fiverr `ranierverginie`) · Ordine $200, Phase 1 (pianificazione e direzione visiva) · Documento interno ElitePublishing, 4 ottobre 2026.
La consegna dell'8 settembre è in revisione (richiesta dell'11 settembre). Questa revisione **non** è un'approvazione della fase e **non** produce il libro intero.

---

## 1. Audit iniziale

**Fonti presenti e lette integralmente**
- `THE-WORLD-Brief-Claude-Code.md` (brief operativo).
- `THE-WORLD-Decisions-Log.docx`: fonte prevalente per le decisioni editoriali.
- `THE-WORLD-Printer-Shortlist-and-RFQ-v2.docx`: base per le quotazioni.
- `THE-WORLD-Decisions-Required-Phase-2.docx` (agosto). Il brief lo dava come mancante, ma è stato allegato.
  - Diversi punti sono superati dal Log: regola "animale prima", Where I Go Next come sola pagina di pianificazione, dorso 30–32 mm.
  - Conferma i "585 drawings" ma non ne dà la distinta.
- Quattro immagini di riferimento della chat d'ordine, fornite in sessione:
  - copertina navy/oro;
  - pagine Japan/Brazil/Egypt;
  - doppia pagina "Where in the world? / Countries I've visited";
  - apertura Europe.

  Sono usate come struttura di partenza, non come grafica approvata. Contengono dati non 2025 e la riga "National animal", ora rimossa.

**Citate ma mancanti**
- Chat privata (`Pasted text(20261004-101532).txt`).
- Testo della richiesta di revisione dell'11/09.
- `THE-WORLD-Editorial-Blueprint-Phase-1 (1).docx`, sia semplice sia annotato (commenti in blu).

Per questo **non** sono stati scritti:
- l'epigrafe;
- la citazione di Melville;
- il page map originale.

Non si dichiara alcuna approvazione grafica precedente.

**Nuovi elaborati:** tutto quanto è in questo repository (vedi `README.md`).

## 2. Cosa è stato fatto

| Attività | Esito | File |
|---|---|---|
| Style guide | 6 pp., in inglese, per il cliente | `style-guide/THE-WORLD-style-guide.pdf` |
| Sei pagine campione | Italy, Japan, United States, Brazil, Egypt, Australia, impaginate su un unico sistema | `sample-pages/` (crema simulato + versione bianca + spread) |
| Illustrazioni | AI (Replicate `google/nano-banana-pro`, scelto dopo un test contro `openai/gpt-image-2`), stile unificato con immagine di riferimento, poi convertite in vettoriale reale con potrace | `assets/illustrations/` |
| Mappe | Natural Earth 1:10m, vettoriali, proiezione equivalente per paese, riquadri AK/HI e Ryukyu | `assets/maps/` |
| Bandiere | Contorni vettoriali ricavati dalle costruzioni SVG (Commons via GitHub); Australia verificata sul Flags Act 1953 | `assets/flags/` |
| Registro colori | 10 voci campione + test di densità 4 pagine (3 varianti) | `color-register/` |
| Page map | Nuova proposta provvisoria: 270 pagine strutturate + 18 non allocate = 288 | `page-map/` |
| Nota al cliente | Contenuto della consegna, 12 decisioni, informazioni mancanti, voci di costo, fasi future | `client/THE-WORLD-Phase1-revision-notes.pdf` |
| Tabella dati e fonti | 41 righe con valore, anno, fonte, URL, note, stato | `data/sample-data.csv` |

**Popolazione.** La fonte è UN WPP 2024, medium variant, letta dal file dati ufficiale (pacchetto R `wpp2024` della UN Population Division, su GitHub).
- Il valore al 1° luglio 2025 è la media dei valori di fine 2024 e fine 2025 del file.
- Il metodo coincide al singolo abitante con i valori pubblicati a metà 2025.

**Superfici e altri dati.** Le superfici vengono dalle agenzie nazionali, ma i siti ufficiali erano bloccati dalla rete dell'ambiente.
- Diversi valori risultano verificati solo tramite snippet di ricerca e sono marcati **TO VERIFY at source** nel CSV.
- Altri dati verificati tramite ricerca:
  - aquila calva, uccello nazionale USA (P.L. 118-206, dic. 2024);
  - sabiá-laranjeira, Brasile (decreto 3/10/2002);
  - diritti del Cristo Redentore, gestiti dall'Arcidiocesi di Rio.

**Limite InDesign.** InDesign non è disponibile.
- Non sono stati creati `.indd` né `.idml`: un IDML non verificabile non va consegnato.
- I sorgenti sono:
  - SVG vettoriali (mappe, bandiere, illustrazioni);
  - font OFL con licenze;
  - template HTML/CSS con geometria in mm 1:1 per i frame InDesign;
  - CSV dati.
- I PDF sono anteprime: i font sono incorporati come Type 3 da Chromium, quindi non sono PDF di stampa.

## 3. Da presentare separatamente

### A. Pronti da sottoporre al cliente
1. Style guide (PDF).
2. Sei pagine campione (PDF crema + PDF bianco) e anteprima della doppia pagina.
3. Dieci voci campione del registro colori (PDF).
4. Test di densità del registro (3 PDF).
5. Page map, **esplicitamente provvisorio** (PDF).
6. Nota di revisione con decisioni richieste e voci di costo (PDF).

### B. Proposte che richiedono approvazione
1. Pallini bandiera in stampa nero, opzioni A/B/C. Raccomandata A: cerchi vuoti con nome del colore e rimando al registro.
2. Ordine di lettura dei colori: campo e strisce, poi emblema.
3. Riga del nome locale quando coincide con l'inglese: nome formale. Convenzione di traslitterazione (Misr/Masr, Nippon/Nihon, diacritici).
4. Brasile: Pan di Zucchero oppure Cristo Redentore con licenza.
5. Registro: 4 pagine a 8,5 pt con budget di caratteri (circa 70/125/215), oppure +2 pagine a 9 pt. Belize, Nepal e Sudafrica oltre budget.
6. Pattern e testo delle 10 voci campione.
7. Bandiere con iscrizioni religiose (Arabia Saudita, Iraq…): iscrizione prestampata.
8. Page map: 18 pagine non allocate, sequenza dei continenti, nomi brevi ONU, Santa Sede, assegnazione M49.
9. Margini provvisori: interno 20, esterno 14, alto 14, basso 16 mm. Griglia 72/8/96 mm e cornice "plate" per le illustrazioni.
10. Copertina: navy oppure Old Pink, solo direzione. Foil sul retro escluso come da RFQ v2, quotabile come opzione.
11. Riga "With:" aggiunta in *My Visit*.
12. Fonte unica UN WPP per la popolazione di tutti i 195 paesi.
13. Font: Cormorant Garamond ed EB Garamond, OFL.

### C. Informazioni mancanti per la produzione finale
- Blueprint (page map, epigrafe, Melville, commenti in blu).
- Chat privata e testo dell'11/09: da rileggere per controllare che nulla contraddica questa revisione.
- Mercato principale, split USA, indirizzo del magazzino NL.
- Tre preventivi comparabili su RFQ v2, poi la scelta tra offset e POD.
- Template e dummy dello stampatore. Da quelli dipendono:
  - dorso (circa 25 mm, stima);
  - peso (1,1–1,2 kg, stima);
  - margini definitivi;
  - campionari di tela e foil;
  - spessori minimi del foil.
- Lettore madrelingua per circa 50 nomi non latini (nei campioni: 日本, مصر).
- Verifica alla fonte di tutte le righe "TO VERIFY" del CSV. Per Istat, IBGE e GSI va usata l'edizione valida nel 2025.
- Verifica delle mappe sulle carte UN Geospatial. Natural Earth è de facto.
- Distinta dei 585 disegni (3 per paese?): da confermare sul Blueprint. Non è un obbligo di questo ordine.

### D. Attività delle fasi future da quotare
- Produzione illustrazioni, con correzione dell'illustratore su ogni immagine AI.
- Ricerca, testi e dati per gli altri 189 paesi, con mappe e bandiere.
- Le altre 185 voci del registro.
- Aperture di continente, bucket list (6 × 15) e spread di chiusura.
- Front e back matter.
- Impaginazione InDesign per continente.
- Copertina e foil sul template dello stampatore.
- Preflight e PDF/X.
- Prova di stampa e controllo in macchina.
- Supporto publishing e marketing: separato e non incluso.

## 4. Rischi e note
- **Token Replicate.** È stato incollato in chat. È stato usato solo come variabile d'ambiente e non è salvato in alcun file. Consigliamo comunque di **ruotarlo** dal pannello Replicate. Sono state fatte circa 14 generazioni.
- **Illustrazioni AI.** Contengono semplificazioni architettoniche, per esempio i gusci dell'Opera House stilizzati. Per i campioni sono accettabili come direzione; in produzione serve la correzione dell'illustratore.
- **Afghanistan.** Va deciso quale bandiera usare. Proposta: prassi ONU alla data di stampa, coerente con la decisione sui confini.
- **Stampa in Cina.** Rischio sul trattamento di Taiwan, già segnalato in RFQ v2.
- **Francia.** Il gallo va verificato: emblema tradizionale o animale ufficiale. Non è tra i sei campioni.
- **Sydney Opera House.** Il Trust ha marchi registrati sull'immagine: rischio basso per un'illustrazione in un libro, ma da verificare.
- **Egitto.** I ministeri si stanno spostando nella New Administrative Capital; la capitale resta Cairo. Da monitorare.
- **Stampatori.** I candidati restano quelli della shortlist. Nessuno è stato contattato e i dati commerciali non sono stati riverificati in questa fase.

## 5. Come rigenerare
Vedi `README.md`.
