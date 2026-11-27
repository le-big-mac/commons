"""Read the six points and their bars back out of the cooperation chart (phone picture and wide picture) and compare with the
six figures and standard errors of the table in the study's README (typed here from that table, which I read myself).
The upright scale is taken from the picture's own grid lines (0, 25, 50, 75, 100%). Reads only."""
import numpy as np
from PIL import Image
from scipy import ndimage
README = {'no slips (blue)': [(0.25, 0.01), (0.57, 0.04), (0.85, 0.03)], '2% slip (orange)': [(0.59, 0.02), (0.77, 0.05), (0.79, 0.03)]}
def near(a, hexcol, tol):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)]); return np.abs(a - c).sum(axis=2) < tol
def runs(v):
    out = []; s = None
    for i, x in enumerate(list(v) + [False]):
        if x and s is None: s = i
        if not x and s is not None: out.append((s, i - 1)); s = None
    return out
for n in ['handshake-popsize-phone', 'handshake-popsize']:
    a = np.asarray(Image.open(f'/home/agent3/site/build/img/{n}.png').convert('RGB')).astype(int)
    H, W = a.shape[:2]
    grid = near(a, '#e4e3df', 14)
    rows = [(s + e) / 2 for s, e in runs(grid.sum(axis=1) > 0.5 * W)]
    assert len(rows) == 5, rows                      # 100%, 75%, 50%, 25%, and the foot of the chart at 0
    ky = np.polyfit(rows, [1.0, 0.75, 0.5, 0.25, 0.0], 1)
    res = max(abs(np.polyval(ky, r) - v) for r, v in zip(rows, [1.0, 0.75, 0.5, 0.25, 0.0]))
    print(f'\n{n}: {W} x {H}; grid lines at rows {rows}; straight-line fit off by at most {100 * res:.2f} points of a percent')
    for name, col in (('no slips (blue)', '#2a78d6'), ('2% slip (orange)', '#eb6834')):
        m = near(a, col, 70)
        # the dots: erode the mask so that the lines (7 or 5 pixels thick) vanish and only the round dots are left
        core = ndimage.binary_erosion(m, iterations=6 if W < 1100 else 5)
        lab, k = ndimage.label(core)
        dots = sorted((ndimage.center_of_mass(core, lab, i)[::-1] for i in range(1, k + 1)))
        assert len(dots) == 3, (name, dots)
        for (cx, cy), (v, e) in zip(dots, README[name]):
            col_pix = np.where(m[:, int(round(cx))])[0]
            # the bar and its caps: the highest and lowest pixel of this colour in a narrow band about the dot's column (the caps are 6 points wide)
            band = m[:, int(round(cx)) - 3:int(round(cx)) + 4].any(axis=1)
            rr = np.where(band)[0]
            # the dot has a pale edge, so the bar is cut off from it: take every row of this colour within 7.5 points of a percent of the dot
            lim = 0.075 / abs(ky[0])
            rr = rr[(rr > cy - lim) & (rr < cy + lim)]
            top, bot = rr.min(), rr.max()
            print(f'  {name:17s} dot at column {cx:6.1f}: {100 * np.polyval(ky, cy):5.1f}% (table {100 * v:.0f}%); this colour runs from {100 * np.polyval(ky, bot):5.1f}% to {100 * np.polyval(ky, top):5.1f}% in the dot\'s column (table {100 * (v - e):.0f}% to {100 * (v + e):.0f}%)')
