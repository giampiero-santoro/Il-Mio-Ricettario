"""Backup: caricamento completo, campi assenti/vuoti, file malformati (stato intatto), Annulla."""
import json, asyncio
from helpers import check, reset_app_state, dismiss_storage_choice

CHIAVI = ["mc_ricettario_v1", "mc_ricettario_libri_v1", "mc_ricettario_raccolte_v1", "mc_ricettario_settimana_v1", "mc_ricettario_settimane_v1",
          "mc_ricettario_pasti_v1", "mc_ricettario_dispensa_prodotti_v1", "mc_ricettario_spesa_extra_v1", "mc_ricettario_note_settimana_v1", "mc_ricettario_spesa_lista_v1"]


def ric(i, nome, rb=None):
    r = {"id": i, "name": nome, "category": "Primi", "servings": 2, "ingredients": [{"name": "Farina", "qty": 100, "unit": "g"}], "steps": [{"text": "x"}]}
    if rb: r["ricettarioId"] = rb
    return r


def backup_completo(prefisso="N"):
    return {
        "formato": "il-mio-ricettario", "versioneFormato": 1, "tipoBackup": "completo",
        "recipes": [ric(prefisso + "1", prefisso + " Ricetta Uno", "rbx"), ric(prefisso + "2", prefisso + " Ricetta Due")],
        "ricettari": [{"id": "default", "name": "Il Mio Ricettario", "cover": ""}, {"id": "rbx", "name": prefisso + " Ricettario X", "cover": ""}],
        "raccolte": [{"id": "c1", "name": prefisso + " Raccolta"}],
        "weekPlan": {}, "planWeeks": {"2026-10-19": {"plan": {"Lunedì": [{"id": "p1", "recipeId": prefisso + "1", "mealType": "Cena", "time": ""}]}, "notes": {}}},
        "mealTypes": ["Colazione", "Pranzo", "Cena"],
        "dispensaItems": [{"id": "d1", "name": prefisso + " Riso", "qty": 1, "unit": "kg"}],
        "shoppingExtraItems": [{"id": "s1", "name": prefisso + " Sale"}], "weekNotes": {}, "spesaLista": [{"id": "l1", "name": prefisso + " Latte"}],
    }


async def snapshot(page):
    return await page.evaluate("ks => Object.fromEntries(ks.map(k => [k, localStorage.getItem(k)]))", CHIAVI)


async def importa(page, dati, nome="b.json"):
    buf = dati if isinstance(dati, (bytes, bytearray)) else json.dumps(dati).encode()
    await page.set_input_files("#import-file-input", {"name": nome, "mimeType": "application/json", "buffer": buf})


async def alert_testo(page, azione):
    msgs = []
    handler = lambda d: msgs.append(d.message)
    page.on("dialog", handler)
    await azione()
    await page.wait_for_timeout(700)
    page.remove_listener("dialog", handler)
    return msgs


async def seed_vecchio(page):
    await page.evaluate("""() => {
      localStorage.setItem('mc_ricettario_v1', JSON.stringify([{id:'old1',name:'Vecchia Ricetta',category:'Primi',servings:2,ingredients:[],steps:[]}]));
      localStorage.setItem('mc_ricettario_dispensa_prodotti_v1', JSON.stringify([{id:'od',name:'Vecchio Prodotto',qty:1,unit:'kg'}]));
      localStorage.setItem('mc_ricettario_raccolte_v1', JSON.stringify([{id:'oc',name:'Vecchia Raccolta'}]));
      localStorage.setItem('mc_ricettario_spesa_lista_v1', JSON.stringify([{id:'ol',name:'Vecchio Latte'}]));
    }""")
    await page.reload(); await page.wait_for_timeout(900); await dismiss_storage_choice(page)


async def sostituisci(page, dati):
    await importa(page, dati)
    await page.locator("#import-dest-overlay.active").wait_for(timeout=5000)
    check(await page.locator('input[value="sostituisci"]').is_checked(), "Backup completo: «Sostituisci» è proposto")
    await page.click("#import-dest-ok")
    await page.locator("#confirm-ok-btn").wait_for(state="visible", timeout=4000)
    await page.evaluate("document.getElementById('confirm-ok-btn').click()")
    await page.wait_for_timeout(800)


async def run(page):
    page.on("dialog", lambda d: asyncio.ensure_future(d.accept()))
    # ---------- A: backup completo sostituisce tutto in modo coerente ----------
    await reset_app_state(page)
    await seed_vecchio(page)
    prima = await snapshot(page)
    await sostituisci(page, backup_completo("N"))
    s = await snapshot(page)
    nomi = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).map(r=>r.id)")
    check(nomi == ["N1", "N2"], f"A: ricette = quelle del backup, nessun residuo del vecchio stato: {nomi}")
    check([x["id"] for x in json.loads(s["mc_ricettario_dispensa_prodotti_v1"])] == ["d1"], "A: dispensa sostituita")
    check([x["id"] for x in json.loads(s["mc_ricettario_raccolte_v1"])] == ["c1"], "A: raccolte sostituite")
    check([x["id"] for x in json.loads(s["mc_ricettario_spesa_lista_v1"])] == ["l1"], "A: lista spesa sostituita")
    check([x["id"] for x in json.loads(s["mc_ricettario_spesa_extra_v1"])] == ["s1"], "A: spesa extra sostituita")
    check(json.loads(s["mc_ricettario_pasti_v1"]) == ["Colazione", "Pranzo", "Cena"], "A: tipi di pasto sostituiti")
    check({x["id"] for x in json.loads(s["mc_ricettario_libri_v1"])} == {"default", "rbx"}, "A: ricettari sostituiti")
    check("2026-10-19" in json.loads(s["mc_ricettario_settimane_v1"]), "A: settimane pianificate sostituite")
    testo = await page.inner_text("body")
    check("Vecchia Ricetta" not in testo, "A: la vecchia ricetta non è più visibile")

    # ---------- E: Annulla ripristina tutto ----------
    await page.locator("#undo-toast:not([hidden])").wait_for(timeout=4000)
    await page.click("#undo-toast-btn")
    await page.wait_for_timeout(700)
    dopo = await snapshot(page)
    for k in CHIAVI:
        check(dopo[k] == prima[k], f"E: Annulla ripristina identica la chiave {k}")
    ids = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).map(r=>r.id)")
    check(ids == ["old1"], f"E: dopo Annulla tornano le ricette di prima: {ids}")

    # ---------- B: campo assente ≠ campo vuoto; vecchi backup ----------
    vecchio = {"recipes": [ric("v1", "Da Vecchio Backup")], "weekPlan": {"Lunedì": "v1"}, "mealTypes": ["Pranzo"],
               "dispensaItems": [], "shoppingExtraItems": [], "weekNotes": {}}
    await seed_vecchio(page)
    await sostituisci(page, vecchio)
    s = await snapshot(page)
    check(json.loads(s["mc_ricettario_dispensa_prodotti_v1"]) == [], "B1: dispensa PRESENTE ma vuota → svuota (non resta il vecchio)")
    check(json.loads(s["mc_ricettario_raccolte_v1"]) == [], "B1: raccolte ASSENTI nel vecchio backup → default vuoto, niente mix col vecchio stato")
    check([x["id"] for x in json.loads(s["mc_ricettario_libri_v1"])] == ["default"], "B1: ricettari assenti → solo il ricettario di partenza")
    check(json.loads(s["mc_ricettario_spesa_lista_v1"]) == [], "B1: lista spesa assente → vuota")
    wp = json.loads(s["mc_ricettario_settimana_v1"])
    check(isinstance(wp.get("Lunedì"), list) and wp["Lunedì"][0]["recipeId"] == "v1", f"B1: vecchio formato di piano convertito: {wp.get('Lunedì')}")
    # B2: backup marcato come completo ma con una sezione mancante → rifiutato, dati intatti
    rotto = backup_completo("M"); del rotto["raccolte"]
    prima = await snapshot(page)
    msgs = await alert_testo(page, lambda: importa(page, rotto))
    check(any("mancano" in m for m in msgs), f"B2: messaggio chiaro: {msgs}")
    check(await snapshot(page) == prima, "B2: backup incompleto → nessuna modifica")

    # ---------- file parziale: si unisce, non sostituisce ----------
    await seed_vecchio(page)
    await page.set_input_files("#import-file-input", [])
    await importa(page, {"recipes": [ric("p1", "Ricetta Parziale")]})
    await page.locator("#import-dest-overlay.active").wait_for(timeout=5000)
    check(not await page.locator("#import-dest-sostituisci-row").is_visible(), "Parziale: nessuna opzione «Sostituisci»")
    await page.click("#import-dest-ok"); await page.wait_for_timeout(700)
    ids = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).map(r=>r.id).sort()")
    check(ids == ["old1", "p1"], f"Parziale: unione senza perdere nulla: {ids}")

    # ---------- C: file malformati → stato invariato + messaggio comprensibile ----------
    casi = {
        "JSON troncato": b'{"recipes": [',
        "file vuoto": b'',
        "testo qualsiasi": b'ciao a tutti',
        "numero": b'42',
        "oggetto senza dati": b'{"foo": 1}',
        "ricette non è un elenco": json.dumps({"recipes": "x"}).encode(),
        "ricetta non oggetto": json.dumps({"recipes": [1, 2]}).encode(),
        "ricetta senza nome": json.dumps({"recipes": [{"id": "z"}]}).encode(),
        "ingredienti non elenco": json.dumps({"recipes": [{"id": "z", "name": "A", "ingredients": "sale"}]}).encode(),
        "settimana con data errata": json.dumps(dict(backup_completo("Q"), planWeeks={"ieri": {"plan": {}, "notes": {}}})).encode(),
        "piano giorno non valido": json.dumps(dict(backup_completo("Q"), planWeeks={"2026-10-19": {"plan": {"Lunedì": 5}, "notes": {}}})).encode(),
        "dispensa con voce non valida": json.dumps(dict(backup_completo("Q"), dispensaItems=[1])).encode(),
        "altro formato": json.dumps({"formato": "altra-app", "recipes": []}).encode(),
        "versione futura": json.dumps(dict(backup_completo("Q"), versioneFormato=99)).encode(),
    }
    for nome, buf in casi.items():
        prima = await snapshot(page)
        msgs = await alert_testo(page, lambda b=buf: importa(page, b))
        check(await snapshot(page) == prima, f"C ({nome}): dati invariati")
        check(len(msgs) >= 1 and ("modificati" in msgs[0] or "toccati" in msgs[0]), f"C ({nome}): messaggio comprensibile: {msgs}")
        check(await page.locator("#import-dest-overlay.active").count() == 0, f"C ({nome}): nessuna finestra di scelta aperta")
        await page.set_input_files("#import-file-input", [])
    ids = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).map(r=>r.id).sort()")
    check(ids == ["old1", "p1"], f"C: ricette ancora quelle di prima: {ids}")
