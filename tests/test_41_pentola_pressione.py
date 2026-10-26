"""Pentola a pressione elettrica: editor (funzioni, predefiniti, duplica/riordina, ultimi valori), riepilogo, avvisi, PDF, compatibilità."""
import asyncio, json, os
from helpers import check, reset_app_state, dismiss_storage_choice

FILE = os.path.join(os.path.dirname(__file__), "..", "esempi", "ricette-pentola-pressione-prova.json")


async def apri_editor(page, titolo):
    await page.evaluate("document.getElementById('nav-recipes-btn').click()")
    await page.locator("#recipe-list h3", has_text=titolo).first.click()
    await page.locator("#view-overlay.active").wait_for()
    await page.evaluate("document.getElementById('edit-recipe-btn').click()")
    await page.locator("#edit-overlay.active").wait_for()


async def run(page):
    page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await reset_app_state(page)
    dati = open(FILE, "rb").read()

    # ---------- import del file di prova (parziale: si unisce, crea la raccolta) ----------
    await page.set_input_files("#import-file-input", {"name": "ricette-pentola-pressione-prova.json", "mimeType": "application/json", "buffer": dati})
    await page.locator("#import-dest-overlay.active").wait_for(timeout=5000)
    await page.click("#import-dest-ok"); await page.wait_for_timeout(900)
    rec = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1'))")
    check([r["id"] for r in rec] == [f"pp_test_0{i}" for i in range(1, 6)], f"5 ricette importate: {[r['id'] for r in rec]}")
    rac = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_raccolte_v1'))")
    check(any(x["name"] == "Pentola a pressione - da testare" for x in rac), f"Raccolta creata: {rac}")
    check(all(r["raccolte"] == ["pp_raccolta_test"] for r in rec), "Ogni ricetta è nella raccolta")
    check(all(not r.get("nutrizioneUtente") for r in rec), "Nessun valore nutrizionale")

    # ---------- vista ricetta: riepilogo accanto al passaggio ----------
    await page.evaluate("document.getElementById('nav-recipes-btn').click()")
    await page.locator("#recipe-list h3", has_text="Brasato").first.click()
    await page.locator("#view-overlay.active").wait_for()
    t = await page.inner_text("#view-steps")
    check("(sauté alto 8 min)" in t, "Vista: sauté alto")
    check("rilascio naturale 15 min, poi rapido" in t and "programma carne/stufato, pressione alta 50 min" in t, "Vista: rilascio misto e programma carne")
    check("(mantenimento caldo 30 min, valvola su sfiato)" in t, "Vista: mantenimento caldo")
    check(await page.locator("#view-steps .step-timer-btn").count() >= 6, "Vista: timer di cottura e di rilascio")
    await page.evaluate("document.getElementById('view-back-btn').click()")
    await page.locator("#recipe-list h3", has_text="Cheesecake").first.click()
    t = await page.inner_text("#view-steps")
    check("con pentola nella pentola, trepiede, stampo, alluminio" in t, f"Vista: accessori: {t[-250:]}")
    await page.evaluate("document.getElementById('view-back-btn').click()")

    # ---------- filtro «Pentola a pressione» ----------
    await page.evaluate("document.getElementById('pressure-filter-btn').click()")
    await page.wait_for_timeout(300)
    check(await page.locator("#recipe-list h3").count() == 5, "Il filtro pentola a pressione trova le 5 ricette")
    await page.evaluate("document.getElementById('pressure-filter-btn').click()")

    # ---------- editor: predefiniti per funzione, duplica, riordina ----------
    await page.click("#new-recipe-btn")
    await page.locator("#edit-overlay.active").wait_for()
    await page.fill("#f-name", "Prova editor")
    await page.fill("#edit-overlay .step-text", "Cuoci il riso")
    await page.evaluate("document.querySelector('#steps-editor .pressure-toggle-btn').click()")
    await page.select_option("#steps-editor .step-fn", "riso")
    v = await page.evaluate("""() => { const b = document.querySelector('#steps-editor .step-block'); return {
        lv: b.querySelector('.step-level').value, t: b.querySelector('.step-time').value, valve: b.querySelector('.step-valve').value,
        rel: b.querySelector('.step-pressure-release').value, relMin: b.querySelector('.step-pressure-release-min').value } }""")
    check(v == {"lv": "alta", "t": "4", "valve": "chiusa", "rel": "Naturale", "relMin": "10"}, f"Programma riso: valori suggeriti: {v}")
    await page.select_option("#steps-editor .step-fn", "pressione")
    v = await page.evaluate("""() => { const b = document.querySelector('#steps-editor .step-block'); return {
        lv: b.querySelector('.step-level').value, valve: b.querySelector('.step-valve').value, rel: b.querySelector('.step-pressure-release').value } }""")
    check(v == {"lv": "alta", "valve": "chiusa", "rel": "Rapido"}, f"Pressione manuale: alta, chiusa, rapido: {v}")
    await page.select_option("#steps-editor .step-fn", "lenta")
    v = await page.evaluate("""() => { const b = document.querySelector('#steps-editor .step-block'); return { h: b.querySelector('.step-hours').value, lv: b.querySelector('.step-level').value, hv: b.querySelector('.step-hours-wrap').style.display } }""")
    check(v["h"] == "6" and v["lv"] == "bassa" and v["hv"] != "none", f"Cottura lenta: 6 ore, bassa: {v}")
    # duplica
    await page.evaluate("document.querySelector('#steps-editor .step-dup').click()")
    check(await page.locator("#steps-editor .step-block").count() == 2, "Duplica passaggio")
    hrs = await page.evaluate("document.querySelectorAll('#steps-editor .step-hours')[1].value")
    check(hrs == "6", "La copia conserva le impostazioni")
    # riordina: il secondo sale
    await page.evaluate("document.querySelectorAll('#steps-editor .step-text')[1].value = 'Secondo'; document.querySelectorAll('#steps-editor .step-up')[1].click()")
    primo = await page.evaluate("document.querySelector('#steps-editor .step-text').value")
    check(primo == "Secondo", "Sposta su")
    # avvisi: pressione senza liquido minimo + legumi con rilascio rapido
    await page.evaluate("""() => { const b = document.querySelectorAll('#steps-editor .step-block')[0]; const f = b.querySelector('.step-fn'); f.value = 'pressione'; f.dispatchEvent(new Event('change', {bubbles:true})); }""")
    await page.locator("#ingredients-editor .ing-name").first.fill("ceci secchi")
    await page.wait_for_timeout(500)
    w = await page.inner_text("#pot-warnings")
    check("manca il liquido minimo" in w, f"Avviso liquido minimo: {w}")
    check("rilascio naturale" in w, f"Avviso rilascio naturale per i legumi: {w}")
    # salvataggio: solo campi compilati, metodo elettrica, passaggio senza impostazioni resta testo
    await page.evaluate("document.querySelectorAll('#steps-editor .step-text')[1].value = 'Solo testo'; const f = document.querySelectorAll('#steps-editor .step-fn')[1]; f.value=''; f.dispatchEvent(new Event('change',{bubbles:true}))")
    await page.click("#save-recipe"); await page.wait_for_timeout(500)
    r = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).find(r => r.name === 'Prova editor')")
    check(r["cookerType"] == "Elettrica", "Metodo impostato su pentola elettrica")
    check(r["steps"][0]["fn"] == "pressione" and "fn" not in r["steps"][1], f"Passaggio senza funzione resta solo testo: {r['steps']}")
    ult = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_pentola_ultimi_v1'))")
    check("pressione" in ult, "Ultimi valori ricordati")

    # ---------- compatibilità: passaggio vecchio (bar + rilascio) invariato ----------
    vecchia = {"id": "old_pp", "name": "Vecchia a pressione", "category": "Primi", "servings": 2, "ingredients": [], "steps": [{"text": "Cuoci", "time": "10", "pressure": "0.8", "pressureUnit": "bar", "pressureRelease": "Rapido", "minLiquid": "250"}]}
    await page.evaluate("r => { const a = JSON.parse(localStorage.getItem('mc_ricettario_v1')); a.push(r); localStorage.setItem('mc_ricettario_v1', JSON.stringify(a)); }", vecchia)
    await page.reload(); await page.wait_for_timeout(900); await dismiss_storage_choice(page)
    await page.evaluate("document.getElementById('nav-recipes-btn').click()")
    await page.locator("#recipe-list h3", has_text="Vecchia a pressione").first.click()
    t = await page.inner_text("#view-steps")
    check("0.8" in t and "Rilascio: Rapido" in t and "Liquido min." in t and "(" not in t, f"Passaggio vecchio mostrato come prima: {t}")

    # ---------- PDF A4: il riepilogo è nel file ----------
    await page.evaluate("document.getElementById('manage-ricettari-btn').click()")
    await page.locator('.ricettario-row[data-id="default"] .ricettario-row-print-btn').click()
    await page.locator("#layout-stampa-overlay.active").wait_for(timeout=3000)
    async with page.expect_download(timeout=20000) as d:
        await page.click("#layout-stampa-ok")
    dl = await d.value
    pdf = open(await dl.path(), "rb").read()
    import re, zlib
    testo = pdf
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", pdf, re.S):
        try: testo += zlib.decompress(m.group(1))
        except Exception: pass
    check(b"pressione alta" in testo and b"rilascio naturale" in testo, "PDF: riepilogo dei passaggi a pressione presente")
    check(b"mantenimento caldo" in testo, "PDF: mantenimento caldo presente")
