"""The four globes of the hemispheres page with lettering large enough for a phone (27 Nov 2026, agent3).
The globes themselves are cut, unchanged, from the page's picture (img/hemi-globes.png, 1100 px wide); only the lettering over
them is drawn anew, larger, in three lines where the page's picture has two (the same words and numbers).
usage: globes_phone.py IN.png OUT.png"""
import sys
from PIL import Image, ImageDraw, ImageFont
import matplotlib
src, out = sys.argv[1:3]
im = Image.open(src).convert('RGB'); W, H = im.size
bg = im.getpixel((5, 5))
# find the four discs: columns and rows where anything is drawn, away from the lettering
import numpy as np
a = np.asarray(im).astype(int); dark = (np.abs(a - np.array(bg)).sum(axis=2) > 12)
def runs(v, minlen):
    out = []; start = None
    for i, x in enumerate(list(v) + [False]):
        if x and start is None: start = i
        if not x and start is not None:
            if i - start >= minlen: out.append((start, i))
            start = None
    return out
rows = runs(dark.sum(axis=1) > W * 0.15, 200)          # two bands of globes
print('bands of globes (rows):', rows)
panels = []
for (r0, r1) in rows:
    cols = runs(dark[r0:r1].sum(axis=0) > (r1 - r0) * 0.15, 200)
    print('  globes in the band (columns):', cols)
    for (c0, c1) in cols: panels.append((c0, r0, c1, r1))
assert len(panels) == 4, panels
font_dir = matplotlib.get_data_path() + '/fonts/ttf/'
f1 = ImageFont.truetype(font_dir + 'DejaVuSans-Bold.ttf', 34); f2 = ImageFont.truetype(font_dir + 'DejaVuSans.ttf', 34)
titles = [("The half with most land", "81.2% of the world's land", "centre 40.8°N, 1.7°E"), ("The other half", "18.8% of the world's land", "centre 40.8°S, 178.3°W"),
          ("The half with most people", "92.7% of the world's people", "centre 52.4°N, 12.7°E"), ("The other half", "7.3% of the world's people", "centre 52.4°S, 167.3°W")]
f3 = ImageFont.truetype(font_dir + 'DejaVuSans.ttf', 28)
pad = 6; gw = max(p[2] - p[0] for p in panels) + 2 * pad; gh = max(p[3] - p[1] for p in panels) + 2 * pad
head = 146; gap = 26
M = 18                                              # a margin, so that the widest line does not touch the edge
canvas = Image.new('RGB', (2 * gw + gap + 2 * M, 2 * (head + gh) + gap + M), bg); d = ImageDraw.Draw(canvas)
for k, (p, (t1, t2, t3)) in enumerate(zip(panels, titles)):
    x0 = M + (k % 2) * (gw + gap); y0 = (k // 2) * (head + gh + gap)
    for j, (t, f, col) in enumerate(((t1, f1, (20, 20, 20)), (t2, f2, (20, 20, 20)), (t3, f3, (82, 81, 78)))):
        w = d.textlength(t, font=f); d.text((x0 + (gw - w) / 2, y0 + 8 + j * 44), t, fill=col, font=f)
    g = im.crop((p[0] - pad, p[1] - pad, p[2] + pad, p[3] + pad)); canvas.paste(g, (x0 + (gw - g.size[0]) // 2, y0 + head))
c = np.asarray(canvas); flat = c.reshape(-1, 3)
uniq, inv = np.unique(flat, axis=0, return_inverse=True)                      # every colour on the canvas, and which one each pixel has
old = np.unique(np.asarray(im).reshape(-1, 3), axis=0)                        # the old picture's colours: the globes use only these
oldset = {tuple(x): i for i, x in enumerate(old)}
text = np.array([x for x in uniq if tuple(x) not in oldset])                  # the new lettering's greys
keep = text[np.argsort(text.sum(axis=1))][np.linspace(0, len(text) - 1, min(len(text), 256 - len(old))).round().astype(int)]
pal = np.vstack([old, keep]).astype(np.uint8)
index = np.array([oldset[tuple(x)] if tuple(x) in oldset else len(old) + int(np.abs(keep.astype(int) - x.astype(int)).sum(axis=1).argmin()) for x in uniq], dtype=np.uint8)
p = Image.fromarray(index[inv.reshape(-1)].reshape(c.shape[:2]), 'P'); p.putpalette(list(pal.flatten()) + [0] * (768 - 3 * len(pal)))
p.save(out, optimize=True); print('written', out, p.size, '; palette', len(pal), 'colours, of which', len(old), 'are the old picture\'s')
