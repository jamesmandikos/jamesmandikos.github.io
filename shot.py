from playwright.sync_api import sync_playwright
import pathlib
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for name, w, h in (("phone", 390, 844), ("ipad", 1024, 768)):
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(url); pg.screenshot(path=f"/private/tmp/claude-501/-Users-jamesmandikos-Documents-Claude-Cowork/521ca424-3a4a-40c4-8673-fe729fed9181/scratchpad/{name}.png", full_page=True)
        print(name, pg.evaluate("document.documentElement.scrollWidth"), [a.get_attribute("href") for a in pg.query_selector_all("a.tile")])
    b.close()
