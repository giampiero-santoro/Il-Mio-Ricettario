/* Il Mio Ricettario — validazione e normalizzazione dei file di backup.
 *
 * Modulo PURO: non tocca localStorage né l'interfaccia. Riceve il contenuto già letto da un
 * file (JSON.parse) e restituisce o un errore comprensibile o i dati normalizzati, pronti
 * per essere applicati in un secondo momento, tutti insieme. Così un file malformato non può
 * mai lasciare l'app a metà.
 *
 * Tipi di file riconosciuti:
 *  - "completo": contiene l'intero stato (ricette, ricettari, raccolte, pianificazione,
 *    pasti, dispensa, liste della spesa, note). Va a SOSTITUIRE i dati in modo coerente.
 *  - "parziale": contiene solo una parte (es. solo le ricette, o un elenco di ricette).
 *    Va UNITO ai dati esistenti, senza cancellare nulla.
 *
 * Il modulo può normalizzare (cioè modificare) l'oggetto che riceve: chi lo chiama deve
 * considerarlo "consumato" e usare solo il risultato.
 */
(function(root){
  'use strict';

  const FORMATO = 'il-mio-ricettario';
  const VERSIONE_FORMATO = 1;
  const CHIAVI = ['recipes','ricettari','raccolte','weekPlan','planWeeks','mealTypes','dispensaItems','shoppingExtraItems','weekNotes','spesaLista'];
  const NOMI = {
    recipes:'ricette', ricettari:'ricettari', raccolte:'raccolte', weekPlan:'piano settimanale', planWeeks:'settimane pianificate',
    mealTypes:'tipi di pasto', dispensaItems:'dispensa', shoppingExtraItems:'spesa extra', weekNotes:'note della settimana', spesaLista:'lista della spesa'
  };
  const GIORNI = ['Lunedì','Martedì','Mercoledì','Giovedì','Venerdì','Sabato','Domenica'];

  const isObj = v => v !== null && typeof v === 'object' && !Array.isArray(v);
  const isStr = v => typeof v === 'string';
  const ko = msg => ({ ok:false, errore: msg });

  function idCasuale(){ return 'r_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2,8); }

  function contaStr(n, s, p){ return n + ' ' + (n === 1 ? s : p); }

  /** Elenco di oggetti (dispensa, spesa…): ogni voce deve essere un oggetto. */
  function listaOggetti(valore, chiave){
    if(!Array.isArray(valore)) return ko(`Nel file «${NOMI[chiave]}» non è un elenco: il file è danneggiato o non è un backup di questo ricettario.`);
    for(let i = 0; i < valore.length; i++){
      if(!isObj(valore[i])) return ko(`Nel file la voce n. ${i+1} di «${NOMI[chiave]}» non è valida.`);
    }
    return { ok:true, valore };
  }

  /** Voci di un giorno della pianificazione (sempre un elenco di oggetti). */
  function vociGiorno(v, opz, dove){
    if(v === undefined || v === null || v === '') return { ok:true, valore: [] };
    if(typeof v === 'string'){
      // vecchio formato: un solo id ricetta per giorno
      return { ok:true, valore: [{ id: opz.idGen(), recipeId: v, mealType: opz.pastoPredefinito, time: '' }] };
    }
    if(!Array.isArray(v)) return ko(`Nel file la pianificazione (${dove}) ha un formato non valido.`);
    for(let i = 0; i < v.length; i++){
      if(!isObj(v[i])) return ko(`Nel file la pianificazione (${dove}) contiene una voce non valida.`);
      if(v[i].id === undefined || v[i].id === null || v[i].id === '') v[i].id = opz.idGen();
    }
    return { ok:true, valore: v };
  }

  function pianoSettimana(piano, opz, dove){
    if(piano === undefined || piano === null) return { ok:true, valore:{} };
    if(!isObj(piano)) return ko(`Nel file la pianificazione (${dove}) ha un formato non valido.`);
    const out = {};
    for(const k of Object.keys(piano)){
      const r = vociGiorno(piano[k], opz, dove + ', ' + k);
      if(!r.ok) return r;
      out[k] = r.valore;
    }
    return { ok:true, valore: out };
  }

  function noteSettimana(note, dove){
    if(note === undefined || note === null) return { ok:true, valore:{} };
    if(!isObj(note)) return ko(`Nel file le note (${dove}) hanno un formato non valido.`);
    for(const k of Object.keys(note)){
      if(note[k] !== null && !isObj(note[k])) return ko(`Nel file le note del giorno «${k}» (${dove}) hanno un formato non valido.`);
    }
    const out = {};
    Object.keys(note).forEach(k => { if(note[k]) out[k] = note[k]; });
    return { ok:true, valore: out };
  }

  function validaChiave(chiave, v, opz, avvisi){
    switch(chiave){
      case 'recipes': {
        if(!Array.isArray(v)) return ko('Nel file «ricette» non è un elenco: il file è danneggiato o non è un backup di questo ricettario.');
        const visti = new Set();
        for(let i = 0; i < v.length; i++){
          const r = v[i];
          if(!isObj(r)) return ko(`Nel file la ricetta n. ${i+1} non è valida.`);
          if((!isStr(r.name) || !r.name.trim()) && isStr(r.title) && r.title.trim()) r.name = r.title; // vecchi file: «title» al posto di «name»
          if(!isStr(r.name) || !r.name.trim()) return ko(`Nel file la ricetta n. ${i+1} non ha un nome.`);
          for(const campo of ['ingredients','steps','tags','allergens','raccolte']){
            if(r[campo] !== undefined && r[campo] !== null && !Array.isArray(r[campo])) return ko(`Nel file la ricetta «${r.name}» ha il campo «${campo}» in un formato non valido.`);
          }
          if(r.photo !== undefined && r.photo !== null && !isStr(r.photo)) return ko(`Nel file la ricetta «${r.name}» ha una foto in un formato non valido.`);
          if(r.id === undefined || r.id === null || r.id === ''){ r.id = opz.idGen(); avvisi.push(`La ricetta «${r.name}» non aveva un identificativo: ne è stato creato uno.`); }
          else if(!isStr(r.id)) r.id = String(r.id);
          if(visti.has(r.id)){ r.id = opz.idGen(); avvisi.push(`La ricetta «${r.name}» compariva due volte con lo stesso identificativo: ne è stato creato uno nuovo.`); }
          visti.add(r.id);
        }
        return { ok:true, valore: v };
      }
      case 'ricettari': {
        if(!Array.isArray(v)) return ko('Nel file «ricettari» non è un elenco: il file è danneggiato o non è un backup di questo ricettario.');
        const visti = new Set(), out = [];
        for(let i = 0; i < v.length; i++){
          const rb = v[i];
          if(!isObj(rb) || !isStr(rb.id) || !rb.id || !isStr(rb.name)) return ko(`Nel file il ricettario n. ${i+1} non è valido.`);
          if(visti.has(rb.id)){ avvisi.push(`Il ricettario «${rb.name}» compariva due volte: tenuta la prima copia.`); continue; }
          visti.add(rb.id); out.push(rb);
        }
        return { ok:true, valore: out };
      }
      case 'raccolte': {
        if(!Array.isArray(v)) return ko('Nel file «raccolte» non è un elenco: il file è danneggiato o non è un backup di questo ricettario.');
        const out = [];
        v.forEach(x => {
          if(isObj(x) && x.id && x.name) out.push({ id: String(x.id), name: String(x.name) });
          else avvisi.push('Una raccolta senza nome o identificativo è stata ignorata.');
        });
        return { ok:true, valore: out };
      }
      case 'mealTypes': {
        if(!Array.isArray(v)) return ko('Nel file «tipi di pasto» non è un elenco: il file è danneggiato.');
        const out = [];
        for(const m of v){
          if(!isStr(m)) return ko('Nel file i tipi di pasto contengono un valore non valido.');
          const t = m.trim();
          if(t && !out.includes(t)) out.push(t);
        }
        return { ok:true, valore: out };
      }
      case 'dispensaItems': case 'shoppingExtraItems': case 'spesaLista':
        return listaOggetti(v, chiave);
      case 'weekPlan': {
        if(!isObj(v)) return ko('Nel file il piano settimanale non ha un formato valido.');
        return pianoSettimana(v, opz, 'piano settimanale');
      }
      case 'weekNotes': {
        if(!isObj(v)) return ko('Nel file le note della settimana non hanno un formato valido.');
        return noteSettimana(v, 'settimana');
      }
      case 'planWeeks': {
        if(!isObj(v)) return ko('Nel file le settimane pianificate non hanno un formato valido.');
        const out = {};
        for(const lun of Object.keys(v)){
          if(!/^\d{4}-\d{2}-\d{2}$/.test(lun)) return ko(`Nel file una settimana pianificata ha una data non valida («${lun}»).`);
          const w = v[lun];
          if(w !== null && !isObj(w)) return ko(`Nel file la settimana del ${lun} ha un formato non valido.`);
          const p = pianoSettimana(w && w.plan, opz, 'settimana ' + lun);
          if(!p.ok) return p;
          const n = noteSettimana(w && w.notes, 'settimana ' + lun);
          if(!n.ok) return n;
          out[lun] = { plan: p.valore, notes: n.valore };
        }
        return { ok:true, valore: out };
      }
    }
    return ko('Dato sconosciuto.');
  }

  /**
   * Analizza il contenuto di un file.
   * @returns {ok:false, errore} oppure {ok:true, tipo:'completo'|'parziale', marcato, dati, presenti, avvisi, conteggi}
   */
  function analizza(parsed, opzioni){
    const opz = Object.assign({ idGen: idCasuale, pastoPredefinito: 'Pranzo' }, opzioni || {});
    const avvisi = [];
    let grezzo, marcato = false, tipoDichiarato = null;

    if(Array.isArray(parsed)){
      grezzo = { recipes: parsed };
    }else if(isObj(parsed)){
      if(parsed.formato !== undefined){
        if(parsed.formato !== FORMATO) return ko('Il file non è un backup di Il Mio Ricettario.');
        marcato = true;
        const ver = Number(parsed.versioneFormato);
        if(parsed.versioneFormato !== undefined && (!isFinite(ver) || ver > VERSIONE_FORMATO)){
          return ko('Il file è stato creato da una versione più recente del ricettario. Aggiorna il sito (ricarica la pagina con Ctrl+Maiusc+R) e riprova: i tuoi dati non sono stati toccati.');
        }
        tipoDichiarato = parsed.tipoBackup === 'parziale' ? 'parziale' : 'completo';
      }
      grezzo = parsed;
    }else{
      return ko('Il file non contiene dati del ricettario.');
    }

    const presenti = CHIAVI.filter(k => grezzo[k] !== undefined);
    if(!presenti.length) return ko('Il file non contiene nessun dato riconoscibile del ricettario (ricette, dispensa, pianificazione…).');

    // Tipo: i file con marcatore dichiarano da sé se sono completi; i vecchi backup
    // (senza marcatore) sono completi se hanno la struttura che l'esportazione produceva.
    let tipo;
    if(marcato) tipo = tipoDichiarato;
    else if(Array.isArray(grezzo.recipes) && Array.isArray(grezzo.dispensaItems) && (grezzo.weekPlan !== undefined || grezzo.planWeeks !== undefined)) tipo = 'completo';
    else tipo = 'parziale';

    if(marcato && tipo === 'completo'){
      const mancanti = CHIAVI.filter(k => grezzo[k] === undefined);
      if(mancanti.length) return ko(`Il backup è incompleto o danneggiato: mancano ${mancanti.map(k => NOMI[k]).join(', ')}. I tuoi dati non sono stati toccati.`);
    }

    const dati = {};
    for(const k of presenti){
      const r = validaChiave(k, grezzo[k], opz, avvisi);
      if(!r.ok) return r;
      dati[k] = r.valore;
    }

    const conteggi = {
      ricette: (dati.recipes || []).length, ricettari: (dati.ricettari || []).length, raccolte: (dati.raccolte || []).length,
      dispensa: (dati.dispensaItems || []).length, settimane: Object.keys(dati.planWeeks || {}).length,
      spesa: (dati.spesaLista || []).length + (dati.shoppingExtraItems || []).length
    };
    return { ok:true, tipo, marcato, dati, presenti, avvisi, conteggi };
  }

  /** Riassunto leggibile di ciò che contiene il file. */
  function riassunto(c){
    const p = [contaStr(c.ricette, 'ricetta', 'ricette')];
    if(c.ricettari) p.push(contaStr(c.ricettari, 'ricettario', 'ricettari'));
    if(c.raccolte) p.push(contaStr(c.raccolte, 'raccolta', 'raccolte'));
    if(c.dispensa) p.push(contaStr(c.dispensa, 'prodotto in dispensa', 'prodotti in dispensa'));
    if(c.settimane) p.push(contaStr(c.settimane, 'settimana pianificata', 'settimane pianificate'));
    if(c.spesa) p.push(contaStr(c.spesa, 'voce della spesa', 'voci della spesa'));
    return p.join(' · ');
  }

  /** Intestazione da aggiungere ai file esportati. */
  function intestazione(tipoBackup, versioneApp){
    return { formato: FORMATO, versioneFormato: VERSIONE_FORMATO, tipoBackup: tipoBackup || 'completo', versioneApp: versioneApp || '', creatoIl: new Date().toISOString() };
  }

  const API = { analizza, riassunto, intestazione, CHIAVI, GIORNI, FORMATO, VERSIONE_FORMATO };
  if(typeof module !== 'undefined' && module.exports) module.exports = API;
  root.BackupImport = API;
})(typeof window !== 'undefined' ? window : globalThis);
