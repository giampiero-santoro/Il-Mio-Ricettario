"""Errori di salvataggio (spazio esaurito) e dati corrotti: nessun falso successo, nessuna perdita."""
import json, asyncio
from helpers import check, reset_app_state, dismiss_storage_choice
from test_38_backup_atomico import CHIAVI, backup_completo, snapshot, importa, seed_vecchio, ric

QUOTA = """(margine) => {
  // Simula un vero limite di spazio: il totale dei dati salvati non può superare quello di adesso + margine.
  if(!window.__origSet) window.__origSet = Storage.prototype.setItem;
  const totale = () => Object.keys(localStorage).reduce((t, k) => t + k.length + localStorage.getItem(k).length, 0);
  const tetto = totale() + margine;
  Storage.prototype.setItem = function(k, v){
    const attuale = this.getItem(k);
    const dopo = totale() - (attuale === null ? 0 : k.length + attuale.length) + k.length + String(v).length;
    if(dopo > tetto){ const e = new Error('quota'); e.name = 'QuotaExceededError'; throw e; }
    return window.__origSet.call(this, k, v);
  };
}"""
RIPRISTINA = "() => { if(window.__origSet){ Storage.prototype.setItem = window.__origSet; } }"


async def run(page):
    msgs = []
    page.on("dialog", lambda d: (msgs.append(d.message), asyncio.ensure_future(d.accept())))

    # ---------- D1: sostituzione con scritture che falliscono a metà → tutto com'era ----------
    for limite in (0, 150, 700):
        await reset_app_state(page)
        await seed_vecchio(page)
        prima = await snapshot(page)
        await page.evaluate(QUOTA, limite)
        msgs.clear()
        grande = backup_completo("N"); grande["recipes"][0]["notes"] = "x" * 4000  # il backup deve occupare molto più dei margini simulati
        await importa(page, grande)
        await page.locator("#import-dest-overlay.active").wait_for(timeout=5000)
        await page.click("#import-dest-ok")
        await page.locator("#confirm-ok-btn").wait_for(state="visible", timeout=4000)
        await page.evaluate("document.getElementById('confirm-ok-btn').click()")
        await page.wait_for_timeout(900)
        await page.evaluate(RIPRISTINA)
        dopo = await snapshot(page)
        diff = [k for k in CHIAVI if dopo[k] != prima[k]]
        check(not diff, f"D1 (margine di spazio {limite}): dati salvati identici a prima; diversi: {diff} {[ (prima[k] or '')[:80] + ' || ' + (dopo[k] or '')[:80] for k in diff]}")
        ids = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).map(r=>r.id)")
        check(ids == ["old1"], f"D1 ({limite}): ricette di prima: {ids}")
        testo = await page.inner_text("body")
        check("N Ricetta Uno" not in testo, f"D1 ({limite}): l'interfaccia non mostra dati non salvati")
        check(any("non è cambiato nulla" in m or "come prima" in m for m in msgs), f"D1 ({limite}): messaggio di errore chiaro: {msgs}")
        check(not any("Backup caricato" in m for m in msgs), f"D1 ({limite}): nessun falso messaggio di successo")
        check(await page.locator("#undo-toast:not([hidden])").count() == 0, f"D1 ({limite}): nessun «Annulla» di un'operazione non avvenuta")

    # ---------- D2: unione (file parziale) con salvataggio fallito → rollback ----------
    await reset_app_state(page)
    await seed_vecchio(page)
    prima = await snapshot(page)
    await page.evaluate(QUOTA, 0)
    msgs.clear()
    await importa(page, {"recipes": [ric("p1", "Ricetta Parziale")]})
    await page.locator("#import-dest-overlay.active").wait_for(timeout=5000)
    await page.click("#import-dest-ok")
    await page.wait_for_timeout(900)
    await page.evaluate(RIPRISTINA)
    check(await snapshot(page) == prima, "D2: unione fallita → dati salvati identici")
    testo = await page.inner_text("body")
    check("Ricetta Parziale" not in testo, "D2: la ricetta non salvata non compare nell'interfaccia")
    check(any("NON riuscita" in m for m in msgs), f"D2: messaggio di errore: {msgs}")
    check(not any("Ricette:" in m and "aggiunta" in m for m in msgs), "D2: nessun falso successo")

    # ---------- D3: salvataggio ricetta dal modulo con spazio esaurito → modulo aperto, nessun falso salvataggio ----------
    await reset_app_state(page)
    await seed_vecchio(page)
    await page.click("#nav-recipes-btn")
    await page.locator("#recipes-view").wait_for(state="visible")
    await page.click("#new-recipe-btn")
    await page.locator("#edit-overlay").wait_for(state="visible")
    await page.fill("#f-name", "Ricetta Non Salvabile")
    await page.evaluate(QUOTA, 0)
    msgs.clear()
    await page.click("#save-recipe")
    await page.wait_for_timeout(700)
    await page.evaluate(RIPRISTINA)
    check(any("NON è stata salvata" in m for m in msgs), f"D3: avviso chiaro: {msgs}")
    check(await page.locator("#f-name").is_visible(), "D3: il modulo resta aperto (non si perde ciò che hai scritto)")
    n = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).length")
    check(n == 1, f"D3: nessuna ricetta fantasma salvata: {n}")
    await page.click("#save-recipe")
    await page.wait_for_timeout(700)
    n = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).length")
    check(n == 2, f"D3: riprovando con spazio disponibile si salva: {n}")

    # ---------- dati corrotti: copia di sicurezza, nessuna cancellazione ----------
    await reset_app_state(page)
    await page.evaluate("() => localStorage.setItem('mc_ricettario_v1', '{non è json')")
    msgs.clear()
    await page.reload(); await page.wait_for_timeout(1500); await dismiss_storage_choice(page)
    copia = await page.evaluate("localStorage.getItem('mc_ricettario_corrotto_mc_ricettario_v1')")
    check(copia == "{non è json", f"Corrotti: copia di sicurezza del testo originale: {copia!r}")
    check(any("non sono leggibili" in m for m in msgs), f"Corrotti: avviso chiaro: {msgs}")
