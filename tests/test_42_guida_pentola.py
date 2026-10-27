"""Guida alla pentola a pressione: pagina nel sito, collegamenti, tabelle e schemi, nessuna richiesta esterna, precache offline."""
from helpers import check, reset_app_state


async def run(page):
    await reset_app_state(page)
    base = page.url.split("/index.html")[0].rstrip("/")
    if base.endswith("/"):
        base = base[:-1]
    # collegamenti dal sito
    check(await page.locator("#nav-guide-pot-link").count() == 1, "Menu: voce guida pentola")
    check((await page.get_attribute("#nav-guide-pot-link", "href")) == "guida-pentola.html", "Menu: href")
    await page.evaluate("document.getElementById('add-recipe-btn') && document.getElementById('add-recipe-btn').click()")
    check(await page.locator("#pot-guide-link").count() == 1, "Modulo ricetta: link alla guida")
    sw = await page.evaluate("fetch('sw.js').then(r=>r.text())")
    check("guida-pentola.html" in sw, "sw.js: guida in precache")
    # la pagina
    p2 = await page.context.new_page()
    ext = []
    p2.on("request", lambda r: ext.append(r.url) if not r.url.startswith(("http://localhost", "http://127.0.0.1", "data:", "blob:")) else None)
    await p2.goto(base + "/guida-pentola.html")
    await p2.wait_for_load_state("load")
    check(await p2.locator("section").count() == 10, "10 sezioni")
    check(await p2.locator("nav.toc a").count() == 10, "Indice con 10 voci")
    check(await p2.locator("table").count() >= 8, "Tabelle presenti")
    check(await p2.locator("svg").count() >= 3, "Schemi presenti")
    t = await p2.inner_text("body")
    for k in ["250 ml", "375 ml", "500 ml", "Burn", "indicativi", "manuale", "pressureRelease", "ricette-pentola-pressione-prova.json"]:
        check(k in t, f"Testo: {k}")
    check(await p2.locator("#back-link").count() == 1, "Link di ritorno")
    for a in await p2.locator("nav.toc a").evaluate_all("els=>els.map(e=>e.getAttribute('href').slice(1))"):
        check(await p2.locator("#" + a).count() == 1, f"Ancora {a}")
    over = await p2.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2")
    check(over, "Nessuno scroll orizzontale (desktop)")
    await p2.set_viewport_size({"width": 390, "height": 800})
    check(await p2.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), "Nessuno scroll orizzontale (telefono)")
    check(not ext, f"Nessuna richiesta esterna: {ext}")
    await p2.close()
