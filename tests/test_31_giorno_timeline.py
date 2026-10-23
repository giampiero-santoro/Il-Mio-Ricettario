"""Vista Giorno: linea del tempo con orari a sinistra e riquadro «in breve» a lato."""
from helpers import check, reset_app_state, dismiss_storage_choice, aggiungi_pasto


async def run(page):
    await reset_app_state(page)
    rec = [{"id": "p1", "name": "Pasta Giorno", "title": "Pasta Giorno", "servings": 2, "category": "Primi", "time": 20,
            "ingredients": [{"name": "Pasta", "qty": 200, "unit": "g"}], "steps": [{"text": "x"}]}]
    await page.evaluate("r=>localStorage.setItem('mc_ricettario_v1',JSON.stringify(r))", rec)
    await page.reload(); await page.wait_for_timeout(900); await dismiss_storage_choice(page)
    await page.evaluate("()=>{window.confirm=()=>false}")
    await page.click("#nav-planning-btn")
    await page.click("#plan-mode-week")
    await page.locator(".plan-matrix").wait_for(state="visible")
    await aggiungi_pasto(page, "Colazione", 0)
    await aggiungi_pasto(page, "Pranzo", 0)
    await page.locator(".plan-week-row").first.locator(".plan-meal-block", has=page.locator(".plan-slot-name", has_text="Pranzo")).locator(".plan-add-btn").click()
    await page.fill("#recipe-picker-search", "Pasta Giorno")
    await page.locator(".recipe-picker-item", has_text="Pasta Giorno").first.click()
    await page.wait_for_timeout(400)
    await page.locator(".plan-grid-day-open").first.click()
    await page.locator(".plan-day-card").wait_for(state="visible")

    side = page.locator(".plan-day-side")
    check(await side.count() == 1, "Riquadro «in breve» presente")
    titolo = await side.locator("h4").inner_text()
    check(titolo == "Lunedì in breve", f"Titolo del riquadro: {titolo}")
    testo = await side.inner_text()
    check("Pasti" in testo and "Ricette" in testo and "Calorie" in testo and "Persone" in testo, f"Voci del riepilogo: {testo!r}")
    righe = await side.locator(".plan-sum-row").evaluate_all("els=>els.map(e=>e.innerText.replace(/\\s+/g,' '))")
    check(any(r.startswith("Pasti") and r.endswith("2") for r in righe) and any(r.startswith("Ricette") and r.endswith("1") for r in righe), f"Conteggi: {righe}")

    # il riquadro sta a destra delle schede, le schede non sono a tutta larghezza
    b = await page.locator(".plan-meal-block").first.bounding_box()
    s = await side.bounding_box()
    check(s["x"] > b["x"] + b["width"], "Il riquadro è a lato della linea del tempo")
    check(b["width"] <= 670, f"Le schede dei pasti sono contenute: {b['width']}")
    # orari a sinistra e in ordine
    t = await page.locator(".plan-tl-time input").evaluate_all("els=>els.map(e=>e.getBoundingClientRect().x)")
    check(len(t) == 2 and t[0] < b["x"], f"Gli orari stanno a sinistra delle schede: {t}")
    # il pulsante della spesa del giorno è nel riquadro
    check(await side.locator(".plan-day-shopping-btn").count() == 1 and await side.locator(".plan-week-totals-btn").count() == 1, "Pulsanti spesa e totali nel riquadro")
