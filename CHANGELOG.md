# Changelog

Tutte le modifiche rilevanti al progetto sono documentate in questo file.

## [3.15.0] — Valori nutrizionali anche per porzione singola

### Modificato
- **Valori nutrizionali per porzione**: sia nella scheda ricetta sia nel PDF esportato, ora compare l'intero elenco (Kcal, Proteine, Grassi, Carboidrati, Fibre, Zuccheri, Sale) sia come **totale ricetta** sia come **per 1 porzione**, uno sotto l'altro. Prima il "per porzione" mostrava solo le Kcal in una riga a parte, tutti gli altri valori si vedevano solo come totale

## [3.14.0] — Metodo di cottura visibile a colpo d'occhio, corretto il riconoscimento di unità e frazioni

### Aggiunto
- **Badge del metodo di cottura sempre visibile**: prima solo la pentola a pressione aveva un'icona sulla card e nella scheda ricetta; ora compaiono anche **🤖 Robot** e **🔥 Tradizionale** (una ricetta senza passaggi robot né pentola mostra sempre "Tradizionale", così il metodo si capisce sempre al primo sguardo, anche nella vista "Cosa posso cucinare?"). Una ricetta che usa sia il robot sia la pentola a pressione mostra entrambe le icone insieme

### Corretto
- **Unità di misura testuali interpretate male durante l'importazione**: nel riconoscimento automatico da testo incollato/JSON-LD e nell'import CSV, unità al singolare come "cucchiaio", "cucchiaino", "tazza", "fetta", "spicchio", "rametto", "filetto" (e "cucchiaini" al plurale) venivano tagliate a metà, lasciando una lettera o sillaba incollata al nome dell'ingrediente (es. "1 cucchiaio di vaniglia" diventava nome ingrediente "o di vaniglia"). Riguardava anche il backup/ripristino CSV: esportare e reimportare una propria ricetta con queste unità la corrompeva silenziosamente
- **Quantità frazionarie tagliate**: quantità scritte come "1/2", "1/4", "3/4" venivano interpretate come solo la parte intera (es. "1/2 cucchiaino" diventava 1 invece di 0,5, raddoppiando l'ingrediente). Ora vengono convertite correttamente in decimale

## [3.13.0] — Import che aggiorna le voci esistenti, avviso modifiche non salvate, Annulla su "consumato", accessibilità

### Aggiunto
- **Backup e CSV possono aggiornare le voci già esistenti**: prima venivano sempre e solo aggiunte le novità. Ora, se il file importato contiene ricette (o prodotti Dispensa, per il backup) già presenti — stesso identificativo per il backup, stesso nome per il CSV — viene chiesto una volta se sostituirle con la versione importata o lasciarle come sono, con un riepilogo finale di quante sono state aggiunte, aggiornate o lasciate invariate. Utile soprattutto per il backup, dato che è il modo pensato per spostare i dati tra dispositivi: prima, una modifica fatta altrove e poi reimportata non sostituiva mai la versione già presente
- **Avviso prima di chiudere con modifiche non salvate**: se il modulo di una ricetta o di un prodotto Dispensa ha modifiche non ancora salvate, chiuderlo (con la "×", toccando fuori dal modulo, chiudendo la scheda del browser o navigando altrove) chiede prima conferma, invece di buttare via il lavoro fatto in silenzio
- **"↺ Annulla" sulla conferma "pasto consumato"**: ora è possibile tornare indietro, ripristinando in Dispensa (dove il prodotto esiste ancora) le quantità che erano state tolte — prima non era possibile, per scelta, tenerla semplice
- **Etichette di accessibilità**: aggiunto un testo alternativo alle foto delle ricette e un'etichetta ai pulsanti di chiusura "×" dei moduli, per chi naviga con uno screen reader

## [3.12.0] — Robustezza del salvataggio, coerenza dei confronti con la Dispensa, "Annulla", ingredienti duplicati

### Aggiunto
- **Compressione automatica delle foto**: le foto delle ricette vengono ridimensionate (max 1400 px sul lato lungo) e ricompresse in JPEG prima di essere salvate, per occupare molto meno spazio nel browser (una foto da cellulare passa tipicamente da qualche MB a poche centinaia di KB)
- **Avviso di spazio esaurito**: se `localStorage` esaurisce lo spazio disponibile e un salvataggio fallisce, ora compare un avviso chiaro (una sola volta a sessione, per non intasare di avvisi) invece che la modifica sparisca in silenzio alla riapertura. Riguarda tutti i salvataggi: ricette, pianificazione, Dispensa, promemoria della lista della spesa
- **"Annulla" nel controllo incrociato con la Dispensa**: dopo aver premuto "Sottrai dalla lista" su una voce, un link "Annulla" permette di tornare alla quantità originale
- **Segnalazione di ingredienti duplicati**: se nella stessa ricetta lo stesso ingrediente (nome e unità) compare più volte, il salvataggio lo segnala e propone di unire le righe sommando le quantità (e i valori nutrizionali, già intesi come totali per riga)

### Modificato
- **Coerenza nella corrispondenza con la Dispensa**: la conferma "pasto consumato" ora usa la stessa logica già introdotta per il controllo incrociato della lista della spesa — un nome identico, oppure uno simile solo se il candidato è unico. Se più prodotti in Dispensa hanno un nome simile a un ingrediente (es. "Farina 00" e "Farina integrale" per "Farina"), non ne sceglie più uno alla cieca: non tocca nessuno dei due e li elenca entrambi nella conferma, lasciando la scelta a te
- Il controllo incrociato della lista della spesa ora usa la stessa funzione di corrispondenza condivisa con la conferma "pasto consumato", invece di una logica duplicata

## [3.11.0] — Conversione unità, corrispondenza elastica e "Sottrai tutto" nella lista della spesa

### Aggiunto
- **Conversione automatica tra unità equivalenti** nel controllo incrociato con la Dispensa: se la ricetta richiede "500 g" e in Dispensa risulta "1 kg" (o viceversa, oppure ml/cl/l), la sottrazione ora scatta comunque, invece di richiedere unità scritte in modo identico
- **Corrispondenza per nome più elastica**: se non c'è un prodotto con lo stesso nome esatto, il controllo incrociato prova anche un confronto più tollerante (lo stesso usato da "Cosa posso cucinare?"), utile per varianti dello stesso ingrediente (es. "Farina" nella ricetta e "Farina 00" in Dispensa). Se i prodotti candidati sono più di uno, vengono solo elencati come promemoria, senza sottrazione automatica, per non rischiare un abbinamento sbagliato
- **"🥫 Sottrai tutto"** nel modal della lista della spesa: applica in un solo tocco tutte le sottrazioni disponibili in quel momento, invece di doverle confermare una per una

## [3.10.0] — Controllo incrociato con la Dispensa nella lista della spesa

### Aggiunto
- **Controllo incrociato con la Dispensa**: ogni voce della lista della spesa (settimana, giorno o singola ricetta) che corrisponde a un prodotto già segnato in Dispensa mostra ora un avviso sotto la riga
- Se l'unità di misura coincide, l'avviso include il pulsante **"Sottrai dalla lista"**: toglie dalla quantità da acquistare quella già disponibile in Dispensa, in modo da comprare solo quello che manca davvero. Se la Dispensa ne contiene già a sufficienza, la riga si aggiorna in "già in Dispensa" e la casella si disabilita
- Se l'unità di misura è diversa o la quantità in Dispensa non è indicata, l'avviso compare comunque come promemoria, ma senza sottrazione automatica (la conversione tra unità diverse resta manuale)

## [3.9.0] — Lista della spesa per giorno/ricetta, rimossa la stampa diretta

### Aggiunto
- **Lista della spesa per singola ricetta**: nuovo pulsante **"🛒 Lista della spesa"** nella scheda ricetta, con gli ingredienti scalati alle porzioni che si stanno visualizzando in quel momento
- **Lista della spesa per singolo giorno**: nuovo pulsante **"🛒 Lista della spesa del giorno"** sotto il titolo di ogni giorno nella vista Pianificazione, con solo le ricette assegnate a quel giorno (scalate in base a "per quante persone")
- Entrambe riusano lo stesso modal della lista della settimana (spunta ingredienti, sincronizzazione con la Dispensa, esportazione PDF); a differenza della lista settimanale, non includono i promemoria "dalla dispensa", non essendo legati a un giorno o a una ricetta specifica

### Corretto
- Rimossa la stampa diretta dal browser (pulsanti "🖨 Stampa", "🖨 Stampa settimana", "🖨 Stampa lista" e la relativa finestra di sistema): su alcuni dispositivi, in particolare mobile, produceva un foglio bianco invece del contenuto. L'esportazione PDF, già presente per ricetta/settimana/lista della spesa, resta l'unico modo per ottenere un documento stampabile ed è più affidabile, perché scarica direttamente un file senza passare dalla finestra di stampa del sistema

### Modificato
- Nella vista Pianificazione, il menu a tendina "⬇ Esporta ▾" della settimana (che conteneva solo "Stampa settimana" ed "Esporta PDF settimana") è tornato un unico pulsante diretto **"⬇ Esporta PDF settimana"**, ora che la stampa non c'è più
- Nella scheda ricetta, il menu "⬇ Esporta ▾" non include più "🖨 Stampa" (restano "⬇ Esporta PDF" ed "⬇ Esporta ricetta (.json)")
- Nel modal della lista della spesa non compare più "🖨 Stampa lista" (resta "⬇ Esporta PDF")

## [3.8.0] — Dispensa unificata, lista della spesa, ordinamento, duplica ricetta

### Aggiunto
- **"Cosa posso cucinare?"** ora usa automaticamente i prodotti della Dispensa, invece di un elenco scritto a mano separato; il campo di testo resta disponibile per aggiungere altri ingredienti non tracciati in Dispensa. L'elenco si aggiorna da solo quando la Dispensa cambia o quando torni sulla vista Ricette
- **Lista della spesa → Dispensa**: spuntando un ingrediente comprato viene aggiunto alla Dispensa (o la sua quantità aumentata, se già presente con la stessa unità di misura), con un piccolo avviso che conferma quanti prodotti sono stati aggiornati
- **Ordinamento della lista ricette**: nuovo menu a tendina con Nome (A-Z/Z-A), Aggiunta di recente, Ultima preparata, Più preparate — di base è per nome
- **"⧉ Duplica"** nella scheda ricetta: crea una copia (con "(copia)" nel nome) e la apre subito in modifica, senza toccare l'originale

### Modificato
- Nella scheda ricetta, "🖨 Stampa", "⬇ Esporta PDF" ed "⬇ Esporta ricetta" sono ora un unico menu a tendina "⬇ Esporta ▾", coerente con la riorganizzazione dei menu già fatta altrove


## [3.7.0] — Conferma consumo pasto

### Aggiunto
- Nuovo pulsante **"✓"** su ogni voce della Pianificazione settimanale, per segnarla come consumata
- Per i pasti aggiunti **"dalla dispensa"**: se era stata indicata una quantità nella stessa unità di misura del prodotto, viene tolta da quel prodotto in Dispensa
- Per i pasti da **ricetta**: gli ingredienti (scalati in base a "per quante persone" impostato in Pianificazione) vengono cercati tra i prodotti in Dispensa per nome, e la quantità viene tolta solo dove l'unità di misura coincide esattamente — altrimenti il prodotto resta invariato. In entrambi i casi viene sempre chiesta conferma, mostrando in anticipo cosa cambierà e cosa no
- Una volta confermato, il segno di spunta resta acceso per quella voce, per evitare di scalare la stessa quantità più di una volta

## [3.6.0] — Riorganizzazione dei menu

### Modificato
- **Lista ricette**: "📋 Importa ricetta" e "📄 Importa ricetta (file)" sono ora un unico menu a tendina "📋 Importa ricetta ▾", come già "📦 Backup e CSV"
- **Lista ricette**: i filtri "🍲 Solo pentola a pressione", "🤖 Solo robot" e "🔥 Solo tradizionale" si sono spostati dentro il pannello filtri (rinominato da "🔍 Altri filtri" a "🔍 Filtri"), in una sezione dedicata "Metodo di cottura" con lo stesso stile a "pillola" già usato per i tag dietetici; il pulsante del pannello mostra ora tra parentesi quanti filtri sono attivi
- **Pianificazione**: "🖨 Stampa settimana" ed "⬇ Esporta PDF settimana" sono ora un unico menu a tendina "⬇ Esporta ▾"
- Nessuna modifica al funzionamento dei filtri o delle esportazioni: solo alla loro organizzazione, per una toolbar meno affollata

## [3.5.0] — Controllo ingredienti mancanti dalla Dispensa

### Aggiunto
- Quando aggiungi una ricetta alla pianificazione settimanale (dalla ricerca in Pianificazione o dal pulsante "📅 Pianifica" nella scheda ricetta), il ricettario controlla i suoi ingredienti rispetto ai prodotti presenti in Dispensa
- Se uno o più ingredienti non risultano in Dispensa, viene mostrato un avviso con l'elenco e chiesta conferma prima di aggiungerli a un promemoria per la lista della spesa
- Questi ingredienti compaiono, con l'etichetta "dalla dispensa", nella lista della spesa generata dalla settimana, nella stampa e nel PDF — anche se per quella settimana non ripianifichi la stessa ricetta — finché non li spunti nella lista (a quel punto vengono rimossi definitivamente dal promemoria) o non risultano coperti da un'altra ricetta pianificata
- I promemoria sono inclusi nel backup JSON

## [3.4.0] — Quantità per i pasti dalla Dispensa

### Aggiunto
- Scegliendo un prodotto della Dispensa da aggiungere come pasto nella Pianificazione, ora viene chiesta una **quantità facoltativa** (precompilata con quella che hai in dispensa, ma modificabile) prima di confermare
- La quantità, se indicata, compare accanto al nome del prodotto nella vista Pianificazione, nella stampa e nel PDF della settimana

## [3.3.2] — Conferma prima di rimuovere un pasto pianificato

### Aggiunto
- Rimuovendo un pasto dalla Pianificazione settimanale (il pulsante "×" su una voce già assegnata a un giorno) viene ora chiesta conferma, con il nome della ricetta o del prodotto coinvolto — come già avveniva eliminando una ricetta dal ricettario o un prodotto dalla Dispensa

## [3.3.1] — Correzione: righe troppo lunghe nel PDF

### Corretto
- Nei PDF (ricetta singola, settimana e lista della spesa) le righe troppo lunghe uscivano dal bordo della pagina invece di andare a capo. Ora il testo viene misurato e spezzato automaticamente per stare nella larghezza della pagina
- I passaggi numerati e gli elenchi puntati (ingredienti, lista della spesa) mantengono un rientro sulle righe andate a capo, allineato al testo dopo il numero o il trattino, per restare leggibili

## [3.3.0] — Filtri "solo robot" e "solo tradizionale"

### Aggiunto
- Due nuovi pulsanti filtro nella lista ricette, accanto a "🍲 Solo pentola a pressione": **"🤖 Solo robot"** (almeno un passaggio con velocità, temperatura o una modalità diversa da Normale) e **"🔥 Solo tradizionale"** (nessun passaggio con impostazioni robot o pentola a pressione)
- I tre filtri per metodo di preparazione si possono combinare liberamente tra loro e con gli altri filtri già presenti (categoria, preferite, tag dietetici, esclusione ingredienti)

## [3.2.0] — Più categorie in Dispensa

### Aggiunto
- Nuove categorie nella Dispensa, per coprire non solo i freschi ma tutto quello che può servire per una ricetta: **Uova**, **Surgelati**, **Pasta, riso e cereali**, **Legumi**, **Farine, zucchero e lieviti**, **Conserve e scatolame**, **Spezie e condimenti**, **Oli, aceti e grassi**, **Bevande**, **Snack e dolciumi**

### Nota
- Le categorie esistenti (Frutta, Verdura, Salumi, Latticini e pronti, Altro) restano invariate: i prodotti già inseriti non cambiano categoria e non serve alcuna migrazione

## [3.1.0] — Valori nutrizionali in Dispensa e pasti dalla Dispensa nella Pianificazione

### Aggiunto
- Valori nutrizionali facoltativi anche per i prodotti della Dispensa (Kcal, Proteine, Grassi, Carboidrati, Fibre, Zuccheri, Sale), inseriti allo stesso modo delle ricette — riferiti alla quantità indicata, non ai 100g; le kcal, se presenti, compaiono anche nella card del prodotto
- Possibilità di aggiungere un prodotto della Dispensa direttamente come pasto nella Pianificazione settimanale: nuovo pulsante **"🥫 Dalla dispensa…"** accanto a "🔍 Cerca ricetta…" in ogni fascia pasto, con la stessa finestra di ricerca
- Le voci pianificate dalla Dispensa si riconoscono da un'etichetta 🥫 e, se toccate, aprono la scheda di modifica del prodotto invece della ricetta
- Le voci dalla Dispensa sono incluse nella stampa e nel PDF della settimana con il nome reale del prodotto

### Modificato
- Eliminando un prodotto dalla Dispensa, viene rimosso automaticamente anche dalla pianificazione settimanale (come già avveniva eliminando una ricetta)
- Il messaggio mostrato generando la lista della spesa senza ricette pianificate ora chiarisce che i prodotti dalla Dispensa non vengono conteggiati, dato che non richiedono acquisti

## [3.0.0] — Sezione Dispensa

### Aggiunto
- Nuova sezione **"🥫 Dispensa"**, separata dal ricettario, per tenere traccia di frutta, verdura, salumi e latticini/prodotti pronti che hai in casa
- Ogni prodotto ha nome, categoria, quantità e unità facoltative, data di scadenza facoltativa e note facoltative
- Le scadenze passate sono evidenziate in rosso, quelle entro 3 giorni in arancione; l'elenco si ordina da solo mettendo prima le scadenze più vicine
- Ricerca per nome e filtro per categoria, come nel ricettario
- I prodotti della Dispensa sono ora inclusi nel backup JSON

## [2.9.0] — Categoria Infusi & Tisane

### Aggiunto
- Nuova categoria **"Infusi & Tisane"**, disponibile nel modulo di modifica e nel filtro per categoria
- L'importazione da testo riconosce automaticamente questa categoria per ricette che parlano di tè, tisane, infusi o camomilla

## [2.8.3] — Tentativo di correzione sfondi bianchi su mobile

### Corretto
- Il sito ora dichiara esplicitamente al browser di essere pensato solo per il tema chiaro (`color-scheme: light`): su alcuni telefoni con la modalità scura attiva, senza questa dichiarazione il browser può applicare colori "di sistema" a pulsanti e campi invece di quelli del sito
- Rimosso l'effetto "flash" grigio/bianco che alcuni browser mobile mostrano di default quando si tocca un pulsante

## [2.8.2] — Correzione stile campo orario

### Corretto
- Il campo dell'orario nella pianificazione mostrava lo sfondo bianco predefinito del browser invece dei colori del sito, soprattutto visibile su cellulare. Ora segue lo stesso stile degli altri campi

## [2.8.1] — Pianificazione giorno per giorno

### Modificato
- La vista Pianificazione ora mostra **un giorno alla volta** come una scheda, invece di tutti e sette impilati: linguette in alto (Lun, Mar, Mer…) per saltare a un giorno preciso, frecce ‹ › per il giorno prima/dopo, si apre già sul giorno di oggi
- Rimossa la funzione "clicca per richiudere" i giorni, non più necessaria con la nuova vista

## [2.8.0] — Importa/esporta singola ricetta

### Aggiunto
- **"⬇ Esporta ricetta"** nella scheda di una ricetta: scarica quella sola ricetta come file `.json`
- **"📄 Importa ricetta (file)"** nella toolbar: legge un file esportato così e lo aggiunge alle tue ricette, ripartendo da zero su preferita, cronologia e contatore preparazioni
- Controllo dei doppioni per nome, e un messaggio dedicato se per sbaglio si prova a importare così un intero file di backup

## [2.7.2] — Scegliere dove salvare i file

### Aggiunto
- Su Chrome ed Edge da computer, esportare backup, CSV o PDF apre ora una finestra "Salva con nome" per scegliere cartella e nome del file, invece di scaricarlo automaticamente
- Su browser che non supportano questa funzione (Safari, Firefox, la maggior parte dei browser da cellulare), il comportamento resta quello di prima: scaricamento automatico nella cartella predefinita
- Nuova sezione nella GUIDA su dove vengono salvati e caricati i file

## [2.7.1] — Valori nutrizionali nel PDF

### Aggiunto
- **"⬇ Esporta PDF"** della singola ricetta ora include anche i valori nutrizionali (se presenti), scalati alle porzioni visualizzate, con la stessa nota su eventuali dati incompleti già vista nella scheda

## [2.7.0] — Valori nutrizionali

### Aggiunto
- **"🍎 Valori nutrizionali"**, facoltativi per ogni ingrediente: Kcal, Proteine, Grassi, Carboidrati, Fibre, Zuccheri, Sale — riferiti alla quantità usata nella ricetta, non per 100g
- Riepilogo nutrizionale nella scheda della ricetta, con totale e valore per porzione, che si ricalcola insieme al +/− delle porzioni
- Segnalazione quando i dati sono inseriti solo su parte degli ingredienti, per non far sembrare completo un totale parziale

### Nota
- Nessun database nutrizionale integrato: i valori vanno inseriti manualmente, per restare un'app offline senza servizi esterni

## [2.6.2] — Pianifica dalla scheda ricetta

### Aggiunto
- **"📅 Pianifica"** nella scheda di una ricetta: scegli giorno, fascia pasto e orario facoltativo e aggiungila alla pianificazione settimanale senza passare dalla vista Pianificazione. Il pannello resta aperto dopo ogni aggiunta, per assegnarla a più giorni di seguito

## [2.6.1] — Ricerca ricette nella pianificazione

### Modificato
- Nella vista Pianificazione, la tendina con tutte le ricette è stata sostituita da **"🔍 Cerca ricetta…"**: apre una finestra con ricerca per nome o ingrediente, comoda anche quando le ricette sono molte

## [2.6.0] — Gestione ricette per pentola a pressione

### Aggiunto
- **"🍲 Impostazioni pentola a pressione"**, facoltative per ogni passaggio come quelle del robot: pressione (valore numerico + unità a scelta tra Bar, PSI o kPa), tipo di rilascio (Naturale/Rapido/Misto), durata del rilascio e liquido minimo richiesto
- **Timer dedicato al rilascio**, separato da quello di cottura in pressione, sia nella scheda della ricetta sia in modalità cucina guidata
- Campo facoltativo **"Tipo pentola a pressione"** (Elettrica / A fornello) a livello di ricetta
- Etichetta **🍲** dedotta automaticamente su schede e vista ricetta quando almeno un passaggio ha impostazioni a pressione, senza bisogno di tag manuali
- Pulsante filtro **"🍲 Solo pentola a pressione"** nella lista ricette

### Nota
- Nessuna modifica alle ricette esistenti: tutti i nuovi campi sono facoltativi e non richiedono migrazione

## [2.5.0] — PDF ricetta, promemoria backup, copia settimana

### Aggiunto
- **"⬇ Esporta PDF"** anche per la singola ricetta, con ingredienti scalati alle porzioni visualizzate
- Promemoria discreto "Ultimo backup: X giorni fa" in cima al menu "📦 Backup e CSV", che segnala in rosso se sono passate più di due settimane
- **"📋 Copia settimana scorsa"** nella vista Pianificazione: prima di ogni "Svuota settimana" viene salvata automaticamente una copia della pianificazione, richiamabile con un click

## [2.4.0] — Esportazione PDF

### Aggiunto
- **"⬇ Esporta PDF settimana"** nella vista Pianificazione: scarica un PDF con il piano di tutti i giorni e la lista della spesa aggregata, senza passare dalla finestra di stampa del browser
- **"⬇ Esporta PDF"** nella lista della spesa: scarica la lista come PDF
- Generatore PDF scritto interamente in JavaScript vanilla (nessuna libreria esterna), multipagina, con supporto alle lettere accentate italiane

### Corretto
- "🖨 Stampa settimana" poteva non produrre nulla su alcuni browser mobili: l'esportazione PDF risolve il problema offrendo un file scaricabile che non dipende dalla finestra di stampa del browser

## [2.3.1] — Riordino dei menu

### Modificato
- La toolbar principale è stata riorganizzata per essere più leggibile, soprattutto su schermi piccoli: "Esporta/Importa backup" ed "Esporta/Importa CSV" sono ora raggruppati in un unico menu a tendina **"📦 Backup e CSV"**
- Il filtro per tag dietetico e il campo "Escludi ingredienti" sono stati spostati in un pannello **"🔍 Altri filtri"** richiudibile, nascosto di default per lasciare la pagina più snella

## [2.3.0] — Import/export CSV

### Aggiunto
- **Importa/esporta CSV**: esporta tutte le ricette in un file `.csv` (una riga per ricetta, apribile in Excel o Fogli Google) e importa ricette da un file con lo stesso formato, senza duplicare quelle già presenti con lo stesso nome

### Rimosso
- Il pulsante "Aggiungi ricette di esempio" e le 24 ricette tradizionali incluse nel codice. Il documento [ricette-tradizionali-ciociare.md](ricette-tradizionali-ciociare.md) resta disponibile come riferimento leggibile/stampabile, ma non è più importabile con un click dall'app

## [2.2.0] — Dispensa, filtri e rifiniture

### Aggiunto
- Dispensa salvata: la lista degli ingredienti scritta in "Cosa posso cucinare?" resta salvata tra una sessione e l'altra, senza doverla riscrivere ogni volta
- Filtro "Escludi ingredienti" per nascondere le ricette che contengono uno o più ingredienti indesiderati (es. allergie)
- Tag dietetici (Vegetariano, Vegano, Senza glutine, Senza lattosio, Piccante) assegnabili a ogni ricetta e filtrabili nella lista
- Un'impostazione "per quante persone" nella vista Pianificazione, che scala automaticamente le quantità della lista della spesa generata dalla settimana
- Contatore "quante volte preparata", accanto alla data dell'ultima preparazione
- "🖨 Stampa settimana": stampa in un unico foglio il piano di tutti i giorni insieme alla lista della spesa
- Giorni della pianificazione richiudibili con un click sul titolo, per una vista più compatta

## [2.1.0] — Pianificazione settimanale rinnovata

### Aggiunto
- La pianificazione settimanale è ora una vista dedicata, separata dal ricettario ("📅 Pianificazione")
- Più ricette per ogni giorno, organizzate in fasce pasto (di base: Colazione, Pranzo, Spuntino, Cena)
- Fasce pasto personalizzabili: se ne possono aggiungere di nuove o rimuovere quelle inutilizzate
- Orario facoltativo per ogni ricetta pianificata, con ordinamento automatico delle voci

### Modificato
- Lista della spesa e "Svuota settimana" si trovano ora nella vista Pianificazione
- Le pianificazioni fatte con il vecchio sistema (una ricetta per giorno) vengono convertite automaticamente al nuovo formato al primo avvio

## [2.0.0] — Ricettario generale

### Modificato
- Il ricettario non è più centrato sul robot da cucina Monsieur Cuisine: ogni passaggio ha ora impostazioni robot facoltative (velocità/temperatura/modalità), al posto del doppio elenco di passaggi "con/senza robot"
- Le ricette esistenti vengono convertite automaticamente al nuovo formato al primo avvio, senza perdite: il vecchio metodo "senza robot" confluisce nelle note della ricetta

### Aggiunto
- Importazione di ricette da testo incollato o dal sorgente di una pagina web, con riconoscimento automatico dei dati strutturati quando disponibili, sempre da rivedere prima di salvare
- 12 nuove ricette di esempio (per un totale di 24), a coprire meglio tutte le categorie

## [1.3.1] — Documentazione ricette

### Aggiunto
- Cartella `ricette/` con un documento markdown leggibile/stampabile contenente tutte le 12 ricette tradizionali, ciascuna con metodo Monsieur Cuisine e metodo senza robot

## [1.3.0] — Metodo senza robot

### Aggiunto
- **Doppio metodo di preparazione**: ogni ricetta può avere sia i passaggi con il Monsieur Cuisine sia un metodo alternativo scritto per fornelli/forno tradizionali
- Interruttore nella vista di lettura per passare dal metodo "Con Monsieur Cuisine" al metodo "Senza robot"
- La modalità cucina guidata ora segue il metodo selezionato (robot o manuale)
- Le 12 ricette tradizionali incluse ora hanno anche il metodo senza robot scritto per ciascuna

## [1.2.0] — Funzioni avanzate

### Aggiunto
- **Esportazione/importazione backup JSON**: scarica tutte le ricette in un file `.json` e ricaricale su un altro dispositivo o dopo aver svuotato la cache del browser
- **Modalità cucina guidata**: naviga i passaggi di una ricetta a schermo intero, un passaggio alla volta, con font grande e timer integrato per i tempi di cottura
- **Timer per i passaggi**: countdown visivo con avviso sonoro al termine, avviabile direttamente durante la modalità cucina guidata
- **Foto per ricetta**: possibilità di allegare un'immagine a ogni ricetta, salvata localmente
- **Ricette preferite**: stellina per contrassegnare le ricette del cuore, con filtro dedicato "Solo preferite"
- **Cronologia "ultima preparazione"**: pulsante "Ho preparato questa oggi" che salva la data, visibile nella card e nella vista dettagliata
- **Lista della spesa automatica**: seleziona più ricette tramite la pianificazione settimanale e genera una lista aggregata degli ingredienti, con caselle di spunta e stampa dedicata
- **Pianificazione settimanale**: assegna una ricetta a ciascun giorno della settimana, come base per la lista della spesa
- **Stampa ricetta singola**: layout dedicato per la stampa pulita di una ricetta, senza elementi di interfaccia superflui

## [1.1.0] — Ricerca per ingredienti

### Aggiunto
- Pannello "Cosa posso cucinare?": inserendo gli ingredienti disponibili, il ricettario mostra le ricette realizzabili subito e quelle a cui mancano pochi ingredienti, evidenziandoli
- Colori distinti per ogni categoria di ricetta

## [1.0.0] — Prima versione

### Aggiunto
- Creazione, modifica ed eliminazione di ricette
- Ingredienti con quantità scalabili in base alle porzioni
- Passaggi con impostazioni robot (velocità, temperatura, tempo, modalità Normale/Reverse/Turbo/Vapore)
- Ricerca per nome/ingrediente e filtro per categoria
- Set di 12 ricette tradizionali laziali/ciociare importabili con un click
- Salvataggio locale tramite `localStorage`, nessun account o server richiesto
