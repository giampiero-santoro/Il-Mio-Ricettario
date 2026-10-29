"""Pianificazione settimanale con la settimana vuota: nome del giorno, «Giorno libero» e «Aggiungi pasto» non si sovrappongono."""
from helpers import check, reset_app_state, dismiss_storage_choice


async def run(page):
    await reset_app_state(page)
    await page.reload(); await page.wait_for_timeout(800); await dismiss_storage_choice(page)
    await page.evaluate("document.getElementById('nav-planning-btn').click()")
    await page.locator(".plan-matrix").wait_for(timeout=4000)
    col = page.locator(".plan-matrix .plan-week-row").first
    box = lambda sel: col.locator(sel).first.bounding_box()
    testa, libero, scelta = await box(".plan-grid-dayhead"), await box(".plan-day-free"), await box(".plan-add-meal")
    check(testa and libero and scelta, "Elementi visibili")
    check(testa["y"] + testa["height"] <= libero["y"] + 1, f"«Giorno libero» sotto il nome del giorno: {testa} {libero}")
    check(libero["y"] + libero["height"] <= scelta["y"] + 1, f"«Aggiungi pasto» sotto «Giorno libero»: {libero} {scelta}")

    # nessuna sovrapposizione tra le celle di giorni diversi e tra le righe
    boxes = await page.evaluate("""()=>[...document.querySelectorAll('.plan-matrix .plan-cell')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})""")
    check(len(boxes) == 21, f"21 celle (7 giorni x 3): {len(boxes)}")
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            ov = a[0] < b[0] + b[2] - 1 and b[0] < a[0] + a[2] - 1 and a[1] < b[1] + b[3] - 1 and b[1] < a[1] + a[3] - 1
            check(not ov, f"Celle sovrapposte {i}/{j}: {a} {b}")
    check(all(b[3] > 10 for b in boxes), "Tutte le celle hanno altezza")
