"""Fonti e ispirazioni: link nel modulo, nella scheda, nel PDF e nella stampa; JSON tollerante; link non validi scartati o bloccati."""
import asyncio, json, re
from helpers import check, reset_app_state, dismiss_storage_choice


async def scarica(page, click):
    async with page.expect_download(timeout=15000) as d:
        await click()
    dl = await d.value
    return dl.suggested_filename, open(await dl.path(), "rb").read()


async def run(page):
    page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    await reset_app_state(page)
    base = {"servings": 4, "time": 10, "category": "Primi", "ingredients": [{"name": "farina", "qty": 100, "unit": "g"}], "steps": [{"text": "Impasta."}], "tags": []}
    ricette = [
        dict(base, id="f1", name="Con fonti", fonti=[{"url": "https://www.giallozafferano.it/ricetta", "titolo": "Giallo Zafferano"}, "esempio.it/pasta", "javascript:alert(1)", "https://www.giallozafferano.it/ricetta"]),
        dict(base, id="f2", name="Alias sources", sources=[{"link": "http://nonna.example.com/x", "title": "Nonna"}, {"url": "ftp://x.it/y"}, "senzapunto"]),
        dict(base, id="f3", name="Senza fonti"),
    ]
    await page.evaluate("r=>localStorage.setItem('mc_ricettario_v1',JSON.stringify(r))", ricette)
    await page.reload(); await page.wait_for_timeout(1000); await dismiss_storage_choice(page)
    rec = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1'))")
    f1 = next(r for r in rec if r["id"] == "f1"); f2 = next(r for r in rec if r["id"] == "f2"); f3 = next(r for r in rec if r["id"] == "f3")
    check([f["url"] for f in f1.get("fonti", [])] == ["https://www.giallozafferano.it/ricetta", "https://esempio.it/pasta"], f"Link validi, senza doppioni né javascript: {f1.get('fonti')}")
    check(f2.get("fonti") == [{"url": "http://nonna.example.com/x", "titolo": "Nonna"}] and "sources" not in f2, f"Alias «sources», ftp e testi senza dominio scartati: {f2.get('fonti')}")
    check("fonti" not in f3, "Nessuna fonte: il campo non c'è")

    # scheda: link che si aprono in una nuova scheda, senza riferimento al ricettario
    await page.evaluate("document.getElementById('nav-recipes-btn').click()")
    await page.locator("#recipe-list h3", has_text="Con fonti").first.click()
    await page.locator("#view-overlay.active").wait_for()
    links = page.locator("#view-sources a")
    check(await links.count() == 2, f"Due link nella scheda: {await links.count()}")
    rel = await links.first.get_attribute("rel"); tg = await links.first.get_attribute("target")
    check("noopener" in rel and "noreferrer" in rel and tg == "_blank", f"Apertura sicura: {rel} {tg}")
    check("Giallo Zafferano" in await page.inner_text("#view-sources"), "Nome del sito mostrato")

    # modulo: modifica, aggiunta di un link senza https, link non valido blocca il salvataggio
    await page.evaluate("document.getElementById('view-edit-btn').click()")
    await page.locator("#edit-overlay.active").wait_for()
    check(await page.locator("#sources-editor .source-row").count() == 2, "Il modulo mostra i 2 link")
    await page.click("#add-source")
    righe = page.locator("#sources-editor .source-row")
    await righe.nth(2).locator(".source-url").fill("non un link")
    await page.click("#save-recipe"); await page.wait_for_timeout(400)
    check(await page.locator("#edit-overlay.active").count() == 1, "Link non valido: il modulo resta aperto")
    check("invalid" in (await righe.nth(2).locator(".source-url").get_attribute("class")), "Riga evidenziata")
    await righe.nth(2).locator(".source-title").fill("Cucchiaio")
    await righe.nth(2).locator(".source-url").fill("www.cucchiaio.it/ricette/x")
    await righe.nth(0).locator(".source-del").click()
    await page.click("#save-recipe"); await page.wait_for_timeout(600)
    rec = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1'))")
    f1 = next(r for r in rec if r["id"] == "f1")
    check([f["url"] for f in f1["fonti"]] == ["https://esempio.it/pasta", "https://www.cucchiaio.it/ricette/x"], f"Salvato: {f1['fonti']}")
    check(f1["fonti"][1]["titolo"] == "Cucchiaio", "Nome salvato")

    # PDF orizzontale (una ricetta) e verticale: la fonte compare
    await page.evaluate("window.showSaveFilePicker = undefined; 0")
    await page.evaluate("document.getElementById('nav-recipes-btn').click()")
    await page.locator("#recipe-list h3", has_text="Con fonti").first.click()
    await page.locator("#view-overlay.active").wait_for()
    await page.evaluate("document.getElementById('view-export-menu-btn') && document.getElementById('view-export-menu-btn').click()")
    nome, pdf = await scarica(page, lambda: page.evaluate("document.getElementById('print-recipe-a4-btn').click()"))
    check(b"Ispirata da" in pdf and b"cucchiaio.it" in pdf, "PDF A4 orizzontale: «Ispirata da» e il sito")
    # PDF verticale (esportazione del ricettario)
    await page.evaluate("document.getElementById('view-close-btn') && document.getElementById('view-close-btn').click()")
    await page.evaluate("document.getElementById('export-all-pdf-btn').click()")
    await page.locator("#export-pdf-overlay.active").wait_for(timeout=4000)
    nome, pdf = await scarica(page, lambda: page.click("#export-pdf-confirm-btn"))
    t = pdf.decode("latin-1")
    check("Ispirata da" in t and "https://www.cucchiaio.it/ricette/x" in t, "PDF verticale: sezione «Ispirata da» con il link")
