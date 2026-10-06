"""Build the hub page (inline pixel-art SVGs) and its PWA icons."""
from PIL import Image, ImageDraw

EMERALD = ["0000000000000000","0000022222000000","0000211111200000","0002111111120000",
 "0021111111112000","0211111111111200","0211112211111200","0211122112111200",
 "0211221121111200","0211211221111200","0211122112111200","0021121121120000",
 "0002112112120000","0000211112000000","0000022220000000","0000000000000000"]
EM_COLS = {"1": "#6ef096", "2": "#148250", "3": "#28be6e"}

# Minecraft-style diamond pickaxe: 1 = light head, 2 = dark head edge, 3 = handle, 4 = handle shade
PICK = ["0000000000000000","0000222222200000","0002111111120000","0000222221112000",
 "0000000034211200","0000000343021200","0000003430021200","0000034300002000",
 "0000343000000000","0003430000000000","0034300000000000","0343000000000000",
 "3430000000000000","4300000000000000","0000000000000000","0000000000000000"]
PICK_COLS = {"1": "#7ff0e6", "2": "#2a9d93", "3": "#a0703c", "4": "#5e3f1e"}

def svg(grid, cols):
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{cols[c]}"/>'
                    for y, row in enumerate(grid) for x, c in enumerate(row) if c != "0")
    return f'<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">{rects}</svg>'

html = open("template.html").read()
html = html.replace("__SPONGE__", open("sponge.svg").read().replace("<svg ", '<svg aria-hidden="true" ', 1))
import random
_r = random.Random(7)
GRASS = ["".join("1" if y < 3 or (y == 3 and _r.random() < .5) else _r.choice("2223") for x in range(16)) for y in range(16)]
GRASS_COLS = {"1": "#5fae3c", "2": "#866043", "3": "#6b4a30"}
html = html.replace("__GRASS__", svg(GRASS, GRASS_COLS))
html = html.replace("__PICKAXE__", svg(PICK, PICK_COLS)).replace("__EMERALD__", svg(EMERALD, EM_COLS))
open("index.html", "w").write(html)

def hexrgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def icon(size):
    # sky over grass/dirt, with the emerald and pickaxe side by side
    img = Image.new("RGB", (size, size), hexrgb("#4aa3df"))
    d = ImageDraw.Draw(img)
    d.rectangle([0, size*0.72, size, size], fill=hexrgb("#8b5a2b"))
    d.rectangle([0, size*0.72, size, size*0.80], fill=hexrgb("#5fae3c"))
    cell = size * 0.026
    for grid, cols, ox in ((EMERALD, EM_COLS, size*0.08), (PICK, PICK_COLS, size*0.50)):
        oy = size * 0.24
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c != "0":
                    d.rectangle([ox + x*cell, oy + y*cell, ox + (x+1)*cell, oy + (y+1)*cell], fill=hexrgb(cols[c]))
    return img

for s in (192, 512):
    icon(s).save(f"icon-{s}.png")
print("built")
