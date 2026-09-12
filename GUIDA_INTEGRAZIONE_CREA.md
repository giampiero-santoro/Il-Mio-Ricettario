# Integrazione della banca dati CREA in "Il Mio Ricettario"

> **Nota preliminare:** nel tuo messaggio erano elencati anche `index.html`,
> `GUIDA.md` e `CHANGELOG.md`, ma solo `README.md` e i tre file del dataset
> CREA sono arrivati effettivamente nell'upload. Questa guida quindi si
> basa sulla struttura descritta nel README e sulle convenzioni note del
> progetto (palette noce scuro/pergamena/oro, font Cormorant Garamond +
> Crimson Pro, file singolo con `localStorage`). Se qualche nome di
> variabile CSS o funzione JS nel tuo `index.html` reale è diverso, è
> sufficiente rinominare i riferimenti nei file forniti — la logica non
> cambia.

## Nota su licenza e attribuzione

I dati CREA (fonte primaria: alimentinutrizione.it, redistribuiti su
Kaggle) restano dati di un ente di ricerca pubblico, ma prima di
pubblicarli su un sito accessibile a chiunque conviene verificare i
termini d'uso indicati nella pagina del dataset Kaggle e su
alimentinutrizione.it, e mantenere sempre una citazione visibile della
fonte (già prevista nel markup fornito più sotto). Non è un problema per
un uso personale, ma è la cosa corretta da controllare per un sito
pubblico.

---

## 1. Architettura e ottimizzazione dati

### Perché un file dati separato, e non tutto dentro `index.html`

L'app è nata come singolo file HTML autosufficiente, ed è un'ottima scelta
per ricette/dispensa/pianificazione (dati piccoli, generati dall'utente).
La banca dati CREA è però un caso diverso: è un dato **statico e di sola
lettura**, non generato dall'utente. Tenerla in un file JSON separato,
caricato con `fetch()` al volo, porta tre vantaggi concreti:

- **Caricamento più veloce**: `index.html` resta leggero; il JSON CREA
  (~200 KB) si scarica in parallelo e viene messo in cache dal browser
  (richieste successive sono istantanee, anche offline dopo la prima
  visita se in futuro aggiungi un service worker).
- **Manutenibilità**: se CREA aggiorna i dati, rigeneri solo `data/crea-alimenti.json`
  con lo script Python, senza toccare il codice dell'app.
- **Git più pulito**: un diff su un file dati da 900 righe non si mescola
  ai diff del codice dell'app.

Il resto della filosofia "nessun account, nessun server" resta intatto:
il file JSON è comunque uno **asset statico** servito da GitHub Pages,
non richiede alcun backend.

### Struttura cartelle consigliata

```
Il-Mio-Ricettario/
├── index.html                      # l'app (invariata nella sua natura)
├── data/
│   ├── crea-alimenti.json          # dataset slim generato dallo script (~200 KB)
│   └── crea-meta.json              # metadati: fonte, data generazione, conteggi
├── js/
│   └── crea-nutrition.js           # ricerca + calcolo (può restare separato
│                                    #   oppure essere incollato dentro
│                                    #   <script> in index.html, a scelta)
├── css/                             # opzionale: se preferisci CSS separato
│   └── crea-nutrition.css
├── scripts/                         # NON pubblicato/usato a runtime dal sito:
│   └── build_crea_data.py           #   serve solo a te per rigenerare i dati
└── source-data/                     # opzionale: dataset grezzo Kaggle,
    ├── crea_food_composition_tables.csv   # utile tenerlo nel repo per
    └── crea_recipes.json                  # poter rigenerare in futuro
```

`scripts/` e `source-data/` non vengono mai richiesti dal browser: sono
lì solo per te (o per chi clona il repo) quando serve rigenerare i dati.
GitHub Pages li pubblicherà comunque (a meno di escluderli), ma non
influiscono sulle prestazioni perché nessuna pagina li carica.

### Perché non serve un "database" vero e proprio

900 alimenti in un array JSON, caricati una volta in memoria, sono
gestibili con una scansione lineare in JavaScript in meno di 1
millisecondo per ogni ricerca: non serve IndexedDB, non serve un indice
invertito, non serve paginazione. Se in futuro il dataset crescesse
molto (es. unendo anche le migliaia di alimenti INRAN), si potrebbe
valutare IndexedDB con un indice sul campo `chiave_ricerca`, ma con
questi numeri sarebbe over-engineering.

---

## 2. Script di elaborazione e pulizia (Python)

Il file `build_crea_data.py` (allegato) fa quanto segue:

1. Legge `crea_food_composition_tables.csv` (900 alimenti, 139 colonne).
2. Seleziona **solo** i campi che "Il Mio Ricettario" già gestisce per
   ogni ingrediente — Kcal, proteine, grassi, carboidrati, fibre,
   zuccheri, sale — così i dati importati da CREA sono immediatamente
   compatibili con i campi manuali già esistenti nell'app.
3. Pulisce i valori: le celle `tr` (traccia) diventano `0`, le celle
   vuote diventano `null` (dato mancante, mostrato come tale invece di
   un fuorviante "0"), le virgole decimali vengono normalizzate.
4. Calcola il **sale** dal sodio con la formula standard delle etichette
   nutrizionali UE (sale = sodio × 2,5), dato che il CSV CREA riporta il
   sodio ma non il sale come voce diretta.
5. Genera una `chiave_ricerca` per ogni alimento (minuscolo, senza
   accenti/punteggiatura) per una ricerca lato client tollerante a
   maiuscole e accenti.
6. Scrive `data/crea-alimenti.json` (compatto, senza spazi superflui) e
   `data/crea-meta.json` (fonte, data di generazione, conteggi).

**Eseguito ora come verifica**: lo script gira correttamente sul CSV che
hai allegato — 900 alimenti elaborati, 0 scartati, 19 categorie,
file finale **197 KB**. Trovi già pronti in questa consegna sia lo
script sia il JSON generato (`data/crea-alimenti.json`), pronto per
essere copiato nel tuo repository così com'è.

```bash
# per rigenerare in futuro (es. dopo un aggiornamento del dataset CREA):
python3 scripts/build_crea_data.py \
    --input source-data/crea_food_composition_tables.csv \
    --outdir data
```

### Nota su `crea_recipes.json` (le ricette standard CREA)

Questo file contiene ~ricette con ingredienti espressi in unità miste e
poco standardizzate (`"218 g"`, `"1 cuc.ino"`, `"2 foglie"`...): un
parsing automatico affidabile delle quantità non è realistico per tutte
le voci. L'uso più pratico, coerente con una funzione che la tua app ha
già, è **non** costruire una pipeline dedicata, ma sfruttare
**"📋 Importa ricetta → incolla testo"**: basta incollare il campo
`preparation` e la lista `ingredients` di una ricetta CREA come testo
semplice, e lasciare che il riconoscimento automatico già presente
nell'app proponga nome/ingredienti/passaggi da correggere prima di
salvare — esattamente come per una ricetta copiata da un sito web. Se in
futuro vuoi comunque automatizzarlo, lo stesso script Python può essere
esteso con una funzione `parse_quantity()` che riconosce i pattern
numero+unità (`g`, `ml`, `kg`, `l`) e segnala per revisione manuale tutto
il resto.

---

## 3. Logica JavaScript frontend

Il file `js/crea-nutrition.js` (allegato) espone l'oggetto globale
`CreaDB`:

| Funzione | Cosa fa |
|---|---|
| `CreaDB.init(dataPath, metaPath)` | Carica una sola volta il JSON e lo mantiene in memoria per tutta la sessione |
| `CreaDB.search(query, limit)` | Ricerca "contiene" tollerante ad accenti/maiuscole, ordinata per posizione nel file |
| `CreaDB.getByCode(codice)` | Recupero diretto per `food_code` CREA |
| `CreaDB.scale(alimento, grammi)` | Valori nutrizionali scalati dalla base "per 100 g" ai grammi effettivi dell'ingrediente |
| `CreaDB.sumIngredients(lista)` | Somma i nutrienti di più ingredienti già scalati (il totale della ricetta) |
| `CreaDB.perPorzione(totale, porzioni)` | Divide il totale per il numero di porzioni |
| `attachCreaAutocomplete(input, onSelect)` | Collega un campo di testo a un menu a tendina di risultati, pronto all'uso |

### Come si aggancia al flusso esistente dell'app

Il README descrive che oggi, per ogni ingrediente, i valori nutrizionali
si inseriscono **manualmente** e vengono sommati automaticamente in un
riepilogo per porzione. L'integrazione CREA non sostituisce questa
logica di somma già esistente: la **precompila**. In pratica, nel form
di un ingrediente della ricetta:

```js
// All'apertura del form "aggiungi ingrediente" della ricetta:
const campoNomeIngrediente = document.getElementById('ingrediente-nome');
attachCreaAutocomplete(campoNomeIngrediente, (alimentoCrea) => {
  const grammi = parseFloat(document.getElementById('ingrediente-quantita').value) || 100;
  const valori = CreaDB.scale(alimentoCrea, grammi);

  // Precompila gli stessi campi manuali che l'app già possiede:
  document.getElementById('ingrediente-kcal').value = valori.kcal ?? '';
  document.getElementById('ingrediente-proteine').value = valori.proteine ?? '';
  document.getElementById('ingrediente-grassi').value = valori.grassi ?? '';
  document.getElementById('ingrediente-carboidrati').value = valori.carboidrati ?? '';
  document.getElementById('ingrediente-fibre').value = valori.fibre ?? '';
  document.getElementById('ingrediente-zuccheri').value = valori.zuccheri ?? '';
  document.getElementById('ingrediente-sale').value = valori.sale ?? '';

  // Salva anche il riferimento (facoltativo, utile se in futuro vuoi
  // ricalcolare quando l'utente cambia la quantità):
  campoNomeIngrediente.dataset.creaCodice = alimentoCrea.codice;
});
```

Restando **campi manuali precompilati** (e non un vincolo rigido al
database), l'utente mantiene la possibilità — già presente nell'app — di
correggere un valore a mano quando la ricetta reale si discosta dal dato
medio CREA (es. un taglio di carne più magro, un prodotto specifico).

I nomi esatti degli `id` sopra sono indicativi: vanno adattati a quelli
reali del tuo form ingredienti in `index.html`.

---

## 4. Interfaccia e tabella nutrizionale (HTML/CSS)

Il file `demo-scheda-nutrizionale.html` (allegato) è una pagina
**autonoma e funzionante** — apribile subito nel browser una volta
copiata insieme a `data/` e `js/` nella stessa cartella — che mostra:

- un campo di ricerca con menu a tendina (`.crea-autocomplete-*`);
- una scheda/etichetta nutrizionale in stile "cartellino da ricettario"
  (bordo oro, sfondo pergamena, titoli in Cormorant Garamond, corpo in
  Crimson Pro);
- la citazione della fonte CREA in calce, come richiesto per
  trasparenza dei dati;
- un avviso quando alcuni valori non sono disponibili nella fonte
  originale, invece di mostrare silenziosamente uno zero fuorviante.

Le variabili CSS (`--colore-noce-scuro`, `--colore-pergamena`,
`--colore-oro`, `--font-titoli`, `--font-testo`...) sono definite in
testa al file con valori plausibili per la palette che usi nei tuoi
progetti: se il tuo `index.html` reale ha già un `:root` con nomi
diversi, ti basta o rinominare questi riferimenti o (più comodo)
rinominare le tue variabili esistenti per farle coincidere — il markup
sotto funziona con entrambe le strade.

Per integrarla nella pagina dettaglio ricetta esistente, la sezione
`<section class="scheda-nutrizionale">` si può riusare identica anche
per il riepilogo per porzione già calcolato dall'app (non solo per la
ricerca di un singolo alimento): basta popolare gli stessi campi con
l'esito di `CreaDB.sumIngredients()` + `CreaDB.perPorzione()` invece che
con `CreaDB.scale()` su un solo alimento.

---

## 5. Sfruttare tutte le proprietà dei due file completi

I due file "slim" (CSV e le 7 voci per ingrediente) restano il cuore del
calcolo nutrizionale delle ricette — restare a 7 campi per ingrediente
non è un limite tecnico ma una scelta di usabilità: un form con ~129
campi per ogni singolo ingrediente sarebbe impossibile da compilare a
mano. Per non lasciare comunque inutilizzato il resto del dataset,
l'integrazione aggiunge due funzionalità **a parte**, entrambe costruite
sui due file JSON completi (non più solo sul CSV):

### 5.1 Scheda nutrizionale CREA completa (tutte le ~129 proprietà)

Nuovo file generato da `scripts/build_crea_completo.py`:
`data/crea-alimenti-completo.json` (2,6 MB) + `data/crea-nutrienti-schema.json`
(8,8 KB, le etichette italiane e le unità di misura, scritte una sola
volta invece che ripetute per ognuno dei 900 alimenti — è per questo che
il file principale non è più pesante).

Dopo aver collegato un ingrediente a un alimento CREA con la ricerca
(🔎), compare accanto un pulsante **"ℹ️"**: apre una scheda con *tutte*
le proprietà disponibili per quell'alimento, organizzate per sezione —
Macronutrienti, Zuccheri (dettaglio), Minerali, Vitamine, Acidi grassi,
Aminoacidi, Altri composti (polifenoli, acidi organici, fitosteroli...).

Il file da 2,6 MB **non si carica all'avvio**: `CreaDB.initCompleto()`
viene chiamato solo la prima volta che l'utente apre davvero una scheda,
così il caricamento iniziale del sito resta leggero come prima.

Una nota di trasparenza: per macronutrienti, minerali e vitamine le
unità di misura (g/mg/µg) sono quelle standard delle tabelle
alimentinutrizione.it, verificate. Per aminoacidi e "altri composti" il
dataset originale non specifica l'unità: la scheda li mostra comunque,
etichettati "n.d.", invece di inventare un'unità plausibile ma non
verificata.

### 5.2 Importa le 56 ricette ufficiali CREA con un clic

Nuovo file generato dallo stesso script: `data/crea-ricette.json` (86
KB). Dal menu **"📋 Importa ricetta ▾"** è stata aggiunta una voce
**"🇮🇹 Da ricette CREA"**: apre un elenco con ricerca e caselle di
selezione multipla delle 56 ricette (Pizza Napoletana STG, Ragù alla
bolognese, Falafel, Hummus, Cannoli siciliani...), per importarle così
come sono con "+ Importa selezionate".

Cosa succede automaticamente all'importazione:
- **categoria** assegnata per parole chiave nel nome (es. "torta" →
  Dolci, "risotto"/"pasta" → Primi, "sugo"/"pesto" → Salse & Sughi) —
  è un'euristica, non infallibile: restano modificabili dopo come
  qualunque altra ricetta;
- **porzioni**: dedotte dal testo originale della fonte quando possibile
  (es. "PER UNA PIZZA" → 1), altrimenti il default a 4 dell'app;
- **preparazione**: il testo CREA diventa un unico passaggio (l'app non
  richiede altro, ma resta comunque modificabile/suddivisibile a mano);
- **ingredienti**: quantità e unità separate automaticamente dal testo
  originale CREA (es. "218 g" → 218 + g). Sui 433 ingredienti totali
  delle 56 ricette, **57 sono stati collegati automaticamente** a un
  alimento della banca dati perché il nome combaciava *esattamente* —
  solo per questi viene precompilata anche la nutrizione, con lo stesso
  criterio prudente già usato per la ricerca manuale (mai un
  abbinamento "quasi giusto": o è certo, o si lascia cercare a te).
  Per tutti gli altri ingredienti resta il pulsante 🔎 già presente per
  collegarli a mano in un secondo momento, se vuoi.
- se una ricetta con lo **stesso nome** è già presente nella tua
  raccolta, viene saltata invece di creare un duplicato (te lo segnala
  un messaggio di riepilogo a importazione conclusa).

### 5.3 La stessa ricerca CREA anche in Dispensa

Il form "Nuovo prodotto" della Dispensa aveva già gli stessi 7 campi
nutrizionali degli ingredienti — con la stessa avvertenza già presente
nell'app ("Riferiti alla quantità indicata sopra, non ai 100g"). Ha
quindi senso agganciarci la stessa ricerca 🔎 + scheda ℹ️: selezioni
l'alimento, i valori si scalano sulla quantità del prodotto (se espressa
in grammi/kg, come per gli ingredienti), e la categoria Dispensa viene
proposta in automatico da quella CREA (es. "Verdure e ortaggi" → Verdura,
"Formaggi e latticini"/"Latte e yogurt" → Latticini e pronti) — di nuovo,
un default modificabile, non un vincolo.

---

## 6. Due nuove viste dedicate: "CREA Alimenti" e "CREA Menù"

Oltre a "Ricettario", "Pianificazione" e "Dispensa", la barra di
navigazione ha ora due voci in più:

### 🌾 CREA Alimenti

Consultazione libera di tutti i 900 alimenti della banca dati: ricerca
per nome, filtro per una delle 19 categorie CREA originali (Cereali e
derivati, Formaggi e latticini, Frutta...), risultati mostrati come
elenco semplice (nome, categoria, kcal/100g). Cliccando una riga si apre
la stessa scheda completa ℹ️ già usata per gli ingredienti — **nessun
codice duplicato**, è la stessa funzione (`apriSchedaCrea`) richiamata
da un punto diverso.

Per non caricare 900 righe di colpo, l'elenco resta vuoto (solo un
suggerimento a schermo) finché non digiti qualcosa o scegli una
categoria; i risultati sono comunque limitati ai primi 200 per volta,
con un avviso se ce ne sono altri — pensato per la consultazione, non
per scorrere l'intera banca dati riga per riga.

### 🇮🇹 CREA Menù

Le stesse 56 ricette ufficiali già disponibili per l'importazione
rapida, ma qui sfogliabili una per una con ricerca e filtro per
categoria (quella dell'app: Primi, Secondi, Dolci...). Cliccando una
ricetta si apre un dettaglio completo — ingredienti con le quantità
originali, preparazione per intero, e i valori nutrizionali ufficiali
CREA del piatto finito per 100 g — con un pulsante **"+ Importa nel
Ricettario"** per aggiungerla alla tua raccolta solo quando decidi che
ti interessa (stesso controllo anti-doppione per nome già visto nel
picker multiplo: le due funzionalità condividono la stessa logica di
importazione, `importaRicetteCreaPerId`, per non mantenerne due copie
leggermente diverse).

Un consiglio per il seguito, se vuoi continuare a svilupparle: **CREA
Alimenti** e **CREA Menù** sono pensate come vetrine di sola
consultazione della fonte ufficiale, distinte dal tuo Ricettario/Dispensa
personali — cioè inserire qui note personali, foto, o modifiche dirette
alla ricetta/alimento non avrebbe senso (cambierebbe la fonte, non la tua
copia): per personalizzare qualcosa da CREA Menù, il modo corretto resta
importarla nel Ricettario e poi modificarla lì, esattamente come fai oggi
con qualunque altra ricetta.

---

## Riepilogo dei file consegnati

| File | Scopo |
|---|---|
| `build_crea_data.py` | Script di pulizia (Python) per il dataset slim (7 valori/ingrediente) |
| `scripts/build_crea_completo.py` | Script (Python) per il profilo nutrizionale completo e le 56 ricette CREA |
| `data/crea-alimenti.json` | Dataset slim per il calcolo delle ricette (900 alimenti, 197 KB) |
| `data/crea-meta.json` | Metadati e fonte del dataset slim |
| `data/crea-alimenti-completo.json` | Profilo nutrizionale integrale, ~129 proprietà/alimento (2,6 MB, caricato solo su richiesta) |
| `data/crea-nutrienti-schema.json` | Etichette italiane e unità di misura dei ~129 nutrienti (8,8 KB) |
| `data/crea-ricette.json` | Le 56 ricette ufficiali CREA, pronte per l'importazione (86 KB) |
| `js/crea-nutrition.js` | Ricerca, scaling, scheda completa, importazione ricette CREA |
| `index.html` | Il tuo file, già integrato con tutte le funzionalità sopra |
| `demo-scheda-nutrizionale.html` | Pagina dimostrativa autonoma del solo dataset slim |

### Prossimi passi consigliati

1. Carica tutta la cartella `data/` (compresi i tre nuovi file) e `js/`
   nel repository, poi sostituisci `index.html` con quello allegato.
2. Apri il sito pubblicato: prova a collegare un ingrediente con 🔎,
   poi apri la sua scheda completa con ℹ️.
3. Prova "📋 Importa ricetta ▾ → 🇮🇹 Da ricette CREA": seleziona una
   ricetta e importala, poi controlla categoria/porzioni assegnate.
4. Prova le due nuove voci di navigazione "🌾 CREA Alimenti" e
   "🇮🇹 CREA Menù": sono vetrine di sola consultazione della fonte
   ufficiale, separate dal tuo Ricettario/Dispensa personali.
5. (Facoltativo) tieni anche `scripts/` e i JSON grezzi di Kaggle nel
   repository se in futuro vorrai rigenerare i dati.
6. Aggiorna `GUIDA.md` e `CHANGELOG.md` del progetto quando sei
   soddisfatto del risultato.
