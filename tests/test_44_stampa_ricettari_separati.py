"""Stampa di più ricettari: tutto insieme / separati in un PDF / un file per ricettario; nome della copertina e del file (orizzontale e verticale)."""
import asyncio, re
from helpers import check, reset_app_state, dismiss_storage_choice


def ric(i, nome, rb, cat="Primi"):
    return {"id": i, "name": nome, "category": cat, "servings": 4, "time": 20, "ingredients": [{"name": "farina", "qty": 100, "unit": "g"}],
            "steps": [{"text": "Impasta."}], "tags": [], "ricettarioId": rb}


async def scarica(page, click):
    async with page.expect_download(timeout=15000) as d:
        await click()
    dl = await d.value
    return dl.suggested_filename, open(await dl.path(), "rb").read()


def pagine(pdf):
    return len(re.findall(rb"/Type /Page /Parent", pdf))


async def apri(page):
    await page.evaluate("document.getElementById('export-all-pdf-btn').click()")
    await page.locator("#export-pdf-overlay.active").wait_for(timeout=4000)


async def run(page):
    await reset_app_state(page)
    libri = [{"id": "default", "name": "Il Mio Ricettario", "cover": ""}, {"id": "b", "name": "Zuppe", "cover": ""}]
    rec = [ric("a1", "Arrosto", "default", "Secondi"), ric("a2", "Bucatini", "default"), ric("b1", "Minestrone", "b"), ric("b2", "Ribollita", "b")]
    await page.evaluate("a=>{localStorage.setItem('mc_ricettario_v1',JSON.stringify(a[0]));localStorage.setItem('mc_ricettario_libri_v1',JSON.stringify(a[1]))}", [rec, libri])
    await page.reload(); await page.wait_for_timeout(1000); await dismiss_storage_choice(page)
    await page.evaluate("window.showSaveFilePicker = undefined; 0")
    await apri(page)
    check(await page.locator("#export-pdf-sep-row").is_visible(), "Scelta dei ricettari visibile con 2 ricettari")
    check(await page.locator("#export-pdf-cover-name").is_visible() and await page.locator("#export-pdf-file-name").is_visible(), "Campi nome copertina e nome file")

    # ---- orizzontale, ricettari separati, nomi scelti ----
    await page.fill("#export-pdf-cover-name", "Libro di famiglia")
    await page.fill("#export-pdf-file-name", "famiglia/2026: prova.pdf")
    await page.check('input[name="export-pdf-modo"][value="separati"]')
    await page.click("#print-a4-confirm-btn")
    await page.locator("#layout-stampa-overlay.active").wait_for(timeout=3000)
    await page.check('input[name="layout-stampa"][value="pagina"]')
    nome, pdf = await scarica(page, lambda: page.click("#layout-stampa-ok"))
    check(nome == "famiglia-2026- prova.pdf", f"Nome file scelto e ripulito: {nome!r}")
    check(b"(Libro di famiglia)" in pdf, "Nome sulla copertina")
    # copertina + indice dei ricettari + 2 x (titolo + indice) + 4 ricette = 10
    check(pagine(pdf) == 10, f"Pagine: copertina, indice dei ricettari, 2 ricettari (titolo, indice, ricette): {pagine(pdf)}")
    check(b"(Indice dei ricettari)" in pdf, "Indice dei ricettari")
    check(pdf.count(b"(Indice)") == 2, f"Un indice per ricettario: {pdf.count(b'(Indice)')}")
    check(pdf.count(b"/Subtype /Link") == 6, f"Collegamenti: 2 ricettari + 4 ricette: {pdf.count(b'/Subtype /Link')}")
    try:
        import io, pypdf
        r = pypdf.PdfReader(io.BytesIO(pdf))
        num = {p.indirect_reference.idnum: i + 1 for i, p in enumerate(r.pages)}
        dest = lambda n: [num[a.get_object()["/Dest"][0].idnum] for a in r.pages[n - 1].get("/Annots", [])]
        check(dest(2) == [3, 7], f"L'indice dei ricettari porta alle pagine di titolo: {dest(2)}")
        check(dest(4) == [5, 6] and dest(8) == [9, 10], f"Gli indici portano alle ricette: {dest(4)} {dest(8)}")
    except ImportError:
        pass
    check(b"(Il Mio Ricettario)" in pdf and b"(Zuppe)" in pdf, "Pagine di titolo dei due ricettari")
    check(b"(2 ricette)" in pdf, "Numero di ricette nel titolo")
    check(all(f"(pag. {n})".encode() in pdf for n in range(2, 11)), "Numerazione continua da pag. 2 a pag. 10")

    # ---- orizzontale, un file per ricettario ----
    await apri(page)
    await page.fill("#export-pdf-file-name", "")
    await page.check('input[name="export-pdf-modo"][value="file"]')
    await page.click("#print-a4-confirm-btn")
    await page.locator("#layout-stampa-overlay.active").wait_for(timeout=3000)
    scaricati = []
    page.on("download", lambda d: scaricati.append(d))
    await page.click("#layout-stampa-ok")
    for _ in range(40):
        if len(scaricati) >= 2: break
        await page.wait_for_timeout(250)
    nomi = sorted(d.suggested_filename for d in scaricati)
    check(len(nomi) == 2, f"Due file scaricati: {nomi}")
    check(any("zuppe" in n for n in nomi) and any("il-mio-ricettario" in n for n in nomi), f"Un file per ricettario: {nomi}")

    # ---- verticale: ricettari separati in un PDF, con nome copertina e file ----
    await apri(page)
    await page.fill("#export-pdf-cover-name", "Il libro di casa")
    await page.fill("#export-pdf-file-name", "casa")
    await page.check('input[name="export-pdf-modo"][value="separati"]')
    nome, pdf = await scarica(page, lambda: page.click("#export-pdf-confirm-btn"))
    check(nome == "casa.pdf", f"Verticale: nome file {nome!r}")
    t = pdf.decode("latin-1")
    check("Il libro di casa" in t, "Verticale: nome sulla copertina")
    check(t.count("(Indice)") == 2 and "(Indice dei ricettari)" in t, f"Verticale: indice dei ricettari + un indice per ricettario: {t.count('(Indice)')}")
    check(t.count("/Subtype /Link") >= 6, f"Verticale: collegamenti negli indici: {t.count('/Subtype /Link')}")
    check(t.index("Il Mio Ricettario") < t.index("Zuppe") and "Minestrone" in t, "Verticale: ricettari in sequenza")
    # verticale: tutto insieme, nome automatico
    await apri(page)
    nome, pdf = await scarica(page, lambda: page.click("#export-pdf-confirm-btn"))
    check(nome.startswith("ricettario-completo-") and nome.endswith(".pdf"), f"Verticale: nome automatico {nome!r}")
    # una sola scelta di ricettario: la scelta «separati» non compare
    await apri(page)
    await page.click("#export-pdf-none-btn")
    await page.locator("#export-pdf-list .export-pdf-item", has_text="Arrosto").click()
    check(not await page.locator("#export-pdf-sep-row").is_visible(), "Con un solo ricettario la scelta non compare")
