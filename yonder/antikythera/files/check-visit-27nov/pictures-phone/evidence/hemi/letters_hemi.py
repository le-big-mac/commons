"""Heights of capital letters and figures in the two phone pictures, in the files' own pixels and at 350 pixels wide.
Each band holds the start of one line of lettering; a glyph is a run of columns that hold ink. Reads only."""
import numpy as np
from PIL import Image
SRC = '/home/agent3/site/build/img'
def glyphs(n, band, dark):
    x0, y0, x1, y1 = band
    a = np.asarray(Image.open(f'{SRC}/{n}.png').convert('RGB')).astype(int)[y0:y1, x0:x1]
    ink = a.max(axis=2) <= dark
    out = []; s = None
    cols = ink.any(axis=0)
    for i, c in enumerate(list(cols) + [False]):
        if c and s is None: s = i
        if not c and s is not None:
            rows = np.where(ink[:, s:i].any(axis=1))[0]; out.append(int(rows[-1] - rows[0] + 1)); s = None
    return out
BANDS = [
    ('hemi-ridge-phone', 'heading "How much land ..." (10.5 pt)', (12, 14, 120, 56), 90),
    ('hemi-ridge-phone', 'under it "Darker blue: ..." (9.5 pt, grey)', (12, 122, 130, 160), 130),
    ('hemi-ridge-phone', 'label "Tarragona" (9.5 pt)', (160, 948, 318, 986), 90),
    ('hemi-ridge-phone', 'label "Nantes (the centre" (9.5 pt)', (628, 492, 915, 530), 90),
    ('hemi-ridge-phone', 'label "southern summit:" (bold)', (698, 948, 1002, 984), 90),
    ('hemi-ridge-phone', 'name "F R A N C E" (9.5 pt, grey)', (617, 664, 785, 700), 120),
    ('hemi-ridge-phone', '"200 km" (9.5 pt)', (58, 1026, 170, 1060), 90),
    ('second-map-phone', 'heading "How many more people ..." (10 pt, grey)', (12, 16, 130, 54), 130),
    ('second-map-phone', 'list "GHS-POP: the maps first used" (10 pt)', (108, 158, 590, 196), 90),
    ('second-map-phone', '"5 million people ..." (9.5 pt, grey)', (205, 448, 330, 486), 130),
    ('second-map-phone', 'scale "10 more" (9.5 pt, grey)', (58, 520, 190, 558), 130),
    ('second-map-phone', 'scale "1975" (9.5 pt, grey)', (178, 1228, 258, 1264), 130),
    ('second-map-phone', '"projections" (9.5 pt, grey)', (846, 1168, 1014, 1206), 130),
]
s = 350 / 1058
for n, what, band, dark in BANDS:
    g = glyphs(n, band, dark)
    print(f'{n:18s} {what:52s} first glyph {g[0]:2d} px high in the file = {g[0] * s:4.1f} px at 350 wide; tallest {max(g)} px = {max(g) * s:4.1f}; all: {g}')
print('numbers on the lines of the map: set at 8.5 pt, turned; by the same proportion as the 9.5 pt figures above their figures are %.1f px high at 350 wide' % (22 * 8.5 / 9.5 * s))
