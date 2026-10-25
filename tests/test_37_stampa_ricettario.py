"""Stampa A4 orizzontale: dal pannello «Gestisci ricettari» e con Stampa del browser dalla scheda aperta."""
from helpers import check, reset_app_state, dismiss_storage_choice


def ric(i, nome, cat="Primi", rb=None, arch=False):
    d = {"id": i, "name": nome, "category": cat, "servings": 4, "time": 20, "ingredients": [{"name": "farina", "qty": 100, "unit": "g"}],
         "steps": [{"text": "Impasta."}], "tags": []}
    if rb: d["ricettarioId"] = rb
    if arch: d["archived"] = True
    return d


async def run(page):
    await reset_app_state(page)
    await page.evaluate("r=>localStorage.setItem('mc_ricettario_v1',JSON.stringify(r))",
                        [ric("a", "Arrosto", "Secondi"), ric("b", "Bucatini"), ric("c", "Vecchia", arch=True), ric("d", "Dolce", "Dolci", rb="altro")])
    await page.evaluate("l=>localStorage.setItem('mc_ricettario_libri_v1',JSON.stringify(l))", [{"id": "default", "name": "Il Mio Ricettario", "cover": ""}, {"id": "altro", "name": "Altro", "cover": ""}])
    await page.reload(); await page.wait_for_timeout(1000); await dismiss_storage_choice(page)
    await page.evaluate("window.__stampe = 0; window.print = () => { window.__stampe++; }; 0")
    await page.evaluate("document.getElementById('manage-ricettari-btn').click()")
    riga = page.locator('.ricettario-row[data-id="default"]')
    await riga.locator(".ricettario-row-print-btn").click()
    await page.locator("#layout-stampa-overlay.active").wait_for(timeout=3000)
    check(await page.is_checked('input[name="layout-stampa"][value="colonne"]'), "Predefinito: due colonne")
    await page.check('input[name="layout-stampa"][value="pagina"]')
    await page.click("#layout-stampa-ok")
    await page.wait_for_timeout(600)
    check(not await page.evaluate("document.getElementById('print-root').classList.contains('ps-colonne')"), "Layout una ricetta per pagina")
    check(await page.evaluate("window.__stampe") == 1, "Stampa avviata dal ricettario")
    titoli = await page.evaluate("[...document.querySelectorAll('#print-root .ps-title')].map(e=>e.textContent)")
    check(titoli == ["Bucatini", "Arrosto"], f"Solo le ricette attive di quel ricettario, per categoria: {titoli}")
    check("A4 landscape" in await page.evaluate("document.getElementById('print-page-style').textContent"), "Pagina A4 orizzontale")
    await page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    check(await page.evaluate("!document.getElementById('print-root')"), "Pulizia dopo la stampa")
    # Stampa del browser con la scheda aperta
    await page.click("#ricettari-close") if await page.locator("#ricettari-overlay.active").count() else None
    await page.click("#nav-recipes-btn")
    await page.locator("#recipe-list h3", has_text="Bucatini").click()
    await page.locator("#view-overlay.active").wait_for()
    await page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    titoli = await page.evaluate("[...document.querySelectorAll('#print-root .ps-title')].map(e=>e.textContent)")
    check(titoli == ["Bucatini"], f"Ctrl+P dalla scheda stampa la scheda pulita: {titoli}")
    await page.evaluate("window.dispatchEvent(new Event('afterprint'))")

    # layout a due colonne, ricordato come predefinito
    await page.evaluate("document.getElementById('manage-ricettari-btn').click()")
    await page.locator('.ricettario-row[data-id="default"] .ricettario-row-print-btn').click()
    check(await page.is_checked('input[name="layout-stampa"][value="pagina"]'), "La scelta precedente è ricordata")
    await page.check('input[name="layout-stampa"][value="colonne"]')
    await page.click("#layout-stampa-ok")
    await page.wait_for_timeout(600)
    check(await page.evaluate("document.getElementById('print-root').classList.contains('ps-colonne')"), "Layout a due colonne")
    check(await page.evaluate("document.querySelectorAll('#print-root .ps-sheet').length") == 2, "Due ricette nel foglio")
    await page.evaluate("window.dispatchEvent(new Event('afterprint'))")
