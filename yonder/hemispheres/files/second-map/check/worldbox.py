"""From the whole-sphere maps saved by search.py (0.25-degree lattice of centres, hard edge): for each grid, the box
holding every centre within 0.1, 0.2 and 0.3 points of that map's best, and the best centre outside the box 40-65 N, 0-30 E.
usage: python -I worldbox.py CHECK_OUT_DIR"""
import sys, json
import numpy as np
od = sys.argv[1]
lats = np.round(np.arange(-90, 90 + 1e-9, 0.25), 6); lons = np.round(np.arange(-180, 180 - 1e-9, 0.25), 6)
names = ['ghs-1975', 'ghs-2000', 'ghs-2005', 'ghs-2010', 'ghs-2015', 'ghs-2020', 'ghs-2025', 'ghs-2030', 'g1-2000', 'g1-2010', 'g1-2020', 'g2-2015', 'g2-2020', 'g2-2025', 'g2-2030']
LA, LO = np.meshgrid(lats, lons, indexing='ij')
allbox = {}
for n in names:
    S = np.load(f'{od}/search-{n}.global.npy').astype(np.float64)
    b = S.max(); txt = []
    for tol in (0.001, 0.002, 0.003):
        m = S >= b - tol
        box = (LA[m].min(), LA[m].max(), LO[m].min(), LO[m].max())
        txt.append(f'within {100 * tol:.1f}: {int(m.sum())} centres, {box[0]:.2f}..{box[1]:.2f} N, {box[2]:.2f}..{box[3]:.2f} E')
        a = allbox.setdefault(tol, list(box)); a[0] = min(a[0], box[0]); a[1] = max(a[1], box[1]); a[2] = min(a[2], box[2]); a[3] = max(a[3], box[3])
    out = ~((LA >= 40) & (LA <= 65) & (LO >= 0) & (LO <= 30))
    k = np.argmax(np.where(out, S, -1)); i, j = np.unravel_index(k, S.shape)
    print(f'{n}: best {100 * b:.4f}%; ' + '; '.join(txt) + f'; best outside 40-65 N, 0-30 E: {100 * (S[i, j] - b):+.3f} points at {lats[i]:.2f} N, {lons[j]:.2f} E')
for tol, a in allbox.items():
    print(f'all fifteen grids, centres within {100 * tol:.1f} points of each grid\'s best: {a[0]:.2f}..{a[1]:.2f} N, {a[2]:.2f}..{a[3]:.2f} E')
