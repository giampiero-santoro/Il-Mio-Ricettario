"""File di salvataggio collegato: carica un backup completo in modo coerente; file rotti o parziali non toccano i dati."""
import asyncio, json
from helpers import check, reset_app_state
from test_38_backup_atomico import backup_completo, snapshot, seed_vecchio

PICKER = """(testo) => {
  window.showOpenFilePicker = async () => [{ name: 'salvataggio.json', getFile: async () => ({ text: async () => testo }),
    queryPermission: async () => 'granted', requestPermission: async () => 'granted' }];
}"""


async def apri(page, testo, msgs):
    msgs.clear()
    await page.evaluate(PICKER, testo)
    await page.evaluate("document.getElementById('file-reconnect-pick-btn').click()")
    await page.wait_for_timeout(1200)


async def run(page):
    msgs = []
    page.on("dialog", lambda d: (msgs.append(d.message), asyncio.ensure_future(d.accept())))
    await reset_app_state(page)
    await seed_vecchio(page)
    prima = await snapshot(page)

    # file rotti / parziali / di altro tipo → nulla cambia, messaggio chiaro
    for nome, testo in {"JSON rotto": '{"recipes": [', "vuoto": '', "parziale": json.dumps({"recipes": [{"id": "x", "name": "Solo ricette"}]}),
                        "struttura errata": json.dumps(dict(backup_completo("Z"), planWeeks="no"))}.items():
        await apri(page, testo, msgs)
        check(await snapshot(page) == prima, f"File collegato ({nome}): dati invariati")
        check(any("non sono stati modificati" in m or "non sono stati toccati" in m for m in msgs), f"File collegato ({nome}): messaggio chiaro: {msgs}")

    # file completo → sostituzione coerente, poi Annulla
    await apri(page, json.dumps(backup_completo("F")), msgs)
    ids = await page.evaluate("JSON.parse(localStorage.getItem('mc_ricettario_v1')).map(r=>r.id)")
    check(ids == ["F1", "F2"], f"File collegato completo: ricette caricate: {ids}")
    s = await snapshot(page)
    check([x["id"] for x in json.loads(s["mc_ricettario_dispensa_prodotti_v1"])] == ["d1"], "File collegato completo: dispensa coerente")
    check([x["id"] for x in json.loads(s["mc_ricettario_raccolte_v1"])] == ["c1"], "File collegato completo: raccolte coerenti")
    await page.locator("#undo-toast:not([hidden])").wait_for(timeout=4000)
    await page.evaluate("document.getElementById('undo-toast-btn').click()")
    await page.wait_for_timeout(900)
    check((await snapshot(page)) == prima, "File collegato: «Annulla» riporta i dati identici a prima")
