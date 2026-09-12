# Aggiunta da inserire in cima a CHANGELOG.md

Non avendo il contenuto reale del tuo `CHANGELOG.md`, ecco una voce
pronta nello stesso formato tipico "versione + data + elenco puntato".
Sostituisci il numero di versione con quello che segue la tua
numerazione attuale, e la data con quella reale del rilascio.

---

## [Da assegnare] — 2026-09-12

### Aggiunto
- Integrazione della banca dati ufficiale **CREA** (Centro di ricerca
  Alimenti e Nutrizione) per i valori nutrizionali: ricerca 🔎
  direttamente da ogni riga ingrediente e da ogni prodotto Dispensa,
  con compilazione automatica di Kcal/proteine/grassi/carboidrati/
  fibre/zuccheri/sale in base alla quantità inserita
- Scheda nutrizionale completa (ℹ️) per ogni alimento collegato a CREA:
  oltre ai 7 valori usati nel calcolo, mostra zuccheri singoli,
  minerali, vitamine, acidi grassi, aminoacidi e altri composti
- Importazione con un clic delle 56 ricette ufficiali CREA dal menu
  "📋 Importa ricetta ▾ → 🇮🇹 Da ricette CREA", con categoria e
  porzioni assegnate automaticamente (sempre correggibili)
- Nuova vista **"🌾 CREA Alimenti"**: consultazione libera di tutti i
  900 alimenti della banca dati, con ricerca e filtro per categoria
- Nuova vista **"🇮🇹 CREA Menù"**: le 56 ricette ufficiali CREA
  sfogliabili con dettaglio (ingredienti, preparazione, valori
  nutrizionali del piatto) e importazione nel Ricettario

### Tecnico
- Nuovi file `data/crea-alimenti.json`, `data/crea-meta.json`,
  `data/crea-alimenti-completo.json`, `data/crea-nutrienti-schema.json`,
  `data/crea-ricette.json` e `js/crea-nutrition.js`, generati dagli
  script in `scripts/` a partire dal dataset ufficiale CREA
