"""Read the two stepped lines back out of the eclipse chart, in the phone picture and in the wide picture, and compare each
with two_lists.json, cycle by cycle. The scales are taken from the pictures' own tick marks and grid lines:
  across: the tick marks under the foot of the chart (phone: 205 BC, AD 250, 500, 750, 1000, 1250, which should stand at
          0, 454, 704, 954, 1204, 1454 years after 205 BC; wide: 0, 200, ... 1600 years after 205 BC)
  up:     the grid lines (phone: 0, 10, 20, 30, 40; wide: 0, 5, ... 40)
Reads only."""
import json
import numpy as np
from PIL import Image
SRC = '/home/agent3/site/build/img'
rows = json.load(open('/srv/commons/antikythera-agent3/dial/two_lists.json'))['F']
A = [r['A'] for r in rows]; S = [r['S'] for r in rows]; CYC = [r['cycle'] for r in rows]
def near(a, hexcol, tol):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (1, 3, 5)])
    return (np.abs(a - c).sum(axis=2) < tol)
def runs(v):
    out = []; s = None
    for i, x in enumerate(list(v) + [False]):
        if x and s is None: s = i
        if not x and s is not None: out.append((s, i - 1)); s = None
    return out
def read(n, xt, yt):
    a = np.asarray(Image.open(f'{SRC}/{n}.png').convert('RGB')).astype(int)
    H, W = a.shape[:2]
    grid = near(a, '#e4e3df', 14)
    # grid lines and the foot of the chart: rows where the grid colour runs across more than half the picture
    long_rows = [r for r in runs(grid.sum(axis=1) > 0.5 * W)]
    centres = [(s + e) / 2 for s, e in long_rows]
    foot = centres[-1]; lines = centres[:-1]            # the lowest is the foot of the chart (the bottom spine), the rest are grid lines
    assert len(lines) == len(yt), (n, centres)
    ky = np.polyfit(lines[::-1], yt, 1)                  # value = ky[0] * row + ky[1]
    resy = max(abs(np.polyval(ky, r) - v) for r, v in zip(lines[::-1], yt))
    # tick marks: just under the foot, short strokes that are not background
    band = a[int(foot) + 4:int(foot) + 7]
    notbg = (np.abs(band - np.array([252, 252, 251])).sum(axis=2) > 20).all(axis=0)
    ticks = [(s + e) / 2 for s, e in runs(notbg) if e - s < 12]
    assert len(ticks) == len(xt), (n, ticks)
    kx = np.polyfit(ticks, xt, 1)                        # years = kx[0] * column + kx[1]
    resx = max(abs(np.polyval(kx, c) - v) for c, v in zip(ticks, xt))
    print(f'\n{n}: {W} x {H}')
    print(f'  up: {len(lines)} grid lines at rows {[round(x, 1) for x in lines[::-1]]} taken as {yt}; straight-line fit off by at most {resy:.3f} months; foot of the chart at row {foot:.1f} = {np.polyval(ky, foot):.2f} months')
    print(f'  across: {len(ticks)} tick marks at columns {[round(x, 1) for x in ticks]} taken as {xt} years after 205 BC; straight-line fit off by at most {resx:.2f} years; one pixel = {kx[0]:.3f} years')
    blue = near(a, '#2a78d6', 70); orange = near(a, '#eb6834', 70)
    def level(mask, col):
        rs = np.where(mask[:, col])[0]
        if len(rs) == 0: return None
        return float(np.polyval(ky, rs.mean())), len(rs)
    col_of = lambda yrs: int(round((yrs - kx[1]) / kx[0]))
    last_orange = max(np.where(orange.any(axis=0))[0]); first_blue = min(np.where(blue.any(axis=0))[0])
    print(f'  the lines run from {np.polyval(kx, first_blue):.0f} to {np.polyval(kx, last_orange):.0f} years after 205 BC (that is to about AD {np.polyval(kx, last_orange) - 204:.0f})')
    bad = 0; seen = 0; hidden = 0; worst = 0.0
    for c, av, sv in zip(CYC, A, S):
        mid = (c + 0.5) * 18.03
        col = col_of(mid)
        if col > last_orange - 2: break
        seen += 1
        lo = level(orange, col); lb = level(blue, col)
        if lo is None or abs(lo[0] - sv) > 0.4: bad += 1; print('   ORANGE differs at cycle', c, lo, sv)
        else: worst = max(worst, abs(lo[0] - sv))
        if lb is None:
            if av == sv: hidden += 1          # the orange line is drawn over the blue where they are equal
            else: bad += 1; print('   BLUE missing at cycle', c, av)
        elif abs(lb[0] - av) > 0.4: bad += 1; print('   BLUE differs at cycle', c, lb, av)
        else: worst = max(worst, abs(lb[0] - av))
    print(f'  cycles in view {seen} (0 to {seen - 1}); levels that differ from the file: {bad}; cycles where the blue line is under the orange (equal counts): {hidden}; largest difference read {worst:.2f} months')
    # where each line comes down to zero: the first column at which the line is at zero, and stays
    for name, mask, vals in (('Moon (blue)', blue, A), ('Sun (orange)', orange, S)):
        z = next(c for c, v in zip(CYC, vals) if v == 0) * 18.03
        # leftmost column where the mask has ink within half a month of zero
        zero_row = (0 - ky[1]) / ky[0]
        colz = None
        for col in range(first_blue, last_orange + 1):
            rs = np.where(mask[:, col])[0]
            if len(rs) and abs(np.polyval(ky, rs.max()) - 0) < 0.6 and np.polyval(ky, rs.max()) < 0.5 and (rs.max() - zero_row) > -1: colz = col; break
        yrs = np.polyval(kx, colz)
        print(f'  {name}: reaches zero at column {colz} = {yrs:.0f} years after 205 BC by the picture\'s own scale = AD {yrs - 204:.0f}; the file says {z:.1f} = AD {z - 204:.1f}')
    return a, kx, ky
P = read('dial-kept-phone', [0, 454, 704, 954, 1204, 1454], [0, 10, 20, 30, 40])
Wd = read('dial-kept-page', [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600], [0, 5, 10, 15, 20, 25, 30, 35, 40])
# where do the grey pointer lines end? the lowest grey pixel of each pointer, in the picture's own scale
for n, (a, kx, ky) in (('dial-kept-phone', P), ('dial-kept-page', Wd)):
    grey = near(a, '#b4b3ad', 24)
    from scipy import ndimage
    lab, k = ndimage.label(grey, structure=np.ones((3, 3)))
    print(f'\n{n}: grey pointer lines (thin strokes more than 40 pixels long)')
    for i in range(1, k + 1):
        ys, xs = np.where(lab == i)
        if ys.max() - ys.min() < 40: continue
        j = ys.argmax(); t = ys.argmin()
        print(f'  from column {xs[t]}, row {ys[t]} (top: {np.polyval(kx, xs[t]):.0f} years, {np.polyval(ky, ys[t]):.1f} months) down to column {xs[j]}, row {ys[j]} = {np.polyval(kx, xs[j]):.0f} years after 205 BC (AD {np.polyval(kx, xs[j]) - 204:.0f}), {np.polyval(ky, ys[j]):.1f} months')
