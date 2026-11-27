"""Read the points of the chart back out of the phone picture and the wide picture and compare with my own working of the
JSON files (out/chart_values.json, written by recompute_hemi.py).
Upright scale: from the picture's own grid lines (10 fewer, 5 fewer, 5 more, 10 more) and the darker line at "level".
Across: from the two ends of the line along the foot of the chart, which the programs set at 1973.5 and 2031.5.
Marks: filled marks by wearing the colour away until the lines vanish; the hollow square as a hole in the orange.
Also: the grey band's edges in years, and the colour and shape of the three marks in the list above the phone chart. Reads only."""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
vals = json.load(open(f'{HERE}/out/chart_values.json'))
COL = {'ghs': '#2a78d6', 'g1': '#eb6834', 'g2': '#1baf7a'}
def near(a, hexcol, tol):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)]); return np.abs(a - c).sum(axis=2) < tol
def runs(v):
    out = []; s = None
    for i, x in enumerate(list(v) + [False]):
        if x and s is None: s = i
        if not x and s is not None: out.append((s, i - 1)); s = None
    return out
for n, er in (('second-map-phone', 4), ('second-map', 3)):
    a = np.asarray(Image.open(f'/home/agent3/site/build/img/{n}.png').convert('RGB')).astype(int)
    H, W = a.shape[:2]
    grid = near(a, '#d9d8d2', 12)
    rows = [(s + e) / 2 for s, e in runs(grid.sum(axis=1) > 0.4 * W)]
    level = [(s + e) / 2 for s, e in runs(near(a, '#52514e', 30).sum(axis=1) > 0.4 * W)]
    rows = [r for r in rows if abs(r - level[0]) > 4]                # the pale edge of the darker line is not a grid line
    assert len(rows) == 5 and len(level) == 1, (rows, level)          # four grid lines and the foot of the chart; one darker line at level
    foot = rows[-1]
    ys = rows[:4] + level; vs = [10, 5, -5, -10, 0]
    ky = np.polyfit(ys, vs, 1); resy = max(abs(np.polyval(ky, r) - v) for r, v in zip(ys, vs))
    fr = runs(grid[int(round(foot))] | grid[int(foot)])
    x0, x1 = max(fr, key=lambda r: r[1] - r[0])
    kx = np.polyfit([x0, x1], [1973.5, 2031.5], 1)
    top_axes = int(np.polyval(np.polyfit(vs, ys, 1), 13.5))
    print(f'\n{n}: {W} x {H}; grid lines and level at rows {[round(y, 1) for y in ys]} taken as {vs}: straight-line fit off by at most {resy:.3f} million; foot at row {foot:.1f} = {np.polyval(ky, foot):.2f} (set at -13.5); '
          f'foot line from column {x0} to {x1}; top of the chart about row {top_axes}')
    band = near(a, '#f1f0ec', 6)
    bc = runs(band[top_axes + 30:int(foot) - 60].mean(axis=0) > 0.5)
    b0, b1 = max(bc, key=lambda r: r[1] - r[0])
    print(f'  grey band from column {b0} to {b1} = years {np.polyval(kx, b0):.1f} to {np.polyval(kx, b1 + 1):.1f} (set at 2022.5 to 2031.5)')
    for key, col in COL.items():
        m = near(a, col, 70); m[:top_axes] = False
        core = ndimage.binary_erosion(m, structure=np.ones((3, 3)), iterations=er)
        lab, k = ndimage.label(core)
        pts = sorted((ndimage.center_of_mass(core, lab, i)[::-1] for i in range(1, k + 1)))
        got = [(float(np.polyval(kx, x)), float(np.polyval(ky, y))) for x, y in pts]
        if key == 'g1':                                               # the hollow square: a hole in the orange
            filled = ndimage.binary_fill_holes(m) & ~m
            lab2, k2 = ndimage.label(filled)
            for i in range(1, k2 + 1):
                if (lab2 == i).sum() > 25:
                    y, x = ndimage.center_of_mass(lab2 == i); got.append((float(np.polyval(kx, x)), float(np.polyval(ky, y)))); print(f'  hollow square found: a hole of {(lab2 == i).sum()} pixels in the orange at column {x:.0f}, row {y:.0f}')
        want = sorted((int(k_.split('-')[1]), v) for k_, v in vals.items() if k_.startswith(key + '-'))
        got.sort()
        ok = len(got) == len(want)
        line = []
        worst = 0
        for (gx, gy), (wx, wy) in zip(got, want):
            line.append(f'{gx:.1f}: {gy:+.2f} (file {wx}: {wy:+.2f})'); worst = max(worst, abs(gy - wy), abs(gx - wx) / 10)
        print(f'  {key}: marks found {len(got)} of {len(want)}; ' + '; '.join(line) + f'   -> largest difference {worst:.2f}')
    if n == 'second-map-phone':
        # the list above the chart: one mark of each colour above the chart, at which row; and its shape by how much of its bounding square it fills
        for key, col in COL.items():
            m = near(a, col, 70); m[top_axes:] = False
            core = ndimage.binary_erosion(m, structure=np.ones((3, 3)), iterations=er); lab, k = ndimage.label(core)
            for i in range(1, k + 1):
                y, x = ndimage.center_of_mass(core, lab, i)
                full = ndimage.label(near(a, col, 70) & (np.abs(np.arange(H)[:, None] - y) < 14) & (np.abs(np.arange(W)[None, :] - x) < 14))[0]
                reg = full == full[int(round(y)), int(round(x))]
                yy, xx = np.where(reg); fill = reg.sum() / ((yy.max() - yy.min() + 1) * (xx.max() - xx.min() + 1))
                print(f'  list above the chart: a {key} mark ({col}) at column {x:.0f}, row {y:.0f}; it fills {fill:.2f} of its bounding square (a square about 1, a circle about 0.79, a diamond about 0.5; the line through it adds a little)')
