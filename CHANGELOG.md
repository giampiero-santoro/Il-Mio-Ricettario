# Changelog

Tutte le modifiche rilevanti al progetto sono documentate in questo file.

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
