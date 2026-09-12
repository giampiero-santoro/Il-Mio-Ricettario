# Guida completa — Il Mio Ricettario

Questa guida spiega passo passo come usare tutte le funzioni del ricettario.

## Indice

1. [Avvio](#avvio)
2. [Aggiungere una ricetta](#aggiungere-una-ricetta)
3. [Importare una ricetta da testo](#importare-una-ricetta-da-testo)
4. [Esportare e importare una singola ricetta](#esportare-e-importare-una-singola-ricetta)
5. [Impostazioni robot per i passaggi (facoltative)](#impostazioni-robot-per-i-passaggi-facoltative)
6. [Impostazioni pentola a pressione (facoltative)](#impostazioni-pentola-a-pressione-facoltative)
7. [Valori nutrizionali (facoltativi)](#valori-nutrizionali-facoltativi)
8. [Tag dietetici](#tag-dietetici)
9. [Visualizzare e scalare le porzioni](#visualizzare-e-scalare-le-porzioni)
10. [Ricerca, filtri ed esclusione ingredienti](#ricerca-filtri-ed-esclusione-ingredienti)
11. [Cosa posso cucinare?](#cosa-posso-cucinare)
12. [Preferite, cronologia e contatore preparazioni](#preferite-cronologia-e-contatore-preparazioni)
13. [Modalità cucina guidata e timer](#modalità-cucina-guidata-e-timer)
14. [Pianificazione settimanale](#pianificazione-settimanale)
15. [Lista della spesa](#lista-della-spesa)
16. [Backup: esportazione e importazione](#backup-esportazione-e-importazione)
17. [Esportazione PDF](#esportazione-pdf)
18. [Esportare e importare CSV](#esportare-e-importare-csv)
19. [Modificare ed eliminare](#modificare-ed-eliminare)
20. [Dispensa](#dispensa)
21. [Salvataggio dei dati](#salvataggio-dei-dati)
22. [Dove vengono salvati e caricati i file](#dove-vengono-salvati-e-caricati-i-file)
23. [Domande frequenti](#domande-frequenti)

## Avvio

Apri il file `index.html` con un doppio click, oppure trascinalo in una finestra del browser. Non serve installare nulla né avere una connessione internet (a parte il primo caricamento dei font, che comunque non è obbligatorio per il funzionamento).

## Aggiungere una ricetta

1. Premi **"+ Nuova ricetta"** in alto
2. Compila nome, categoria, porzioni base e tempo totale
3. Se vuoi, seleziona i **tag dietetici** pertinenti e carica una **foto** — viene ridimensionata e compressa automaticamente prima di essere salvata, per occupare meno spazio nel browser
4. Aggiungi gli **ingredienti** uno per uno. Se lo stesso ingrediente (nome e unità di misura) finisce per comparire due volte, al momento di salvare il ricettario te lo segnala e propone di unire le righe sommando le quantità
5. Aggiungi i **passaggi** della preparazione (vedi sotto per le impostazioni robot facoltative)
6. Scrivi eventuali **note personali**
7. Premi **"Salva ricetta"**

Se chiudi il modulo (con la "×" o toccando fuori) mentre hai scritto qualcosa senza aver ancora salvato, il ricettario chiede conferma prima di buttare via le modifiche — capita anche provando a chiudere la scheda del browser o a navigare altrove. Vale anche per il modulo dei prodotti in Dispensa.

## Importare una ricetta da testo

1. Premi **"📋 Importa ricetta ▾"** e scegli **"Da testo o link"**
2. Incolla il testo di una ricetta trovata online, in un libro, o altrove — oppure, per un riconoscimento più preciso, il codice sorgente della pagina web che la contiene (tasto destro sulla pagina → "Visualizza sorgente", poi Ctrl/Cmd+A e copia)
3. Premi **"Analizza e compila"**: il ricettario cerca prima dati strutturati nella pagina (usati da molti siti di ricette) e, se non li trova, prova un riconoscimento più libero dal testo
4. Si apre il modulo di modifica già precompilato: **controlla e correggi ogni campo** — soprattutto quantità e categoria — prima di premere "Salva ricetta". Il riconoscimento automatico è un aiuto, non è mai perfetto

## Esportare e importare una singola ricetta

A differenza del backup e del CSV, che riguardano tutte le ricette insieme, puoi anche scambiare **una ricetta alla volta** come file — comodo per mandarla a qualcuno che usa anche lui questo ricettario:

- Dalla scheda di una ricetta, **"⬇ Esporta ▾" → "⬇ Esporta ricetta (.json)"** scarica un file `.json` con solo quella ricetta
- **"📋 Importa ricetta ▾" → "Da file (.json)"** legge un file esportato così e lo aggiunge alle tue ricette
- Chi riceve la ricetta parte "pulito": preferita, cronologia e contatore delle preparazioni non vengono copiati da chi l'ha esportata
- Se hai già una ricetta con lo stesso nome, l'importazione si ferma per evitare doppioni — rinominala prima di riprovare

## Impostazioni robot per i passaggi (facoltative)

Ogni passaggio si scrive in modo normale, come faresti per qualsiasi ricetta. Se in quel passaggio usi un robot da cucina, premi **"🤖 Impostazioni robot"** sotto il testo del passaggio per aggiungere:

- **Velocità** (0-10)
- **Temperatura** in °C (0-130)
- **Modalità**: Normale, Reverse (mescola senza tritare), Turbo (sminuzza alla massima velocità), Vapore

Il campo **Durata (min)** è invece sempre visibile: serve anche da timer nella modalità cucina guidata, che tu usi un robot oppure no.

## Impostazioni pentola a pressione (facoltative)

Come per il robot, se in un passaggio usi la pentola a pressione premi **"🍲 Impostazioni pentola a pressione"** sotto il testo del passaggio per aggiungere:

- **Pressione**: un numero, con l'unità che preferisci (Bar, PSI o kPa) — puoi usare unità diverse per ricette diverse, il ricettario non fa conversioni tra loro
- **Rilascio**: Naturale, Rapido, oppure Misto (un po' naturale e poi rapido)
- **Durata rilascio (min)**: quanto dura il rilascio naturale — non compare se scegli "Rapido", perché in quel caso non c'è attesa. Questa durata alimenta un **timer separato** da quello della cottura in pressione, sia nella scheda della ricetta sia in modalità cucina guidata
- **Liquido minimo (ml)**: promemoria della quantità minima di liquido necessaria per fare pressione — non è un ingrediente della ricetta, è un avviso tecnico

Nel modulo di modifica trovi anche, accanto a porzioni e tempo, un campo facoltativo **"Tipo pentola a pressione"** (Elettrica / A fornello) valido per l'intera ricetta.

Le ricette mostrano automaticamente un'etichetta del metodo di cottura, nella lista e nella scheda, dedotta dai passaggi — non serve spuntare nulla a mano: **🍲** se c'è almeno un passaggio a pressione, **🤖** se c'è almeno un passaggio con impostazioni robot, **🔥 Tradizionale** se non ne ha nessuno dei due. Una ricetta che usa entrambi i metodi mostra sia 🍲 sia 🤖.

## Valori nutrizionali (facoltativi)

Il ricettario non ha un database nutrizionale: i valori li inserisci tu (ad esempio copiandoli da un'etichetta), e il ricettario fa i conti al posto tuo.

1. Nel modulo di modifica, premi **"🍎 Valori nutrizionali"** vicino agli ingredienti: compaiono per ogni ingrediente i campi Kcal, Proteine, Grassi, Carboidrati, Fibre, Zuccheri e Sale
2. Inserisci i valori **riferiti alla quantità di quell'ingrediente così com'è scritta nella ricetta** (non per 100g) — puoi compilarli anche solo per alcuni ingredienti, se non conosci gli altri
3. Nella scheda della ricetta compare un riepilogo con il totale e il valore per porzione, che si ricalcola da solo quando cambi le porzioni con il +/−
4. Il riepilogo è incluso anche nell'**"⬇ Esporta PDF"** della ricetta
5. Se non hai inserito i dati per tutti gli ingredienti, il riepilogo (e il PDF) lo segnala, così sai che il totale reale potrebbe essere più alto

## Tag dietetici

Nel modulo di modifica puoi selezionare uno o più tag: Vegetariano, Vegano, Senza glutine, Senza lattosio, Piccante. Compaiono nella scheda della ricetta e si possono usare come filtro nella lista (vedi sezione successiva).

## Visualizzare e scalare le porzioni

Cliccando su una ricetta si apre la vista di lettura, con ingredienti, passaggi numerati e un controllo **+/−** per aumentare o diminuire le porzioni: le quantità si ricalcolano automaticamente in proporzione.

## Ricerca, filtri ed esclusione ingredienti

- Il campo di ricerca cerca sia nel nome della ricetta sia negli ingredienti
- Il menu a tendina filtra per categoria
- Il menu a tendina accanto alla categoria cambia l'ordine della lista: Nome (A-Z o Z-A), Aggiunta di recente, Ultima preparata, Più preparate — di base è per nome (A-Z)
- **"★ Solo preferite"** mostra solo le ricette con la stellina
- **"🔍 Filtri"** apre un pannello con altre opzioni, tenute nascoste di default per non affollare la pagina — il pulsante mostra tra parentesi quanti filtri sono attivi (es. "🔍 Filtri (2)"):
  - **Metodo di cottura**: "🍲 Pentola a pressione" (almeno un passaggio a pressione), "🤖 Robot" (almeno un passaggio con velocità, temperatura o una modalità diversa da Normale), "🔥 Tradizionale" (nessuna impostazione robot né pressione) — si possono combinare liberamente tra loro
  - **"Escludi ingredienti"**, che nasconde le ricette contenenti uno o più ingredienti scritti lì (separati da virgola) — utile per allergie o cose che non vuoi usare in quel momento
  - le "pillole" per il tag dietetico (puoi selezionarne più di una insieme)

## Cosa posso cucinare?

Usa automaticamente i prodotti che hai già in **Dispensa** — non serve più riscriverli a mano:

1. Se vuoi, scrivi nel campo anche altri ingredienti che hai ma non sono in Dispensa (es. erbe fresche, avanzi), separati da virgola — la lista resta salvata anche se chiudi e riapri il ricettario
2. Premi **"Trova ricette"** (funziona anche a campo vuoto, se hai già qualcosa in Dispensa)
3. Le ricette si ordinano per numero di ingredienti mancanti, con badge verde **"✓ Puoi farla"** o arancione **"Manca X ingr."**
4. Premi **"Mostra tutte"** per tornare alla visualizzazione normale

Il confronto riconosce varianti semplici (es. "pomodoro" riconosce "pomodori pelati"), ma è un controllo testuale di base. Se aggiorni la Dispensa mentre questa vista è attiva, l'elenco delle ricette si aggiorna da solo.

## Preferite, cronologia e contatore preparazioni

- La stellina ★ contrassegna una ricetta come preferita; il pulsante **"★ Solo preferite"** filtra rapidamente
- Nella vista dettagliata, **"Ho preparato questa oggi"** registra la data e aggiorna il contatore di quante volte hai preparato quella ricetta, entrambi visibili nella card e nella vista

## Modalità cucina guidata e timer

1. Apri una ricetta e premi **"👩‍🍳 Modalità cucina"**
2. Un passaggio alla volta, a caratteri grandi
3. **"← Indietro"** / **"Avanti →"** per navigare
4. Se il passaggio ha una durata, premi **"Avvia timer"**: countdown visivo con avviso sonoro al termine
5. Se il passaggio ha anche un rilascio pressione con una durata (Naturale o Misto), compare un secondo pulsante **"Avvia timer rilascio"**, con il proprio countdown indipendente dal primo
6. **"Esci ✕"** per tornare alla vista normale

## Pianificazione settimanale

La pianificazione è una vista separata dal ricettario: premi **"📅 Pianificazione"** in alto per aprirla.

Puoi anche saltare la ricerca e pianificare al volo mentre guardi una ricetta: nella sua scheda, premi **"📅 Pianifica"** per scegliere giorno, fascia e orario facoltativo senza uscire dalla vista. Il pannello resta aperto dopo ogni aggiunta, così puoi assegnare la stessa ricetta a più giorni di seguito.

- Si vede **un giorno alla volta**, come una scheda: usa le linguette in alto (Lun, Mar, Mer…) per saltare a un giorno preciso, oppure le frecce ‹ › ai lati per andare al giorno prima/dopo. Si apre già sul giorno di oggi
- Ogni giorno è diviso in **fasce pasto** (di base: Colazione, Pranzo, Spuntino, Cena) e ciascuna fascia può contenere più ricette
- Premi **"+ Aggiungi fascia pasto"** per crearne di nuove (es. "Aperitivo"); il cestino su una fascia la rimuove — le ricette già assegnate a quella fascia restano visibili sotto "Altro", non si perdono
- Per aggiungere una ricetta: imposta prima l'**orario facoltativo**, poi premi **"🔍 Cerca ricetta…"** — si apre una finestra dove puoi cercare per nome o ingrediente e toccare quella che vuoi, invece di scorrere un elenco lungo
- Quando aggiungi una ricetta alla pianificazione (da qui o dal pulsante "📅 Pianifica" nella sua scheda), il ricettario controlla i suoi ingredienti rispetto a quello che hai segnato nella Dispensa: se qualcosa manca, te lo segnala e ti chiede conferma prima di aggiungerlo a un promemoria per la lista della spesa
- Per aggiungere invece un prodotto della Dispensa come pasto (es. uno yogurt a colazione, della frutta come spuntino): imposta l'orario facoltativo e premi **"🥫 Dalla dispensa…"** — si apre una finestra di ricerca sui prodotti che hai in dispensa, allo stesso modo di quella delle ricette. Scelto il prodotto, viene chiesta una **quantità facoltativa** per quel pasto (precompilata con quella che hai in dispensa, ma modificabile): se la indichi, compare accanto al nome nella pianificazione
- Le voci di ogni fascia si ordinano da sole per orario
- Clicca sul nome di una voce pianificata per aprirne la scheda: quelle con l'etichetta 🥫 aprono la scheda del prodotto in Dispensa, le altre la scheda della ricetta
- **"✓"** su una voce pianificata la segna come consumata e prova ad aggiornare la Dispensa di conseguenza (chiede sempre conferma, mostrando cosa sta per cambiare):
  - per un pasto aggiunto **"dalla dispensa"**, se avevi indicato una quantità nella stessa unità di misura del prodotto, quella quantità viene tolta dal prodotto
  - per un pasto da **ricetta**, il ricettario cerca tra i prodotti in Dispensa un nome identico agli ingredienti, oppure — se non c'è — un nome simile ma solo quando è candidato un unico prodotto (le quantità sono scalate in base a "per quante persone" impostato in Pianificazione), e toglie la quantità usata solo dove l'unità di misura coincide esattamente — altrimenti lascia il prodotto invariato e te lo segnala. Se i prodotti con un nome simile sono più di uno (es. "Farina 00" e "Farina integrale" per l'ingrediente "Farina"), non ne tocca nessuno e te li elenca entrambi, per lasciare a te la scelta
  - una volta confermato, il segno di spunta resta acceso e accanto compare **"↺"**: lo tocchi per annullare, il che riporta il pasto a "da consumare" e ripristina in Dispensa (dove il prodotto esiste ancora) quanto era stato tolto
- **"Svuota settimana"** cancella tutta la pianificazione, tutti i giorni compresi (chiede conferma) — prima di farlo, il ricettario salva automaticamente una copia come "settimana scorsa"
- **"📋 Copia settimana scorsa"** ripristina quella copia al posto della pianificazione attuale (chiede conferma, perché la sovrascrive). Non è legata a un calendario reale: è semplicemente l'ultima pianificazione che avevi prima dell'ultima volta che hai premuto "Svuota settimana"

## Lista della spesa

Puoi generare la lista della spesa a tre livelli diversi, a seconda di cosa ti serve in quel momento:

- **Per l'intera settimana pianificata**: nella vista Pianificazione, imposta prima **"Per quante persone stai pianificando?"** — le quantità verranno scalate di conseguenza rispetto alle porzioni base di ogni ricetta — poi premi **"🛒 Lista della spesa (settimana)"**. Il ricettario somma gli ingredienti di tutte le ricette pianificate nei sette giorni, raggruppandoli per nome e unità. I prodotti aggiunti dalla Dispensa non vengono conteggiati, dato che li hai già in casa. Compaiono anche gli ingredienti segnalati come mancanti dalla Dispensa quando hai pianificato una ricetta (etichetta "dalla dispensa"), anche se per questa settimana non hai ripianificato quella ricetta — restano come promemoria finché non li spunti, oppure finché un ingrediente con lo stesso nome non compare già tra quelli di un'altra ricetta pianificata per la settimana in corso
- **Per un singolo giorno**: nella vista Pianificazione, apri il giorno che ti interessa con le linguette o le frecce ‹ ›, poi premi **"🛒 Lista della spesa del giorno"** sotto al titolo del giorno. Include solo le ricette assegnate a quel giorno (scalate sempre in base a "per quante persone"), senza i promemoria dalla Dispensa, che non sono legati a un giorno preciso
- **Per una singola ricetta**: apri la ricetta e premi **"🛒 Lista della spesa"** nella sua scheda. Include solo gli ingredienti di quella ricetta, scalati alle porzioni che stai visualizzando in quel momento (indipendenti da "per quante persone" della Pianificazione)

In tutti e tre i casi si apre la stessa finestra: spunta gli ingredienti man mano che li acquisti ed ognuno viene anche aggiunto alla Dispensa (o la sua quantità aumentata, se già presente con la stessa unità di misura) — un piccolo avviso conferma quanti prodotti sono stati aggiornati. Per quelli con l'etichetta "dalla dispensa" (presenti solo nella lista della settimana), spuntarli li toglie anche definitivamente dal promemoria. Togliere la spunta non annulla l'aggiornamento in Dispensa. Premi **"⬇ Esporta PDF"** per scaricarla come file.

Ogni ingrediente che compare più volte (anche da ricette diverse, se pianifichi più ricette nella stessa lista) viene sommato in un'unica riga, purché il nome e l'unità di misura coincidano esattamente.

**Controllo incrociato con la Dispensa**: se un ingrediente della lista corrisponde a un prodotto che hai già segnato in Dispensa, sotto la riga compare un avviso. Il ricettario cerca prima un prodotto con lo stesso nome; se non lo trova, prova anche una corrispondenza più elastica come quella di "Cosa posso cucinare?" (utile per varianti dello stesso ingrediente, es. "Farina" nella ricetta e "Farina 00" in Dispensa) — ma solo quando è candidato un unico prodotto: se ce ne sono più di uno possibile, ti vengono elencati ma senza sottrazione automatica, per non rischiare di sbagliare
- Se la quantità in Dispensa è nella stessa unità di misura (oppure in un'unità equivalente convertibile automaticamente: grammi/chilogrammi, millilitri/centilitri/litri) compare **"Sottrai dalla lista"**: un tocco toglie quella quantità da quella da acquistare, così compri solo quello che ti manca davvero. Se quello che hai in Dispensa basta o avanza, la riga si aggiorna con "già in Dispensa" e la casella si disabilita, perché non serve comprarne altro
- Dopo aver sottratto, compare **"Annulla"** al posto di "Sottrai dalla lista": riporta la riga alla quantità originale, comodo se hai premuto per sbaglio o hai cambiato idea
- Se l'unità di misura non è convertibile automaticamente (es. "pezzi" contro "grammi") o la quantità in Dispensa non è indicata, compare comunque un avviso che te lo ricorda, ma senza sottrazione automatica: la conversione resta a te
- **"🥫 Sottrai tutto"**, sopra "⬇ Esporta PDF", applica in un solo tocco tutte le sottrazioni disponibili in quel momento nella lista, senza doverle confermare una per una


## Backup: esportazione e importazione

Tutte le funzioni di questa sezione e della prossima si trovano sotto il menu **"📦 Backup e CSV"** in alto, per non affollare la pagina. In cima al menu trovi anche un promemoria discreto ("Ultimo backup: X giorni fa"), che diventa rosso dopo due settimane senza backup.

- **Esporta backup**: scarica un file `.json` con tutte le ricette, la pianificazione settimanale, le fasce pasto personalizzate e i promemoria di ingredienti mancanti dalla Dispensa. Fallo periodicamente, o prima di cancellare i dati del browser
- **Importa backup**: seleziona un file `.json` esportato in precedenza per ricaricare i dati. Le ricette e i prodotti Dispensa nuovi (identificativo non già presente) vengono sempre aggiunti; se il backup contiene anche voci già presenti (stesso identificativo — capita importando un backup più recente esportato da un altro dispositivo), ti viene chiesto una volta se sostituirle con la versione dal backup oppure lasciarle come sono. Alla fine un riepilogo ti dice quante ne sono state aggiunte, aggiornate o lasciate invariate

## Esportazione PDF

- Dalla vista di una ricetta, il menu **"⬇ Esporta ▾"** offre **"⬇ Esporta PDF"** per scaricarla come file (con ingredienti già scalati alle porzioni che stai visualizzando)
- Dalla lista della spesa (settimana, giorno o singola ricetta), **"⬇ Esporta PDF"** scarica la lista come file
- Dalla vista Pianificazione, **"⬇ Esporta PDF settimana"** scarica un file con il piano di tutti i giorni insieme alla lista della spesa aggregata
- Il PDF è generato interamente dal ricettario stesso (nessun servizio esterno): supporta più pagine e le lettere accentate italiane; eventuali emoji o simboli non standard nel testo vengono sostituiti con "?"
- Non è più disponibile la stampa diretta dal browser (la finestra "Stampa" di sistema): su alcuni dispositivi, in particolare mobile, produceva un foglio vuoto. L'esportazione PDF sostituisce completamente questa funzione ed è più affidabile, perché genera un file scaricabile senza passare dalla finestra di stampa

## Esportare e importare CSV

Oltre al backup JSON completo, puoi scambiare le ricette in formato CSV (una riga per ricetta), comodo per aprirle in Excel o Fogli Google:

- **"⬇ Esporta CSV"** scarica un file `.csv` con tutte le tue ricette: nome, categoria, porzioni, tempo, tag, ingredienti e passaggi sono ciascuno in una colonna. Dentro la stessa cella, più ingredienti o passaggi sono separati da " | "
- **"⬆ Importa CSV"** legge un file con lo stesso formato (le colonne Nome, Ingredienti e Passaggi sono obbligatorie) e aggiunge le ricette che non hai già (il confronto è per nome). Per quelle che invece corrispondono a un nome già presente, ti viene chiesto una volta se sostituirle con la versione dal CSV o lasciarle come sono — se scegli di sostituirle, foto, preferita e cronologia della ricetta esistente restano invariate, dato che il CSV non le contiene
- Il riconoscimento di quantità/unità negli ingredienti e delle impostazioni robot nei passaggi è automatico ma approssimativo, soprattutto se modifichi il CSV a mano: controlla sempre le ricette importate

## Modificare ed eliminare

- Dalla vista di una ricetta, **"Modifica"** per aprirla in modalità editing
- **"⧉ Duplica"** crea una copia della ricetta (con "(copia)" nel nome) e la apre subito in modifica, senza toccare l'originale — comodo per creare varianti, es. una versione vegetariana, senza riscrivere tutto da capo
- **"Elimina ricetta"** la rimuove definitivamente (chiede conferma) e la toglie automaticamente anche dalla pianificazione settimanale

## Dispensa

La Dispensa è una sezione separata dal ricettario, per tenere traccia di quello che hai in casa — non ricette, ma prodotti veri e propri come frutta, verdura, salumi, yogurt: premi **"🥫 Dispensa"** in alto per aprirla.

1. Premi **"+ Nuovo prodotto"**
2. Scrivi il nome e scegli una categoria tra quelle disponibili: dai freschi (Frutta, Verdura, Uova, Salumi, Latticini e pronti) ai Surgelati, fino alla dispensa vera e propria (Pasta/riso e cereali, Legumi, Farine/zucchero e lieviti, Conserve e scatolame, Spezie e condimenti, Oli/aceti e grassi, Bevande, Snack e dolciumi), oppure Altro per tutto il resto
3. Quantità, unità, data di scadenza e note sono tutte facoltative
4. Se vuoi, premi **"🍎 Valori nutrizionali"** per aggiungere Kcal, Proteine, Grassi, Carboidrati, Fibre, Zuccheri e Sale, riferiti alla quantità indicata sopra (non ai 100g) — utile ad esempio per uno yogurt o un affettato già confezionato
5. Premi **"Salva prodotto"**

Nell'elenco, i prodotti si ordinano da soli mettendo prima quelli con la scadenza più vicina: le scadenze già passate sono evidenziate in rosso, quelle entro 3 giorni in arancione. Se hai inserito le kcal, compaiono anche nella card, accanto alla quantità. Cerca per nome o filtra per categoria con i controlli in alto. Clicca su un prodotto per modificarlo o eliminarlo.

Un prodotto della Dispensa si può anche pianificare direttamente come pasto nella Pianificazione settimanale (vedi sezione successiva) — comodo per cose semplici come uno yogurt a colazione o della frutta come spuntino, senza dover creare una ricetta apposta.

I prodotti della Dispensa sono inclusi nel backup JSON, insieme alle ricette e alla pianificazione.

## Salvataggio dei dati

Tutto è salvato nel `localStorage` del browser che stai usando:

- Non serve connessione internet per salvare o leggere i dati
- I dati **non si sincronizzano** automaticamente tra browser o dispositivi diversi — usa il backup per trasferirli
- Se cancelli i dati di navigazione del browser (cache, cookie, dati dei siti), tutto viene perso
- Lo spazio disponibile non è illimitato (di solito qualche MB): le foto delle ricette vengono ridimensionate e compresse automaticamente per occuparne meno. Se nonostante questo lo spazio dovesse esaurirsi, un avviso ti informa che il salvataggio non è andato a buon fine, invece di fallire senza dirtelo — a quel punto conviene esportare subito un backup e liberare un po' di spazio (es. riducendo il numero di foto)

## Dove vengono salvati e caricati i file

- **Caricare un file** (Importa backup, Importa CSV): si apre sempre la finestra di scelta file del tuo dispositivo, dove puoi navigare in qualsiasi cartella o servizio collegato (es. Google Drive, iCloud Drive) per scegliere il file da importare
- **Salvare un file** (backup, CSV, PDF): su Chrome o Edge da computer, si apre una finestra "Salva con nome" dove scegli tu la cartella e il nome del file. Su cellulare, e su Safari o Firefox in generale, questo non è ancora possibile per limiti del browser stesso: il file viene scaricato automaticamente nella cartella "Download" predefinita del dispositivo, da cui potrai comunque spostarlo o condividerlo in un secondo momento

## Domande frequenti

**Posso usarlo su più dispositivi?**
Sì, ma ogni dispositivo/browser avrà il proprio set di dati salvati localmente, non sincronizzato — usa esporta/importa backup per spostarli.

**Il riconoscimento automatico nell'importazione da testo funziona sempre?**
No: funziona meglio con pagine di ricette che includono dati strutturati (la maggior parte dei blog di cucina seri li ha). Con testo libero il riconoscimento è più approssimativo. In ogni caso, controlla sempre i campi prima di salvare.

**Posso aggiungere altre categorie o altri tag dietetici?**
Le categorie e i tag disponibili sono fissi nel codice. Se vuoi personalizzarli, puoi modificare gli elenchi nel file `index.html` (cerca `CATEGORY_COLORS` per le categorie delle ricette, `PANTRY_CATEGORY_COLORS` per quelle della Dispensa, e `TAG_OPTIONS` per i tag dietetici). Le **fasce pasto** della pianificazione, invece, si possono già aggiungere e rimuovere direttamente dall'app, senza toccare il codice.
