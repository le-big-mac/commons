"""Heights of letters in the phone pictures, measured in the files' own pixels and scaled to the 350-pixel column of a phone
(the browser draws the picture 348 wide inside a 1-pixel border; I give both). Reads only.
A glyph is a run of columns in a band that hold ink (dark, nearly grey pixels); its height is the rows that hold ink."""
import sys
import numpy as np
from PIL import Image
SRC = '/home/agent3/site/build/img'
def glyphs(n, band, thr=150):
    x0, y0, x1, y1 = band
    a = np.asarray(Image.open(f'{SRC}/{n}.png').convert('RGB')).astype(int)[y0:y1, x0:x1]
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    grey = (a.max(axis=2) - a.min(axis=2)) < 40
    ink = (lum < thr) & grey
    cols = ink.any(axis=0)
    out = []; start = None
    for i, c in enumerate(list(cols) + [False]):
        if c and start is None: start = i
        if not c and start is not None:
            rows = np.where(ink[:, start:i].any(axis=1))[0]
            out.append((x0 + start, x0 + i - 1, y0 + rows[0], y0 + rows[-1], rows[-1] - rows[0] + 1)); start = None
    return out
W = {'dial-today-phone': 1058, 'dial-kept-phone': 1058, 'handshake-popsize-phone': 1058, 'dial-today-page': 1224, 'dial-kept-page': 1292, 'handshake-popsize': 1122}
BANDS = [
    ('dial-today-phone', 'name "Mars: less than 1° apart" (10.5 pt)', (5, 50, 430, 112)),
    ('dial-today-phone', 'name "Moon: 105° apart" (bold)', (705, 50, 1055, 112)),
    ('dial-today-phone', '"Earth" (9.5 pt)', (545, 745, 640, 790)),
    ('dial-today-phone', 'legend "where the pointer would stand" (10 pt)', (315, 1520, 820, 1565)),
    ('dial-kept-phone', 'heading "Marked months that held an eclipse" (10 pt)', (8, 18, 600, 62)),
    ('dial-kept-phone', '"Moon: none since" (10 pt)', (555, 485, 850, 528)),
    ('dial-kept-phone', 'scale "205 BC" (9.5 pt)', (60, 940, 185, 985)),
    ('dial-kept-phone', 'scale "AD 250"', (325, 940, 445, 985)),
    ('dial-kept-phone', 'scale "40" at the side', (45, 195, 100, 232)),
    ('handshake-popsize-phone', 'heading "Share of moves that are cooperative" (10 pt)', (8, 15, 610, 60)),
    ('handshake-popsize-phone', '"25%" beside a point (10 pt)', (295, 650, 375, 695)),
    ('handshake-popsize-phone', 'scale "100%" at the side (9.5 pt)', (30, 75, 128, 118)),
    ('handshake-popsize-phone', 'scale "100 machines"', (160, 828, 380, 872)),
    ('dial-today-page', 'WIDE: name "Mars: less than 1° apart"', (80, 445, 390, 485)),
    ('dial-kept-page', 'WIDE: "Moon: none since"', (815, 362, 1012, 392)),
    ('dial-kept-page', 'WIDE: small print "Counted in NASA\'s catalogue"', (90, 745, 815, 772)),
    ('handshake-popsize', 'WIDE: "25%" beside a point', (295, 485, 350, 512)),
]
for n, what, band in BANDS:
    g = glyphs(n, band)
    hs = [h for *_, h in g]
    tall = max(hs); first = g[0][4]
    s350, s348 = 350 / W[n], 348 / W[n]
    print(f'{n:26s} {what:58s} glyphs {len(g):2d}; first glyph {first:2d} px high, tallest {tall:2d} px in the file -> first {first * s350:4.1f} px, tallest {tall * s350:4.1f} px at 350 wide ({first * s348:4.1f} at 348)')
    if '-v' in sys.argv: print('    heights:', hs)
