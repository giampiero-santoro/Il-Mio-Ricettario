/* Il Mio Ricettario — impostazioni per pentola a pressione elettrica (tipo Instant Pot).
 *
 * Modulo PURO (nessun accesso a pagina o memoria del browser): funzioni, valori predefiniti,
 * riepilogo leggibile e avvisi. Tutti i campi del passaggio sono facoltativi: un passaggio senza
 * `fn` resta solo testo (o usa i vecchi campi pressure/pressureRelease/minLiquid, invariati).
 *
 * Campi del passaggio (tutti facoltativi):
 *   fn           saute | pressione | lenta | vapore | caldo | yogurt | riso | zuppa | fagioli | carne | porridge | dolci
 *   level        bassa | media | alta   (sauté: livello; pressione/programmi: alta o bassa; cottura lenta: bassa o alta)
 *   time         durata in minuti (la cottura lenta si inserisce in ore, ma si salva in minuti)
 *   pressureRelease  Naturale | Rapido | Misto     (già esistente)
 *   pressureReleaseMin  minuti di rilascio naturale (già esistente; con «Misto»: naturale per N minuti, poi rapido)
 *   minLiquid    liquido minimo in ml   (già esistente)
 *   valve        chiusa | sfiato
 *   fillMax      1/2 | 2/3              livello massimo di riempimento
 *   accessories  [cestello, trepiede, stampo, pentola-nella-pentola, alluminio]
 * Campo della ricetta: potLiters ("3", "6" o "8"; se manca si usa 6).
 */
(function(root){
  'use strict';

  const FUNZIONI = {
    saute:    { label: 'Rosolatura / Sauté', gruppo: 'calore',    livelli: ['bassa', 'media', 'alta'], livelloEtichette: { bassa: 'basso', media: 'medio', alta: 'alto' } },
    pressione:{ label: 'Pressione manuale',  gruppo: 'pressione', livelli: ['alta', 'bassa'] },
    lenta:    { label: 'Cottura lenta',      gruppo: 'lenta',     livelli: ['bassa', 'alta'] },
    vapore:   { label: 'Vapore',             gruppo: 'pressione', livelli: [] },
    caldo:    { label: 'Mantenimento caldo', gruppo: 'calore',    livelli: [] },
    yogurt:   { label: 'Yogurt',             gruppo: 'calore',    livelli: [] },
    riso:     { label: 'Programma Riso',         gruppo: 'pressione', livelli: ['alta', 'bassa'], programma: true },
    zuppa:    { label: 'Programma Zuppa/Brodo',  gruppo: 'pressione', livelli: ['alta', 'bassa'], programma: true },
    fagioli:  { label: 'Programma Fagioli',      gruppo: 'pressione', livelli: ['alta', 'bassa'], programma: true },
    carne:    { label: 'Programma Carne/Stufato',gruppo: 'pressione', livelli: ['alta', 'bassa'], programma: true },
    porridge: { label: 'Programma Porridge',     gruppo: 'pressione', livelli: ['alta', 'bassa'], programma: true },
    dolci:    { label: 'Programma Dolci',        gruppo: 'pressione', livelli: ['alta', 'bassa'], programma: true }
  };
  const ORDINE_FUNZIONI = ['pressione', 'saute', 'lenta', 'vapore', 'caldo', 'yogurt', 'riso', 'zuppa', 'fagioli', 'carne', 'porridge', 'dolci'];

  // Valori suggeriti (sempre modificabili). Tempi tipici da manuale, da verificare sul proprio modello.
  const PREDEFINITI = {
    saute:    { level: 'media', time: 5 },
    pressione:{ level: 'alta', time: 10, valve: 'chiusa', pressureRelease: 'Rapido' },
    lenta:    { level: 'bassa', time: 360, valve: 'sfiato' },
    vapore:   { time: 5, valve: 'chiusa', pressureRelease: 'Rapido' },
    caldo:    { time: 30, valve: 'sfiato' },
    yogurt:   { time: 480, valve: 'sfiato' },
    riso:     { level: 'alta', time: 4,  valve: 'chiusa', pressureRelease: 'Naturale', pressureReleaseMin: 10 },
    zuppa:    { level: 'alta', time: 30, valve: 'chiusa', pressureRelease: 'Naturale', pressureReleaseMin: 15 },
    fagioli:  { level: 'alta', time: 25, valve: 'chiusa', pressureRelease: 'Naturale', pressureReleaseMin: 20 },
    carne:    { level: 'alta', time: 35, valve: 'chiusa', pressureRelease: 'Naturale', pressureReleaseMin: 15 },
    porridge: { level: 'alta', time: 10, valve: 'chiusa', pressureRelease: 'Naturale', pressureReleaseMin: 10 },
    dolci:    { level: 'alta', time: 30, valve: 'chiusa', pressureRelease: 'Naturale', pressureReleaseMin: 10 }
  };

  const ACCESSORI = {
    cestello: 'cestello/vaporiera', trepiede: 'trepiede', stampo: 'stampo (es. springform)',
    'pentola-nella-pentola': 'pentola nella pentola', alluminio: 'alluminio'
  };
  const ACC_BREVE = { cestello: 'cestello', trepiede: 'trepiede', stampo: 'stampo', 'pentola-nella-pentola': 'pentola nella pentola', alluminio: 'alluminio' };
  const VALVOLE = { chiusa: 'valvola chiusa', sfiato: 'valvola su sfiato' };
  const RIEMPIMENTO = { '1/2': 'metà', '2/3': 'due terzi' };

  const info = fn => FUNZIONI[fn] || null;
  const usaPressione = fn => !!(info(fn) && info(fn).gruppo === 'pressione');

  /** Valori suggeriti per una funzione, uniti a quelli usati l'ultima volta (se forniti). */
  function valoriPredefiniti(fn, ultimi){
    const base = Object.assign({}, PREDEFINITI[fn] || {});
    if(ultimi && typeof ultimi === 'object'){
      ['level', 'time', 'valve', 'pressureRelease', 'pressureReleaseMin', 'minLiquid', 'fillMax'].forEach(k => {
        if(ultimi[k] !== undefined && ultimi[k] !== null && ultimi[k] !== '') base[k] = ultimi[k];
      });
    }
    return base;
  }

  function durata(min){
    const m = Math.round(Number(min));
    if(!isFinite(m) || m <= 0) return '';
    const h = Math.floor(m / 60), r = m % 60;
    if(!h) return m + ' min';
    return r ? `${h} h ${r} min` : `${h} h`;
  }

  function accessoriDi(s){
    return (Array.isArray(s.accessories) ? s.accessories : []).filter(a => ACCESSORI[a]);
  }

  /** Rilascio come testo: «naturale completo», «naturale 10 min», «naturale 10 min, poi rapido», «rapido». */
  function testoRilascio(s){
    const r = s.pressureRelease;
    const n = Number(s.pressureReleaseMin);
    if(r === 'Rapido') return 'rilascio rapido';
    if(r === 'Misto') return n > 0 ? `rilascio naturale ${n} min, poi rapido` : 'rilascio misto (naturale, poi rapido)';
    if(r === 'Naturale') return n > 0 ? `rilascio naturale ${n} min` : 'rilascio naturale completo';
    return '';
  }

  /**
   * Riepilogo leggibile di un passaggio con `fn`, per esempio
   * «pressione alta 20 min, rilascio naturale 10 min, liquido min 250 ml, valvola chiusa».
   * Restituisce '' se il passaggio non usa la pentola (resta solo testo).
   */
  function riepilogo(s){
    const f = info(s && s.fn);
    if(!f) return '';
    const parti = [];
    const t = durata(s.time);
    const lv = s.level;
    if(s.fn === 'saute'){
      parti.push('sauté' + (lv && f.livelloEtichette[lv] ? ' ' + f.livelloEtichette[lv] : '') + (t ? ' ' + t : ''));
    }else if(s.fn === 'pressione'){
      parti.push('pressione' + (lv ? ' ' + lv : '') + (t ? ' ' + t : ''));
    }else if(s.fn === 'lenta'){
      parti.push('cottura lenta' + (lv ? ' ' + lv : '') + (t ? ' ' + t : ''));
    }else if(s.fn === 'vapore'){
      parti.push('vapore' + (t ? ' ' + t : ''));
    }else if(s.fn === 'caldo'){
      parti.push('mantenimento caldo' + (t ? ' ' + t : ''));
    }else if(s.fn === 'yogurt'){
      parti.push('yogurt' + (t ? ' ' + t : ''));
    }else{
      const nome = f.label.replace('Programma ', '').toLowerCase();
      parti.push(`programma ${nome}` + (lv ? `, pressione ${lv}` : '') + (t ? ' ' + t : ''));
    }
    if(usaPressione(s.fn)){
      const rel = testoRilascio(s);
      if(rel) parti.push(rel);
    }
    if(s.minLiquid) parti.push(`liquido min ${s.minLiquid} ml`);
    if(s.valve && VALVOLE[s.valve]) parti.push(VALVOLE[s.valve]);
    if(s.fillMax && RIEMPIMENTO[s.fillMax]) parti.push(`riempimento max ${s.fillMax === '1/2' ? '1/2' : '2/3'}`);
    const acc = accessoriDi(s);
    if(acc.length) parti.push('con ' + acc.map(a => ACC_BREVE[a]).join(', '));
    return parti.join(', ');
  }

  // ---------- Avvisi (non bloccanti) ----------
  const RE_NATURALE = /\b(ceci|fagiol\w*|lenticch\w*|cicerchi\w*|fave|piselli secchi|legumi|riso|orzo|farro|avena|cereali|pasta|spaghetti|penne|fusilli|rigatoni|maccheroni|latte|panna|farina)\b/i;
  const RE_LATTE_NO = /latte di cocco|latte di mandorla|pasta di acciughe|pasta di (?:pomodoro|peperoncino|curry)|farina di cocco/i;

  function mlDi(ing){
    const q = parseFloat(String(ing && ing.qty).replace(',', '.'));
    if(!isFinite(q) || q <= 0) return 0;
    const u = String(ing.unit || '').trim().toLowerCase();
    if(u === 'ml') return q;
    if(u === 'cl') return q * 10;
    if(u === 'dl') return q * 100;
    if(['l', 'lt', 'litro', 'litri'].includes(u)) return q * 1000;
    return 0;
  }
  /** Stima del volume dei soli ingredienti liquidi (ml, cl, dl, l). I solidi non sono contati. */
  function stimaLiquidiMl(ricetta){
    return Math.round((ricetta.ingredients || []).reduce((t, i) => t + mlDi(i), 0));
  }
  function capacitaLitri(ricetta){
    const v = parseFloat(ricetta && ricetta.potLiters);
    return v > 0 ? v : 6;
  }

  /** Elenco di avvisi (testi) per la ricetta o per il modulo in modifica. */
  function avvisi(ricetta){
    const out = [];
    const passi = ricetta.steps || [];
    const nomi = (ricetta.ingredients || []).map(i => String(i.name || '')).filter(n => !RE_LATTE_NO.test(n));
    const delicati = nomi.filter(n => RE_NATURALE.test(n));
    const stima = stimaLiquidiMl(ricetta);
    const cap = capacitaLitri(ricetta) * 1000;
    passi.forEach((s, idx) => {
      const n = idx + 1;
      if(!info(s.fn) || !usaPressione(s.fn)) return;
      if(!(Number(s.minLiquid) > 0)){
        out.push(`Passaggio ${n}: manca il liquido minimo (la pentola a pressione ne richiede, in genere almeno 250 ml).`);
      }
      const max = s.fillMax === '1/2' ? 0.5 : (s.fillMax === '2/3' ? 2 / 3 : 0);
      if(max && stima > cap * max){
        out.push(`Passaggio ${n}: i liquidi (circa ${stima} ml, stima senza i solidi) superano il riempimento massimo di ${s.fillMax === '1/2' ? 'metà' : 'due terzi'} per una pentola da ${capacitaLitri(ricetta)} L (${Math.round(cap * max)} ml).`);
      }
      if(delicati.length && s.pressureRelease === 'Rapido'){
        const soloRisoBreve = delicati.every(x => /\briso\b/i.test(x)) && Number(s.time) > 0 && Number(s.time) <= 8;
        if(!soloRisoBreve){
          out.push(`Passaggio ${n}: con ${delicati.slice(0, 3).join(', ').toLowerCase()} conviene il rilascio naturale (il rapido può far schizzare schiuma dalla valvola).`);
        }
      }
    });
    return out;
  }

  const API = { FUNZIONI, ORDINE_FUNZIONI, PREDEFINITI, ACCESSORI, VALVOLE, RIEMPIMENTO, usaPressione, valoriPredefiniti, durata, riepilogo, avvisi, stimaLiquidiMl, capacitaLitri, testoRilascio };
  if(typeof module !== 'undefined' && module.exports) module.exports = API;
  root.PotSettings = API;
})(typeof window !== 'undefined' ? window : globalThis);
