"""Libreria nella pagina Oggi: riquadri che vanno a capo (colore, icona, conteggio, barra), copertina, clic = filtro per ricettario."""
from helpers import check, reset_app_state, dismiss_storage_choice


def ric(i, rb, cat="Primi"):
    return {"id": i, "name": "Ricetta " + i, "category": cat, "servings": 4, "time": 10, "ingredients": [], "steps": [], "tags": [], "ricettarioId": rb}


async def run(page):
    await reset_app_state(page)
    libri = [{"id": "default", "name": "Il Mio Ricettario", "cover": ""}, {"id": "b", "name": "Primi - Grandi Classici", "cover": ""},
             {"id": "c", "name": "Zuppe", "cover": "data:image/gif;base64,R0lGODlhAQABAAAAACw="}, {"id": "d", "name": "Vegetariano - Vegano", "cover": ""}]
    rec = [ric(f"b{i}", "b") for i in range(3)] + [ric("c1", "c")] + [ric(f"d{i}", "d") for i in range(2)]
    await page.evaluate("a=>{localStorage.setItem('mc_ricettario_v1',JSON.stringify(a[0]));localStorage.setItem('mc_ricettario_libri_v1',JSON.stringify(a[1]))}", [rec, libri])
    await page.reload(); await page.wait_for_timeout(1000); await dismiss_storage_choice(page)
    await page.evaluate("document.getElementById('nav-today-btn') && document.getElementById('nav-today-btn').click()")
    tiles = page.locator(".library-tile")
    check(await tiles.count() == 4, f"4 riquadri: {await tiles.count()}")
    t = await page.inner_text(".library-grid")
    check("0 ricette" in t and "3 ricette" in t and "1 ricetta" in t and "2 ricette" in t, f"Conteggi: {t!r}")
    check(await page.locator(".library-tile-bar").count() == 4, "Barra per ogni riquadro")
    colori = await page.evaluate("[...document.querySelectorAll('.library-tile')].map(e=>e.style.getPropertyValue('--c'))")
    check(len(set(colori)) == 4, f"Un colore diverso per ricettario: {colori}")
    check(await page.locator(".library-tile-cover").count() == 1, "Copertina al posto dell'icona")
    ic = await page.evaluate("[...document.querySelectorAll('.library-tile-ic')].map(e=>e.textContent.trim())")
    check(ic[1] == "🍝" and ic[3] == "🥬", f"Icone dal nome: {ic}")
    sc = await page.evaluate("(()=>{const g=document.querySelector('.library-grid');return g.scrollWidth<=g.clientWidth+1})()")
    check(sc, "Nessuno scorrimento orizzontale")
    await tiles.nth(1).click()
    await page.wait_for_timeout(500)
    check(await page.locator("#recipe-list h3").count() == 3, f"Il clic mostra le 3 ricette del ricettario: {await page.locator('#recipe-list h3').count()}")
